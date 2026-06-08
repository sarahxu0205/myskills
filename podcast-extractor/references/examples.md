# 输入/输出示例

## 示例 1：简短播客（2 个话题）

### Input（原始文字稿片段）

```
说话人 1 00:00
大家好，欢迎来到《科技早知道》，我是主持人小明。今天我们有请到了 AI 研究员李博士，来聊聊最近很火的 Agent 话题。

李博士 00:30
谢谢邀请。其实 Agent 这个概念并不新，但今年大模型让它真正落地了。我觉得核心变化是：从"工具"变成了"同事"。

说话人 1 01:00
"同事"这个说法很有意思，能具体讲讲吗？

李博士 01:15
以前我们用软件，是我们告诉它每一步做什么。现在 Agent 是给它一个目标，它自己规划步骤、调用工具、完成任务。根据我们的测试，在客服场景下，Agent 的处理效率比传统工单系统提升了 3 倍，准确率从 72% 提升到 89%。

说话人 1 02:00
那企业现在用 Agent 最大的障碍是什么？

李博士 02:20
不是技术，是组织。很多公司把 Agent 当成 IT 项目，让技术部主导。但 Agent 改变的是业务流程，必须业务部牵头。我们服务了 50 多家企业，成功率不到 40%，失败的原因 80% 是组织问题。

说话人 1 03:00
能给听众一些行动建议吗？

李博士 03:15
第一，先找一个具体的业务场景，别做大而全的"AI 转型"。第二，让业务部门当项目负责人，IT 只提供支持。第三，准备好现有流程的 SOP，Agent 需要学习你们现在最好的做法。
```

### Output（生成的 HTML 关键片段）

**Header 区域：**
```html
<header>
    <h1 class="podcast-title">科技早知道 - Agent：从工具到同事</h1>
    <div class="podcast-meta">
        2026-06-08 · 15分钟 · 主持人：小明
    </div>
    <div class="tag-container">
        <span class="tag">#AI</span>
        <span class="tag">#Agent</span>
        <span class="tag">#企业落地</span>
    </div>
</header>
```

**核心观点卡片：**
```html
<div class="key-point">
    <div class="key-point-title">1. Agent 的本质是从"工具"变成"同事"</div>
    <div class="key-point-content">
        传统软件需要人告诉它每一步做什么，Agent 只需给定目标，就能自主规划步骤、调用工具、完成任务。
    </div>
    <span class="certainty certainty-confirmed">已确认（嘉宾自身研究成果）</span>
</div>

<div class="key-point">
    <div class="key-point-title">2. Agent 落地的最大障碍是组织而非技术</div>
    <div class="key-point-content">
        50+企业实践中成功率不到 40%，80% 的失败原因是组织问题——把 Agent 当成 IT 项目而非业务变革。
    </div>
    <span class="certainty certainty-confirmed">已确认（50+企业服务数据）</span>
</div>
```

**话题卡片：**
```html
<div class="topic-card">
    <div class="topic-header">
        <span class="topic-title">话题一：Agent 的核心变化——从工具到同事</span>
        <span class="timestamp">⏱ 00:00 - 02:00</span>
    </div>
    
    <div class="topic-section">
        <div class="topic-section-title">核心内容</div>
        <p>Agent 与大模型的结合让它从概念走向落地。核心变化是交互模式的转变：从"人指挥每一步"到"人给目标，Agent 自主执行"。</p>
    </div>

    <div class="topic-section">
        <div class="topic-section-title">关键数据</div>
        <ul>
            <li>客服场景效率提升 3 倍</li>
            <li>准确率从 72% 提升到 89%</li>
        </ul>
    </div>

    <div class="topic-section">
        <div class="topic-section-title">可执行建议</div>
        <ul>
            <li><span class="priority-high">【高优先级】</span>找一个具体业务场景启动，避免大而全的"AI 转型"</li>
            <li><span class="priority-high">【高优先级】</span>让业务部门当项目负责人，IT 只提供支持</li>
            <li><span class="priority-medium">【中优先级】</span>准备好现有流程的 SOP，Agent 需要学习最佳实践</li>
        </ul>
    </div>

    <div class="topic-section">
        <div class="topic-section-title">原话摘录</div>
        <div class="quote-box">我觉得核心变化是：从"工具"变成了"同事"</div>
        <div class="quote-box">不是技术，是组织。很多公司把 Agent 当成 IT 项目，让技术部主导</div>
    </div>
</div>
```

---

## 示例 2：长播客（8 个话题，对应 FDE 播客）

### Input（原始文字稿片段）

```
说话人 1 00:00
嗨，我是Koji，那本周十字路口呢，我们来聊一个最近非常热门的话题FDE...

说话人 2 02:29
我们有个本质的认知，就 AI 跟传统软件是本来是非常不一样的...

说话人 3 02:54
今天的 AI 在企业里面，别把它看成一个软件...你得把它看成一个新的员工在上岗...
```

### Output（生成的 HTML 关键片段）

**一句话总结：**
```html
<div class="summary-box">
    OpenAI和Anthropic在同一天宣布成立10亿美元级别的FDE企业AI合资公司，RollingAI的两位合伙人从4年+的一线实践出发，揭示了FDE的本质——不是卖软件，而是像HRBP一样把"数字员工"送入企业、帮它上岗并产生业务结果。
</div>
```

**核心观点（5个，带确定性标签）：**
```html
<div class="key-point">
    <div class="key-point-title">1. AI不是软件，是劳动力，FDE是帮数字员工上岗的HRBP</div>
    <div class="key-point-content">传统软件是工具，需要人操作；AI本身就是劳动力...</div>
    <span class="certainty certainty-confirmed">已确认（嘉宾自身业务实践）</span>
</div>

<div class="key-point">
    <div class="key-point-title">2. 咨询行业的交付物从PPT变成了智能体，上线周期从半年压缩到15天</div>
    <div class="key-point-content">传统咨询交付200页PPT，现在交付的是智能体...</div>
    <span class="certainty certainty-confirmed">已确认（嘉宾公司内部标准）</span>
</div>

<div class="key-point">
    <div class="key-point-title">4. 从"标准化保底线"到"智能体赋能一线拿最优解"——下一代管理智慧来自中国</div>
    <div class="key-point-content">SOP代表慢和落后，标准化只能做到全局60分...</div>
    <span class="certainty certainty-speculative">推测/观点（嘉宾对中国市场的判断）</span>
</div>
```

**话题卡片（8个话题之一）：**
```html
<div class="topic-card">
    <div class="topic-header">
        <span class="topic-title">话题三：AI赋能一线——副店长、营养师、租房管家的实践</span>
        <span class="timestamp">⏱ 08:00 - 22:00</span>
    </div>
    
    <div class="topic-section">
        <div class="topic-section-title">关键数据</div>
        <ul>
            <li>乳品企业：600万在线用户，1人+50多个机器人运营，单次服务成本从16元降到0.04-0.1元</li>
            <li>租房平台：管家从1对500提升到1对1200，目标1对2000</li>
        </ul>
    </div>

    <div class="topic-section">
        <div class="topic-section-title">案例/故事</div>
        <p><strong>1. 乳品企业营养师：</strong>用AI替代真人营养师服务600万用户...</p>
        <p><strong>2. 租房平台管家：</strong>管家被日常琐事困住，AI负责回复日常琐事...</p>
    </div>

    <div class="topic-section">
        <div class="topic-section-title">原话摘录</div>
        <div class="quote-box">AI最大的红利不在于顶部或总部做策略性的事，而是把智慧陪在店长、销售人员身边</div>
        <div class="quote-box">AI是能给店长很多补充思考的，但得店长和AI在一起才能得出正确结论</div>
    </div>
</div>
```

**可执行清单（按优先级分色）：**
```html
<h3>高优先级</h3>
<ul class="action-list">
    <li><span class="priority-high">【高优先级】</span>企业引入AI时，把它当成"新员工入职"项目而非IT项目</li>
    <li><span class="priority-high">【高优先级】</span>AI项目必须由业务部门主导，IT团队提供支持</li>
    <!-- ... -->
</ul>

<h3>中优先级</h3>
<ul class="action-list">
    <li><span class="priority-medium">【中优先级】</span>咨询公司把交付物从"报告"变成"可运行的智能体"</li>
    <!-- ... -->
</ul>
```

## 提取要点说明

1. **元信息提取**：从文字稿开头识别播客名称、主持人、嘉宾姓名和背景
2. **一句话总结**：综合全部内容，用 1-2 句话概括核心主题和价值主张
3. **核心观点**：提取 3-5 个最重要的观点，每个配确定性标签（已确认/推测/有争议）
4. **话题拆解**：按时间顺序划分话题，每个话题包含核心内容、数据、案例、方法论、建议、原话
5. **时间戳映射**：根据文字稿中的时间标记或内容逻辑推断大致时间范围
6. **可执行建议**：按优先级分类，确保具体可操作
7. **原文折叠**：将完整文字稿放入 `<details>` 标签，默认折叠
