---
name: resume-optimizer
description: 根据 JD 做匹配度诊断、优化简历、补全项目经历（严守诚信）。触发词：根据JD改简历、优化简历、简历匹配度、简历诊断、项目经历不够、简历适配JD、帮我润色简历、简历怎么写、简历提升、简历量化。
version: 2.0.0
---

# 简历优化器 Resume Optimizer

## 输入
- 目标 JD（必填）
- 用户当前简历（必填，支持文本或文件内容）
- 可选：目标行业/级别、已有项目清单

## 共享口径（必读）
- STAR/量化表达：`references/star-framework.md`
- ATS 关键词对齐：`references/ats-keywords.md`
- 诚信红线：`references/redlines.md`

## 流程
### 步骤1：JD 诊断
拆 JD 为「能力模型」：硬技能 / 软技能 / 业务域知识 / 隐性要求（级别对应复杂度与 ownership 量级）。
产出：能力清单（必需/加分）、匹配度评分(0–100)与分布、缺口清单。

### 步骤2：简历优化
- 对齐 ATS：JD 高频词自然嵌入（见 ats-keywords，AI 岗务必覆盖 LLM/RAG/Agent 等原词），保留可机器解析的简洁排版。
- 量化成果：每条经历按 star-framework 用「动作+量化结果」改写；**AI/大模型岗结果可用模型/系统指标量化**（准确率、延迟、吞吐、成本下降，见 star-framework 示例）。
- 岗位前置：最相关经历放最显眼；一页为佳（资深两页）。
  模块顺序：个人信息 → 求职意向 → 核心优势 → 经历 → 教育/其他。
产出可落到 .docx（用 docx skill）或给 Markdown。

### 步骤3：项目补全（严守诚信）
1. 先扫描已有真实经历，用 STAR 重构贴合 JD 能力的项目。
2. 真实经历覆盖不了的关键能力 → 告知是「缺口」，给两类建议：
   - A. 学习路径：短期可完成小项目/课程，标注「需用户真实完成」。
   - B. 参考样例（仅练习）：**必须标注「⚠️ 仅供面试讲述参考，非真实经历，切勿写入正式简历」**。
3. 绝不替用户凭空生成"真实项目"塞进简历（见 redlines）。

## 输出格式
```
【JD 能力模型】表（必需/加分）
【匹配度】分数 + 分布
【缺口】清单
【优化后简历】Markdown / docx
【项目补全建议】真实重构 X 条 + 缺口学习路径 + 参考样例（标注）
【下一步】建议先 company-research 背调，再 interview-prep 准备题库
```

## 关联
- 上游：`interview-coach`
- 下游：`company-research` → `interview-prep` / `mock-interview`
