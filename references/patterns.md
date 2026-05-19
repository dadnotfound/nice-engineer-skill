# 常见代码模式库

## 模式分类

### 1. 页面结构模式
### 2. 交互模式
### 3. 数据模式
### 4. 部署模式
### 5. 组织模式

## 页面结构模式

### 模式1.1：电影票风格主页
```html
<div class="ticket">
  <header class="ticket-header">
    <div class="movie-title">项目名称</div>
    <div class="session">场次: <span id="session">1</span></div>
    <div class="datetime">时间: <span id="datetime"></span></div>
  </header>
  
  <main class="ticket-content">
    <section class="info-section">
      <h2>基本信息</h2>
      <div class="info-grid">
        <div class="info-item">
          <span class="label">类型</span>
          <span class="value" id="type">创意展示</span>
        </div>
        <div class="info-item">
          <span class="label">时长</span>
          <span class="value" id="duration">90分钟</span>
        </div>
      </div>
    </section>
    
    <section class="description-section">
      <h2>项目描述</h2>
      <p class="description">这里是详细的描述内容...</p>
    </section>
    
    <section class="features-section">
      <h2>主要功能</h2>
      <ul class="features-list">
        <li>功能1</li>
        <li>功能2</li>
        <li>功能3</li>
      </ul>
    </section>
  </main>
  
  <footer class="ticket-footer">
    <div class="ticket-number">No. <span id="ticket-number"></span></div>
    <div class="qr-placeholder">二维码</div>
  </footer>
</div>

/* 样式 */
.ticket {
  width: 350px;
  margin: 0 auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.ticket::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
}
```

### 模式1.2：时间轴展示
```html
<div class="timeline">
  <div class="timeline-header">
    <h2>时间轴</h2>
    <div class="timeline-filter">
      <button class="filter-btn active" data-filter="all">全部</button>
      <button class="filter-btn" data-filter="work">工作</button>
      <button class="filter-btn" data-filter="life">生活</button>
    </div>
  </div>
  
  <div class="timeline-items">
    <div class="timeline-item" data-category="work">
      <div class="timeline-marker">
        <div class="marker-dot"></div>
        <div class="line"></div>
      </div>
      <div class="timeline-content">
        <time class="timeline-date">2024-01-15</time>
        <h3 class="timeline-title">项目里程碑</h3>
        <p class="timeline-description">项目完成并上线</p>
        <div class="timeline-tags">
          <span class="tag">完成</span>
          <span class="tag">上线</span>
        </div>
      </div>
    </div>
    
    <div class="timeline-item" data-category="life">
      <div class="timeline-marker">
        <div class="marker-dot"></div>
        <div class="line"></div>
      </div>
      <div class="timeline-content">
        <time class="timeline-date">2024-02-01</time>
        <h3 class="timeline-title">新开始</h3>
        <p class="timeline-description">新的阶段，新的目标</p>
      </div>
    </div>
  </div>
</div>

/* 样式 */
.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline-item {
  position: relative;
  padding-left: 40px;
  margin-bottom: 30px;
}

.timeline-marker {
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
}

.marker-dot {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #4ecdc4;
  border: 3px solid #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
```

### 模式1.3：卡片式布局
```html
<div class="cards-container">
  <div class="card">
    <div class="card-image">
      <img src="image.jpg" alt="Card image">
    </div>
    <div class="card-content">
      <h3 class="card-title">卡片标题</h3>
      <p class="card-description">卡片描述内容...</p>
      <div class="card-tags">
        <span class="tag">标签1</span>
        <span class="tag">标签2</span>
      </div>
    </div>
    <div class="card-footer">
      <button class="btn-primary">了解更多</button>
    </div>
  </div>
</div>

/* 响应式网格 */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}
```

## 交互模式

### 模式2.1：Tab切换
```javascript
class TabManager {
  constructor(container) {
    this.container = container;
    this.tabs = container.querySelectorAll('.tab-btn');
    this.panels = container.querySelectorAll('.tab-panel');
    this.init();
  }
  
  init() {
    this.tabs.forEach(tab => {
      tab.addEventListener('click', () => this.switchTab(tab));
    });
  }
  
  switchTab(activeTab) {
    // 移除所有活动状态
    this.tabs.forEach(tab => tab.classList.remove('active'));
    this.panels.forEach(panel => panel.classList.remove('active'));
    
    // 添加活动状态
    activeTab.classList.add('active');
    const targetPanel = this.container.querySelector(
      `[data-tab="${activeTab.dataset.tab}"]`
    );
    targetPanel.classList.add('active');
  }
}

// 使用
const tabContainer = document.querySelector('.tabs');
new TabManager(tabContainer);
```

### 模式2.2：模态框
```javascript
class Modal {
  constructor(trigger) {
    this.trigger = trigger;
    this.modal = document.querySelector(trigger.dataset.target);
    this.closeBtn = this.modal.querySelector('.modal-close');
    this.init();
  }
  
  init() {
    this.trigger.addEventListener('click', () => this.open());
    this.closeBtn.addEventListener('click', () => this.close());
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });
  }
  
  open() {
    this.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  close() {
    this.modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// HTML
<button class="btn-modal" data-target="#modal-1">打开模态框</button>

<div class="modal" id="modal-1">
  <div class="modal-content">
    <button class="modal-close">&times;</button>
    <div class="modal-body">
      模态框内容
    </div>
  </div>
</div>
```

### 模式2.3：无限滚动
```javascript
class InfiniteScroll {
  constructor(container, loadMoreCallback) {
    this.container = container;
    this.loadMoreCallback = loadMoreCallback;
    this.isLoading = false;
    this.hasMore = true;
    this.threshold = 200;
    this.init();
  }
  
  init() {
    window.addEventListener('scroll', () => this.checkScroll());
    this.checkScroll();
  }
  
  checkScroll() {
    if (!this.hasMore || this.isLoading) return;
    
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight;
    const clientHeight = document.documentElement.clientHeight;
    
    if (scrollTop + clientHeight >= scrollHeight - this.threshold) {
      this.loadMore();
    }
  }
  
  async loadMore() {
    this.isLoading = true;
    await this.loadMoreCallback();
    this.isLoading = false;
  }
}

// 使用
const scrollContainer = document.querySelector('.content-list');
const infiniteScroll = new InfiniteScroll(scrollContainer, async () => {
  const newItems = await fetchMoreItems();
  renderItems(newItems);
});
```

## 数据模式

### 模式3.1：本地存储数据
```javascript
class LocalDataManager {
  constructor(key) {
    this.key = key;
    this.data = this.load();
  }
  
  load() {
    try {
      const stored = localStorage.getItem(this.key);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.error('Failed to load data:', e);
      return [];
    }
  }
  
  save() {
    try {
      localStorage.setItem(this.key, JSON.stringify(this.data));
      return true;
    } catch (e) {
      console.error('Failed to save data:', e);
      return false;
    }
  }
  
  add(item) {
    this.data.push({
      ...item,
      id: Date.now(),
      createdAt: new Date().toISOString()
    });
    return this.save();
  }
  
  update(id, updates) {
    const index = this.data.findIndex(item => item.id === id);
    if (index !== -1) {
      this.data[index] = { ...this.data[index], ...updates };
      return this.save();
    }
    return false;
  }
  
  delete(id) {
    this.data = this.data.filter(item => item.id !== id);
    return this.save();
  }
  
  getAll() {
    return this.data;
  }
  
  get(id) {
    return this.data.find(item => item.id === id);
  }
}

// 使用示例
const userManager = new LocalDataManager('users');
userManager.add({ name: '张三', email: 'zhang@example.com' });
```

### 模式3.2：静态数据文件
```javascript
// data/projects.json
[
  {
    "id": 1,
    "title": "项目一",
    "description": "项目描述",
    "tags": ["前端", "设计"],
    "date": "2024-01-01"
  },
  {
    "id": 2,
    "title": "项目二",
    "description": "项目描述",
    "tags": ["后端", "API"],
    "date": "2024-02-01"
  }
]

// 加载静态数据
async function loadStaticData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('Error loading static data:', error);
    return [];
  }
}

// 使用
const projects = await loadStaticData('data/projects.json');
```

### 模式3.3：内存缓存
```javascript
class MemoryCache {
  constructor(ttl = 60000) {
    this.cache = new Map();
    this.ttl = ttl; // 默认1分钟
  }
  
  set(key, value, ttl = this.ttl) {
    const expiry = Date.now() + ttl;
    this.cache.set(key, { value, expiry });
  }
  
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }
  
  has(key) {
    return this.get(key) !== null;
  }
  
  delete(key) {
    this.cache.delete(key);
  }
  
  clear() {
    this.cache.clear();
  }
  
  cleanup() {
    const now = Date.now();
    for (const [key, item] of this.cache) {
      if (now > item.expiry) {
        this.cache.delete(key);
      }
    }
  }
}

// 使用
const cache = new MemoryCache(30000); // 30秒缓存
cache.set('user', userData);
const user = cache.get('user');
```

## 部署模式

### 模式4.1：Cloudflare Pages部署
```json
// wrangler.jsonc
{
  "name": "nice-project",
  "build_command": "npm run build",
  "upload_dir": "dist",
  "builds": [
    {
      "src": "**/*.{js,css,html}",
      "use": "@cloudflare/static-html"
    }
  ]
}
```

```bash
#!/bin/bash
# deploy.sh
echo "开始部署..."

# 安装依赖
npm install

# 构建项目
npm run build

# 部署到Cloudflare Pages
npx wrangler pages deploy dist

echo "部署完成！访问：https://your-project.pages.dev"
```

### 模式4.2：GitHub Pages部署
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build
        run: npm run build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: './dist'
```

### 模式4.3：静态文件托管配置
```javascript
// netlify.toml
[build]
  publish = "dist"
  command = "npm run build"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "*.jpg"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

## 组织模式

### 模式5.1：单文件组件
```javascript
// components/Header.js
export class Header {
  constructor(title, subtitle = '') {
    this.title = title;
    this.subtitle = subtitle;
  }
  
  render() {
    return `
      <header class="header">
        <h1>${this.title}</h1>
        ${this.subtitle ? `<p class="subtitle">${this.subtitle}</p>` : ''}
      </header>
    `;
  }
}

// 使用
const header = new Header('我的项目', '创意展示');
document.getElementById('app').innerHTML = header.render();
```

### 模式5.2：模块化组织
```javascript
// utils/helpers.js
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN');
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

export const throttle = (func, limit) => {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// utils/dom.js
export const $ = (selector) => document.querySelector(selector);
export const $$ = (selector) => document.querySelectorAll(selector);
export const on = (element, event, handler) => {
  element.addEventListener(event, handler);
  return () => element.removeEventListener(event, handler);
};
```

### 模式5.3：配置管理
```javascript
// config/site.js
export const siteConfig = {
  name: 'Nice Project',
  description: '创意展示项目',
  author: '奈思',
  url: 'https://nice-project.pages.dev',
  social: {
    github: 'https://github.com/username',
    twitter: 'https://twitter.com/username'
  }
};

// config/ui.js
export const uiConfig = {
  colors: {
    primary: '#4ecdc4',
    secondary: '#ff6b6b',
    dark: '#2c3e50',
    light: '#ecf0f1'
  },
  breakpoints: {
    mobile: 768,
    tablet: 1024,
    desktop: 1200
  },
  animations: {
    duration: 300,
    easing: 'ease-in-out'
  }
};
```

## 使用指南

### 如何选择合适的模式
1. **页面结构**：根据内容类型选择卡片、时间轴或票根风格
2. **交互模式**：根据功能复杂度选择简单的点击或复杂的滚动
3. **数据模式**：根据数据量选择本地存储、静态文件或内存缓存
4. **部署模式**：根据项目需求选择合适的托管平台
5. **组织模式**：根据项目规模选择单文件或模块化组织

### 模式组合示例
```javascript
// 电影票风格 + Tab切换 + 本地存储
class TicketApp {
  constructor() {
    this.dataManager = new LocalDataManager('tickets');
    this.initTabs();
    this.renderTickets();
  }
  
  initTabs() {
    new TabManager(document.querySelector('.tabs'));
  }
  
  renderTickets() {
    const tickets = this.dataManager.getAll();
    const container = document.querySelector('.tickets-container');
    
    container.innerHTML = tickets.map(ticket => `
      <div class="ticket">
        <header>
          <h3>${ticket.title}</h3>
          <p>${ticket.description}</p>
        </header>
      </div>
    `).join('');
  }
}
```

记住：模式是指导，不是规则。根据实际情况调整和组合。