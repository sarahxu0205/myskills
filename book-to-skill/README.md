# Book-to-Skill 元 Skill

将任何方法论书籍转换为可复用 Skill 的强大工具。

## 功能概述

Book-to-Skill 是一个**元 Skill**，它能够：
- 自动解析 PDF/TXT 书籍内容
- 通过 16 个核心问题深度分析方法论
- 生成标准化的 Skill 文件结构
- 提取方法步骤、核心原则、工具模板等关键信息

## 16 个核心问题框架

1. **书籍定位** - 解决什么问题？目标受众是谁？
2. **方法步骤** - 具体的操作步骤和依赖关系
3. **核心规矩** - 作者反复强调的原则
4. **警告与坑** - 常见错误和避坑指南
5. **关键提问** - 作者抛给读者的思考问题
6. **适用场景** - 适用与不适用的情况
7. **前置条件** - 需要的知识、工具、环境准备
8. **预期产出** - 执行后的具体结果
9. **检验标准** - 如何判断方法被正确执行
10. **核心原理** - 方法背后的理论基础
11. **配套资源** - 工具、模板、案例、练习材料
12. **学习路径** - 从入门到熟练的路径
13. **方法变体** - 常见变体和场景调整
14. **进阶技巧** - 高级技巧和优化方向
15. **AI 辅助点** - 适合 AI 辅助的步骤
16. **Skill 化建议** - 典型调用场景和触发条件

## 使用方法

### 方式一：使用 Skill 自动处理

当用户上传 PDF 或 TXT 书籍并表达转换意图时，Claude 会自动调用此 Skill：

```
用户: "请把这本《Getting Things Done》转换成 Skill"
→ Claude 自动执行 book-to-skill 流程
```

### 方式二：手动执行脚本

#### 1. 提取书籍内容

**PDF 格式：**
```bash
python3 scripts/extract_pdf.py /path/to/book.pdf --output ./output
```

**TXT 格式：**
```bash
python3 scripts/extract_txt.py /path/to/book.txt --output ./output
```

参数说明：
- `pdf_path` / `txt_path`: 书籍文件路径
- `--output`: 输出目录
- `--max-pages`: 最大处理页数（可选，仅 PDF）

输出文件：
- `extraction_result.json` - 结构化提取结果
- `full_text.txt` - 完整文本内容

#### 2. 分析内容（AI 辅助）

基于提取的内容，AI 会按照 `references/analysis_template.json` 的格式，回答 16 个问题，生成分析结果。

#### 3. 生成 Skill

```bash
python3 scripts/generate_skill.py --analysis ./analysis.json --output ./skills
```

参数说明：
- `--analysis`: 分析结果 JSON 文件路径
- `--output`: Skill 输出目录
- `--template`: 自定义模板文件（可选）

输出结构：
```
skill-name/
├── SKILL.md          # 主 Skill 文件
├── scripts/          # 辅助脚本
├── references/       # 参考资料
├── assets/           # 资源文件
└── .gitignore
```

### 方式三：一键执行（推荐）

使用 `run_pipeline.py` 一键串联完整流程：

```bash
python3 run_pipeline.py /path/to/book.pdf --output ./my-skill  # PDF
python3 run_pipeline.py /path/to/book.txt --output ./my-skill  # TXT
```

支持的参数：
- `--output`: 输出目录（默认 ./output）
- `--skip-extract`: 跳过提取步骤（使用已有的 extraction_result.json）
- `--skip-generate`: 跳过生成步骤（仅提取和分析）
- `--max-pages`: 最大处理页数
- `--max-chars`: full_text 最大字符数（0表示不限制）
- `--template`: 自定义 SKILL.md 模板

## 文件说明

### SKILL.md
主 Skill 文件，包含完整的元 Skill 说明和 16 个问题框架。

### scripts/extract_pdf.py
PDF 内容提取脚本，功能包括：
- 提取元数据（书名、作者、页数等）
- 提取完整文本内容
- 识别章节结构
- 支持大文件分块处理

### scripts/extract_txt.py
TXT 内容提取脚本，功能包括：
- 自动检测编码（UTF-8、GBK、GB2312、Big5 等）
- 从文件开头或文件名提取书名和作者
- 按虚拟页切分文本（便于章节检测）
- 识别章节结构（与 PDF 脚本使用相同的正则模式）
- 支持大文件分块处理

### scripts/generate_skill.py
Skill 生成脚本，功能包括：
- 基于分析结果生成 SKILL.md
- 自动创建标准目录结构
- 生成配套配置文件

### references/analysis_template.json
16 个问题分析模板，用于指导 AI 进行系统化分析。

### references/sample_analysis.json
示例分析结果（基于 GTD 书籍），展示完整的输出格式。

### evals/evals.json
测试用例，用于验证 Skill 功能。

## 工作流程

```
用户上传 PDF/TXT
    ↓
提取书籍内容 (extract_pdf.py / extract_txt.py)
    ↓
AI 分析 - 16 个问题
    ↓
生成分析结果 (analysis.json)
    ↓
生成 Skill (generate_skill.py)
    ↓
输出标准化 Skill 目录
```

## 示例

### 输入
《Getting Things Done》PDF 或 TXT 文件

### 处理
1. 提取书名、作者、章节结构
2. 分析 GTD 的五个步骤：收集、理清、组织、回顾、执行
3. 提取两分钟原则、下一步行动等核心原则
4. 识别适用场景和注意事项

### 输出
`getting-things-done` Skill，包含：
- 完整的 GTD 方法论说明
- 五个核心步骤的详细操作指南
- 清单模板和工具建议
- AI 辅助建议

## 注意事项

1. **版权尊重**: 生成的 Skill 仅供个人学习使用
2. **内容提炼**: Skill 是书籍内容的提炼，而非全文复制
3. **实用性优先**: 重点关注可操作的方法论
4. **持续优化**: 随着理解深入，持续改进 Skill

## 依赖安装

```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install PyPDF2 pdfplumber xpinyin
```

## 许可证

本元 Skill 仅供学习和研究使用。请尊重原书版权。

## 贡献

欢迎提交 Issue 和 PR 来改进这个元 Skill！
