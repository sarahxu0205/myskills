---
name: "wxa-skills-polish"
description: "对 wxa-skills-generate 生成的小程序 AI SKILL 初稿进行标准化二轮优化。用户手动调用，修复接口描述、Schema、组件绑定、API 返回值和组件 UI，补充官方最佳实践。"
---

# wxa-skills-polish

## 用途

在 `wxa-skills-generate` 生成小程序 AI SKILL 的第一版初稿后，执行标准化的第二轮优化，使 SKILL 达到可发布状态。

## 触发时机

**用户手动调用**。当用户明确表达以下意图时触发：
- "优化生成的 SKILL"
- "打磨 AI 技能"
- "修复生成后的技能"
- "对 SKILL 进行二轮优化"

## 优化清单

按顺序执行以下修复。每项修复针对 `<miniprogramRoot>/skills/{skillName}/` 下的特定文件（`<miniprogramRoot>` 为小程序源码根目录，以 `project.config.json` 中的 `miniprogramRoot` 为准，未配置时通常为项目根目录或 `miniprogram`）。

### 1. 修复工程配置

**目标文件**：`app.json`、`page-meta.json`

- 确保 `subPackages` 的 `root` 为 `"skills"`（不能是 `"skills/xxx"` 或项目根目录）。`skills/` 目录应位于小程序源码根目录（`<miniprogramRoot>`）下，以 `project.config.json` 中的 `miniprogramRoot` 配置为准。
- 确保 skills 分包标记 `"independent": true`。
- 确保 `app.json` 开启 `"lazyCodeLoading": "requiredComponents"`。
- 确保 `app.json` 中 `agent.skills` 正确配置每个 SKILL 的 `name`、`description`、`path`。
- 确保 `app.json` 中 `agent.pageMetadata` 指向 `page-meta.json`。
- 确保 `page-meta.json` 声明了 SKILL 涉及的所有页面（首页、列表、详情、编辑等）。格式如下：
  ```json
  {
    "pages": [
      {
        "path": "pages/home/home",
        "name": "首页名称",
        "description": "页面功能描述"
      }
    ]
  }
  ```
  `pages` 为对象数组，每个对象必须包含 `path`（页面路径）、`name`（页面名称）、`description`（页面功能描述）。
- 确保调试基础库版本为 `3.16.1` 或更高。
- 如需支持暗黑模式，确保 `app.json` 中 `"darkmode": true`。

### 2. 信息源与分工

**核心原则**：不同信息源在 AI 决策时的注意力权重不同，写在错误的位置会显著降低准确率。

| 信息源 | 注意力权重 | 说明 |
|---|---|---|
| 原子接口返回的 `content` | ★★★★★ | 离当前决策点最近，模型会把它当作"事实 + 动作"读取（参见 https://developers.weixin.qq.com/miniprogram/dev/ai/best-practices.html）。这里出现错误话术，会让模型偏离 SKILL.md 的约定。 |
| 原子接口声明（mcp.json）里的 `description` | ★★★★ | 影响模型"选不选这个接口"，写得模糊时模型容易选错。 |
| 原子接口声明（mcp.json）里的 `inputSchema.description` | ★★★★ | 影响模型"怎么填参数"，是字段级约束的核心位置，比写在 SKILL.md 长文里更有效。 |
| `SKILL.md` | ★★★ | 适合写业务流程编排、跨接口规则、意图分流、通用规范。 |

**内容分工**：

| 信息源 | 写什么 |
|---|---|
| 原子接口返回的 `content` | 本次调用结果与下一步动作 |
| 原子接口声明里的 `description` | 接口本身的功能、调用时机、不适用场景 |
| 原子接口声明里的 `inputSchema.description` | 参数语义、取值来源、缺省处理 |
| `SKILL.md` | 业务流程编排、跨接口规则、意图分流、通用规范 |

**常见错位（必须避免）**：
- 把"接口本身的功能"写到 `SKILL.md`：长文膨胀、与 `mcp.json` 易不一致。`SKILL.md` 中的接口清单只写"前置条件 + 上下游关系"。
- 把"跨多接口的业务规则"写到单个接口的 `description`：仅在调用该接口时生效，其他接口决策时模型读不到。应写在 `SKILL.md`。
- 把"接口功能描述"写到 `content`：`content` 只承载本次调用结果与下一步动作，功能描述属于 `description`。

**通用写作原则**：
1. **同一约束在一处书写**。重复书写容易因措辞不一致引发冲突。
2. **硬约束放在权重更高的位置**。能在代码层面基于规则强校验的约束，优先做代码校验。
3. **给出可执行出口**。只写"不要做 X"而不写"应做什么"，模型会缺少出口。每条禁令都应配一个明确的替代动作。

### 3. 补全 mcp.json 接口描述

**目标文件**：`mcp.json`

对 `apis` 数组中的每个接口对象：

#### 3.1 接口 description 书写规范

1. **接口名使用语义化名称**。如 `searchDrinks` 优于 `search`。
2. **首句声明「业务对象」，而非「入参」**。
   - 反例："按关键词、温度、杯型搜索商品列表（仅饮品）……" —— 首句强调入参，且"商品"语义过宽，模型可能误命中其他商品类目。
   - 推荐："搜索饮品。按关键词、温度、杯型检索……" —— 首句先点明业务对象，再描述入参维度。
3. **不写内部实现细节**。实现具体细节对模型选择接口没有帮助，会挤占真正重要的"使用边界"信息。
4. **职责单一，描述互不重叠**。接口之间避免包含关系；描述面向模型而非用户，措辞简洁即可。
5. **同名字段统一命名**。同一含义的字段在不同接口保持一致，例如饮品 ID 始终用 `drinkId`，不要混用 `itemId`。

#### 3.2 字段级 description 书写规范

**入参字段选取**：优先传 ID 而非自然语言，例如门店传 `storeId` 而非省市街道，饮品传 `drinkId` 而非饮品名称、类目。模型不必再从自然语言中反复提取和匹配，参数歧义更少，推理也更快、更稳。

**普通字段 description**：举例时给多个不同样本（避免被当默认值），并配明确的缺省处理。单一举例容易被模型当作"标准答案"。

```js
// 反例：只举一个例子，且未说明缺省处理
"keyword": { "description": "饮品关键词，如『拿铁』" }

// 推荐：多样化举例 + 缺省处理
"keyword": {
  "description": "饮品关键词，例如『拿铁』『美式』『奶茶』。用户未说出具体饮品时，不要填写本字段，应改走饮品推荐接口。"
}
```

**ID 类字段 description**：声明取值来源接口。业务 ID 容易被按格式凑出，需在 description 中显式声明来源。

```js
// 反例
"drinkId": { "description": "饮品 ID" }

// 推荐
"drinkId": {
  "description": "饮品唯一标识，取自上游接口 searchDrinks 或 getRecommendedDrinks 返回的 drinkId 原值。不要从用户自然语言（如『那个拿铁』）推断，也不要使用示例值。上下文无可用 drinkId 时，应先调 searchDrinks。"
}
```

### 4. 规范化 API 返回值

**目标文件**：`apis/*.js`

每个 API handler 必须返回如下结构的对象：

```js
return {
  content: [
    { type: 'text', text: '当前客观状态陈述...' },
    { type: 'text', text: '下一步引导...' }
  ],
  structuredContent: { /* 供原子组件渲染的结构化数据 */ },
  _meta: { /* 渲染需要但 AI 无需理解的数据 */ },
  isError: false
}
```

#### 4.1 通用规则

**输入校验**

小程序 AI 生成的参数不保证正确，原子接口需校验类型与有效性（如 `drinkId` 是否存在）。

**返回内容**

- `structuredContent` 与 `content` 都会提供给小程序 AI：前者承载结构化数据（卡片展示内容），后者承载结果说明与决策约束，两者避免重复。
- 渲染需要但小程序 AI 无需理解的内容（如图片地址、后台冗余字段）通过 `_meta` 传递。

**错误处理**

- 返回明确的错误原因与下一步指引：
    - 缺信息："缺少收货地址，需用户补充"；
    - 无结果："未找到相关饮品，可换关键词重试"。

参数非法时，返回 `isError: true`，`content` 说明缺失/错误的字段及正确填法：

```js
// 推荐：参数校验示例
if (!args.drinkId || typeof args.drinkId !== 'string') {
  return {
    content: [
      { type: 'text', text: '调用失败：缺少必填参数 drinkId，或 drinkId 类型不正确。' },
      { type: 'text', text: '请通过 searchDrinks 或 getRecommendedDrinks 获取有效的 drinkId 后，再调用本接口。' }
    ],
    isError: true
  }
}
```

#### 4.2 事实 + 动作两段式

content 应先陈述本次返回的客观状态，再给出下一步动作。仅有动作没有事实时，模型可能把"展示卡片"理解为"准备调下一步接口"而跳过等待用户确认。

```js
// 反例：仅给动作，缺少事实
"接下来请务必为用户展示订单确认卡片。"

// 推荐：事实 + 动作
"已根据所选规格生成订单。请展示订单确认卡片，并用一句话引导用户核对后下单。"
```

#### 4.3 失败/空结果

当接口执行失败、返回空结果或参数不合法时，`content` 同样遵循"事实 + 动作"两段式，但在动作段中需明确包含下一步出口以及不应做的动作。

1. **陈述具体事实**：把问题原因写清楚（不要只写"失败了"）。
2. **给出下一步出口及不应做的动作**：告诉 AI 接下来应该做什么，同时明确禁止哪些错误操作（如禁止再重复尝试调用此原子接口）。该条须与具体事实配对出现，不要只写禁令而不给出口。

```js
// 反例：信息不足，模型会盲目重试
return {
  content: [{ type: 'text', text: '搜索失败，请重试。' }],
  isError: true
}

// 推荐：事实 + 动作两段式
return {
  content: [
    { type: 'text', text: '搜索饮品失败：当前门店（storeId=xxx）未营业，无法提供饮品列表。' },
    { type: 'text', text: '请引导用户更换门店，或切换到"无需门店"的推荐模式。禁止在相同门店下重复调用 searchDrinks，结果不会改变。' }
  ],
  isError: true
}
```

### 5. 修复 API 模块导出与导入

**目标文件**：`apis/*.js`、`index.js`

检查 API 文件的导出方式：

```js
// 方式 A：导出函数本身（官方推荐）
module.exports = function handler(args) { ... }

// 方式 B：导出对象（wxa-skills-generate 常见生成方式）
module.exports = { handlerName: function(args) { ... } }
```

- 若 API 文件使用方式 A（`module.exports = function`），则 `index.js` 使用直接导入：
  ```js
  const handlerName = require('./apis/handlerName.js')
  ```
- 若 API 文件使用方式 B（`module.exports = { handlerName }`），则 `index.js` 必须使用解构导入：
  ```js
  const { handlerName } = require('./apis/handlerName.js')
  ```

**关键**：确保 `skill.registerAPI('name', handler)` 注册的是**函数本身**，而不是对象。

### 6. 修复 SKILL.md 文档

**目标文件**：`SKILL.md`

按官方最佳实践，SKILL.md 应包含以下章节：

- **业务流程图**：使用 ASCII 流程图展示用户意图到接口调用的完整链路。
- **原子接口依赖关系表**：表格列出各接口的名称、作用、绑定组件、前置条件。
- **业务约束（跨接口铁律）**：
  - 输出形态约束：绑定组件的接口成功返回后必须展示卡片，禁止以纯文本列出卡片中的详情数据。
  - 执行顺序约束：明确接口调用先后顺序（如 A 必须在 B 之后调用）。
  - 并发串行约束：涉及状态变更的接口（如支付、下单、预约）不应并发调用，须等上一笔结束（成功、失败或取消）后再发起。
  - 数据来源约束：ID 类参数必须来自上游接口返回的字段原值，禁止编造或从用户自然语言推断。
- **用户意图分流**：列出直接触发本 SKILL 的用户话术，以及意图分流规则（模糊意图 → 接口 A，明确关键词 → 接口 B）。

### 7. 修复 setRelatedPage 调用

**目标文件**：`components/*/index.js`

- 正确的参数名是 `path`，不是 `page`：
  ```js
  viewCtx.setRelatedPage({ path: 'pages/index/index', query: 'foo=bar' })
  ```
- 空状态卡片：将 `path` 设为小程序首页。
- 数据卡片：设置 `query` 跳转到详情页。
- 原子组件的 `relatedPage` 应在 `mcp.json` 的 `components` 数组中配置，组件内动态设置仅用于覆盖默认行为。

### 8. 组件事件与后续接口调用

**目标文件**：`components/*/index.js`

当用户在组件内触发操作（如点击按钮、选择选项）需要调用下一个原子接口时，使用 `sendFollowUpMessage`：

```js
wx.modelContext.getContext(this).sendFollowUpMessage({
  content: [
    { type: 'text', text: '用户操作描述' },
    { type: 'api/call', data: { name: 'nextApiName', arguments: { /* 参数 */ } } }
  ]
})
```

确保 `api/call` 中的 `name` 与 `mcp.json` 中注册的接口名称一致。

### 9. 上行消息文案规范

**目标文件**：`apis/*.js`、`components/*/index.js`

上行消息文案指 `content` 中 `type: 'text'` 的内容，以及 `sendFollowUpMessage` 中的 `text` 内容。文案质量直接影响 AI 会话的流畅度和用户体验。

#### 9.1 基本原则

1. **用户视角出发**：文案是"给用户看的"，不是"给开发者看的"。
2. **操作语义准确**：同一 UI 元素的文案不可出现两种语义（如"下单"按钮的文案不能既叫"立即购买"又叫"确认预约"）。
3. **会话承接自然**：用语应与用户表达习惯一致，避免专业术语堆砌，让用户感知到自己"在与一个懂自己的人交流"。
4. **对话简洁清晰**：避免冗余、重复、过长的表达。

#### 9.2 具体撰写原则

| 原则 | 说明 | 示例 |
|---|---|---|
| **用户视角出发** | 消息需站在用户视角表述，可使用第一人称，一般不建议使用其他人称 | 参见官方文档 |
| **不可上行系统消息** | 即使是用户操作导致的异常系统消息，也不可以上行，需要转换成用户操作 | 参见官方文档 |
| **自然语言表达** | 用自然语言表达，摒弃字段罗列、编码等技术性描述格式 | 参见官方文档 |
| **使用生活化语言** | 表意准确基础上，优先选用生活化口语，规避专业性过强的术语 | 参见官方文档 |
| **仅限用户已明确表达的信息** | 信息仅限用户当前操作可推导内容，不可擅自补充用户未说明的偏好或诉求 | 参见官方文档 |
| **描述当前操作** | 描述聚焦当下操作，不能描述其他环节或提前预判未来操作 | 参见官方文档 |
| **信息充分但不过载** | 只保留能推动当前对话或有助于模型理解的必备信息，次要信息可以不说明 | 参见官方文档 |
| **简洁但不歧义** | 精简文案长度的同时保证表意清晰，尤其多选择场景下规避这个、那个等指代模糊的用词 | 参见官方文档 |
| **处理敏感信息** | 身份证号、手机号等隐私信息禁止明文展示，必要时脱敏模糊表述 | 参见官方文档 |
| **其他通用性文案规范** | 无错别字，无病句，正确断句，正确使用空格、标点符号等 | 参见官方文档 |

### 10. 打磨原子组件 UI

**目标文件**：`components/*/{index.wxml,index.wxss,index.js}`

#### 基础尺寸

- 根据内容复杂度选择合适的卡片尺寸，保持组件尺寸的一致性。
- 避免同一页面出现过多不同尺寸的卡片，维持视觉秩序。

#### 背景

- 浅色模式下使用白色或浅灰色背景。
- 深色模式下使用深灰色或黑色背景，确保文字对比度满足可读性要求。
- 避免使用复杂渐变背景。

#### 边距

- 卡片内保持统一的内边距，确保内容与边缘有合适的呼吸空间。
- 元素之间保持均匀的间距，避免信息拥挤。

#### 字体

- 使用层级化的字体规范：标题加粗突出，正文清晰易读，辅助文字使用较小字号和灰色。
- 避免同一组件中出现过多不同的字号，保持视觉简洁。

#### 布局

- 根据信息类型选择合适的布局模式：左图右文、上图下文、纯文本列表等。
- 保持布局的一致性，同一类型的信息使用相同的排列方式。
- 空状态使用居中布局，配合插图与引导文案。

#### 操作

- 主操作使用醒目样式（如深色背景），次操作使用弱化样式（如浅色背景或边框）。
- 修复微信 `button` 默认 padding/margin，显式设置 `height`、`line-height`、`padding: 0`、`margin: 0`、`border: none`。
- 组件中每个可交互元素必须绑定 `bindtap`，禁止出现无事件绑定的"死"按钮。

#### 顶部胶囊

- 使用圆角胶囊样式，保持与整体设计语言一致。
- 胶囊内的文字和图标需居中对齐，保持视觉平衡。

#### 其他注意事项

- 在 glass-easel 中避免使用 `transform: rotate()`、`calc()` 和复杂渐变，这些经常无法渲染。
- 过期态声明：当业务存在"卡片到某时刻作废"语义时（如限时优惠、过期订单），在 `mcp.json` 的 `components[]` 中声明 `expirable: true` 和 `expiredText`（如 `expiredText: "该优惠已过期"`）。

### 11. 全局提示词（可选）

**目标文件**：`AGENTS.md`（如适用）

如果小程序有多个 SKILL 或需要全局行为引导，可在项目根目录创建 `AGENTS.md`：
- 说明服务范围和背景知识。
- 描述多个 SKILL 的关联关系和选择策略。
- 引导小程序 AI 生成"猜你想问"内容。
- 在 `app.json` 的 `agent` 字段中通过 `instruction` 指定路径。

### 12. 验证与测试

- 在微信开发者工具中使用"小程序 AI 编译"模式编译。
- 检查 AI 面板中是否能看到**所有**接口（如有缺失，检查 `inputSchema` 根级是否有 `description`）。
- 逐个触发接口，确认绑定的原子组件能正确渲染。
- 测试组件内按钮点击是否能正确触发 `sendFollowUpMessage` 并调用后续接口。
- 测试右上角跳转入口是否正确指向对应页面。
- 测试空状态、暗黑模式等边界场景。

## 输出

所有修复完成后，向用户提供修改摘要，列出本次二轮优化涉及的具体文件和关键改动点。SKILL 即可进入第二轮测试。

## 参考文档
- [小程序 AI 开发模式接入指南](https://developers.weixin.qq.com/miniprogram/dev/ai/integration.html)
- [小程序 AI 最佳实践](https://developers.weixin.qq.com/miniprogram/dev/ai/best-practices.html)
