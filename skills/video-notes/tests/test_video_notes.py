import importlib.util
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace as Args
import unittest

spec = importlib.util.spec_from_file_location("notes", Path(__file__).parents[1] / "scripts/video_notes.py")
notes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notes)


class NotesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="笔记 测试 ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.video = self.root / "video.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "color=red:s=96x64:r=10:d=3", "-pix_fmt", "yuv420p", str(self.video)], check=True)
        self.srt = self.root / "source.srt"
        self.srt.write_text("1\n00:00:00,125 --> 00:00:01,200\n第一步\n\n"
                            "2\n00:00:01,200 --> 00:00:02,900\n第二步\n")
        self.work = self.root / "work"
        self.args = Args(video=self.video, transcript=self.srt, window_seconds=1, source_url="https://www.bilibili.com/video/BVexample/?p=2",
                         title="示例笔记", source_note="Compared matching source samples", work_dir=self.work, start=0, end=None)
        notes.prepare(self.args)

    def reviewed(self):
        job = notes.read_json(self.work / "job.json")
        for w in job["windows"]:
            (self.work / w["chunk"]).write_text("## 步骤\n\n真实来源说明。\n")
            notes.review(Args(work_dir=self.work, window=w["id"], source_reviewed=True, visual_reviewed=True, note="Read source and viewed preview"))

    def delivery(self):
        self.reviewed()
        captures = self.root / "captures"
        captures.mkdir()
        image = captures / "f001.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(self.video), "-frames:v", "1", str(image)], check=True)
        value = notes.digest(image)
        figures = [{"id": "f001", "timestamp": .5, "caption": "安装界面", "source_segment_ids": ["seg00001"], "reviewed_sha256": value}]
        notes.save_json(self.work / "note-plan.json", {"figures": figures})
        job = notes.read_json(self.work / "job.json")
        notes.save_json(captures / "captures.json", {"video_sha256": job["input"]["video_sha256"], "failures": [],
                        "figures": [{"id": "f001", "timestamp": .5, "file": "f001.jpg", "sha256": value}]})
        draft = self.work / "draft.md"
        draft.write_text("# 标题 {{body}}\n\n## 安装\n\n说明。\n\n<!-- figure:f001 -->\n\n## 安装\n\n<script>alert(1)</script>\n")
        out = self.root / "delivery"
        args = Args(draft=draft, plan=self.work / "note-plan.json", captures=captures / "captures.json", output_dir=out)
        notes.assemble(args)
        notes.render(Args(markdown=out / "note.md", output_dir=out))
        return args, out

    def test_portable_delivery_links_and_html_escaping(self):
        args, out = self.delivery()
        self.assertTrue(notes.validate(args)["ok"])
        text = (out / "note.md").read_text()
        self.assertIn("p=2&t=0", text)
        self.assertNotIn("<!-- figure:", text)
        page = (out / "note.html").read_text()
        self.assertIn("<title>标题 {{body}}</title>", page)
        self.assertIn('id="安装-2"', page)
        self.assertNotIn("<script>alert(1)</script>", page)
        moved = self.root / "moved"
        out.rename(moved)
        args.output_dir = moved
        self.assertTrue(notes.validate(args)["ok"])

    def test_changed_draft_source_and_render_invalidate_evidence(self):
        args, out = self.delivery()
        (out / "note.md").write_text((out / "note.md").read_text() + "\n新内容")
        with self.assertRaises(ValueError): notes.validate(args)
        self.srt.write_text(self.srt.read_text() + "\n")
        with self.assertRaises(ValueError): notes.checked_job(self.work)
        with self.assertRaises(ValueError): notes.prepare(self.args)

    def test_missing_or_unreviewed_images_are_rejected(self):
        args, out = self.delivery()
        plan = notes.read_json(args.plan)
        del plan["figures"][0]["reviewed_sha256"]
        notes.save_json(args.plan, plan)
        with self.assertRaises(ValueError): notes.assemble(args)
        (out / "images/f001.jpg").unlink()
        with self.assertRaises(ValueError): notes.render(Args(markdown=out / "note.md", output_dir=out))

    def test_bad_cues_and_asset_traversal(self):
        self.srt.write_text("1\n00:00:00,125 --> 00:00:01,200\n第一步\n\n2\nbroken --> line\n错\n")
        with self.assertRaises(ValueError): notes.subtitle_segments(self.srt, 3)
        with self.assertRaises(ValueError): notes.inside(self.work, "../source.srt")
        self.srt.write_text("1\n00:00:00,125 --> 00:00:09,200\n错媒体\n")
        with self.assertRaises(ValueError): notes.subtitle_segments(self.srt, 3)

    def test_scope_extension_and_missing_windows(self):
        args = Args(**vars(self.args))
        args.work_dir = self.root / "sample"
        args.end = 1
        notes.prepare(args)
        job = notes.read_json(args.work_dir / "job.json")
        self.assertEqual(job["source"]["range"]["end"], 1.2)
        self.assertEqual(job["windows"][0]["segment_ids"], ["seg00001"])
        self.reviewed()
        job = notes.read_json(self.work / "job.json")
        job["windows"].pop()
        notes.save_json(self.work / "job.json", job)
        with self.assertRaises(ValueError): notes.checked_job(self.work)

    def test_source_part_change_is_not_silently_accepted(self):
        self.reviewed()
        job = notes.read_json(self.work / "job.json")
        job["source"]["part"] = 1
        notes.save_json(self.work / "job.json", job)
        with self.assertRaises(ValueError): notes.checked_job(self.work)


if __name__ == "__main__":
    unittest.main()
