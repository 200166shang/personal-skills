# 下载与转写 Skill 集中维护

2026-10-16。迁移目标是统一源码维护，不改变媒体处理行为，不安装/修改智能体，不重新生成已完成的笔记。

## 来源与历史

| 新位置 | 原仓库 | 导入的 origin/main |
| --- | --- | --- |
| `skills/local-whisper/` | [local-whisper-skill](https://github.com/200166shang/local-whisper-skill) | `3effd19b46e7a939bfca613ec5b5fee18acfce0e` |
| `skills/yt-dlp-download/` | [yt-dlp-download](https://github.com/200166shang/yt-dlp-download) | `412622f52c6b676235581b2648eec8a7dd77d50e` |

使用未 squash 的 Git subtree 导入，原提交及作者保留在当前分支祖先中。下载仓库先整体导入，再通过 git mv 将 Skill、测试和说明放到集合仓库的规范位置；没有 Git submodule 或第二套嵌套仓库。合并此 PR 时应使用 **merge commit**，不要 squash/rebase，否则原仓库提交不再是主线祖先。可用 `git merge-base --is-ancestor <上表提交> HEAD` 检查。

下载器测试迁至 `skills/yt-dlp-download/tests/`，54P 元数据 fixture 一并保留；原验收报告改为 `research/yt-dlp-playlist-validation.md`。Whisper 的 MIT LICENSE 原样放在其 Skill 目录内，不扩展到集合中其他代码。

合并后，这两个 Skill 以 personal-skills 为唯一维护位置。本 PR 没有修改或归档远端旧仓库；旧源目录也保留。旧仓库的迁移公告和归档可以在本 PR 合并后单独执行，避免提前让未合并代码成为安装入口。

## 保持不变

- 两份 SKILL.md、原运行脚本、引用规则、依赖版本及下载器 uv.lock 字节一致；逐文件核对了 Whisper 的 7 份运行/规则/许可证文件和下载器的 10 份运行/规则/配置文件。
- Skill 名称仍为 local-whisper、yt-dlp-download，安装路径仍是现有的技能目录名，现有智能体引用无需变化。
- 下载质量、目录参数、输出根目录、缓存位置、ASR 后端选择及模型下载机制保持原样。
- 不提交模型、虚拟环境、Cookie、登录状态、实际媒体、转写、生成笔记或机器相关 setup 标记。

## 定向安装

在仓库根目录执行：

```sh
node bin/install.mjs --list
node bin/install.mjs --skill local-whisper --skill yt-dlp-download
node bin/install.mjs --skill local-whisper --skill yt-dlp-download --force
```

不指定 --skill 仍安装全部，已有副本默认跳过；可重复指定 --skill。无效技能名和未知参数在任何目的目录写入前报错。--list 仅读取。--force 将原安装目录移到 `$CODEX_HOME/skill-backups/<唯一批次>/<技能名>/`，先在发现目录以外准备新副本，成功后再替换；失败可保留/恢复原副本。未选中的技能和智能体不改变。环境、缓存、字节码、setup 锁与完成标记不会从源码复制到安装目录。

系统仍需预先提供 uv 及相应媒体工具。下载器首次启动保留原 setup/doctor 机制，在安装目录 runtime/.venv 准备锁定环境；Whisper 使用共享 uv/模型缓存。迁移不新增依赖安装器、模型调用或 GPU 驱动管理。

## 验证

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
