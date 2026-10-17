# 视频课程记录、Obsidian 与网站发布的实践调研

日期：2026-10-17。状态：一手项目文档调研，不是实施规范或迁移验收。未安装插件、运行发布、核验端到端同步或修改用户 Vault。项目说明证明存在这些工作流，不证明用户采用比例。浏览到的文档会变化；实施前应锁定版本并验证。

## 观察到的做法

1. **视频记录直接写入 Vault。** YTranscript 支持将 YouTube 转录插入正文，或在侧栏查看带可点击时间点的转录。YouTube Transcript Fetcher 支持 Markdown/PDF/SRT、视频元数据、可选清理与摘要、默认目录，以及扫描视频身份属性避免重复创建。插件的功能声明不构成字幕准确性或当前平台抓取成功率保证。[YTranscript](https://github.com/lstrzepek/obsidian-yt-transcript)、[Transcript Fetcher](https://github.com/ljantzen/obsidian-youtube-transcript)。
2. **本地资料是实体文件。** Obsidian Web Clipper 将网页内容保存到本地 Vault；附件可以直接下载到 Vault，拖入编辑器时复制到附件目录。没有必要先生成网站再从网页搬回 Obsidian。[Web Clipper](https://obsidian.md/help/web-clipper)、[Attachments](https://obsidian.md/help/attachments)。
3. **Vault 内容生成网站。** Quartz 的内容位于 content 目录，可用 Obsidian 编辑。构建生成网页，可以部署到托管平台或自有服务器。因此本地 Markdown 和网站正文不需要分别维护。[Authoring](https://quartz.jzhao.xyz/getting-started/authoring-content)、[Hosting](https://quartz.jzhao.xyz/hosting)。
4. **从 Vault 选择发布。** Digital Garden 使用 dg-publish 标记发布笔记，GitHub 与托管平台承接网站；也有桌面端导出笔记和图片到本地目录的命令。本地导出当前为全量，不提供发布 diff 跟踪。筛选发布不等于网页访问控制。[Getting started](https://docs.forestry.md/getting-started/01-getting-started/)、[Commands](https://docs.forestry.md/getting-started/02-commands/)。
5. **官方托管与密码访问。** Obsidian Publish 从 Vault 选择新增/更新笔记，辅助选择引用媒体；取消发布保留本地文件。支持站点级密码，当前不支持逐篇不同密码。[Publishing](https://obsidian.md/help/publish/publish)、[Security](https://obsidian.md/help/publish/security)。官方说明不建议用 Publish 承载大量大视频/音频。[Media](https://obsidian.md/help/publish/media)。

## 易混淆的边界

- Quartz 的 Private Pages 是构建筛选，不是登录保护；官方还提醒非 Markdown 附件会输出，需要 ignorePatterns 额外排除。[Private Pages](https://quartz.jzhao.xyz/features/private-pages)。
- 私有 GitHub 仓库不使 Pages 自动私有。私有 Pages 的组织发布需要 Enterprise Cloud。[GitHub visibility](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)。
- 单篇视频转录插件不等于完整课程批量系统；以上资料没有证明它们满足 B 站、小鹅通、多课排序、全源忠实审核、最终截图审核及缓存生命周期。现有项目的总结功能也不能替代本仓库 faithful 模式。
- 本次没有获得足以比较各方案市场份额、私有课程库普及率或统一缓存保留期限的证据。没有把论坛个案当成普遍规则。

## 针对本项目的推论，尚未实施

将课程记录定位为稳定来源档案：生成/审核后将 Markdown 与实际图片写入 Vault，保留来源身份、课次、时间戳、原始转写和当前审核证据；HTML 是可重建阅读产物。视频、预览、模型和任务状态留在 Vault 外。以稳定来源 ID 检测重复；已存在课时先比较版本再替换。私人学习心得另行链接。

若只为阅读和同步，可先只使用 Obsidian；需要网页再选 Publish（省维护、站点密码）或 Quartz（自控部署、单独配置访问控制）。GitHub 是可选源码与版本层，不是必须先建设的环节。缓存保留期限、目录和导入协议需要针对本地工作流另行设计，不能归因于这些项目的共同约定。
