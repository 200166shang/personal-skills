"""Offline relocation regressions; no ASR model or Ollama download is performed."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('local_transcribe', ROOT/'scripts/transcribe.py')
asr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asr)
spec = importlib.util.spec_from_file_location('local_translate', ROOT/'scripts/translate.py')
translate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(translate)


class RelocatedWhisperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='whisper relocation ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.audio = self.root/'sample.wav'
        with wave.open(str(self.audio), 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(b'\0\0' * 16000)

    def test_relocated_launchers_help_needs_no_model(self):
        p = subprocess.run([str(ROOT/'scripts/run.sh'), '--help'], text=True, capture_output=True, check=True)
        self.assertIn('--mixed-language', p.stdout)
        p = subprocess.run([sys.executable, str(ROOT/'scripts/translate.py'), '--help'], text=True, capture_output=True, check=True)
        self.assertIn('--target-language', p.stdout)

    def test_dry_run_keeps_cpu_plan_and_writes_no_transcript(self):
        out = self.root/'out'
        p = subprocess.run([sys.executable, str(ROOT/'scripts/transcribe.py'), str(self.audio),
                            '--backend', 'faster-whisper', '--device', 'cpu', '--model', 'small',
                            '--output-dir', str(out), '--dry-run'], text=True, capture_output=True, check=True)
        plan = json.loads(p.stdout)
        self.assertEqual((plan['backend'], plan['model'], plan['device'], plan['compute_type']),
                         ('faster-whisper', 'small', 'cpu', 'int8'))
        self.assertFalse(out.exists())

    def test_mixed_language_plan_uses_window_capable_backend(self):
        p = subprocess.run([sys.executable, str(ROOT/'scripts/transcribe.py'), str(self.audio),
                            '--mixed-language', '--device', 'cpu', '--dry-run'], text=True, capture_output=True, check=True)
        plan = json.loads(p.stdout)
        self.assertEqual(plan['backend'], 'faster-whisper')
        self.assertTrue(plan['mixed_language'])

    def test_all_output_formats_preserve_text_timestamps_and_validate(self):
        payload = {'segments': [dict(start=0.125, end=1.2, text='第一步', language='zh'),
                                dict(start=1.2, end=2.9, text='Next step', language='en')]}
        out = self.root/'out'
        files = asr.write_outputs(payload, out, 'lecture', asr.requested_formats('all'))
        self.assertEqual({p.suffix for p in files}, {'.txt', '.srt', '.vtt', '.json', '.tsv'})
        self.assertIn('00:00:00,125 --> 00:00:01,200\n第一步', (out/'lecture.srt').read_text())
        self.assertTrue((out/'lecture.vtt').read_text().startswith('WEBVTT'))
        self.assertEqual(json.loads((out/'lecture.json').read_text()), payload)
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_outputs.py'), str(out/'lecture.json')], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload['segments'][0]['words'] = [dict(start=0, end=2, word='bad alignment')]
        (out/'lecture.json').write_text(json.dumps(payload))
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_outputs.py'), str(out/'lecture.json')], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_missing_translation_model_requires_explicit_preparation(self):
        with self.assertRaises(SystemExit):
            translate.choose_model('qwen3:8b', [])
        self.assertEqual(translate.choose_model('auto', ['qwen3:8b']), 'qwen3:8b')


if __name__ == '__main__':
    unittest.main()
