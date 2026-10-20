# 实现、验证与交付

## 工具使用

`figure_style.py` 的色板读取只使用标准库；绘图接口需要 Matplotlib / NumPy。脚本的资源路径相对自身解析，复制 skill 后仍然有效。

先运行：

```bash
python /path/to/nature-figure-style/scripts/figure_style.py list
python /path/to/nature-figure-style/scripts/figure_style.py palette ocean-uncertainty
```

在绘图脚本中动态导入（将 `skill_dir` 设为当前 skill 实际位置）：

```python
import importlib.util
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

skill_dir = Path('/path/to/nature-figure-style')
spec = importlib.util.spec_from_file_location('figure_style', skill_dir / 'scripts/figure_style.py')
style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style)

# 从数据真实组别建立固定映射，不能让面板之间各自重新循环色板。
colors = style.get_palette('composition-six')
group_colors = {'control': colors[2], 'treatment': colors[0]}
with style.rc_context():
    fig, ax = plt.subplots(figsize=(90 / 25.4, 65 / 25.4), layout='constrained')
    # 在此读取并绘制用户真实数据；示例不预设统计检验或样本量。
    style.style_axes(ax)
    style.save_figure(fig, '/absolute/output/figure')
    plt.close(fig)

# 仅当真实数据存在实质中点时使用。例如 centered_values 已有可靠定义：
# cmap = style.make_cmap('rose-blue-diverging')
# norm = TwoSlopeNorm(vmin=-2, vcenter=0, vmax=2)
```

`rc_context` 只在上下文内调整字体和线宽，不永久修改全局配置；`style_axes(full_box=True)` 保留四边框。`get_palette(name, n)` 对超出色数的请求报错，不静默循环。色板的默认顺序是提取/整理顺序，不代表适合任何数据的类别或强度排序。

`make_cmap` 只是锚点插值，不证明亮度单调或感知均匀。对非负强度选顺序映射；对有中点的偏离用明确归一化；不要把 `development-vivid` 插值后当通用热图。

`save_figure` 同时保存 SVG、PDF、PNG，默认 PNG 600 dpi，不使用 `bbox_inches='tight'`，从而保留设置的画布尺寸。先用布局管理器或调整边距把标签放进画布。若用户指定透明底或不同位图分辨率，按需求修改导出设置。

SVG 保留文本以便编辑，查看环境需有对应字体；PDF 使用嵌入字体模式。密集点层可单独 `rasterized=True`，线与文字保留矢量。位图升高 dpi 无法修复错误图例或过小字号。

## R / ggplot2

同样从 JSON 取色，沿用原项目工具，不为使用本 skill 强制改写语言：

```r
library(jsonlite)
lib <- fromJSON('/path/to/nature-figure-style/references/corpus.json', simplifyVector=FALSE)
entry <- Filter(function(p) p$id == 'composition-six', lib$palettes)[[1]]
cols <- vapply(entry$colors, function(c) c$hex, character(1))
# 显式命名，ggplot 子面板丢失类别时仍保持颜色身份。
group_colors <- c(control=cols[3], treatment=cols[1])
# p + scale_color_manual(values=group_colors) +
#   theme_classic(base_size=8) + theme(legend.title=element_blank())
```

这是颜色读取示例；统计方法、字体依赖和输出设备按用户项目选择。本包演示已验证 Python 路径，未在当前环境运行 R。

## 渲染检查

交付前打开实际导出的 PNG 或将矢量文件渲染成图查看。先检查整版阅读顺序，再按最终尺寸看细节；超大屏预览不等于印刷可读。

- 字母编号、小标题、轴标题、刻度和色条标签无裁切、遮挡、碰撞；数字与单位、负号、上下标可读。
- 同一实体跨面板同色；图例顺序对应堆叠顺序；缺失组别没有导致颜色位移。
- 不确定性带的含义、数据线与拟合线身份、n、归一化/变换和色条范围均可追溯到输入。不要从参考图猜统计值。
- 白底浅色点可辨；红绿或相近淡紫类别有冗余编码；有色觉预览工具时实际检查，不能仅凭色板名称断言无障碍。
- 热图各面板若共享色条应共享归一化；局部放大与总览坐标一致；多轴单位清楚。
- 机制图逐条核对有向边与抑制关系；分区、轮廓引导线和作用箭头不混用；标签不能藏在位图素材中无法编辑。
- 最终画布尺寸符合用户要求。下游若会裁切/拼版，重新检查最终字体尺寸。

修复已发现问题后再输出。缺少渲染能力时明确说明尚未视觉验证，不能把“文件已保存”当作“布局已通过”。

## 交付内容

通常交付绘图代码、可编辑 SVG/PDF、PNG 预览；按用户指定格式调整。数据不适合公开时不要打包上传。简短说明所选参考 ID、色板及颜色语义、布局、统计定义与必要限制。无需输出整份分析过程。

可选 `figure-design.json` 建议字段：`reference_ids`、`palette_id`、`color_mapping`、`canvas_mm`、`data_source`、`uncertainty_definition`、`transforms`、`outputs`。不是通用强制模板；用于多图项目保持一致。
