# yt-dlp Download

面向 AI Agent 的网页音视频下载 Skill，基于官方 [yt-dlp](https://github.com/yt-dlp/yt-dlp)。

支持下载你有权访问的 YouTube、哔哩哔哩及其他兼容站点的视频、音频和指定语言字幕。视频默认选择最低分辨率，结果保存到临时目录。

## 安装

```bash
npx -y skills add 200166shang/yt-dlp-download --skill yt-dlp-download -g -a codex -y
```

安装完成后，新开一个 Codex 会话。

## 使用

直接告诉 Agent：

```text
下载这个 YouTube 视频：URL
```

```text
下载这个视频的英文音频：URL
```

```text
下载这个视频的简体中文字幕：URL
```

```text
下载这个哔哩哔哩视频：URL
```

## 能力

- 下载最低分辨率视频
- 提取音频
- 下载人工字幕或自动字幕
- 按语言选择音轨和字幕
- 支持 YouTube、哔哩哔哩及其他 yt-dlp 兼容站点
- 支持复用浏览器登录状态
- 断点续传与失败重试
- 返回适合 Agent 处理的结构化结果

## 系统要求

系统需要安装：

- [Node.js](https://nodejs.org/)
- [uv](https://docs.astral.sh/uv/)
- [FFmpeg](https://ffmpeg.org/)

yt-dlp 和 Python 依赖会在首次使用时自动安装到 Skill 自己的隔离环境中。

## 更新

```bash
npx -y skills update yt-dlp-download
```

## 使用边界

仅用于下载你已经拥有或明确获权访问的内容。

本项目不会绕过登录、付费、DRM 或账号权限限制。


## 目录与范围下载

封装新增 `catalog URL`、`download URL --playlist` 和 `--playlist-items 5:9`。
无列表参数仍只处理单视频；范围使用列表位置而非章节标签。每项独立结果保留成功、
失败和未尝试状态，部分失败退出非零。数据根目录仍通过子命令前的 `--data-dir PATH`
指定。详见 Skill 的 CLI contract。仅改封装 Skill/脚本，未修改上游 yt-dlp。
