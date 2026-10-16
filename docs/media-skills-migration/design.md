# 下载与转写 Skill 集中维护

状态：已实施并通过 PR #16 合入主线，2026-10-16。迁移目标是统一源码维护，不改变媒体处理行为，不安装/修改智能体，不重新生成已完成的笔记。

## 来源与历史

| 新位置 | 原仓库 | 导入的 origin/main |
| --- | --- | --- |
| `skills/local-whisper/` | [local-whisper-skill](https://github.com/200166shang/local-whisper-skill) | `3effd19b46e7a939bfca613ec5b5fee18acfce0e` |
| `skills/yt-dlp-download/` | [yt-dlp-download](https://github.com/200166shang/yt-dlp-download) | `412622f52c6b676235581b2648eec8a7dd77d50e` |

使用未 squash 的 Git subtree 导入，原提交及作者保留在当前分支祖先中。下载仓库先整体导入，再通过 git mv 将 Skill、测试和说明放到集合仓库的规范位置；没有 Git submodule 或第二套嵌套仓库。PR #16 已使用 **merge commit** 合入，原仓库提交仍是主线祖先；后续同类历史导入也应保留祖先关系。可用 `git merge-base --is-ancestor <上表提交> HEAD` 检查。

下载器测试迁至 `skills/yt-dlp-download/tests/`，54P 元数据 fixture 一并保留；原验收报告现位于[下载器验收记录](../yt-dlp-download/validation.md)。Whisper 的 MIT LICENSE 原样放在其 Skill 目录内，不扩展到集合中其他代码。

这两个 Skill 以 personal-skills 为唯一维护位置。迁移没有修改或归档远端旧仓库，旧源目录也保留；旧仓库的迁移公告和归档是独立的后续操作，不属于已执行结果。

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

## 验收与决策

迁移的已执行检查见[验收记录](validation.md)，历史来源维护决策见 [ADR 0003](../adr/0003-one-media-skill-source.md)。这些记录不代表后续每个环境都已重新完成模型推理或线上下载。
