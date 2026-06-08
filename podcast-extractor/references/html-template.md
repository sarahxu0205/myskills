# HTML 输出模板

## 使用说明

1. 将 `{{占位符}}` 替换为实际提取的内容
2. 如果某个区块无相关内容，保留区块但显示"[无相关内容]"，或删除该区块
3. 生成完整的单文件 HTML，所有样式内嵌在 `<style>` 标签中，无外部依赖
4. 确保替换所有占位符，不保留任何 `{{...}}` 形式的文本

## 占位符速查表

| 占位符 | 说明 | 示例 |
|---|---|---|
| `{{PODCAST_NAME}}` | 播客名称 | 十字路口 |
| `{{EPISODE_TITLE}}` | 本期标题 | FDE：AI 时代的新岗位出现 |
| `{{PUBLISH_DATE}}` | 发布日期 | 2026-06-04 |
| `{{DURATION}}` | 时长 | 55分钟 7秒 |
| `{{HOST}}` | 主持人姓名 | Koji |
| `{{TAG1}}` `{{TAG2}}` ... | 主题标签（可扩展多个） | AI落地、企业转型 |
| `{{GUEST1_NAME}}` | 嘉宾1姓名 | 阿甘 |
| `{{GUEST1_TITLE}}` | 嘉宾1职位 | RollingAI 合伙人 |
| `{{GUEST1_BIO}}` | 嘉宾1简介 | 米兰理工/同济 · ENFJ |
| `{{ONE_SENTENCE_SUMMARY}}` | 一句话总结本期核心内容 | OpenAI和Anthropic... |
| `{{KEY_POINTS_COUNT}}` | 核心观点数量 | 5 |
| `{{KEY_POINT_NUMBER}}` | 观点序号 | 1 |
| `{{KEY_POINT_TITLE}}` | 观点标题 | AI不是软件，是劳动力... |
| `{{KEY_POINT_CONTENT}}` | 观点详细阐述 | 传统软件是工具... |
| `{{CERTAINTY_CLASS}}` | 确定性 CSS 类名 | confirmed / speculative / controversial |
| `{{CERTAINTY_LABEL}}` | 确定性标签文本 | 已确认（嘉宾自身业务实践） |
| `{{TOPIC_NUMBER}}` | 话题序号 | 话题一 |
| `{{TOPIC_TITLE}}` | 话题标题 | FDE的本质——从卖软件到送数字员工上岗 |
| `{{TIMESTAMP_RANGE}}` | 时间戳范围 | 00:00 - 04:00 |
| `{{TOPIC_CORE_CONTENT}}` | 话题核心内容段落 | FDE最早来自Pilot... |
| `{{DATA_POINT_1}}` `{{DATA_POINT_2}}` ... | 关键数据点 | OpenAI和Anthropic各成立10亿美元级别FDE合资公司 |
| `{{CASE_STORY}}` | 案例/故事描述 | 乳品企业案例：原有渠道不适合... |
| `{{METHOD_1}}` `{{METHOD_2}}` ... | 方法论条目 | FDE三大工作：业务融合、知识治理、系统对接 |
| `{{PRIORITY_CLASS}}` | 优先级 CSS 类名 | high / medium / low |
| `{{PRIORITY_LABEL}}` | 优先级标签文本 | 高优先级 |
| `{{ACTION_ITEM}}` | 可执行建议内容 | 企业引入AI时，不要把它当成IT项目... |
| `{{QUOTE_1}}` `{{QUOTE_2}}` ... | 原话摘录/金句 | AI跟传统软件本来是非常不一样的... |
| `{{BOOK_1}}` `{{BOOK_2}}` ... | 推荐书籍 | 《XXX》 |
| `{{ARTICLE_1}}` `{{ARTICLE_2}}` ... | 推荐文章/报告 | 《XXX》 |
| `{{CONCEPT_1}}` `{{CONCEPT_2}}` ... | 关键概念/术语 | FDE（Forward Deployed Engineer） |
| `{{HIGH_PRIORITY_ACTION_1}}` ... | 高优先级行动项 | 企业引入AI时，把它当成"新员工入职"项目... |
| `{{MEDIUM_PRIORITY_ACTION_1}}` ... | 中优先级行动项 | 咨询公司把交付物从"报告"变成... |
| `{{LOW_PRIORITY_ACTION_1}}` ... | 低优先级行动项 | 建议年轻人先去大平台培养商业judgment... |
| `{{QUESTION_1_TITLE}}` | 开放性问题标题 | FDE人才的培养路径 |
| `{{QUESTION_1_CONTENT}}` | 开放性问题描述 | 商业判断力（taste/feeling）是否真的是天生的？... |
| `{{SPEAKER_NAME}}` | 说话人标识 | 说话人 1 / 嘉宾姓名 |
| `{{TIME}}` | 时间戳 | 00:00 |
| `{{TRANSCRIPT_PARAGRAPH}}` | 原文段落 | 嗨，我是Koji，那本周十字路口呢... |
| `{{GENERATED_DATE}}` | 生成日期 | 2026-06-08 |

## CSS 样式

```css
:root {
    --bg-color: #f8f6f2;
    --text-color: #2c2c2c;
    --accent-color: #d4a373;
    --accent-light: #e9d5a8;
    --secondary-color: #6b8e9f;
    --card-bg: #ffffff;
    --border-color: #e0dcd5;
    --code-bg: #f4f1ea;
    --highlight-bg: #fff8e7;
    --quote-bg: #faf8f3;
    --quote-border: #c9b896;
    --tag-bg: #f0ebe3;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: "Noto Serif SC", "Songti SC", "SimSun", serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.8;
    padding: 40px 20px;
}

.container { max-width: 900px; margin: 0 auto; }

/* Header */
header {
    text-align: center;
    margin-bottom: 50px;
    padding: 40px 0;
    border-bottom: 2px solid var(--accent-color);
}

.podcast-title {
    font-size: 2.4em;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 15px;
    letter-spacing: 2px;
    line-height: 1.3;
}

.podcast-meta {
    font-size: 1em;
    color: var(--secondary-color);
    margin-bottom: 20px;
}

.tag-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-top: 15px;
}

.tag {
    display: inline-block;
    background: var(--tag-bg);
    color: var(--text-color);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    border: 1px solid var(--border-color);
}

/* Sections */
.section {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 35px;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid var(--border-color);
}

h2 {
    font-size: 1.6em;
    color: var(--accent-color);
    margin-bottom: 25px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--accent-light);
    font-weight: 600;
}

h3 {
    font-size: 1.3em;
    color: var(--secondary-color);
    margin: 25px 0 15px 0;
    font-weight: 600;
}

h4 {
    font-size: 1.1em;
    color: var(--text-color);
    margin: 20px 0 10px 0;
    font-weight: 600;
}

p { margin-bottom: 15px; text-align: justify; }

ul, ol { margin-left: 25px; margin-bottom: 20px; }

li { margin-bottom: 10px; }

/* Summary Box */
.summary-box {
    background: var(--highlight-bg);
    border-left: 4px solid var(--accent-color);
    padding: 25px;
    margin: 20px 0;
    border-radius: 0 8px 8px 0;
    font-size: 1.05em;
    line-height: 1.9;
}

/* Key Points */
.key-point {
    background: var(--quote-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.key-point-title {
    font-weight: 600;
    color: var(--accent-color);
    margin-bottom: 10px;
    font-size: 1.1em;
}

.key-point-content { margin-bottom: 10px; }

.certainty {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    margin-top: 8px;
}

.certainty-confirmed { background: #e8f5e9; color: #2e7d32; }
.certainty-speculative { background: #fff3e0; color: #e65100; }
.certainty-controversial { background: #ffebee; color: #c62828; }

/* Topic Cards */
.topic-card {
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 25px;
    margin-bottom: 25px;
}

.topic-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 10px;
}

.topic-title {
    font-size: 1.2em;
    font-weight: 600;
    color: var(--text-color);
    flex: 1;
}

.timestamp {
    color: var(--secondary-color);
    font-size: 0.9em;
    white-space: nowrap;
}

.topic-section { margin-bottom: 15px; }

.topic-section-title {
    font-weight: 600;
    color: var(--accent-color);
    margin-bottom: 8px;
    font-size: 0.95em;
}

/* Quotes */
.quote-box {
    background: var(--quote-bg);
    border-left: 3px solid var(--quote-border);
    padding: 15px 20px;
    margin: 15px 0;
    border-radius: 0 6px 6px 0;
    font-style: italic;
    color: #555;
}

.quote-box::before {
    content: """;
    font-size: 2em;
    color: var(--accent-light);
    line-height: 0.1em;
    margin-right: 5px;
    vertical-align: middle;
}

/* Action Items */
.action-list { list-style: none; margin-left: 0; }

.action-list li {
    position: relative;
    padding-left: 30px;
    margin-bottom: 12px;
}

.action-list li::before {
    content: "☐";
    position: absolute;
    left: 0;
    color: var(--accent-color);
    font-size: 1.2em;
}

.priority-high { color: #c62828; font-weight: 600; }
.priority-medium { color: #f57c00; font-weight: 600; }
.priority-low { color: #689f38; font-weight: 600; }

/* Details/Summary for collapsible content */
details {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    margin-bottom: 20px;
    overflow: hidden;
}

summary {
    padding: 18px 25px;
    cursor: pointer;
    font-weight: 600;
    color: var(--text-color);
    background: var(--bg-color);
    border-bottom: 1px solid var(--border-color);
    transition: background 0.2s;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

summary:hover { background: var(--highlight-bg); }

summary::after {
    content: "▼";
    font-size: 0.8em;
    color: var(--accent-color);
    transition: transform 0.2s;
}

details[open] summary::after { transform: rotate(180deg); }

details > div { padding: 25px; }

/* Original transcript */
.transcript {
    background: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 25px;
    max-height: 600px;
    overflow-y: auto;
    font-family: "Noto Sans SC", "Microsoft YaHei", sans-serif;
    font-size: 0.95em;
    line-height: 1.8;
    color: #444;
}

.transcript p { margin-bottom: 12px; text-align: left; }

.speaker { font-weight: 600; color: var(--accent-color); }
.time { color: var(--secondary-color); font-size: 0.9em; }

/* References */
.ref-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 15px 0;
}

.ref-item {
    background: var(--bg-color);
    padding: 12px 15px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
}

/* Footer */
footer {
    text-align: center;
    margin-top: 60px;
    padding-top: 30px;
    border-top: 1px solid var(--border-color);
    color: var(--secondary-color);
    font-size: 0.9em;
}

/* Responsive */
@media (max-width: 768px) {
    .podcast-title { font-size: 1.8em; }
    .section { padding: 25px; }
    .ref-grid { grid-template-columns: 1fr; }
    .topic-header { flex-direction: column; }
}

/* Back to top button */
.back-to-top {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: var(--accent-color);
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    z-index: 100;
    font-size: 1.2em;
}

.back-to-top.visible { opacity: 1; }

/* Topic navigation */
.topic-nav {
    background: var(--card-bg);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    border: 1px solid var(--border-color);
}

.topic-nav h3 {
    margin: 0 0 12px 0;
    font-size: 1em;
    color: var(--accent-color);
}

.topic-nav a {
    display: block;
    color: var(--secondary-color);
    text-decoration: none;
    padding: 6px 0;
    border-bottom: 1px solid var(--border-color);
    font-size: 0.9em;
    transition: color 0.2s;
}

.topic-nav a:last-child { border-bottom: none; }

.topic-nav a:hover { color: var(--accent-color); }

/* Print styles */
@media print {
    body { padding: 20px; background: white; }
    .section { box-shadow: none; border: 1px solid #ddd; break-inside: avoid; }
    details { break-inside: avoid; }
    .back-to-top { display: none; }
    .topic-nav { display: none; }
}
```

## HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{PODCAST_NAME}} - {{EPISODE_TITLE}}</title>
    <style>
        /* 将上方 CSS 样式完整粘贴到这里 */
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1 class="podcast-title">{{PODCAST_NAME}} - {{EPISODE_TITLE}}</h1>
            <div class="podcast-meta">
                {{PUBLISH_DATE}} · {{DURATION}} · 主持人：{{HOST}}
            </div>
            <div class="tag-container">
                <span class="tag">#{{TAG1}}</span>
                <span class="tag">#{{TAG2}}</span>
                <span class="tag">#{{TAG3}}</span>
                <!-- 根据实际标签数量扩展 -->
            </div>
        </header>

        <!-- Topic Navigation -->
        <nav class="topic-nav">
            <h3>快速导航</h3>
            <a href="#summary">一句话总结</a>
            <a href="#key-points">核心观点</a>
            <a href="#topics">详细内容拆解</a>
            <a href="#references">引用与推荐资源</a>
            <a href="#actions">可执行清单</a>
            <a href="#questions">开放性问题</a>
            <a href="#transcript">播客原文</a>
        </nav>

        <!-- Guests -->
        <div class="section">
            <h2>嘉宾信息</h2>
            <div class="ref-grid">
                <div class="ref-item">
                    <strong>{{GUEST1_NAME}}</strong><br>
                    {{GUEST1_TITLE}}<br>
                    {{GUEST1_BIO}}
                </div>
                <!-- 根据实际嘉宾数量扩展 -->
            </div>
        </div>

        <!-- One Sentence Summary -->
        <div class="section" id="summary">
            <h2>一句话总结</h2>
            <div class="summary-box">
                {{ONE_SENTENCE_SUMMARY}}
            </div>
        </div>

        <!-- Key Points -->
        <div class="section" id="key-points">
            <h2>核心观点（{{KEY_POINTS_COUNT}}个）</h2>
            
            <div class="key-point">
                <div class="key-point-title">{{KEY_POINT_NUMBER}}. {{KEY_POINT_TITLE}}</div>
                <div class="key-point-content">
                    {{KEY_POINT_CONTENT}}
                </div>
                <span class="certainty certainty-{{CERTAINTY_CLASS}}">{{CERTAINTY_LABEL}}</span>
            </div>
            <!-- 根据实际观点数量重复上述结构 -->
        </div>

        <!-- Detailed Content -->
        <div class="section" id="topics">
            <h2>详细内容拆解</h2>

            <div class="topic-card">
                <div class="topic-header">
                    <span class="topic-title">{{TOPIC_NUMBER}}：{{TOPIC_TITLE}}</span>
                    <span class="timestamp">⏱ {{TIMESTAMP_RANGE}}</span>
                </div>
                
                <div class="topic-section">
                    <div class="topic-section-title">核心内容</div>
                    <p>{{TOPIC_CORE_CONTENT}}</p>
                </div>

                <div class="topic-section">
                    <div class="topic-section-title">关键数据</div>
                    <ul>
                        <li>{{DATA_POINT_1}}</li>
                        <li>{{DATA_POINT_2}}</li>
                        <!-- 根据实际数据点数量扩展 -->
                    </ul>
                </div>

                <div class="topic-section">
                    <div class="topic-section-title">案例/故事</div>
                    <p>{{CASE_STORY}}</p>
                </div>

                <div class="topic-section">
                    <div class="topic-section-title">方法论</div>
                    <ul>
                        <li>{{METHOD_1}}</li>
                        <li>{{METHOD_2}}</li>
                        <!-- 根据实际方法论数量扩展 -->
                    </ul>
                </div>

                <div class="topic-section">
                    <div class="topic-section-title">可执行建议</div>
                    <ul>
                        <li><span class="priority-{{PRIORITY_CLASS}}">【{{PRIORITY_LABEL}}】</span>{{ACTION_ITEM}}</li>
                        <!-- 根据实际建议数量扩展 -->
                    </ul>
                </div>

                <div class="topic-section">
                    <div class="topic-section-title">原话摘录</div>
                    <div class="quote-box">{{QUOTE_1}}</div>
                    <div class="quote-box">{{QUOTE_2}}</div>
                    <!-- 根据实际引用数量扩展 -->
                </div>
            </div>
            <!-- 根据实际话题数量重复上述 topic-card 结构 -->
        </div>

        <!-- References -->
        <div class="section" id="references">
            <h2>引用与推荐资源</h2>
            
            <h3>书籍</h3>
            <div class="ref-grid">
                <div class="ref-item">《{{BOOK_1}}》</div>
                <!-- 根据实际数量扩展 -->
            </div>

            <h3>文章/报告</h3>
            <div class="ref-grid">
                <div class="ref-item">{{ARTICLE_1}}</div>
                <!-- 根据实际数量扩展 -->
            </div>

            <h3>概念/术语</h3>
            <div class="ref-grid">
                <div class="ref-item">{{CONCEPT_1}}</div>
                <!-- 根据实际数量扩展 -->
            </div>
        </div>

        <!-- Action Items -->
        <div class="section" id="actions">
            <h2>可执行清单</h2>
            
            <h3>高优先级</h3>
            <ul class="action-list">
                <li><span class="priority-high">【高优先级】</span>{{HIGH_PRIORITY_ACTION_1}}</li>
                <!-- 根据实际数量扩展 -->
            </ul>

            <h3>中优先级</h3>
            <ul class="action-list">
                <li><span class="priority-medium">【中优先级】</span>{{MEDIUM_PRIORITY_ACTION_1}}</li>
                <!-- 根据实际数量扩展 -->
            </ul>

            <h3>低优先级</h3>
            <ul class="action-list">
                <li><span class="priority-low">【低优先级】</span>{{LOW_PRIORITY_ACTION_1}}</li>
                <!-- 根据实际数量扩展 -->
            </ul>
        </div>

        <!-- Open Questions -->
        <div class="section" id="questions">
            <h2>开放性问题/待深入研究</h2>
            <ol>
                <li><strong>{{QUESTION_1_TITLE}}：</strong>{{QUESTION_1_CONTENT}}</li>
                <!-- 根据实际数量扩展 -->
            </ol>
        </div>

        <!-- Personal Notes -->
        <div class="section">
            <h2>个人笔记/思考</h2>
            <p style="color: #888; font-style: italic;">[留给用户自己填写]</p>
        </div>

        <!-- Original Transcript (Collapsible) -->
        <details id="transcript">
            <summary>📄 查看播客原文（点击展开）</summary>
            <div class="transcript">
                <p><span class="speaker">{{SPEAKER_NAME}}</span> <span class="time">{{TIME}}</span><br>
                {{TRANSCRIPT_PARAGRAPH}}</p>
                <!-- 根据实际段落数量扩展 -->
            </div>
        </details>

        <footer>
            <p>由播客内容提取器自动生成 · {{GENERATED_DATE}}</p>
        </footer>
    </div>

    <!-- Back to top button -->
    <div class="back-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">↑</div>
    <script>
        const btn = document.querySelector('.back-to-top');
        window.addEventListener('scroll', () => {
            btn.classList.toggle('visible', window.scrollY > 300);
        });
    </script>
</body>
</html>
```

## 设计规范

1. **整体风格**：温暖优雅的纸质阅读风格
   - 背景色：米白色（#f8f6f2）
   - 强调色：暖棕色（#d4a373）
   - 辅助色：灰蓝色（#6b8e9f）
   - 卡片背景：纯白色（#ffffff）

2. **布局结构**：
   - 顶部：播客标题 + 元信息（日期、时长、主持人）+ 标签云
   - 嘉宾信息卡片（如有）
   - 一句话总结（高亮引用框）
   - 核心观点（独立卡片，带确定性标签）
   - 详细内容拆解（话题卡片，含时间戳）
   - 引用与推荐资源
   - 可执行清单（带复选框，按优先级分色）
   - 开放性问题
   - 个人笔记区域
   - 底部可折叠原文区域（使用 `<details>`/`<summary>` 标签）

3. **视觉元素**：
   - 核心观点卡片：独立卡片 + 确定性标签（绿色=已确认，橙色=推测，红色=有争议）
   - 金句引用框：左侧边框 + 引号图标 + 斜体
   - 优先级标签：高优先级=红色，中优先级=橙色，低优先级=绿色
   - 话题卡片：圆角边框 + 阴影 + 时间戳标签
   - 可折叠原文：底部 `<details>` 标签，默认折叠

4. **技术要求**：
   - 纯 HTML/CSS，无外部依赖
   - 所有样式内嵌在 `<style>` 标签中
   - 响应式设计，支持移动端
   - 中文内容使用系统默认中文字体栈
   - 打印友好（@media print 优化）
