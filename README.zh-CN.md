# Personal Skills

[English](./README.md) | **简体中文**

一个用于集中维护个人小型、可复用 AI Agent Skill 的仓库。

这个仓库主要用来存放那些值得长期保留和重复使用、但又没有复杂到需要单独建立项目的 Skill。整体目标是让每个 Skill 都保持轻量、清晰、可组合，并且方便直接阅读和理解。

## 仓库定位

这里适合存放职责明确、可以在不同任务或项目中重复使用的小型 Skill。

如果某个项目已经有独立的架构设计、版本演进、发布流程或长期路线图，则更适合继续作为独立仓库维护，而不是放进这里。

## 基本原则

- **小而专注**：一个 Skill 尽量解决一个明确的问题。
- **可复用**：优先沉淀能够跨任务、跨项目重复使用的能力。
- **可组合**：多个简单 Skill 可以协作完成复杂任务，而不是不断膨胀成一个大型 Workflow。
- **可阅读**：Skill 的行为应该容易检查、理解和修改。
- **轻量化**：在真实需求出现之前，不提前引入复杂的基础设施。

## Skills

本仓库是个人 Learning skills 的唯一维护来源：

- `learning`：根据意图选择学习工作流。
- `learning-plan`：用一个简短 Markdown 状态页记录长期方向、当前主线、学习书签、下一步和暂缓主题。
- `learning-learn`：讲解问题并保存持久化学习记录。
- `learning-review`：从已学资料中筛选少量代表性面试问题和口述答案，确认后逐题练习。
- `learning-practice`：用小型练习应用已学内容。
- `learning-resources`：整理外部学习资料。
- `learning-organize`：把已探索的问题组织成主题文章。
- `learning-transcript`：将 ASR 文件整理为忠实讲稿。

在本仓库维护完整 skill 目录，包括可选的 `agents/` 元数据和 `references/`。不在其他项目或本机安装目录维护另一份副本。

## 安装

在本地仓库运行：

```bash
node bin/install.mjs
```

如需用仓库版本替换已安装的同名 skill，并清除源目录中已不存在的旧文件：

```bash
node bin/install.mjs --force
```

这些改动合并到 `main` 后，也可以从 GitHub 直接安装：

```bash
npx --yes github:200166shang/personal-skills
```

## License

License 信息后续补充。
