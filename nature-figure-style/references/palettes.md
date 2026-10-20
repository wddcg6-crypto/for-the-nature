# 色板与取色证据

## 读取方式

`corpus.json` 是精确值的唯一数据源。以下色序为提取/整理顺序，不等于自动适用的类别顺序或连续数值顺序。24 套色板共 150 个色位，包含跨色板重复值和一个新增白色锚点，并非 150 个独立原始颜色。

- 无标记：采用图中可读 HEX；采样值另存于 JSON，不把轻微压缩差异误判为设计差异。
- `*`：文字不清或明显不符，采用色块中心 13×13 像素的逐通道中位数。
- `†`：为新图适配新增的锚点，不是从图中抄录的色号。
- 取样坐标以原图左上角为原点，单位为像素。截图未含可依赖的原始设计色彩配置，不宣称数值可还原原论文。

## 24 套色板

### protein-pink-teal

来源：`IMG_3030.WEBP` · 用途类型：`categorical`。

配对类别；优先选一个粉色与一个青色，浅变体作同类层级。

`#DEAEC3` → `#ECAFC6` → `#FBC8DB` → `#56A1B8` → `#6FBFD7` → `#A3DCEC`


### protein-soft-pair

来源：`IMG_3030.WEBP` · 用途类型：`categorical`。

两家族的淡色填充；避免把全部浅粉/浅蓝当可区分曲线。

`#EBB3CF` → `#F8CBE0` → `#E3D5ED` → `#8AB2D1` → `#B1D7F2` → `#BFC9E4`


### rose-blue-diverging

来源：`IMG_3030.WEBP` · 用途类型：`diverging`。

蓝→白→玫瑰，白色是适配新增中点；只用于有实质中点的数据。

`#5293C9` → `#97CEFF` → `#B2D0E8` → `#FFFFFF`† → `#ECADC4` → `#E797B4` → `#DF81A5`

- #FFFFFF：新增白色中点，用于有实质中点的发散尺度。

### expression-blue-pink

来源：`IMG_3030.WEBP` · 用途类型：`sequential-candidate`。

从蓝至粉的候选锚点；原图范围为正值，按新数据选择归一化，不自动取零中心。

`#71B0FD` → `#9ECAFE` → `#C4DFFC` → `#FFEEF8` → `#FECEE6` → `#FDC0E1`


### ocean-uncertainty

来源：`IMG_3031.WEBP` · 用途类型：`mixed`。

前五色可作浅色面积，末两色作数据线；绑定明确系列并加线型。

`#D5E8F1` → `#ABD7DF` → `#CAEBE7` → `#A9D9BB` → `#90B4CF` → `#337BAC` → `#4FB1B2`


### lavender-coral

来源：`IMG_3032.WEBP` · 用途类型：`categorical`。

淡紫与暖珊瑚形成视觉家族；少量分类优先挑相隔较远的颜色。

`#B6B3D6` → `#CFCCE3` → `#D5D3DE` → `#D5D1D1` → `#F6DFD6` → `#F8B2A2` → `#F1837A` → `#E9687A`


### immune-blue-rose

来源：`IMG_3033.WEBP` · 用途类型：`schematic`。

浅蓝空间、中蓝轮廓/结构、近白背景、玫瑰与奶黄实体。

`#BBD1E7` → `#6D8BC3` → `#FDF5F1` → `#E9B6BE` → `#F3E19C`


### organelle-lavender

来源：`IMG_3034.WEBP` · 用途类型：`schematic`。

浅紫底、两级紫色细胞器、粉色辅助；用形状和标签区分类别。

`#F0ECF7` → `#CAADD8` → `#AF8FD0` → `#EFC0D2` → `#F6ECF6`


### rna-blue-lilac

来源：`IMG_3035.WEBP` · 用途类型：`schematic`。

浅蓝胞质、中蓝结构、极淡紫外区、紫/绿节点；深色箭头另设。

`#E2F0FF` → `#85A2D2` → `#F9F2FE` → `#C2ACDA` → `#C0DB82`


### assay-gold-teal-red

来源：`IMG_3036.WEBP` · 用途类型：`categorical`。

金/青/暗红区分三种方法；同方法的信号与残差同色。

`#F09B00` → `#016171` → `#AE2012`


### flux-teal-sand

来源：`IMG_3036.WEBP` · 用途类型：`sequential`。

青→绿→沙的连续尺度候选；检查亮度、数据归一化与色条范围。

`#096176` → `#AFD2B7` → `#E6D9A5`


### spectral-teal-ochre

来源：`IMG_3037.WEBP` · 用途类型：`ordered-candidate`。

多波段层叠曲线候选；截图提取顺序不是数值排序，必要时重排。

`#005F73` → `#0A9396` → `#CA6702` → `#EE9B00` → `#9C2327` → `#BE450D`


### tme-pastel

来源：`IMG_3038.WEBP` · 用途类型：`schematic`。

浅粉底，粉/紫/绿/黄实体；颜色身份在总体与局部机制中一致。

`#FCF1F0` → `#FCCCCB` → `#BDB5E1` → `#B0D992` → `#F9D580`


### genome-tracks

来源：`IMG_3039.WEBP` · 用途类型：`categorical`。

四组基因组轨道分类色；保留轨道名称，红绿需辅以标签。

`#B15D2F` → `#E72035` → `#237BBA` → `#43AA59`


### cell-atlas-nine

来源：`IMG_3040.WEBP` · 用途类型：`categorical`。

九类细胞离散映射；浅黄绿小点需要对比检查，不作为连续色谱。

`#9E0142` → `#D53E4F` → `#FDAE61` → `#5E4FA2` → `#ABDDA4` → `#E6F598` → `#3288BD` → `#FEE08B` → `#66C2A5`


### age-composition

来源：`IMG_3041.WEBP` · 用途类型：`categorical`。

前五色为时期类别，黑色为样本量/风险等辅助层，不作第六时期。

`#639DD0` → `#E1959A` → `#FFC79A` → `#7CC1F3` → `#E1EDDC` → `#000000`


### development-vivid

来源：`IMG_3042.WEBP` · 用途类型：`categorical`。

密集多类别候选；有强饱和色，绿色色号/色块不一致须注意。

`#850662` → `#FFBDE5` → `#785FF6` → `#2100FA` → `#9EFFFF` → `#00AFB2` → `#22B24B` → `#B56D2D` → `#FF6B24`

- #22B24B：标注与截图色块的最大 RGB 通道差为 42；两者分别保留，不宣称为论文原始色。

### development-families

来源：`IMG_3043.WEBP` · 用途类型：`categorical`。

紫粉与青蓝的家族层级；不适合所有相近色同时作为重叠细线。

`#D37DB5` → `#AD60A5` → `#7E2E92` → `#E775AD` → `#00B0B2` → `#83D4E4` → `#4D91CC` → `#A0C3E7` → `#6B65AF`


### botanical-pastel

来源：`IMG_3044.WEBP` · 用途类型：`schematic`。

环境底色、植物实体和性状强调；中性色给背景，粉紫给少量主体。

`#C8BBDA` → `#FBF8E5` → `#BCB1AB` → `#D4BAF7` → `#FAD89F` → `#FE96A1` → `#BD6C71`* → `#E5F8E6`* → `#F5F4E9`* → `#FFF6E5`

- #BD6C71：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。
- #E5F8E6：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。
- #F5F4E9：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。

### tissue-lilac-peach

来源：`IMG_3045.WEBP` · 用途类型：`schematic`。

组织/细胞的紫与桃色分区；黄色细胞器，动作箭头另设深青色。

`#C4AFD1` → `#F0E9F4` → `#F0D4CA` → `#E3A798` → `#EEE6C6`


### functional-mint-salmon

来源：`IMG_3046.WEBP` · 用途类型：`schematic`。

绿/鲑红对应相反功能，灰为中性，淡色作分栏底；辅以文字或形状。

`#7AB393` → `#FBA799` → `#E9EAF2` → `#7FB558` → `#FDF1A3` → `#C3E4E2` → `#FEEAEA`* → `#EDDBE8`* → `#C6C7C2`* → `#CDEBDE`

- #FEEAEA：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。
- #EDDBE8：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。
- #C6C7C2：色号文字被水印遮挡，未补猜；采用指定色块中心 13×13 像素的逐通道中位数。

### nano-blue-lilac

来源：`IMG_3047.WEBP` · 用途类型：`schematic`。

蓝/青背景与细胞，中紫材料、玫瑰作用、浅黄辅助；深蓝箭头另设。

`#DCE8F1` → `#F4E4BE` → `#A9ABD2` → `#D4EEED` → `#E3BDCE`


### hydrogel-mint-rose

来源：`IMG_3048.WEBP` · 用途类型：`schematic`。

采样薄荷底、淡粉组织、桃色材料、玫瑰强调、黄箭头；第一色已纠错。

`#E0F0E6`* → `#EED2D0` → `#F4D9BA` → `#E993A9` → `#F2E193`

- #E0F0E6：标注 #EEE6C6 与薄荷绿色块明显不符；绘图采用色块中位采样值。 标注与截图色块的最大 RGB 通道差为 32；两者分别保留，不宣称为论文原始色。

### composition-six

来源：`IMG_3049.WEBP` · 用途类型：`categorical`。

前五色候选类别，灰可映射 Others；按真实分组建立显式映射。

`#E64B34` → `#4DBBD6` → `#3C5487` → `#F29B80` → `#8591B4` → `#808080`


## 选择与转换

对分类数据先选差异足够大的少数颜色。对实体背景、边缘、区间带分别选色，不把色板从第一位机械循环。对连续数据确认归一化和亮度变化，必要时使用用户指定或已有项目的连续色图，只借用本库布局。

`kind` 中的 `candidate` 表示可作为重建的候选锚点，不是已证明感知均匀的色图。库内未认证任何色板为色盲安全；应对实际图形进行预览和冗余编码。
