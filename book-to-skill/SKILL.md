---
name: book-to-skill
description: 将方法论书籍转换为可复用 Skill 的元 Skill。当用户上传一本 PDF 或 TXT 格式的书籍（尤其是方法论、工具书、指南类书籍）并希望将其核心方法提取为 Skill 时，使用此 Skill。典型触发场景："把这本书变成 skill"、"提取这本书的方法论"、"将这本 PDF/TXT 转换为 skill"、"分析这本书的核心方法"、"帮我总结这本书的方法/框架"、"提炼这本书的核心要点"、用户上传 PDF/TXT 书籍后询问如何处理、即使没有明确提到 "skill" 只要用户希望从书籍中提取可复用的方法论/框架/操作指南也应使用此 Skill。此 Skill 会自动解析 PDF/TXT，提取书名、作者、关键章节，并通过 16 个核心问题深度分析书籍内容，最终生成结构化的 Skill 文件。
---

# Book to Skill 元 Skill

## 概述

本 Skill 用于将任何方法论书籍（工具书、指南、方法论著作）转换为结构化的、可复用的 Skill 格式。通过系统化的 16 个问题框架，深度提取书籍中的方法步骤、核心原则、警告提示、案例示例和工具模板。

## 使用流程

### 第一步：接收用户输入

1. **确认输入文件**：用户应提供 PDF 或 TXT 格式的书籍文件
2. **明确目标**：确认用户希望将书籍转换为 Skill
3. **了解背景**（可选）：询问用户是否有特定的使用场景或关注点
4. **确认书籍类型**（可选）：如果用户已说明书籍类型为方法论/工具书，可跳过后续的类型检测步骤

### 第二步：解析书籍内容

根据文件格式选择对应的提取脚本：

**PDF 格式：**
```bash
python3 scripts/extract_pdf.py <pdf_path> --output <output_dir>
```

**TXT 格式：**
```bash
python3 scripts/extract_txt.py <txt_path> --output <output_dir>
```

> 也可使用 `run_pipeline.py` 一键执行，它会根据文件扩展名自动选择对应的提取脚本。

脚本会提取：
- 书籍元数据（书名、作者、出版信息）
- 完整文本内容
- 章节结构
- 目录信息

### 第 2.5 步：检测书籍类型

在深度分析之前，先判断书籍是否属于方法论/工具书范畴。基于第二步提取的文本内容和章节结构进行判断。

**判断依据（满足任一即为方法论书籍）：**
- 书籍内容包含明确的方法步骤、操作指南、流程框架
- 章节结构呈现"步骤型"或"原则型"（如"第一步"、"原则 1"、"Rule 1"）
- 书籍定位是解决特定问题或传授特定技能
- analysis_template.json 中的 16 个问题能够有效回答

**非方法论书籍的特征（满足任一即应拒绝）：**
- 纯叙事类：小说、短篇集、散文集
- 纯记录类：传记、回忆录、历史纪实（无方法论提炼）
- 纯欣赏类：诗歌集、摄影集、画册
- 纯知识类：教科书、百科全书、词典（非方法论导向）

**处理方式：**
如果判定为非方法论书籍，直接回复用户：

> 这本书（《书名》）看起来属于 [小说/传记/散文] 类型，不属于方法论工具书。本 Skill 专为方法论、工具书、指南类书籍设计，通过 16 个问题框架提取可操作的方法步骤和核心原则。对于此类书籍，建议：
> 1. 如果书中包含可提炼的方法论（如人物传记中的管理智慧），可以明确告知我关注点，我会针对性提取
> 2. 如果只是想了解书籍内容，可以直接提问，无需生成 Skill

**注意：** 边界模糊的书籍（如《乔布斯传》既算传记也包含管理方法论）不要直接拒绝，应倾向继续处理。

### 第三步：深度分析

在开始分析之前，先读取以下参考文件：

1. **读取 `references/analysis_framework.md`** -- 获取完整的 16 个问题分析框架
2. **读取 `references/analysis_template.json`** -- 了解每个问题的期望输出格式
3. **参考 `references/sample_analysis.json`** -- 查看 GTD 书籍的完整分析示例

然后基于提取的书籍内容，按照 16 个问题框架系统性地分析书籍内容，将结果保存为 JSON 格式。

16 个问题涵盖：书籍定位、方法步骤、核心规矩、警告提示、关键提问、适用场景、前置条件、预期产出、检验标准、核心原理、配套资源、学习路径、方法变体、进阶技巧、AI 辅助点、Skill 化建议。

### 第四步：生成 Skill 文件

基于以上分析，生成标准的 Skill 文件结构：

```
<skill-name>/
├── SKILL.md              # 主 Skill 文件
├── scripts/              # 辅助脚本（如需要）
├── references/           # 参考资料
└── assets/               # 资源文件
```

使用 `scripts/generate_skill.py` 脚本生成 Skill：

```bash
python3 scripts/generate_skill.py \
  --analysis <analysis_json> \
  --output <skill_output_dir>
```

### 第五步：验证与优化

1. **完整性检查**：确保所有 16 个问题都有答案
2. **逻辑一致性**：检查内容逻辑是否一致
3. **可操作性**：验证生成的 Skill 是否可操作
4. **用户反馈**：根据用户反馈进行调整

### 附：大书籍增量分析

对于超过 300 页的大型书籍（或超过 50 万字的 TXT 文件），建议分批分析：

**PDF 格式：**
```bash
# 分批提取（共分 3 批）
python3 scripts/extract_pdf.py book.pdf --output ./output --chunk 0 --chunk-total 3
python3 scripts/extract_pdf.py book.pdf --output ./output --chunk 1 --chunk-total 3
python3 scripts/extract_pdf.py book.pdf --output ./output --chunk 2 --chunk-total 3
```

**TXT 格式：**
```bash
# 分批提取（共分 3 批）
python3 scripts/extract_txt.py book.txt --output ./output --chunk 0 --chunk-total 3
python3 scripts/extract_txt.py book.txt --output ./output --chunk 1 --chunk-total 3
python3 scripts/extract_txt.py book.txt --output ./output --chunk 2 --chunk-total 3
```

1. 分批提取书籍内容
2. 逐批进行 16 个问题分析
3. 合并各批次的分析结果为完整 JSON
4. 用合并后的 JSON 生成最终 Skill

## 输出格式规范

### SKILL.md 结构

```markdown
---
name: <skill-name>
description: <基于问题 1 和 16 生成的描述，典型触发场景：场景 1；场景 2；场景 3>
---

# <书籍标题> Skill

## 概述

<基于问题 1：书籍定位>

## 核心方法

### 方法步骤
<基于问题 2：步骤详解>

### 核心原则
<基于问题 3：核心规矩>

### 注意事项
<基于问题 4：警告与坑>

## 使用指南

### 适用场景
<基于问题 6：适用/不适用场景>

### 前置准备
<基于问题 7：前置条件>

### 预期产出
<基于问题 8：预期产出>

### 检验标准
<基于问题 9：检验标准>

## 深入理解

### 核心原理
<基于问题 10：核心原理>

### 关键提问
<基于问题 5：关键提问>

## 实践资源

### 配套工具
<基于问题 11：配套资源>

### 学习路径
<基于问题 12：学习路径>

### 方法变体
<基于问题 13：常见变体>

### 进阶技巧
<基于问题 14：进阶技巧>

## AI 辅助建议

<基于问题 15：AI 辅助点>
```

## 命名规范

Skill 名称应遵循以下规范：
- 使用小写字母和连字符
- 简洁明了，体现书籍核心主题
- 避免使用书名全称（除非书名本身就是方法名）
- 示例：`getting-things-done`、`atomic-habits`、`deep-work`

## 注意事项

1. **版权尊重**：生成的 Skill 仅供个人学习使用，不得用于商业目的
2. **内容提炼**：Skill 应该是对书籍内容的提炼，而非全文复制
3. **实用性优先**：重点关注可操作的方法论，而非理论阐述
4. **保持更新**：随着对书籍理解的深入，持续优化 Skill

## 示例

### 输入
用户上传《Getting Things Done》PDF 或 TXT 文件

### 处理流程
1. 提取书籍内容
2. 通过 16 个问题分析
3. 生成 `getting-things-done` Skill

### 输出
结构化的 GTD Skill，包含：
- 收集、处理、组织、回顾、执行五个步骤
- 两分钟原则、下一步行动等核心原则
- 清单、流程图等工具模板

## Supporting Files

| 文件路径 | 用途 | 读取时机 |
|---------|------|---------|
| `scripts/extract_pdf.py` | PDF 内容提取脚本 | 第二步执行时 |
| `scripts/extract_txt.py` | TXT 内容提取脚本 | 第二步执行时 |
| `scripts/generate_skill.py` | Skill 文件生成脚本 | 第四步执行时 |
| `references/analysis_framework.md` | 16 个问题分析框架（详细版） | 第三步分析前必读 |
| `references/analysis_template.json` | 分析结果 JSON 模板 | 第三步分析前必读 |
| `references/sample_analysis.json` | GTD 书籍完整分析示例 | 第三步分析时参考 |
