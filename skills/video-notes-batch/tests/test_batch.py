import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
import unittest

SCRIPT = Path(__file__).parents[1] / 'scripts/video_notes_batch.py'


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        spec = importlib.util.spec_from_file_location('batch', SCRIPT)
        self.b = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.b)

    def manifest(self, labels=('2.1', '2.2', '2.10')):
        entries = []
        for i, label in enumerate(labels):
            video = self.root / f'{i}.mp4'
            video.write_bytes(f'video-{i}'.encode())
            transcript = self.root / f'{i}.srt'
            transcript.write_text('1\n00:00:00,000 --> 00:00:01,000\n正文\n')
            entries.append(dict(id=f'l{i}', label=label, title=f'{label} title',
                                video=str(video), transcript=str(transcript), source_url=''))
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'title': 'Course', 'entries': entries}))
        return manifest

    def init(self, **kw):
        return self.b.initialize(self.manifest(), self.root/'work', self.root/'out', **kw)

    def test_exact_labels_and_frozen_inputs(self):
        self.init(labels=['2.1', '2.2'])
        state = self.b.read(self.root/'work/batch.json')
        self.assertEqual([x['label'] for x in state['lessons']], ['2.1', '2.2'])
        self.assertTrue(all(x['input_fingerprint'] for x in state['lessons']))
        (self.root/'0.mp4').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.b.claim(self.root/'work', lesson_id='l0')

    def test_atomic_claim_capacity_and_stale_results(self):
        self.init()
        one = self.b.claim(self.root/'work', lesson_id='l0')
        self.b.claim(self.root/'work', lesson_id='l1')
        with self.assertRaises(ValueError):
            self.b.claim(self.root/'work', lesson_id='l2')
        with self.assertRaises(ValueError):
            self.b.claim(self.root/'work', lesson_id='l0')
        self.b.recover(self.root/'work', one['claim_token'], 'worker stopped')
        newer = self.b.claim(self.root/'work', lesson_id='l0')
        self.assertNotEqual(one['claim_token'], newer['claim_token'])
        result = dict(self.b.read(one['task'])['result_template'], status='failed', error='late')
        path = self.root/'late.json'
        path.write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            self.b.record(self.root/'work', one['claim_token'], path)

    def test_no_silent_input_or_mode_reuse(self):
        self.init()
        with self.assertRaises(ValueError):
            self.b.initialize(self.root/'manifest.json', self.root/'work', self.root/'out', mode='summary')
        self.assertEqual(self.b.status(self.root/'work')['counts'], {'ready': 3})

    def test_resume_preserves_live_claims(self):
        self.init()
        one = self.b.claim(self.root/'work', lesson_id='l0')
        before = (self.root/'work/batch.json').read_bytes()
        self.b.resume(self.root/'work')
        self.assertEqual(before, (self.root/'work/batch.json').read_bytes())
        self.assertIn(one['claim_token'], [a['claim_token'] for a in self.b.status(self.root/'work')['active']])

    def test_duplicate_labels_and_empty_selection_fail_before_work(self):
        m = self.manifest(('2.1', '2.1'))
        with self.assertRaises(ValueError):
            self.b.initialize(m, self.root/'work', self.root/'out', labels=['2.1'])
        self.assertFalse((self.root/'work').exists())
        for labels in (['9.9'], [], ['']):
            with self.assertRaises(ValueError):
                self.b.initialize(m, self.root/'work', self.root/'out', labels=labels)

    def test_result_requires_dispatch_evidence(self):
        self.init()
        one = self.b.claim(self.root/'work', lesson_id='l0')
        task = self.b.read(one['task'])
        result = dict(task['result_template'], status='failed', error='test')
        path = Path(task['attempt_dir'])/'result.json'
        path.write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            self.b.record(self.root/'work', one['claim_token'], path)
        self.b.attach(self.root/'work', one['claim_token'], 'agent-a', 'test', 'fresh')
        self.assertEqual(self.b.record(self.root/'work', one['claim_token'], path)['state'], 'ready')

    def test_concurrent_claims_respect_capacity(self):
        self.init()
        def attempt(i):
            try:
                return self.b.claim(self.root/'work', lesson_id=f'l{i}')['claim_token']
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(attempt, range(3)))
        self.assertEqual(sum(bool(x) for x in results), 2)
        self.assertEqual(len(self.b.status(self.root/'work')['active']), 2)

    def complete_fixture(self):
        cli = Path(__file__).parents[3]/'skills/video-notes/scripts/video-notes'
        manifest = self.manifest(('2.1',))
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        'color=red:s=96x64:r=10:d=1', '-pix_fmt', 'yuv420p', str(self.root/'0.mp4')], check=True)
        self.b.initialize(manifest, self.root/'work', self.root/'out', notes_cli=cli)
        one = self.b.claim(self.root/'work')
        self.b.attach(self.root/'work', one['claim_token'], 'test-writer', 'test', 'fresh')
        task = self.b.read(one['task'])
        job = Path(task['job_dir'])
        delivery = Path(task['delivery_dir'])
        def run(*args):
            completed = subprocess.run([str(cli), *map(str, args)], check=True, capture_output=True, text=True)
            return json.loads(completed.stdout)
        run('prepare', '--video', task['video'], '--transcript', task['transcript'], '--work-dir', job,
            '--title', task['title'], '--source-note', 'Synthetic red frame and one synthetic cue', '--mode', 'faithful')
        (job/'chunks/w001.md').write_text('正文。\n\n<!-- figure:f001 -->\n')
        run('review', '--work-dir', job, '--window', 'w001', '--source-reviewed', '--visual-reviewed', '--note', 'Synthetic fixture')
        (job/'draft.md').write_text('# Synthetic\n\n正文。\n\n<!-- figure:f001 -->\n')
        image = job/'f001.jpg'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', task['video'], '-frames:v', '1', str(image)], check=True)
        fig = dict(id='f001', timestamp=.2, caption='Red frame', source_segment_ids=['seg00001'], reviewed_sha256=self.b.digest(image))
        self.b.save(job/'note-plan.json', {'figures': [fig]})
        self.b.save(job/'captures.json', dict(video_sha256=task['video_sha256'], failures=[], figures=[dict(fig, file='f001.jpg', sha256=self.b.digest(image))]))
        run('assemble', '--draft', job/'draft.md', '--plan', job/'note-plan.json', '--captures', job/'captures.json', '--output-dir', delivery)
        run('render', '--markdown', delivery/'note.md', '--output-dir', delivery)
        run('validate', '--plan', job/'note-plan.json', '--output-dir', delivery)
        result = Path(task['attempt_dir'])/'result.json'
        self.b.save(result, dict(task['result_template'], status='drafted'))
        self.b.record(self.root/'work', one['claim_token'], result)
        return task

    def pass_fixture(self):
        self.complete_fixture()
        one = self.b.claim(self.root/'work', stage='reviewer')
        task = self.b.read(one['task'])
        with self.assertRaises(ValueError):
            self.b.attach(self.root/'work', one['claim_token'], 'test-writer', 'test', 'fresh')
        self.b.attach(self.root/'work', one['claim_token'], 'test-reviewer', 'test', 'fresh')
        result = dict(task['result_template'], status='PASS', artifact_fingerprint=task['candidate']['artifact_fingerprint'],
                      reviewed_windows=task['candidate']['windows'], viewed_images=task['candidate']['images'],
                      source_matching_evidence='Synthetic fixture red frame and source cue', findings=[])
        path = Path(task['attempt_dir'])/'result.json'
        self.b.save(path, result)
        self.b.record(self.root/'work', one['claim_token'], path)
        return task

    def test_real_package_independent_review_and_publish(self):
        self.pass_fixture()
        self.b.publish(self.root/'work', 'l0')
        before = self.b.tree(self.root/'out/l0')
        (self.root/'0.mp4').unlink()
        (self.root/'0.srt').unlink()
        self.assertTrue(self.b.resume(self.root/'work')['ok'])
        self.assertTrue(self.b.publish(self.root/'work', 'l0')['cache_hit'])
        self.assertEqual(before, self.b.tree(self.root/'out/l0'))
        self.assertTrue(self.b.index(self.root/'work')['complete'])

    def test_changed_candidate_invalidates_pass(self):
        task = self.pass_fixture()
        (Path(task['candidate']['delivery_dir'])/'note.md').write_text('changed after review')
        with self.assertRaises(ValueError):
            self.b.publish(self.root/'work', 'l0')
        self.assertFalse(self.b.resume(self.root/'work')['ok'])

    def test_checkpoint_moves_progress_into_new_attempt(self):
        self.complete_fixture()
        # Simulate interruption in a separate new batch rather than forging completion.
        state = self.b.read(self.root/'work/batch.json')
        item = state['lessons'][0]
        item['state'] = 'repair_ready'
        self.b.save(self.root/'work/batch.json', state)
        one = self.b.claim(self.root/'work')
        self.b.attach(self.root/'work', one['claim_token'], 'checkpoint-writer', 'test', 'fresh')
        task = self.b.read(one['task'])
        result = Path(task['attempt_dir'])/'result.json'
        self.b.save(result, dict(task['result_template'], status='checkpoint', bookmark='Finish merge'))
        self.b.record(self.root/'work', one['claim_token'], result)
        two = self.b.claim(self.root/'work')
        copied = self.b.read(two['task'])
        self.assertNotEqual(task['job_dir'], copied['job_dir'])
        self.assertEqual(self.b.tree(task['job_dir']), self.b.tree(copied['job_dir']))
        self.assertEqual(copied['resume_from']['bookmark'], 'Finish merge')


    def test_review_retry_requires_new_context_and_actionable_fix(self):
        self.complete_fixture()
        one = self.b.claim(self.root/'work', stage='reviewer')
        task = self.b.read(one['task'])
        self.b.attach(self.root/'work', one['claim_token'], 'review-a', 'test', 'fresh')
        path = Path(task['attempt_dir'])/'result.json'
        result = dict(task['result_template'], status='FIX', artifact_fingerprint=task['candidate']['artifact_fingerprint'],
                      reviewed_windows=task['candidate']['windows'], viewed_images=task['candidate']['images'],
                      source_matching_evidence='Synthetic review', findings=[])
        self.b.save(path, result)
        with self.assertRaises(ValueError):
            self.b.record(self.root/'work', one['claim_token'], path)
        state = self.b.read(self.root/'work/batch.json')
        self.assertEqual(state['lessons'][0]['repairs'], 0)
        self.assertEqual(state['lessons'][0]['state'], 'reviewing')
        self.b.save(path, dict(task['result_template'], status='failed', error='review interrupted'))
        self.b.record(self.root/'work', one['claim_token'], path)
        two = self.b.claim(self.root/'work', stage='reviewer')
        with self.assertRaises(ValueError):
            self.b.attach(self.root/'work', two['claim_token'], 'review-a', 'test', 'fresh')
        self.b.attach(self.root/'work', two['claim_token'], 'review-b', 'test', 'fresh')

    def test_scan_preserves_natural_lesson_order_and_part_identity(self):
        course = self.root/'course'
        for label, part in [('2.10', 14), ('2.2', 6), ('2.1', 5)]:
            d = course/f'{label} GPIO [BVexample_p{part}]'
            d.mkdir(parents=True)
            (d/'video.mp4').write_bytes(b'video')
            (d/'transcript.srt').write_text('source')
        result = self.b.scan(course)
        self.assertEqual([e['label'] for e in result['entries']], ['2.1', '2.2', '2.10'])
        self.assertEqual([e['id'] for e in result['entries']], ['BVexample_p5', 'BVexample_p6', 'BVexample_p14'])
        flat = self.root/'flat'
        flat.mkdir()
        (flat/'Course p05 2.1 GPIO [BVexample_p5].mp4').write_bytes(b'video')
        (flat/'transcript.srt').write_text('source')
        self.assertEqual(self.b.scan(flat)['entries'][0]['label'], '2.1')

    def test_publication_names_are_reserved_and_ids_are_portable(self):
        manifest = self.manifest(('2.1', '2.2'))
        raw = self.b.read(manifest)
        for reserved in ('index.html', 'INDEX.MD', 'batch-report.json'):
            raw['entries'][0]['id'] = reserved
            self.b.save(manifest, raw)
            with self.assertRaises(ValueError):
                self.b.initialize(manifest, self.root/'work', self.root/'out')
            self.assertFalse((self.root/'work').exists())
        raw['entries'][0]['id'] = 'Lesson'
        raw['entries'][1]['id'] = 'lesson'
        self.b.save(manifest, raw)
        with self.assertRaises(ValueError):
            self.b.initialize(manifest, self.root/'work', self.root/'out')


if __name__ == '__main__':
    unittest.main()
