# 批量图文笔记验收课程目录核实

状态：目录证据快照，不代表当前在线可用性；五课实际结果见[验收记录](../docs/video-notes-batch/validation.md)。

核实日期：2026-10-16（Asia/Shanghai）。本报告仅核实公开目录元信息，没有下载视频、音频或运行 ASR。

## 一手证据与课程范围

对 [B 站公开视频元信息接口](https://api.bilibili.com/x/web-interface/view?bvid=BV11X4y1j7si) 的一次正常、无登录请求，返回 HTTP 200、`code=0`、`message=OK`。响应中的课程标题为 **铁头山羊stm32 入门教程【新版】**，`bvid=BV11X4y1j7si`、`aid=359140104`、`videos=54`，`data.pages` 实际包含 **54** 项。

用户给出的 `?p=2` 定位到 **1.1 [准备]安装开发环境**，并不意味着验收范围 2.1—2.5 对应 P2—P5。对 `data.pages[].part` 的完整标题匹配确认：**验收范围对应 P5—P9，共五节**。各节的 `page`、`part`、`duration`、`cid` 均直接取自上述接口。

| 章节 | 分 P | 完整分集标题（原样） | 时长 | duration 秒 | cid | 预期下载器 media_id | Canonical URL |
|---|---:|---|---|---:|---:|---|---|
| 2.1 | 5 | 2.1 [GPIO]4种输出模式 | 32:53 | 1973 | 26335970481 | `BV11X4y1j7si_p5` | [P5](https://www.bilibili.com/video/BV11X4y1j7si/?p=5) |
| 2.2 | 6 | 2.2 [GPIO]IO的最大输出速度 | 10:25 | 625 | 26054951429 | `BV11X4y1j7si_p6` | [P6](https://www.bilibili.com/video/BV11X4y1j7si/?p=6) |
| 2.3 | 7 | 2.3 [GPIO]LED闪灯实验 | 42:34 | 2554 | 26351173764 | `BV11X4y1j7si_p7` | [P7](https://www.bilibili.com/video/BV11X4y1j7si/?p=7) |
| 2.4 | 8 | 2.4 [GPIO]4种输入模式 | 15:37 | 937 | 26360349837 | `BV11X4y1j7si_p8` | [P8](https://www.bilibili.com/video/BV11X4y1j7si/?p=8) |
| 2.5 | 9 | 2.5 [GPIO]按钮实验 | 20:33 | 1233 | 26054951605 | `BV11X4y1j7si_p9` | [P9](https://www.bilibili.com/video/BV11X4y1j7si/?p=9) |

五节元信息时长合计 **7322 秒，即 2 小时 2 分 2 秒**。这只是输入规模，不是运行耗时预测。来源：[公开目录响应](https://api.bilibili.com/x/web-interface/view?bvid=BV11X4y1j7si)。

## ID 约定的本地代码依据

现有已安装下载器 `runtime/src/yt_dlp_download/cli.py` 的 `_inventory()` 直接返回 yt-dlp 的 `info.id`；`_download()` 同样以该 ID 构建 `<data-dir>/<platform>/<media-id>`。已安装 yt-dlp 的 B 站 extractor 在 `metainfo` 中构建：

```python
'id': f'{video_id}{format_field(part_id, None, "_p%d")}'
```

因此，上表 `_p5`—`_p9` 与现有下载器分集 ID 约定一致，但它们是**依据公开目录与已安装 extractor 代码推导的预期 ID**，尚未通过各节成功的 `inspect` 响应逐项实测。当时检查的下载器现已归入[仓库内 CLI](../skills/yt-dlp-download/runtime/src/yt_dlp_download/cli.py)；上游片段来自核实时安装的 yt-dlp B 站 extractor，本报告不依赖该机器的虚拟环境路径。

## 核实时点的可用性与未确认项

- 同轮父任务对现有 `yt-dlp-download inspect` 的 P2 页面检查遇到 HTTP 412。因此，**公开目录可获取不等于现有单视频下载链路当前可用**。没有针对该风控反复重试、使用代理或伪造登录绕过。
- 此处的一次公开元信息接口请求独立成功，足以确认本次五节的标题、分 P、时长和 cid；无需从页面 412 推断目录不存在或内容不可访问。
- 各节可下载性、现有字幕轨道、实际下载画质、媒体实际时长及与转写的时间对齐均未验证，应在后续执行阶段按已有下载与转写 Skill 检查。元信息中的源尺寸也不能替代实际下载画质。
- BV 的目录未来可以变更。后续执行应重新发现目录，核对以上标题与 `cid`，固定本次清单；不要只按位置号盲目处理。

## 本轮原始响应

原始公共响应暂存于 `/tmp/video-notes-batch-bili-view.json`，HTTP 响应头暂存于 `/tmp/video-notes-batch-bili-headers.txt`，仅供本轮核查；`/tmp` 文件不是长期归档来源。长期事实依据是上面引用的一手接口及表格快照。此报告不含 Cookie、授权令牌或媒体下载地址。

长期保存的精简目录 fixture 见[下载器测试数据](../skills/yt-dlp-download/tests/fixtures/bilibili-pages.json)。原临时响应和本机代码检查仅描述核实时点，不是读取本报告的前置条件。
