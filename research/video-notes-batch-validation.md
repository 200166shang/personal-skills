# 多课图文笔记验收 — 2026-10-16

范围：当前智能体调用原子能力；新 batch 只管理已准备本地课时的隔离制作，不接管下载/ASR，不新增或修改 Agent，不改变 learning-transcript。

## 实际课程结果

使用本地已经下载的 `BV11X4y1j7si` P5–P9 视频及对应 SRT。五课均按 faithful 模式处理完整视频，源文件 SHA 与课时身份冻结。每课使用新的写作者和独立审稿者，十次创建均显式 `fork_turns="none"`，没有指定固定模型。

| 章节 | P | 实际媒体秒数 | 全文窗口 | 最终图片 | 内容/图片独立审稿 |
| --- | --- | ---: | ---: | ---: | --- |
| 2.1 | P5 | 1972.309 | 17 | 18 | PASS |
| 2.2 | P6 | 624.618 | 6 | 9 | PASS |
| 2.3 | P7 | 2553.514 | 22 | 19 | PASS |
| 2.4 | P8 | 936.682 | 8 | 10 | PASS |
| 2.5 | P9 | 1232.277 | 11 | 16 | PASS |

最终状态 **5/5 published**，共 **64 个窗口、72 张图**。发布结果是逐课 Markdown、离线 HTML、图片、源转写与校验记录，另有课程 `index.md`、`index.html`、`batch-report.json`。索引仅链接，不再次总结讲稿。

本机输出：`~/Media/Library/bilibili/STM32入门教程/GPIO-2.1-2.5-忠实图文讲稿/`。任务/尝试/审稿日志：`~/Library/Application Support/video-notes-batch/jobs/stm32-gpio-2.1-2.5-v1/`，其中 `acceptance.json` 保存检查摘要。媒体和产物均不入库。

## 隔离与恢复证据

- 实际 writer/reviewer ID 逐课独立（`/root/gpio_p5_writer`、`/root/gpio_p5_review`，依此至 p9），任务只传本课文件指针；协调者仅读取状态、路径与审稿摘要，没有载入五课正文/转写。宿主创建记录可在本次会话核对。
- 批次事件重放的活跃峰值为 2，审稿包含在额度内；结束后没有活跃 claim。
- 真实批次中先发布 P5/P6，再继续其余课时，前两课全部文件哈希前后相同。
- 运行中 resume 保留两个活跃任务；最终 resume 返回 published=5、所有检查通过，`batch.json` 字节未改变。
- 独立工具试用在临时目录重现中断、另一课继续、过期结果拒绝、checkpoint 接续和快照损坏拒绝。发现的重复审稿上下文、空 FIX、保留文件名冲突已修复并回归验证。

## 自动与安装验证

- batch：13 项 unittest，通过。包括实际 FFmpeg 单课包、独立审稿绑定、稿变后 PASS 失效、并发抢占、断点、缓存删除后已发布结果仍可校验、精确章节和自然排序、输出保留名、大小写身份冲突。
- 原 video-notes：8 项；video-frames：4 项；既有 agent 安装器：3 项，均通过。安装器源代码和 Agent 模板未修改。
- 独立下载封装：12 项 pytest，通过，其中本地 HTTP HTML5 播放列表经原生 yt-dlp 实际下载，仅选第 2 项并用 FFprobe 验证音视频流。54P 第一方目录 fixture 证明 P5–P9 标题/cid/范围对应；不代表当前线上下载成功。
- Skill frontmatter 检查和临时 CODEX_HOME 安装通过：脚本与引用完整，没有创建 agents 配置，learning-transcript 保留。npm 包预览包含新 Skill。
- 已定向安装 video-notes-batch 与下载封装；旧下载封装纯 Skill 文件备份到 `~/.codex/skill-backups/`，未整体 force 替换其他技能。

## 验证范围与限制

独立审稿 PASS 指完整来源、身份与最终图片核对；HTML/图片/CSS 的结构校验另行通过。六个 HTML 页的本地资源链接和锚点已静态检查。此前浏览器 file:// 访问被拒，本轮未绕过，也未执行桌面/窄屏布局、缩放交互的浏览器验证；这一项仍未测，不能把内容审稿 PASS 当成浏览器交互通过。P8 首份报告将该限制记为 UNCERTAIN，原报告保留为 result.initial.json；澄清既定审稿范围后，复核者单独记录内容/图片 PASS 和交互未测。

当前 B 站公开目录与原生媒体页面请求返回 HTTP 412，已停止重复请求。真实笔记复用已有本地视频；下载封装的新线上 Bilibili/YouTube 下载未验证成功。独立改动见 https://github.com/200166shang/yt-dlp-download/pull/1 。

Claude Code 提供宿主适配说明，未在该宿主实际运行。文件锁/token 是协作机制，不是 OS 沙箱；派发记录、字数比例和审稿判断不构成绝对语义或画面覆盖证明。
