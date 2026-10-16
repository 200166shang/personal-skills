import argparse
from pathlib import Path
import pytest
from yt_dlp_download import cli


def test_selection_is_inclusive_ordered_and_validated():
    assert cli._selection('5:9,2,5', 10) == [2, 5, 6, 7, 8, 9]
    for value in ('0', '-1', '4:2', '11', '', '1::3', 'all'):
        with pytest.raises(ValueError):
            cli._selection(value, 10)


def test_native_catalog_keeps_unavailable_positions():
    raw = dict(id='PL1', title='course', extractor_key='YoutubeTab', _type='playlist', entries=[
        dict(id='a', title='A', url='https://www.youtube.com/watch?v=a', duration=4),
        None,
        dict(id='c', title='[Private video]', availability='private')])
    data = cli._catalog_result(raw, 'https://www.youtube.com/playlist?list=PL1')
    assert [x['index'] for x in data['entries']] == [1, 2, 3]
    assert data['entries'][1]['available'] is False
    assert data['entries'][2]['available'] is False
    assert data['entries'][0]['url'] == 'https://www.youtube.com/watch?v=a'


def test_bilibili_catalog_expands_part_without_changing_single_inspect(monkeypatch):
    monkeypatch.setattr(cli, "_public_bili_catalog", lambda url: None)
    seen = []
    class Fake:
        def __init__(self, opts): seen.append(opts)
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def extract_info(self, url, download=False):
            seen.append(url)
            return dict(_type='playlist', id='BVabc', extractor_key='BiliBili', entries=[
                dict(id='BVabc_p1', title='one', url='https://www.bilibili.com/video/BVabc?p=1'),
                dict(id='BVabc_p2', title='two', url='https://www.bilibili.com/video/BVabc?p=2')])
    monkeypatch.setattr(cli.yt_dlp, 'YoutubeDL', Fake)
    result = cli._catalog('https://www.bilibili.com/video/BVabc/?p=2')
    assert len(result['entries']) == 2
    assert '?p=2' not in seen[1]
    assert seen[0]['noplaylist'] is False
    assert cli._base_options()['noplaylist'] is True


def test_batch_keeps_partial_results_and_does_not_expand_range(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, '_catalog', lambda *a: dict(ok=True, entries=[
        dict(index=i, id=str(i), title=str(i), available=True, url=f'https://example.com/{i}') for i in range(1, 6)]))
    called = []
    def one(args):
        called.append(args.url)
        if args.url.endswith('/3'): raise ValueError('unavailable')
        return dict(ok=True, files=['/confirmed/file'])
    monkeypatch.setattr(cli, '_download', one)
    args = cli._parser().parse_args(['download', 'https://example.com/list', '--playlist-items', '2:4'])
    result = cli._download_batch(args)
    assert called == ['https://example.com/2', 'https://example.com/3', 'https://example.com/4']
    assert result['ok'] is False
    assert [r['ok'] for r in result['results']] == [True, False, True]
    assert [r['index'] for r in result['results']] == [2, 3, 4]


def test_default_download_does_not_enable_playlist():
    args = cli._parser().parse_args(['download', 'https://example.com/video'])
    assert not args.playlist and args.playlist_items is None


def test_real_generic_playlist_downloads_only_selected_item(tmp_path, monkeypatch):
    base = cli._base_options
    monkeypatch.setattr(cli, '_base_options', lambda browser=None: dict(base(browser), proxy=''))
    import functools
    import http.server
    import subprocess
    import threading
    from urllib.parse import urlsplit
    import yt_dlp
    serve = tmp_path/'serve'
    serve.mkdir()
    for n, color in ((1, 'red'), (2, 'blue')):
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        f'color={color}:s=96x64:r=10:d=1', '-f', 'lavfi', '-i', 'anullsrc=r=8000:cl=mono',
                        '-shortest', '-pix_fmt', 'yuv420p', str(serve/f'v{n}.mp4')], check=True)
    (serve/'index.html').write_text('<title>Local fixture</title><video src="v1.mp4" controls></video><video src="v2.mp4" controls></video>')
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(serve))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f'http://127.0.0.1:{server.server_port}/index.html'
        args = cli._parser().parse_args(['--data-dir', str(tmp_path/'downloads'), 'download', url, '--playlist-items', '2'])
        result = cli._download_batch(args)
        assert result['ok'], result
        assert len(result['results']) == 1 and result['selected_indices'] == [2]
        files = result['results'][0]['files']
        assert len(files) == 1 and Path(files[0]).is_file()
        check = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', files[0]], capture_output=True, text=True, check=True)
        assert 'video' in check.stdout and 'audio' in check.stdout
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_actual_54_part_metadata_fixture_selects_gpio_sections(monkeypatch):
    import io
    payload = (Path(__file__).parent/'fixtures/bilibili-pages.json').read_text()
    monkeypatch.setattr(cli, 'urlopen', lambda *a, **kw: io.StringIO(payload))
    catalog = cli._catalog('https://www.bilibili.com/video/BV11X4y1j7si/?p=2')
    assert catalog['count'] == 54 and catalog['complete']
    selected = [catalog['entries'][i-1] for i in cli._selection('5:9', 54)]
    assert [e['title'].split()[0] for e in selected] == ['2.1', '2.2', '2.3', '2.4', '2.5']
    assert [e['provider']['cid'] for e in selected] == [26335970481, 26054951429, 26351173764, 26360349837, 26054951605]
    assert sum(e['duration'] for e in selected) == 7322


def test_platform_rejection_stops_remaining_requests(monkeypatch):
    monkeypatch.setattr(cli, '_catalog', lambda *a: dict(ok=True, complete=True, entries=[
        dict(index=i, id=str(i), available=True, url=f'https://example.com/{i}') for i in range(1, 4)]))
    calls = []
    def denied(args):
        calls.append(args.url)
        raise ValueError('HTTP Error 412: Precondition Failed')
    monkeypatch.setattr(cli, '_download', denied)
    args = cli._parser().parse_args(['download', 'https://example.com/list', '--playlist'])
    result = cli._download_batch(args)
    assert len(calls) == 1
    assert [x['status'] for x in result['results']] == ['failed', 'not_attempted', 'not_attempted']
