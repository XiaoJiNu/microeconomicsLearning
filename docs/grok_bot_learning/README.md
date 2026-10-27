# Grok Bot 学习记录

本目录是 Grok Bot 的书序辅导材料，对齐曼昆《经济学原理》第 8 版微观分册第 1–22 章。课文按章写在 `chapters/`。第 1 章正文以 [`chapters/ch01/`](chapters/ch01/README.md) 为准，第 2 章正文以 [`chapters/ch02/`](chapters/ch02/README.md) 为准，状态都为**文档齐备**（材料完整）。

以前的勾选页和对照表仍可当地图。它们不代替第 1 章和第 2 章的正文。本路径从头学，不把别处做过的进度当成免修。

## 建议入口

按这个顺序打开：

1. [全书概述](book_overview.md)（约 8–10 分钟的阅读，讲清目标、获得和用法）与 [全书思维导图](book_mindmap.md)
2. [第 1 章概述与思维导图](chapters/ch01/README.md)（先读章首，约 5–8 分钟）。配套 [勾选清单](chapters/ch01/CHECKLIST.md) 与 [术语表](chapters/ch01/GLOSSARY.md)
3. 第 1 章小课 [01](chapters/ch01/01_tradeoffs.md) 到 [07](chapters/ch01/07_macro_boundary_review.md)
4. [第 2 章概述与思维导图](chapters/ch02/README.md)。配套 [勾选清单](chapters/ch02/CHECKLIST.md) 与 [术语表](chapters/ch02/GLOSSARY.md)
5. 第 2 章小课 [01](chapters/ch02/01_scientist_models.md) 到 [06](chapters/ch02/06_disagreement_review.md)

## 每一章都要先有概述和导图

以后每个 `chapters/chNN/` 在小课之前必须带上两样东西：整章**概述**，以及一张能在 GitHub 上读的 **思维导图**（mermaid）。先看完整章怎样连在一起，再进入单课。第 3–22 章按同一模板补。当前第 1 章和第 2 章文档齐备，第 3 章起尚未写正文。

每一课再带这些，后面的章同样遵守：

- 至少一张手绘白板 sketchnote，放在该章 `assets/`，用相对路径嵌进课文。节奏是标题、图、一句说明，放在书中例子旁边。
- 对照表不要求每课一张。容易写混的几对放在章复盘。
- 每一课开头写「原书对应」：列出本课覆盖的原书目录标题。若只开入口或只标边界，写明正文展开在哪一章。
- 每一章 README 写「原书目录覆盖表」：原书这一章的目录标题都要有课、深度和状态。

图用来看机制，表用来核对口径。不要用干净的信息图代替手绘图。

## 分支怎么用

辅导材料和提交在 `grok-bot`。没有明确要求时，不把这个分支合并进 `main`。

`gpt6-pro` 上的课程若有更新，在本分支用 rebase 或 merge 从 `gpt6-pro` 同步。同步是为了让对照表跟着仓库走，不在本分支改 `course_gpt6_pro` 或 `course_20h` 的课文。

## 对照地图

这些文件保留，用来对目录和旧排法，不代替 `chapters/` 里的正文：

- [按书序学](book_order_path.md)
- [全书概述](book_overview.md)
- [第 1–22 章落到哪](chapter_map.md)
- [为什么旧课文对着目录会觉得缺一块](gap_analysis_vs_mankiw.md)
- [第 1 章旧清单](ch01_learning_plan.md)（历史对照）

`docs/course_gpt6_pro/` 仍是另一套按问题编排的 100 小课。某一章的 `chapters/chNN/` 还没写时，书序表里的课号只说明想法落在哪，不表示可以凭旧进度跳过。
