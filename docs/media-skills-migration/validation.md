# 下载与转写 Skill 迁移验收

状态：2026-10-16 迁移实施的验证快照，随 PR #16 合入；不是本次文档整理重新运行的结果。范围与来源见[设计](design.md)。


- 新安装器先以旧实现运行 5 项测试，全部失败，复现选项被忽略、无定向安装、替换无备份、复制运行缓存等问题。实现后这 5 项及既有智能体安装器 3 项均通过。
- Whisper 新增 5 项无模型回归：迁移后启动帮助、CPU dry-run、混合语言 dry-run、五种文件格式和时间戳校验、缺少翻译模型时明确失败。
- 下载器原有 12 项 pytest 全部通过，包括真实本地 HTML5 播放列表经 yt-dlp 仅下载选定项，以及第一方 54P 元数据 fixture。
- 既有 video-notes-batch 13 项、video-notes 8 项、video-frames 4 项通过。合计 **50 项测试通过**。
- 临时 CODEX_HOME 中仅安装两个目标 Skill，从仓库外目录启动各自帮助入口；下载器在新位置实际完成首次运行环境准备，均成功。没有创建智能体配置，也没有下载 Whisper 模型。
- 下载器通过内置 Skill 结构校验。Whisper 保留原 `compatibility` 元数据字段；当前内置 quick_validate.py 不支持该字段并报错，本次没有为消除校验器限制而改写原 SKILL.md。另以 YAML 解析验证名称、描述、compatibility、脚本/引用路径及许可证完整。npm 打包预览检查完整包含运行文件、锁文件、测试 fixture 和 Whisper LICENSE，排除运行缓存。

常用测试入口（仓库根目录）：

```sh
node --test tests/*.test.mjs
python3 -B -m unittest discover -s skills/local-whisper/tests -v
uv run --frozen --project skills/yt-dlp-download/runtime --group dev python -B -m pytest skills/yt-dlp-download/tests -q
```

本次没有重新调用线上视频平台或执行神经网络 ASR/字幕翻译；运行代码与原版本字节一致，验证聚焦文件迁移、独立安装、接口和输出兼容。两个迁入 Skill 的原使用说明中的安装仓库地址已更新，其运行规则未改动。
