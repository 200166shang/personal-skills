import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

from PIL import Image

spec = importlib.util.spec_from_file_location("frames", Path(__file__).parents[1] / "scripts/video_frames.py")
frames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frames)


class FramesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="video-测试 ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.video = self.root / "颜色 视频.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "color=red:s=80x120:r=10:d=1", "-f", "lavfi", "-i",
                        "color=blue:s=80x120:r=10:d=1", "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0",
                        "-pix_fmt", "yuv420p", str(self.video)], check=True)

    def test_capture_observable_color_and_no_failed_link(self):
        plan = self.root / "plan.json"
        frames.save_json(plan, {"figures": [{"id": "red", "timestamp": .2}, {"id": "blue", "timestamp": 1.2}]})
        result = frames.capture(SimpleNamespace(video=self.video, plan=plan, output_dir=self.root / "captures"))
        self.assertTrue(result["ok"])
        with Image.open(self.root / "captures/red.jpg") as im:
            r, g, b = im.getpixel((40, 60))
            self.assertGreater(r, b + 100)
        with Image.open(self.root / "captures/blue.jpg") as im:
            r, g, b = im.getpixel((40, 60))
            self.assertGreater(b, r + 100)
        frames.save_json(plan, {"figures": [{"id": "bad", "timestamp": 3}]})
        with self.assertRaises(ValueError):
            frames.capture(SimpleNamespace(video=self.video, plan=plan, output_dir=self.root / "captures"))
        self.assertFalse((self.root / "captures/bad.jpg").exists())

    def test_partial_sheet_preserves_tail_aspect_and_cache(self):
        args = SimpleNamespace(video=self.video, start=0, end=2, interval=.8, grid="2x2",
                               cell_width=320, output_dir=self.root / "preview")
        result = frames.preview(args)
        data = json.loads(Path(result["manifest"]).read_text())
        self.assertEqual(len(data["sheets"]), 1)
        self.assertEqual(len(data["sheets"][0]["cells"]), 4)
        self.assertAlmostEqual(data["sheets"][0]["cells"][-1]["timestamp"], 1.9)
        with Image.open(self.root / "preview/preview-001.jpg") as image:
            self.assertEqual(image.size, (160, 296))
        self.assertTrue(frames.preview(args)["cache_hit"])
        (self.root / "preview/preview-001.jpg").write_bytes(b"corrupt cache")
        self.assertFalse(frames.preview(args)["cache_hit"])
        args.interval = .5
        with self.assertRaises(ValueError):
            frames.preview(args)

    def test_hours_nonfinite_and_duplicate_ids(self):
        self.assertEqual(frames.timestamp(3661.234), "01:01:01.234")
        for interval in (0, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                frames.sample_times(0, 1, interval)
        plan = self.root / "duplicate.json"
        frames.save_json(plan, {"figures": [{"id": "x", "timestamp": .2}, {"id": "x", "timestamp": .4}]})
        with self.assertRaises(ValueError):
            frames.capture(SimpleNamespace(video=self.video, plan=plan, output_dir=self.root / "out"))

    def test_audio_tail_is_not_sampled_as_video(self):
        longer = self.root / "audio-tail.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(self.video), "-f", "lavfi",
                        "-i", "anullsrc=r=44100:cl=mono", "-t", "3", "-c:v", "copy", "-c:a", "aac", str(longer)], check=True)
        result = frames.preview(SimpleNamespace(video=longer, start=0, end=None, interval=1, grid="2x2",
                                               cell_width=320, output_dir=self.root / "audio-preview"))
        times = [c["timestamp"] for s in result["sheets"] for c in s["cells"]]
        self.assertLess(max(times), 2)


if __name__ == "__main__":
    unittest.main()
