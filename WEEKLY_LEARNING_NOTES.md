
 
# Computational Research Foundations — Weekly Learning Notes

> 用途：把每周真正学会的概念、代码逻辑、研究判断和 debugging case 留下来。重点不是“记命令”，而是能够用自己的话解释：**为什么这样做、什么时候这样做、哪里容易错、结果能说明什么、不能说明什么。**

## 如何使用这份文档

- 每周结束时新增一个 `Week N` section，不覆盖旧内容。
- 每个概念至少写四件事：**大白话、为什么重要、一个例子、一个常见误区**。
- 新的 debugging case 只记录真实发生过的问题。
- 每周最后回答一次“我现在能独立做什么？”和“下一周还欠什么？”。
- 建议把 Markdown 版本放在 `computational-foundations/` 仓库根目录，用 Git 记录每周变化。

---

## 当前总进度快照

目前已经完成两周左右的基础训练。Week 1 主要解决“能不能独立把一个小分析从数据跑到结果并复现”；Week 2 主要解决“面对多个相关变量时，怎么区分相关、解释、预测和验证”。

**现在已经建立的主线：**

`raw data → inspect → validate → clean → analyze → diagnose → validate → interpret → document → version control`

---

# Week 1 — Scientific Python, Data Handling, Regression & Reproducibility

## 1. Python 变量、list、dict：代码其实是在管理“对象”

### 大白话
变量名可以理解成“贴在对象上的标签”。例如 `x = [1, 2, 3]`，`x` 是标签，真正的数据是那个 list。

`y = x` 并不一定复制了一份新数据；对可变对象来说，`x` 和 `y` 可能指向同一个对象。要独立复制，可以使用 `.copy()` 等方法。

### 为什么重要
研究代码经常会先保留原始数据，再生成 cleaned data。如果无意中原地修改同一个对象，可能把 raw data 也改掉。

### 一句话记忆
**变量名不是数据本身；赋值也不等于独立复制。**

---

## 2. list of dictionaries：一条 record 里有多个字段

例如：

```python
{"year": 2018, "temperature": 4.2}
```

一个 dict 是一条 observation；多个 dict 放进 list，就像一个很原始的小表格。

### 关键理解
清理缺失数据时，最好保留整条 record，而不是只把 temperature 单独抽出来，否则会丢失 `year ↔ temperature` 的对应关系。

### 一句话记忆
**数据分析不只是数值，还要保留数值和它的身份、时间、地点之间的对应关系。**

---

## 3. Function：把一个重复的“做事流程”装进盒子

### 大白话
function 就像一个小机器：给它 input，它按照固定规则处理，最后 `return` output。

```python
def mean_valid(values):
    ...
    return result
```

### Parameter vs argument
- parameter：定义 function 时写的占位名。
- argument：真正调用时传进去的具体值。

### `return` vs `print`
- `print()`：只是显示给人看。
- `return`：把结果交回程序，后面的代码还能继续使用。

### Scope
function 里面创建的变量通常是 local variable，只在 function 内部有效。

### 常见坑
把 `return` 写进 `for` loop 里面，会让 function 提前结束，只处理到前面的 observation。

### 一句话记忆
**function 的价值不是“少写几行”，而是把一个可靠的分析步骤封装成可以重复使用的 unit。**

---

## 4. Script execution order 与 hidden state

### 大白话
Python `.py` 文件从上到下执行。一个变量或 function 要先定义，后面才能使用。

Notebook 比较危险的地方是：旧变量可能还活在 memory 里，所以屏幕上的代码顺序和真正的运行状态可能不一样。

### 典型依赖链

`data → means → slope → intercept → predictions → residuals → RMSE`

如果中间某一步用了旧变量，后面的结果都会受影响。

### 一句话记忆
**能“跑出来”不代表能“从零复现”。真正可靠的代码要从第一行重新运行也得到同样结果。**

---

## 5. Missing values：缺失不是“0”

### 大白话
没有测到一个值，不等于那个值是 0。

在 pandas 里，数值列的缺失常显示为 `NaN`。

常用检查：

```python
df.isna().sum()
```

清理：

```python
clean_df = df.dropna(subset=["temperature"]).copy()
```

### 为什么 `.copy()` 好
保留原始 `df`，另建 `clean_df`，避免把 raw data 原地覆盖。

### 一句话记忆
**missingness 是数据质量信息，不是垃圾；先理解，再决定怎么处理。**

---

## 6. NumPy：让“整组数字一起算”

### Python list vs NumPy array

```python
[1, 2, 3] * 2
```

会重复 list；但：

```python
np.array([1, 2, 3]) * 2
```

会逐元素得到 `[2, 4, 6]`。

### Vectorization
以前用 `for` loop 一个一个算，现在可以对整个 array 做：

```python
year_deviations = years - mean_year
products = year_deviations * temperature_deviations
```

### 为什么对遥感重要
raster 本质上就是二维或多维 numerical array。NDVI、temperature grid、DEM 都天然适合 NumPy 风格的运算。

### 一句话记忆
**NumPy 适合规则的 numerical arrays；vectorization 就是把“逐个算”变成“整块算”。**

---

## 7. pandas：处理“带字段名的表格”

### 大白话
如果 NumPy 更像数学矩阵，那么 pandas 更像 Excel/CSV 表格，而且每一列有名字。

- `DataFrame`：整张表。
- `Series`：一列。

常用检查：

```python
df.head()
df.shape
df.columns
df.dtypes
df.isna().sum()
df.describe()
```

### pandas vs NumPy
- pandas：适合 `site | year | temperature | ndvi` 这种 records。
- NumPy：适合 raster / matrix / array 数值运算。

### 一句话记忆
**pandas 管表格和字段；NumPy 管数值数组和计算。**

---

## 8. Data validation：没缺失不代表没问题

我们实际检查过：

### Duplicate
```python
df.duplicated()
df.duplicated(subset=["year"], keep=False)
```

“整行重复”和“关键 identifier 重复”不是一回事。

### Impossible / implausible values
例如 400°C 虽然不是 missing，但明显不合理。

Boolean filtering：

```python
invalid = (df["temperature"] > 60) | (df["temperature"] < -50)
df[invalid]
```

### Chronological consistency
```python
df["year"].is_monotonic_increasing
df["year"].diff()
```

`is_monotonic_increasing` 允许相等，所以 `2024, 2024` 仍可能是 True；严格递增要进一步检查 `diff() <= 0`。

### Metadata / units
`temperature = 4.2` 本身不完整，还需要知道是 °C、°F 还是 K。

### 一句话记忆
**data cleaning 是删缺失；data validation 是问“这个数据在科学上和结构上合理吗？”**

---

## 9. Linear regression：找一条“整体最合适的直线”

简单线性回归：

`y = intercept + slope × x`

### Slope

`slope = Σ[(x-x̄)(y-ȳ)] / Σ[(x-x̄)²]`

### 大白话解释
- numerator：x 和 y 是否一起偏高、一起偏低。
- denominator：x 自己分散得有多开。
- slope：x 每变化 1 个单位，y 平均变化多少。

### 为什么 denominator 要平方
不平方的话，偏差正负会互相抵消，最后常常加起来接近 0。

### Intercept

`intercept = mean_y - slope × mean_x`

它是回归线在 `x=0` 时的预测值，但不一定具有科学解释。例如 year=0 的 temperature 没什么意义。

### 一句话记忆
**slope 是整体线性趋势，不要求每一个 observation 都同方向变化。**

---

## 10. Prediction、Residual、MSE、RMSE

### Prediction
把 x 放进 fitted model，得到预测 y。

### Residual

`residual = actual - predicted`

- residual > 0：模型低估了 actual。
- residual < 0：模型高估了 actual。

### MSE
把 residual 平方再平均。

### RMSE
MSE 再开平方，回到原本单位。

如果 NDVI 的 RMSE = 0.03，就是平均预测误差量级约 0.03 NDVI unit。

### 关键理解
RMSE 只告诉你“错多大”，residual pattern 还告诉你“怎么错”。

### 一句话记忆
**一个小 RMSE 不自动代表模型好；还要看 residual pattern、sample size、validation 和 generalization。**

---

## 11. Residual diagnostics 的第一层直觉

理想 residual：
- 围绕 0；
- 没有明显系统 pattern；
- 不应该越到后面误差越来越大。

如果 residual 全部朝一个方向，说明模型可能有 systematic bias。

如果 residual magnitude 越来越大，可能意味着 heteroscedasticity、遗漏变量、结构变化等，但不能直接跳到“它一定是 exponential”。

### 一句话记忆
**residual 是模型没解释掉的部分；pattern 往往比一个总分更有信息。**

---

## 12. Visualization：图不是装饰，是诊断工具

我们做过：
- observed scatter；
- fitted line；
- residual vs year plot。

图可以快速发现：
- 整体趋势；
- outlier；
- curvature；
- residual pattern；
- extrapolation。

### 一句话记忆
**表格告诉你数字，图让你看到结构。**

---

## 13. Virtual environment 与 dependencies

### `.venv`
给这个项目一个独立的 Python 软件环境。

### 为什么重要
你的电脑全局装了 package，不代表项目环境里就有。

我们实际遇到过：

`ModuleNotFoundError: No module named 'matplotlib'`

### `requirements.txt`
记录项目直接依赖及版本，例如：

```text
matplotlib==3.9.4
numpy==2.0.2
pandas==2.3.3
```

### 一句话记忆
**代码只是研究的一半；环境和依赖也是可复现性的一部分。**

---

## 14. Git 与 GitHub：版本控制不是网盘

### Git
记录代码变化的版本控制系统。

### GitHub
把 Git repository 放到远程平台，方便备份、展示和协作。

### 三个状态

`working directory → staging area → commit`

- 文件存在，不代表会进下一个 commit。
- `git add`：选择下一次提交的变化。
- `git commit`：形成一个版本快照。
- `git push`：推送到 GitHub。

### 常用诊断
- `git status`：我现在在哪个状态？
- `git diff`：working tree 改了什么？
- `git diff --staged`：准备提交什么？
- `git restore`：撤销不想要的修改。

### 一句话记忆
**Git 的价值不是“备份 final.py”，而是留下分析是怎么一步步变成现在这样的。**

---

## Week 1 Debugging 关键经验

真实遇到过：
- `return` 在 loop 里导致 function 提前结束；
- stale variable / execution order；
- 缺 matplotlib dependency；
- CSV 文件存在但为空 → `EmptyDataError`；
- Git author identity 配置不对；
- GitHub HTTPS 密码认证失败；
- README 写错目录；
- 文件没有 staged；
- `git diff` 进入 pager；
- 新文件夹建错层级。

**共同方法：**

`读完整错误信息 → 判断哪一层坏了 → 检查状态 → 做最小修复 → 重跑 → 验证 → 记录 lesson`

---

# Week 2 — Multivariable Environmental Analysis & Model Validation

## 1. Sentinel-2、Red、NIR、NDVI、pixel、raster

### Sentinel-2
光学遥感卫星，记录地表在不同波段的反射信息。

### Red 与 NIR
健康植被通常：
- 吸收较多 Red；
- 反射较多 NIR。

### NDVI

`NDVI = (NIR - Red) / (NIR + Red)`

它是 vegetation greenness 的 proxy，不是“植物数量”或“生态健康”的万能指标。

### Pixel
影像中的一个格子，对应地面上的一个区域。

### Raster
由规则 pixel 网格组成的空间数据，本质上接近二维 numerical array。

### 一句话记忆
**NDVI 是用红光和近红外反射差异估出来的“绿度代理指标”。**

---

## 2. Correlation：两个变量“一起变”的程度

相关系数 `r` 范围大致是 -1 到 +1。

- `r > 0`：一个高时另一个也倾向高。
- `r < 0`：一个高时另一个倾向低。
- `|r|` 越接近 1：线性关联越强。

例如：

`elevation ↔ NDVI r ≈ -0.993`

大白话：高海拔 site 倾向有更低 NDVI。

### 不能这样说
`r = 0.986` ≠ “98.6% 被解释”。

在简单线性回归的特殊情况下才有：

`R² = r²`

但 `R²` 也不是因果比例。

### 一句话记忆
**correlation 描述一起变，不告诉你谁导致谁。**

---

## 3. Multiple regression：同时考虑多个 predictors

形式：

`NDVI = β0 + β1 temperature + β2 elevation + β3 precipitation + error`

### X 与 y
- `X`：predictor matrix，多列输入。
- `y`：outcome，一列结果。

例如：
- X shape = `(14, 3)`：14 条 observation，3 个 predictors。
- y shape = `(14,)`：14 个 NDVI outcomes。

### 一句话记忆
**X 是模型看见的条件，y 是模型想解释/预测的结果。**

---

## 4. 为什么要加 constant / intercept

statsmodels 里：

```python
X = sm.add_constant(X)
```

会多出一列全是 `1.0` 的 `const`。

因为：

`β0 = β0 × 1`

这样模型就能估计 intercept；否则可能被迫通过原点。

### 一句话记忆
**constant 那列 1，是给 intercept 一个可以被估计的位置。**

---

## 5. “Holding other variables constant” 到底是什么意思

如果：

`β_temperature = 0.035`

可以说：

**holding elevation and precipitation constant, a 1°C increase in temperature is associated with a 0.035 increase in NDVI.**

不是说现实里真的把山按住不动，而是模型在统计上尝试比较“其他 predictors 相同条件下”的 temperature difference。

### 一句话记忆
**multiple regression 的 coefficient 是条件关联，不是简单相关。**

---

## 6. R²：模型在当前样本里拟合得多紧

例如 `R² = 0.994`：模型对当前 14 条数据的 variation 拟合得非常紧。

### 但不能说
- “模型解释了真实生态机制的 99.4%”；
- “模型一定能预测未来”；
- “所有 coefficients 都可信”。

### 一句话记忆
**高 R² 是 in-sample fit 好，不等于机制对，也不等于 out-of-sample prediction 好。**

---

## 7. p-value：不是“变量有多重要”的分数

我们的同一个 temperature：
- temperature-only model：非常显著；
- 加入 elevation 后：p-value 变大到不显著。

这说明 p-value 依赖：
- model specification；
- sample；
- 其他 predictors；
- assumptions。

### 一句话记忆
**p-value 不是变量自带的标签，而是“在这个模型和这批数据下”的结果。**

---

## 8. Multicollinearity：predictors 自己太像了

我们的数据中：
- elevation ↔ temperature ≈ -0.997；
- elevation ↔ precipitation ≈ +0.994。

大白话：temperature、elevation、precipitation 几乎在描述同一条 environmental gradient。

### 后果
模型很难判断 NDVI 的变化应该“分多少功劳/责任”给每个 predictor。

可能出现：
- coefficient 不稳定；
- 正负号反转；
- standard error 变大；
- inference 变困难。

### 一句话记忆
**predictors 太像，就像三个证人讲几乎一样的话，模型很难判断谁提供了独立信息。**

---

## 9. VIF：量化一个 predictor 和其他 predictors 重叠多少

公式：

`VIF = 1 / (1 - R²)`

这里的 R² 是：用其他 predictors 去预测这个 predictor。

粗略经验：
- VIF ≈ 1：没什么共线性；
- > 5：值得注意；
- > 10：通常比较严重。

我们的结果大约：
- temperature ≈ 201；
- elevation ≈ 215；
- precipitation ≈ 100。

说明严重 multicollinearity。

### 一句话记忆
**VIF 高 = 这个 predictor 很大一部分信息其实其他 predictors 已经说过了。**

---

## 10. Condition number：数值问题和共线性的警报器

OLS summary 中 condition number 很大。

它可能受：
- predictors 尺度差异；
- multicollinearity；
- 其他 numerical problems
影响。

因为我们同时已经看到极高 predictor correlations 和 VIF，所以这里不只是尺度问题。

### 一句话记忆
**condition number 是“有事值得查”的警报，不是单独定罪的证据。**

---

## 11. Coefficient instability：模型一换，系数就变脸

我们看到 temperature coefficient：

- temperature only：`+0.0381`
- temperature + elevation：`-0.0283`
- full model：`-0.0407`

这说明 temperature 的独立 effect estimate 非常不稳定。

### 关键结论
不能因为 full model 预测好，就说 `-0.0407` 一定是真实 ecological effect。

### 一句话记忆
**如果 coefficient 连方向都随 model specification 改变，就要对机制解释非常谨慎。**

---

## 12. Prediction vs Inference

### Prediction
问题：**新数据来了，我能不能预测准？**

关心：
- RMSE / MAE；
- validation；
- generalization。

### Inference
问题：**temperature 本身与 NDVI 的独立关系是什么？**

关心：
- coefficient 稳定性；
- confounding；
- multicollinearity；
- assumptions；
- uncertainty。

### 关键句
**A model can predict well without identifying the true mechanism.**

### 一句话记忆
**预测准和解释对，是两个不同目标。**

---

## 13. Training data vs unseen test data

### 为什么不能在同一批数据上 fit 又评价
模型已经“看过”这些 observation，所以得到的 error 可能过于乐观。

真正的 validation 应该让模型预测没参与 fitting 的 observation。

### 一句话记忆
**训练成绩不能当期末考试成绩。**

---

## 14. Interpolation vs Extrapolation

### 不是看离回归线多远
“内/外”看的是 predictor space，不是 residual。

### Interpolation
test observation 没见过，但 predictor values 落在 training data 已经覆盖的范围内。

### Extrapolation
test observation 的 predictor values 落在 training range 之外，或在训练数据几乎没有支持的区域。

### Residual 是另一件事
- 离 prediction 多远 → error / residual；
- 输入落不落在 training domain → interpolation / extrapolation。

### 多 predictor 时
即使 temperature 和 elevation 分别都在范围内，某个“high elevation + high temperature”组合可能训练中从未出现，也可能属于 multivariate extrapolation / distribution shift。

### 一句话记忆
**inter/extrapolation 看 input 在哪里；residual 看 prediction 错多少。**

---

## 15. High-elevation holdout：专门考模型“范围外”能力

我们把最高海拔 4 个 sites 留作 test。

Temperature-only model：
- RMSE ≈ 0.0443；
- residual 全为负；
- 越往高海拔走，负误差越大。

这意味着 model 在 novel low-temperature/high-elevation conditions 下系统性 overpredict NDVI。

### 一句话记忆
**一个总体 RMSE 可能掩盖 systematic bias；一定要看 individual residuals。**

---

## 16. LOOCV：小样本下轮流让每一个 observation 当一次 test

Leave-One-Out Cross-Validation：

- 每轮用 13 个 train；
- 留 1 个 test；
- 做 14 次；
- 汇总所有 out-of-sample errors。

优点：小样本时能充分利用数据。

局限：它主要反映整体 generalization，不等于专门测试极端 extrapolation。

### 一句话记忆
**一次 train/test split 可能碰巧；LOOCV 用很多次轮流考试降低这种偶然性。**

---

## 17. Model comparison：复杂模型不一定好，也不一定坏

我们的结果：

| Model | High-elevation holdout RMSE | LOOCV RMSE |
|---|---:|---:|
| Temperature only | 0.04433 | 0.02422 |
| Elevation only | 0.02045 | 0.01738 |
| Full model | **0.01397** | **0.01380** |

### 结论
在这组 illustrative data 和当前 validation 中，full model prediction 最好。

但它仍有严重 multicollinearity，所以 individual coefficients 不适合强解释。

### 一句话记忆
**复杂模型要不要，用 validation 说话；但预测表现好不等于 coefficients 就可信。**

---

## 18. Refactoring：不改变结果地把代码变清楚

### 问题
原来 temperature/elevation/full model 的 fit → predict → residual → RMSE 复制了很多遍。

复制粘贴容易造成：
- 某一处公式改错；
- 变量名混乱；
- 旧代码重复执行；
- RMSE 被错写成 squared error。

### 解决
写 helper functions：

```python
calculate_rmse(...)
fit_and_evaluate(...)
loocv_rmse(...)
```

### Behavior-preserving refactoring
重构前后得到相同结果，说明只是改善代码结构，没有偷偷改变科学结果。

### 一句话记忆
**refactoring = 改代码组织，不改分析含义。**

---

## Week 2 Debugging 关键经验

真实遇到过：
- column name 写成不存在的 `site_id` → `KeyError`；
- 把示例里的 `...` 原样运行 → DataFrame 出现 `Ellipsis`；
- 重复 model blocks 导致计算混乱；
- squared errors 一度被误叫成 RMSE；
- `IndentationError`；
- function 调用时还没定义 → `NameError`；
- function 定义重复。

### 这周更高一级的 debugging lesson
**不是只有“程序报错”才叫 bug。代码能运行但概念或计算含义错了，也是更危险的 bug。**

---

# 两周连起来的核心研究思维

## 1. 先问问题，再选工具
不要：

`我会 pandas → 找个地方用 pandas`

而应该：

`我的研究问题是什么 → 数据结构是什么 → 要检查什么 → 什么方法合适`

## 2. 先检查数据，再跑模型

`read → inspect → validate → clean → model`

而不是：

`read → model`

## 3. 一个数字永远不够
- correlation 强，不等于 causation；
- R² 高，不等于 generalization；
- p < 0.05，不等于 mechanism established；
- RMSE 低，不等于所有条件都预测好；
- coefficient 漂亮，不等于稳定。

## 4. 结果要问“在什么条件下成立”
例如：

“Full model RMSE 最低”更准确的说法是：

**在这组 illustrative data、当前 holdout 与 LOOCV 设置下，full model 得到最低 prediction error。**

## 5. Research computing 的目标
不是“会写很多 Python”，而是：
- 能把研究问题翻译成 analysis workflow；
- 能发现数据和模型的问题；
- 能解释方法假设；
- 能复现结果；
- 能说清楚结论边界。

---

# 核心公式速查

### Simple regression slope
`slope = Σ[(x-x̄)(y-ȳ)] / Σ[(x-x̄)²]`

### Intercept
`intercept = ȳ - slope × x̄`

### Residual
`residual = actual - predicted`

### MSE
`MSE = mean(residual²)`

### RMSE
`RMSE = sqrt(MSE)`

### Correlation 与 simple regression R²
`R² = r²`（仅在简单线性回归等相应条件下）

### VIF
`VIF = 1 / (1 - R²_j)`

---

# 常见误区速查

| 误区 | 更准确的理解 |
|---|---|
| r=0.63 = “63%相关” | r 是相关系数，不是百分比 |
| r=0.986 = “解释98.6%” | 不能；简单线性情境下才可看 r² |
| 高 R² = 模型一定好 | 只是当前样本拟合紧 |
| p<0.05 = 变量是原因 | p-value 不建立因果 |
| low RMSE = 模型 everywhere 都好 | 还要看 split、domain、residual pattern |
| test data = extrapolation | test 可以是 interpolation，也可以是 extrapolation |
| 离回归线远 = extrapolation | 那是 residual 大；extrapolation 看 predictor space |
| 多 predictors = 一定更好 | 需要 validation；还可能有 multicollinearity |
| prediction 好 = coefficient 可解释 | 完全不一定 |
| code runs = code correct | 能运行也可能概念/统计逻辑错 |

---

# 当前我已经可以独立解释的内容

- Python function 为什么需要 `return`，以及 scope / execution order。
- NumPy vectorization 与 pandas DataFrame 的角色区别。
- CSV 的 inspection、missingness、duplicate、range、chronology、metadata 检查。
- simple regression 的 slope / intercept / prediction / residual / RMSE。
- 为什么 residual pattern 重要。
- correlation 与 causation 的区别。
- multiple regression 中 “holding other variables constant” 的含义。
- multicollinearity、VIF 与 coefficient instability。
- prediction 与 inference 的区别。
- interpolation 与 extrapolation 的区别。
- holdout validation 与 LOOCV 的用途。
- 为什么一个模型可以预测好但机制解释不可靠。
- Git 的 working / staging / commit / push 基本流程。
- 为什么 `.venv` 和 `requirements.txt` 属于 reproducibility。

---

# 自测题（进入下一周前）

1. 为什么 `y = x` 对 list 不一定是独立复制？
2. 为什么 missing value 不能直接当成 0？
3. pandas 与 NumPy 各自最适合处理什么？
4. 为什么 slope 的 denominator 用 squared deviations？
5. residual 为负表示模型高估还是低估？
6. RMSE 很低为什么仍不能马上说模型好？
7. `r = 0.9` 能不能说“90% 被解释”？
8. multiple regression 中 “holding elevation constant” 是什么意思？
9. VIF 很高说明什么？
10. 为什么 temperature coefficient 会从正变负？
11. prediction 与 inference 的目标有什么不同？
12. interpolation 和 extrapolation 是看 y 的误差大小，还是看 predictor space？
13. LOOCV 为什么比一次 split 更稳健一些？
14. 为什么 full model prediction 最好，仍不能强解释它的 coefficients？
15. 为什么 refactoring 后必须检查结果是否和原来一致？

---

# Weekly Update Template（Week 3 以后复制此模板）

## Week N — [主题]

### 1. 本周研究问题
- 我试图回答什么问题？
- 为什么这个问题值得回答？

### 2. 新概念（大白话）
#### Concept A — [英文术语]
**大白话：**

**为什么重要：**

**最小例子：**

**常见误区：**

**一句话记忆：**

#### Concept B — [英文术语]
**大白话：**

**为什么重要：**

**最小例子：**

**常见误区：**

**一句话记忆：**

### 3. 本周代码能力
- 我现在能独立写什么？
- 哪些还需要参考文档？
- 哪些代码已经封装成 function？

### 4. Research reasoning
- 数据有哪些限制？
- 方法有哪些 assumptions？
- 结果能说明什么？
- 结果不能说明什么？

### 5. Validation / diagnostics
- 用了什么 validation？
- 看了什么 residual / diagnostic？
- 是否发现 distribution shift / extrapolation / instability？

### 6. Debugging cases
#### Case N — [标题]
**Problem：**

**Expected：**

**What went wrong：**

**Diagnosis：**

**Fix：**

**Verification：**

**Lesson：**

### 7. Reproducibility / Git
- 本周新增 dependencies：
- requirements 是否更新：
- commit message：
- working tree 是否 clean：

### 8. 本周最重要的 3 句话
1.
2.
3.

### 9. 自测
- [ ] 我能不用 ChatGPT 解释本周核心概念。
- [ ] 我能从空白文件重新写出核心 workflow。
- [ ] 我能解释一个真实 debugging case。
- [ ] 我能说清楚结果的边界。

### 10. Next week
- 下一周要补的概念：
- 下一周要完成的分析：
- 下一周要减少的 AI 依赖：
