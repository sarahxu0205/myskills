---
name: "miniprogram-performance-optimizer"
description: "识别小程序性能瓶颈并提供优化建议。在开发过程中检测性能问题时调用，或用户主动请求性能优化时使用。"
---

# 小程序性能优化技能

## 技能概述

本技能用于识别小程序代码中的性能瓶颈，并提供基于微信官方最佳实践的优化建议。覆盖启动性能和运行时性能两大核心领域。

## 何时调用

**必须立即调用此技能的情况：**
- 用户明确要求进行性能优化
- 用户提到小程序启动慢、卡顿、白屏等性能问题
- 代码审查时发现潜在性能问题
- 用户询问如何提升小程序性能
- 在部署前进行性能检查

**建议调用的情况：**
- 大量使用 setData 操作
- 页面结构复杂、组件嵌套深
- 图片或资源加载较多
- 长列表渲染场景
- 频繁进行数据请求

## 性能优化领域

### 1. 启动性能优化

#### 1.1 代码包体积优化
**检测点：**
- 主包大小是否超过 2MB
- 是否有未使用的代码和资源
- 是否合理使用分包加载
- 图片资源是否经过压缩

**优化建议：**
- 使用分包加载，将非首屏内容放入分包
- 压缩图片资源，使用 webp 格式
- 移除未使用的代码和资源
- 按需引入第三方库
- 使用云开发 CDN 加速资源加载

**代码示例：**
```javascript
// app.json - 分包配置
{
  "pages": [
    "pages/index/index"
  ],
  "subPackages": [
    {
      "root": "packageA",
      "pages": [
        "pages/cat/cat",
        "pages/dog/dog"
      ]
    }
  ]
}
```

#### 1.2 代码注入优化
**检测点：**
- app.js 初始化逻辑是否复杂
- 是否有不必要的全局变量
- 是否有过多的同步操作

**优化建议：**
- 简化 app.js 初始化逻辑
- 延迟加载非关键模块
- 避免在启动时进行大量计算
- 减少全局变量使用

#### 1.3 首屏渲染优化
**检测点：**
- 首页 WXML 结构是否复杂
- 是否有阻塞渲染的脚本
- 首屏资源加载策略

**优化建议：**
- 简化首页 WXML 结构
- 使用骨架屏提升用户体验
- 延迟加载非首屏图片
- 避免在 Page.onLoad 中进行耗时操作

**代码示例：**
```javascript
// 首页优化示例
Page({
  data: {
    items: [],
    showSkeleton: true
  },

  onLoad() {
    // 先显示骨架屏
    this.loadData();
  },

  async loadData() {
    try {
      const res = await wx.request({
        url: 'https://api.example.com/data'
      });
      this.setData({
        items: res.data,
        showSkeleton: false
      });
    } catch (error) {
      console.error('加载数据失败', error);
    }
  }
});
```

### 2. 运行时性能优化

#### 2.1 合理使用 setData
**检测点：**
- setData 调用频率是否过高
- 每次 setData 传递的数据量是否过大
- 是否有不必要的数据更新
- 是否在 setData 中进行复杂计算

**优化建议：**
- 合并多次 setData 为一次
- 只更新变化的数据字段
- 避免频繁调用 setData（建议 16ms 间隔）
- 不要在 setData 中进行复杂计算
- 使用 dataPath 精确更新数据

**代码示例：**
```javascript
// ❌ 不推荐：频繁调用 setData
Page({
  data: {
    name: '',
    age: 0,
    city: ''
  },
  updateUserInfo() {
    this.setData({ name: '张三' });
    this.setData({ age: 25 });
    this.setData({ city: '北京' });
  }
});

// ✅ 推荐：合并 setData 调用
Page({
  data: {
    name: '',
    age: 0,
    city: ''
  },
  updateUserInfo() {
    this.setData({
      name: '张三',
      age: 25,
      city: '北京'
    });
  }
});

// ✅ 推荐：使用 dataPath 精确更新
Page({
  data: {
    user: {
      info: {
        name: '张三',
        age: 25
      }
    }
  },
  updateAge() {
    this.setData({
      'user.info.age': 26
    });
  }
});
```

#### 2.2 渲染性能优化
**检测点：**
- WXML 节点数量是否过多（建议 < 1000）
- 组件嵌套层级是否过深（建议 < 10 层）
- 是否有不必要的 wx:if 和 wx:for
- 是否合理使用 hidden 属性

**优化建议：**
- 减少 WXML 节点数量
- 降低组件嵌套层级
- 合理使用 wx:if 和 hidden
- 避免在列表中使用复杂的条件渲染
- 使用 virtual-list 处理长列表

**代码示例：**
```xml
<!-- ❌ 不推荐：过多的条件渲染 -->
<view wx:if="{{type === 'A'}}">内容 A</view>
<view wx:elif="{{type === 'B'}}">内容 B</view>
<view wx:elif="{{type === 'C'}}">内容 C</view>
<view wx:else">其他内容</view>

<!-- ✅ 推荐：使用 hidden 或模板 -->
<view hidden="{{type !== 'A'}}">内容 A</view>
<view hidden="{{type !== 'B'}}">内容 B</view>
<view hidden="{{type !== 'C'}}">内容 C</view>
<view hidden="{{type !== 'D'}}">其他内容</view>

<!-- ✅ 推荐：长列表使用虚拟列表 -->
<recycle-view batch="{{batchSetRecycleData}}" height="{{height}}" id="recycleId">
  <view slot="before">列表头部</view>
  <recycle-item wx:for="{{recycleList}}" wx:key="id">
    <view>{{item.name}}</view>
  </recycle-item>
  <view slot="after">列表尾部</view>
</recycle-view>
```

#### 2.3 页面切换优化
**检测点：**
- 页面切换是否流畅
- 是否有不必要的页面预加载
- 页面栈是否管理合理

**优化建议：**
- 使用预加载机制提升切换体验
- 合理管理页面栈，及时销毁不需要的页面
- 避免在 onShow 中进行耗时操作
- 使用 wx.navigateTo 代替 wx.redirectTo（除非必要）

**代码示例：**
```javascript
// 预加载页面
Page({
  onLoad() {
    // 预加载下一个页面
    wx.preloadPage({
      url: '/pages/detail/detail?id=123'
    });
  }
});

// 合理使用页面跳转
// ✅ 推荐：保留当前页面
wx.navigateTo({
  url: '/pages/detail/detail'
});

// ⚠️ 谨慎使用：关闭当前页面
wx.redirectTo({
  url: '/pages/detail/detail'
});
```

#### 2.4 资源加载优化
**检测点：**
- 图片资源是否过大
- 是否有重复的资源加载
- 是否合理使用缓存
- 网络请求是否合理

**优化建议：**
- 压缩图片，使用合适的尺寸
- 使用懒加载技术
- 合理设置缓存策略
- 合并网络请求，减少请求次数
- 使用 CDN 加速资源加载

**代码示例：**
```javascript
// 图片懒加载
Page({
  data: {
    images: []
  },

  onLoad() {
    this.loadImages();
  },

  loadImages() {
    // 只加载可视区域内的图片
    const visibleImages = this.getVisibleImages();
    this.setData({ images: visibleImages });
  },

  onReachBottom() {
    // 滚动到底部时加载更多
    this.loadMoreImages();
  }
});

// 网络请求优化
Page({
  async loadData() {
    try {
      // 使用 Promise.all 并行请求
      const [data1, data2, data3] = await Promise.all([
        wx.request({ url: '/api/data1' }),
        wx.request({ url: '/api/data2' }),
        wx.request({ url: '/api/data3' })
      ]);

      this.setData({
        data1: data1.data,
        data2: data2.data,
        data3: data3.data
      });
    } catch (error) {
      console.error('请求失败', error);
    }
  }
});
```

#### 2.5 内存优化
**检测点：**
- 是否有内存泄漏
- 是否有不必要的数据存储
- 定时器是否正确清理
- 事件监听是否正确解绑

**优化建议：**
- 及时清理不再使用的数据
- 在 onUnload 中清理定时器和监听器
- 避免存储大量数据在 page.data 中
- 使用云存储代替本地存储大文件
- 定期检查内存使用情况

**代码示例：**
```javascript
Page({
  data: {
    timer: null,
    items: []
  },

  onLoad() {
    // 创建定时器
    this.data.timer = setInterval(() => {
      this.updateData();
    }, 1000);

    // 添加事件监听
    wx.onMemoryWarning(this.handleMemoryWarning);
  },

  onUnload() {
    // 清理定时器
    if (this.data.timer) {
      clearInterval(this.data.timer);
      this.data.timer = null;
    }

    // 移除事件监听
    wx.offMemoryWarning(this.handleMemoryWarning);

    // 清理数据
    this.setData({ items: [] });
  },

  handleMemoryWarning(res) {
    console.warn('内存警告', res);
    // 清理不必要的数据
    this.cleanupData();
  },

  cleanupData() {
    // 清理逻辑
    const filteredItems = this.data.items.filter(item => item.keep);
    this.setData({ items: filteredItems });
  }
});
```

## 性能检测清单

### 启动性能检测
- [ ] 主包大小是否 < 2MB
- [ ] 是否使用了分包加载
- [ ] 图片资源是否已压缩
- [ ] app.js 初始化是否简洁
- [ ] 首屏渲染时间是否 < 2.6s (Android) / 0.9s (iOS)

### 运行时性能检测
- [ ] setData 调用频率是否合理
- [ ] WXML 节点数量是否 < 1000
- [ ] 组件嵌套层级是否 < 10 层
- [ ] 是否有内存泄漏风险
- [ ] 图片资源是否使用了懒加载
- [ ] 网络请求是否合理合并

## 性能优化工具

### 微信开发者工具性能面板
- 启动性能分析
- 渲染性能分析
- 内存使用分析
- 网络请求分析

### 真机调试
- 使用真机进行性能测试
- 关注实际用户体验
- 测试不同设备型号

## 使用示例

**场景 1：用户反馈小程序启动慢**
```
1. 检查主包大小
2. 分析 app.js 初始化逻辑
3. 检查首页 WXML 复杂度
4. 提供分包加载建议
5. 建议使用骨架屏
```

**场景 2：页面滚动卡顿**
```
1. 检查 WXML 节点数量
2. 分析 setData 调用频率
3. 检查是否有长列表未优化
4. 建议使用虚拟列表
5. 优化图片加载策略
```

**场景 3：内存占用过高**
```
1. 检查是否有内存泄漏
2. 分析数据存储策略
3. 检查定时器和监听器清理
4. 建议使用云存储
5. 优化数据清理逻辑
```

## 注意事项

1. **性能优化要循序渐进**：不要一次性进行过多优化，每次优化后进行测试验证
2. **关注实际体验**：性能指标很重要，但用户体验更重要
3. **设备差异**：不同设备的性能表现不同，要考虑低端设备
4. **持续监控**：性能优化是一个持续的过程，需要定期检查和优化
5. **权衡取舍**：有些优化可能影响代码可读性，需要权衡

## 参考资料

- [微信小程序性能优化指南](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start.html)
- [微信小程序运行时性能](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips.html)
- [微信小程序性能分析工具](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/perf_diagnostic_tool.html)
