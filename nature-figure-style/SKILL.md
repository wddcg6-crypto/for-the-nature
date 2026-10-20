---
name: nature-figure-style
description: >-
  Create or restyle scientific figures using an analyzed collection of 20 reference images: publication-style statistical panels, uncertainty curves, heatmaps, UMAP and composition plots, and biological mechanism diagrams. Use when the user requests 科研绘图、论文配图、Nature 风格、参考 for the nature 图片风格, or invokes this skill. Applies the collection's specific palettes, layout patterns and visual hierarchy while preserving data meaning.
---

# 科研绘图参考库：for the nature

将参考图的视觉经验转化为适合当前数据的图，而不是复制参考图中的科学结论。该库来自 20 张本地参考截图的逐张审阅，包含 24 套色板、150 个色位；不是 Nature 官方规范，也不是模型微调。

## 使用流程

1. 从用户材料中确认图的任务、数据含义、分组、单位、误差定义及交付尺寸。能合理推断的排版细节自行决定；缺失真实数据时可以先搭版，但不能伪造实验结果、显著性、UMAP 或生物通路。演示数据必须明确标注。
2. 阅读 [设计规则](references/design-rules.md)，按下表选择 1–3 张相近参考；再阅读 [逐图分析](references/image-catalog.md) 中对应条目。用户已有指定配色、期刊规范或图形语法时优先保留。
3. 从 [色板与证据](references/palettes.md) 选择色板 ID。精确值、来源、采样坐标和标注异常见 [corpus.json](references/corpus.json)。把颜色映射到明确的类别/数值/空间分区，保证跨面板一致；不能把全部色板颜色自动当成同一组分类色。
4. 在实现前明确一个简短设计方案：参考图 ID、色板及其语义、面板结构、输出尺寸。对于普通请求直接继续绘图，无需等用户确认。
5. 使用当前环境适合的 Python/R/矢量工具绘制。优先代码生成数据图和可编辑标签；机制图使用矢量形状、合法可用的素材或用户要求的绘图工具，保留对象与箭头的科学含义。不要把图片生成模型画出的曲线当成真实数据图。
6. 导出后按 [验证与交付](references/rendering.md) 渲染并检查，修复裁切、遮挡和小字号。交付可编辑源文件、适合用途的矢量文件/位图与简短设计说明。

## 根据任务选择参考

| 当前任务 | 优先查看 | 色板起点 |
|---|---|---|
| 两组实验、散点/小提琴、柱状图 | IMG_3030、3032 | protein-pink-teal、lavender-coral |
| 多地区/条件趋势与不确定性 | IMG_3031 | ocean-uncertainty |
| 模型与数据、残差、时频热图 | IMG_3036、3037 | assay-gold-teal-red、flux-teal-sand |
| 基因组信号与局部放大 | IMG_3039 | genome-tracks |
| UMAP/细胞分类、发育图谱 | IMG_3040、3042、3043 | cell-atlas-nine、development-families |
| 年龄/时间构成比、环形概览 | IMG_3041、3049 | age-composition、composition-six |
| 细胞结构、RNA 加工 | IMG_3034、3035 | organelle-lavender、rna-blue-lilac |
| 免疫交互、总体到局部机制 | IMG_3033、3038、3046 | immune-blue-rose、tme-pastel、functional-mint-salmon |
| 植物/生态演化示意 | IMG_3044 | botanical-pastel |
| 材料合成、递送、组织作用 | IMG_3045、3047、3048 | tissue-lilac-peach、nano-blue-lilac、hydrogel-mint-rose |

## 必须保留的经验边界

- 原图中的社交媒体水印、底部配色卡、截图大白边和示例宣传外框不属于论文图版式，不带入成图。
- 浅色背景/置信带与深色数据线承担不同功能；同色家族不等于可相互区分的类别。必要时加线型、点型、标签或拆面板。
- 发散色只用于存在实质中点的数据。IMG_3030 的部分粉蓝色条对应正值范围，不能因外观是双色就假定零中心。
- 精确字号、线宽和列宽无法从截图推回；参考文档中的毫米/pt 数值都是可调整的实现起点，不能称为原论文测量值或期刊要求。
- 图名中的 “Nature” 仅指用户收藏的风格集合。截图中印出的论文信息未经本库外部核验；不要据此声称全部图片出自 Nature。

## 可复用工具

工具路径相对于本 skill 目录；不要依赖创建时的绝对路径。

```bash
python scripts/figure_style.py list
python scripts/figure_style.py palette composition-six
python scripts/figure_style.py preview --output /absolute/output/palette-atlas
python scripts/figure_style.py demo --output /absolute/output/style-demo
```

`list` / `palette` 仅需 Python 标准库；预览和绘图需要 Matplotlib、NumPy。可导入 `figure_style.py` 的 `get_palette`、`rc_context`、`style_axes`、`make_cmap`、`save_figure`，见 [实现说明](references/rendering.md)。脚本提供绘图样式，不替用户决定统计方法。

如果本地 `.private-reference/IMG_*.WEBP` 存在，可打开相应原图进一步比对；这些图片不进入公开包。没有原图时使用逐图分析和色板证据即可，不要求桌面路径或私有工具。
