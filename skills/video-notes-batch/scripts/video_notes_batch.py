#!/usr/bin/env python3
"""Persistent local lesson queue. The host creates agents; this CLI never calls a model."""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote
import uuid


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
        name = f.name
    os.replace(name, path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def inside(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'Path outside assigned directory: {path}')
    return path


def tree(root):
    root = Path(root)
    result = {}
    if root.is_symlink():
        raise ValueError('Symlink directories are not portable deliverables')
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlink in artifact tree: {path}')
        if path.is_file():
            result[str(path.relative_to(root))] = digest(path)
    if not result:
        raise ValueError(f'Empty artifact tree: {root}')
    return result


@contextmanager
def locked(work):
    work = Path(work).resolve(strict=True)
    with (work/'.batch.lock').open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        state = read(work/'batch.json')
        yield work, state


def changed(work, state, event, **details):
    state['events'].append(dict(time=now(), event=event, **details))
    save(work/'batch.json', state)


def sources(lesson):
    for key in ('video', 'transcript'):
        if digest(lesson[key]) != lesson[f'{key}_sha256']:
            raise ValueError(f'{key} changed for {lesson["id"]}; start a new batch')


def safe_id(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', value):
        raise ValueError(f'Invalid lesson id: {value}')
    return value


def initialize(manifest, work, output, labels=None, mode='faithful', max_active=2, notes_cli=None):
    if mode not in ('faithful', 'summary') or not 1 <= max_active <= 2:
        raise ValueError('Require faithful|summary and max-active 1 or 2')
    manifest = Path(manifest).resolve(strict=True)
    raw = read(manifest)
    entries = raw['entries']
    if not entries:
        raise ValueError('Empty manifest')
    ids = [safe_id(str(e['id'])) for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate lesson identities')
    if labels:
        for label in labels:
            if sum(e.get('label') == label for e in entries) != 1:
                raise ValueError(f'Label missing or ambiguous: {label}')
        entries = [e for e in entries if e.get('label') in labels]
    frozen = []
    seen = set()
    for e in entries:
        item = {k: e.get(k, '') for k in ('id', 'title', 'label', 'source_url', 'source_key')}
        item['id'] = str(item['id'])
        for key in ('video', 'transcript'):
            path = Path(e[key]).expanduser()
            if not path.is_absolute():
                path = manifest.parent/path
            item[key] = str(path.resolve(strict=True))
            if not Path(item[key]).is_file():
                raise ValueError(f'{key} must be a file')
            item[f'{key}_sha256'] = digest(item[key])
        identity = item['source_key'] or (item['video_sha256'], item['transcript_sha256'])
        if identity in seen:
            raise ValueError('Duplicate source in selected lessons')
        seen.add(identity)
        item['mode'] = mode
        item['input_fingerprint'] = fingerprint(item)
        item.update(state='ready', attempts=0, repairs=0, agents=[], active=None)
        frozen.append(item)
    work, output = Path(work).resolve(), Path(output).resolve()
    if work == output or work.is_relative_to(output) or output.is_relative_to(work):
        raise ValueError('Work and publication directories must be separate')
    cli = str(Path(notes_cli).resolve(strict=True)) if notes_cli else None
    config = dict(title=raw.get('title', '视频笔记'), entries=[{k: v for k, v in e.items()
                  if k not in ('state', 'attempts', 'repairs', 'agents', 'active')} for e in frozen],
                  output=str(output), mode=mode, max_active=max_active, notes_cli=cli)
    batch_hash = fingerprint(config)
    work.mkdir(parents=True, exist_ok=True)
    with (work/'.batch.lock').open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        if (work/'batch.json').exists():
            if read(work/'batch.json')['fingerprint'] != batch_hash:
                raise ValueError('Batch inputs changed; choose a new work directory')
            return dict(ok=True, batch=str(work), cache_hit=True)
        state = dict(schema_version=1, fingerprint=batch_hash, title=config['title'], mode=mode,
                     output=str(output), max_active=max_active, notes_cli=cli, lessons=frozen,
                     events=[dict(time=now(), event='initialized')])
        save(work/'selection.json', config)
        save(work/'batch.json', state)
    return dict(ok=True, batch=str(work), lessons=len(frozen), cache_hit=False)


def stage_for(item):
    return {'ready': 'writer', 'repair_ready': 'writer', 'review_ready': 'reviewer'}.get(item['state'])


def status(work):
    with locked(work) as (_, s):
        return dict(ok=True, title=s['title'], counts=dict(Counter(x['state'] for x in s['lessons'])),
                    active=[dict(lesson_id=x['id'], **x['active']) for x in s['lessons'] if x['active']],
                    ready=[dict(lesson_id=x['id'], stage=stage_for(x)) for x in s['lessons'] if stage_for(x)],
                    lessons=[dict(lesson_id=x['id'], title=x['title'], state=x['state'],
                                  error=x.get('error'), published=x.get('published')) for x in s['lessons']])


def claim(work, lesson_id=None, stage=None):
    with locked(work) as (work, s):
        if sum(bool(x['active']) for x in s['lessons']) >= s['max_active']:
            raise ValueError('Active agent capacity reached; wait for a result')
        candidates = [x for x in s['lessons'] if stage_for(x) and (not lesson_id or x['id'] == lesson_id)
                      and (not stage or stage_for(x) == stage)]
        candidates.sort(key=lambda x: stage_for(x) != 'reviewer')
        if not candidates:
            raise ValueError('No matching ready lesson')
        item = candidates[0]
        sources(item)
        stage = stage_for(item)
        token = uuid.uuid4().hex
        attempt = work/'lessons'/item['id']/'attempts'/token
        attempt.mkdir(parents=True)
        base = item.get('candidate') or item.get('checkpoint')
        if stage == 'writer' and base:
            if tree(base['job_dir']) != base['job_files']:
                raise ValueError('Saved progress changed')
            shutil.copytree(base['job_dir'], attempt/'job')
        binding = dict(lesson_id=item['id'], claim_token=token, stage=stage, mode=s['mode'],
                       input_fingerprint=item['input_fingerprint'], batch_fingerprint=s['fingerprint'])
        task = dict(schema_version=1, input_kind='single_lesson', **binding,
                    title=item['title'], source_url=item['source_url'], video=item['video'],
                    transcript=item['transcript'], video_sha256=item['video_sha256'],
                    transcript_sha256=item['transcript_sha256'], attempt_dir=str(attempt),
                    job_dir=str(attempt/'job'), delivery_dir=str(attempt/'delivery'),
                    notes_cli=s['notes_cli'], result_template=binding)
        if stage == 'reviewer':
            task['candidate'] = item['candidate']
        elif base:
            task['resume_from'] = base
        if item.get('review'):
            task['previous_review'] = item['review']
        save(attempt/'task.json', task)
        item['active'] = dict(claim_token=token, stage=stage, task=str(attempt/'task.json'), started=now())
        item['state'] = 'writing' if stage == 'writer' else 'reviewing'
        item['attempts'] += 1
        changed(work, s, 'claimed', **binding)
        return dict(ok=True, **item['active'])


def locate(s, token):
    for item in s['lessons']:
        if item['active'] and item['active']['claim_token'] == token:
            return item, read(item['active']['task'])
    raise ValueError('Unknown, consumed or revoked claim token')


def attach(work, token, agent_id, host, isolation):
    if not agent_id.strip() or not host.strip() or isolation != 'fresh':
        raise ValueError('Record actual host/agent id and fresh-context dispatch')
    with locked(work) as (work, s):
        item, task = locate(s, token)
        if item['active'].get('agent_id'):
            raise ValueError('Dispatch already attached')
        for other in s['lessons']:
            for a in other['agents']:
                if a['agent_id'] == agent_id and (other['id'] != item['id'] or a['stage'] != task['stage'] or task['stage'] == 'reviewer'):
                    raise ValueError('Agent identity crossed lessons/roles or reused a reviewer context')
        evidence = dict(agent_id=agent_id, host=host, isolation=isolation, stage=task['stage'], claim_token=token)
        item['agents'].append(evidence)
        item['active'].update(evidence)
        changed(work, s, 'dispatched', lesson_id=item['id'], **evidence)
    return dict(ok=True)


def check_job(item, job_dir, complete=False):
    job = read(Path(job_dir)/'job.json')
    if (job['input']['video_sha256'] != item['video_sha256'] or
        job['input']['transcript_sha256'] != item['transcript_sha256'] or
        job['input'].get('mode') != item['mode'] or job['input']['source_url'] != item['source_url']):
        raise ValueError('Wrong lesson sources or mode in job')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                            '-of', 'json', item['video']], capture_output=True, text=True, check=True, timeout=60)
    duration = float(json.loads(probe.stdout)['format']['duration'])
    if (job['input']['start'] != 0 or job['source']['range']['start'] != 0 or
        abs(job['input']['end'] - duration) > .01 or
        abs(job['source']['duration'] - duration) > .01 or
        abs(job['source']['range']['end'] - duration) > .01):
        raise ValueError('Batch requires the full actual video, not a sample')
    if digest(Path(job_dir)/'transcript.json') != job['normalized_sha256']:
        raise ValueError('Normalized transcript changed')
    for window in job['windows']:
        if window['status'] == 'reviewed':
            chunk = inside(job_dir, Path(job_dir)/window['chunk'])
            if digest(chunk) != window['sha256']:
                raise ValueError('Checkpoint chunk changed after review')
        elif complete:
            raise ValueError('Some lesson windows remain unreviewed')
    return job


def validate_candidate(s, item, task):
    job_dir, delivery = Path(task['job_dir']), Path(task['delivery_dir'])
    job = check_job(item, job_dir, complete=True)
    for name in ('note.md', 'note.html', 'render.json', 'validation.json', 'sources/source.json',
                 'sources/review.json', 'sources/transcript.json'):
        if not (delivery/name).is_file():
            raise ValueError(f'Missing delivery artifact: {name}')
    if not list((delivery/'images').glob('*')):
        raise ValueError('Illustrated notes require actual images')
    if not s['notes_cli']:
        raise ValueError('Initialize with --notes-cli to validate real single-lesson output')
    checked = subprocess.run([s['notes_cli'], 'validate', '--plan', str(job_dir/'note-plan.json'),
                              '--output-dir', str(delivery)], capture_output=True, text=True, timeout=120)
    (Path(task['attempt_dir'])/'validation.log').write_text(checked.stdout+checked.stderr)
    if checked.returncode or not json.loads(checked.stdout).get('ok'):
        raise ValueError('Single-lesson validation failed; see attempt/validation.log')
    if read(delivery/'sources/source.json') != job['source']:
        raise ValueError('Wrong delivered source')
    # Snapshot the candidate before assigning a separate reviewer. Old attempts remain isolated.
    frozen = Path(task['attempt_dir'])/'snapshot'
    if frozen.exists():
        raise ValueError('Snapshot already exists; use a new attempt')
    job_files, files = tree(job_dir), tree(delivery)
    shutil.copytree(job_dir, frozen/'job')
    shutil.copytree(delivery, frozen/'delivery')
    if tree(frozen/'job') != job_files or tree(frozen/'delivery') != files:
        raise ValueError('Files changed while snapshotting')
    return dict(job_dir=str(frozen/'job'), job_files=job_files, delivery_dir=str(frozen/'delivery'),
                files=files, artifact_fingerprint=fingerprint(files),
                windows=[x['id'] for x in job['windows']],
                images=sorted(x for x in files if x.startswith('images/')))


def record(work, token, result_path):
    with locked(work) as (work, s):
        item, task = locate(s, token)
        if not item['active'].get('agent_id'):
            raise ValueError('Attach actual dispatch evidence before recording a result')
        result_path = inside(task['attempt_dir'], result_path)
        result = read(result_path)
        for k, v in task['result_template'].items():
            if result.get(k) != v:
                raise ValueError(f'Result binding mismatch: {k}')
        sources(item)
        outcome = result.get('status')
        if outcome == 'failed':
            item['failures'] = item.get('failures', 0) + 1
            item['error'] = str(result.get('error', 'Unspecified failure'))
            if result.get('needs_attention'):
                item['state'] = 'needs_attention'
            elif item['failures'] >= 3:
                item['state'] = 'failed'
            else:
                item['state'] = 'review_ready' if task['stage'] == 'reviewer' else 'ready'
        elif task['stage'] == 'writer' and outcome == 'checkpoint':
            check_job(item, task['job_dir'])
            frozen = Path(task['attempt_dir'])/'checkpoint'
            files = tree(task['job_dir'])
            shutil.copytree(task['job_dir'], frozen)
            if tree(frozen) != files:
                raise ValueError('Progress changed during checkpoint')
            item['checkpoint'] = dict(job_dir=str(frozen), job_files=files,
                                      bookmark=str(result.get('bookmark', 'Continue first pending window')))
            item.pop('candidate', None)
            item['state'] = 'ready'
        elif task['stage'] == 'writer' and outcome == 'drafted':
            item['candidate'] = validate_candidate(s, item, task)
            item.pop('checkpoint', None)
            item['state'] = 'review_ready'
        elif task['stage'] == 'reviewer' and outcome in ('PASS', 'FIX', 'UNCERTAIN'):
            candidate = item['candidate']
            if tree(candidate['delivery_dir']) != candidate['files'] or tree(candidate['job_dir']) != candidate['job_files']:
                raise ValueError('Candidate changed since review was assigned')
            if result.get('artifact_fingerprint') != candidate['artifact_fingerprint']:
                raise ValueError('Review is bound to another draft')
            if (result.get('reviewed_windows') != candidate['windows'] or
                sorted(result.get('viewed_images', [])) != candidate['images'] or
                not result.get('source_matching_evidence', '').strip()):
                raise ValueError('Full source/windows and final image review evidence is required')
            findings = result.get('findings')
            if not isinstance(findings, list) or (outcome == 'PASS' and findings) or (outcome == 'FIX' and not findings):
                raise ValueError('PASS requires no findings; FIX requires actionable findings')
            item['review'] = dict(result, reviewer_agent_id=item['active']['agent_id'])
            if outcome == 'PASS':
                item['state'] = 'passed'
            elif outcome == 'UNCERTAIN' or item['repairs'] >= 2:
                item['state'] = 'needs_attention'
            else:
                item['repairs'] += 1
                item['state'] = 'repair_ready'
        else:
            raise ValueError('Invalid outcome for this stage')
        item['active'] = None
        changed(work, s, 'recorded', lesson_id=item['id'], claim_token=token,
                outcome=outcome, result=str(result_path), result_sha256=digest(result_path))
        return dict(ok=True, lesson_id=item['id'], state=item['state'])


def recover(work, token, reason):
    if not reason.strip():
        raise ValueError('Record why the old worker is stopped/unreachable')
    with locked(work) as (work, s):
        item, task = locate(s, token)
        item['recoveries'] = item.get('recoveries', 0) + 1
        item['state'] = ('needs_attention' if item['recoveries'] >= 3 else
                         'review_ready' if task['stage'] == 'reviewer' else 'ready')
        item['active'] = None
        changed(work, s, 'revoked', lesson_id=item['id'], claim_token=token, reason=reason)
        return dict(ok=True, lesson_id=item['id'], state=item['state'])


def resume(work):
    report = status(work)
    report['checks'] = []
    with locked(work) as (_, s):
        for item in s['lessons']:
            try:
                if item['state'] == 'published':
                    if tree(item['published']['directory']) != item['published']['files']:
                        raise ValueError('Published files changed')
                else:
                    sources(item)
                    base = item.get('candidate') or item.get('checkpoint')
                    if base and tree(base['job_dir']) != base['job_files']:
                        raise ValueError('Saved job changed')
                    if item.get('candidate') and tree(item['candidate']['delivery_dir']) != item['candidate']['files']:
                        raise ValueError('Candidate changed')
                report['checks'].append(dict(lesson_id=item['id'], ok=True))
            except (ValueError, OSError) as exc:
                report['checks'].append(dict(lesson_id=item['id'], ok=False, error=str(exc)))
    report['ok'] = all(x['ok'] for x in report['checks'])
    report['recovery'] = 'Active claims are preserved. Confirm worker termination before explicit recover --token.'
    return report


def publish(work, lesson_id):
    with locked(work) as (work, s):
        item = next(x for x in s['lessons'] if x['id'] == lesson_id)
        if item['state'] == 'published':
            if tree(item['published']['directory']) != item['published']['files']:
                raise ValueError('Published artifacts changed; preserve them and investigate')
            return dict(ok=True, cache_hit=True, directory=item['published']['directory'])
        if item['state'] != 'passed':
            raise ValueError('Publish requires independent PASS')
        candidate = item['candidate']
        if tree(candidate['delivery_dir']) != candidate['files'] or tree(candidate['job_dir']) != candidate['job_files']:
            raise ValueError('PASS invalidated by changed candidate')
        sources(item)
        root = Path(s['output'])
        root.mkdir(parents=True, exist_ok=True)
        target = root/item['id']
        files = candidate['files']
        if target.exists():
            if tree(target) != files:
                raise ValueError('Publication target already contains another version')
        else:
            staging = Path(tempfile.mkdtemp(prefix='.publishing-', dir=root))
            try:
                shutil.copytree(candidate['delivery_dir'], staging/'lesson')
                if tree(staging/'lesson') != files:
                    raise ValueError('Candidate changed during publication')
                os.rename(staging/'lesson', target)
            finally:
                shutil.rmtree(staging)
        item['published'] = dict(directory=str(target), files=files)
        item['state'] = 'published'
        changed(work, s, 'published', lesson_id=item['id'], directory=str(target))
    return dict(ok=True, directory=str(target))


def index(work):
    with locked(work) as (_, s):
        root = Path(s['output'])
        root.mkdir(parents=True, exist_ok=True)
        rows, md = [], ['# '+s['title'].replace('\n', ' '), '']
        for x in s['lessons']:
            label = x['title'] or x['id']
            if x['state'] == 'published':
                if tree(x['published']['directory']) != x['published']['files']:
                    raise ValueError('Published artifacts changed')
                url = quote(x['id'])+'/note.html'
                rows.append(f'<li><a href="{url}">{html.escape(label)}</a> · published</li>')
                escaped = re.sub(r'([\\`*{}\[\]<>_])', r'\\\1', label.replace('\n', ' '))
                md.append(f'- [{escaped}]({quote(x["id"])}/note.md) · published')
            else:
                rows.append(f'<li>{html.escape(label)} · {html.escape(x["state"])}</li>')
                md.append(f'- {label.replace(chr(10), " ")} · {x["state"]}')
        page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        page += '<title>'+html.escape(s['title'])+'</title><style>body{max-width:55rem;margin:3rem auto;padding:0 1rem;font:18px/1.8 system-ui}li{margin:1rem 0}a{color:#17685e}</style>'
        page += '<h1>'+html.escape(s['title'])+'</h1><ul>'+''.join(rows)+'</ul></html>'
        (root/'index.html').write_text(page, encoding='utf-8')
        (root/'index.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
        report = dict(schema_version=1, title=s['title'], mode=s['mode'],
                      complete=all(x['state'] == 'published' for x in s['lessons']),
                      counts=dict(Counter(x['state'] for x in s['lessons'])),
                      lessons=[dict(id=x['id'], title=x['title'], state=x['state'],
                                    published=x.get('published'), review=x.get('review'), error=x.get('error')) for x in s['lessons']],
                      events=s['events'])
        save(root/'batch-report.json', report)
        return dict(ok=True, complete=report['complete'], counts=report['counts'], index=str(root/'index.html'))


def scan(directory):
    root = Path(directory).expanduser().resolve(strict=True)
    extensions = {'.mp4', '.mkv', '.webm', '.mov', '.m4v'}
    entries = []
    videos = (p for p in root.rglob('*') if p.suffix.lower() in extensions and p.is_file())
    natural = lambda p: [int(x) if x.isdigit() else x.casefold() for x in re.split(r'(\d+)', str(p))]
    for video in sorted(videos, key=natural):
        subtitles = [video.with_suffix('.srt'), video.parent/'transcript.srt', video.with_suffix('.json')]
        transcript = next((p for p in subtitles if p.is_file()), None)
        if transcript is None:
            raise ValueError(f'Prepare a matching SRT/JSON first: {video}')
        name = video.parent.name if video.stem == 'video' else video.stem
        media = re.search(r'(BV[A-Za-z0-9]+)_p(\d+)', name)
        label = re.search(r'(?:^|\s)(\d+(?:\.\d+)+)(?![\d.])', name)
        entries.append(dict(id=media[0] if media else 'local-'+fingerprint(str(video))[:16], title=name,
                            label=label[1] if label else '', video=str(video), transcript=str(transcript),
                            source_key=media[0] if media else str(video),
                            source_url=f'https://www.bilibili.com/video/{media[1]}/?p={media[2]}' if media else ''))
    if not entries:
        raise ValueError('No local lessons found')
    return dict(title=root.name, entries=entries)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('scan'); a.add_argument('--directory', type=Path, required=True); a.add_argument('--output', type=Path, required=True)
    a = sub.add_parser('init'); a.add_argument('--manifest', type=Path, required=True); a.add_argument('--work-dir', type=Path, required=True); a.add_argument('--output-dir', type=Path, required=True)
    a.add_argument('--labels'); a.add_argument('--mode', choices=('faithful', 'summary'), default='faithful'); a.add_argument('--max-active', type=int, default=2); a.add_argument('--notes-cli', type=Path, required=True)
    for name in ('status', 'next', 'resume', 'index', 'claim', 'attach', 'record', 'recover', 'publish'):
        a = sub.add_parser(name); a.add_argument('--batch', type=Path, required=True)
        if name == 'claim':
            a.add_argument('--lesson'); a.add_argument('--stage', choices=('writer', 'reviewer'))
        if name in ('attach', 'record', 'recover'):
            a.add_argument('--token', required=True)
        if name == 'attach':
            a.add_argument('--agent-id', required=True); a.add_argument('--host', required=True); a.add_argument('--isolation', choices=('fresh',), required=True)
        if name == 'record': a.add_argument('--result', type=Path, required=True)
        if name == 'recover': a.add_argument('--reason', required=True)
        if name == 'publish': a.add_argument('--lesson', required=True)
    args = p.parse_args()
    try:
        if args.command == 'scan':
            data = scan(args.directory); save(args.output, data); result = dict(ok=True, manifest=str(args.output.resolve()), lessons=len(data['entries']))
        elif args.command == 'init':
            result = initialize(args.manifest, args.work_dir, args.output_dir, [x.strip() for x in args.labels.split(',')] if args.labels else None, args.mode, args.max_active, args.notes_cli)
        elif args.command in ('status', 'next'): result = status(args.batch)
        elif args.command == 'claim': result = claim(args.batch, args.lesson, args.stage)
        elif args.command == 'attach': result = attach(args.batch, args.token, args.agent_id, args.host, args.isolation)
        elif args.command == 'record': result = record(args.batch, args.token, args.result)
        elif args.command == 'recover': result = recover(args.batch, args.token, args.reason)
        elif args.command == 'publish': result = publish(args.batch, args.lesson)
        elif args.command == 'resume': result = resume(args.batch)
        else: result = index(args.batch)
    except (ValueError, KeyError, TypeError, OSError, StopIteration, subprocess.SubprocessError) as exc:
        result = dict(ok=False, error=str(exc))
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
