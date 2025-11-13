# 学生财务管理系统前端

基于 Vue 3 + TypeScript + Vite 构建的现代化前端应用，提供完整的个人财务管理功能。

## 🎯 项目概述

这是一个功能完整的学生财务管理系统前端，支持收支记录管理、预算设置、财务目标跟踪、数据统计分析等核心功能。系统采用现代化的技术栈，提供流畅的用户体验和强大的数据可视化能力。

## 🚀 技术栈

- **前端框架**: Vue 3.5.22
- **构建工具**: Vite 6.0.0
- **编程语言**: TypeScript 5.6.2
- **UI组件库**: Element Plus 2.9.0
- **图表库**: ECharts 5.4.3
- **状态管理**: Pinia 2.3.0
- **路由管理**: Vue Router 4.5.0
- **HTTP客户端**: Axios 1.7.9
- **CSS预处理器**: SCSS
- **代码规范**: ESLint + Prettier

## 🛠️ 开发环境配置

### 推荐IDE设置

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (禁用Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

### TypeScript支持

项目已配置完整的TypeScript支持，包括：
- `.vue`文件类型推断
- API响应类型定义
- 组件Props类型检查
- 严格的类型安全验证

如果需要优化TypeScript性能，可启用Volar的[Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669)。

## 📦 项目结构

```
src/
├── api/              # API接口定义
├── assets/           # 静态资源
├── components/       # 可复用组件
├── composables/      # Vue组合式函数
├── layouts/          # 布局组件
├── router/           # 路由配置
├── stores/           # 状态管理
├── types/            # TypeScript类型定义
├── utils/            # 工具函数
├── views/            # 页面组件
└── main.ts           # 应用入口
```

## 🎯 核心功能

### 📊 交易管理
- 收支记录CRUD操作
- 交易分类管理
- 多条件筛选和搜索
- 批量操作支持

### 📈 数据统计
- 收支趋势分析
- 分类消费统计
- 月度财务摘要
- 自定义时间范围统计

### 💰 预算管理
- 月度预算设置
- 预算执行跟踪
- 超支提醒
- 预算完成度分析

### 🎯 财务目标
- 储蓄目标设定
- 目标进度跟踪
- 完成状态管理
- 目标达成分析

### 👥 学生管理
- 学生信息管理
- 缴费记录跟踪
- 财务统计分析
- 多维度筛选搜索

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境启动

```bash
npm run dev
```

访问 http://localhost:5173 查看应用

### 生产环境构建

```bash
npm run build
```

### 代码质量检查

```bash
npm run lint        # ESLint检查
npm run type-check  # TypeScript类型检查
```

## 🔧 环境配置

### 开发环境变量

创建 `.env.development` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_TITLE=学生财务管理系统
```

### 生产环境变量

创建 `.env.production` 文件：

```env
VITE_API_BASE_URL=https://your-domain.com/api
VITE_APP_TITLE=学生财务管理系统
```

## 📱 响应式设计

- 桌面端: 完整功能展示
- 平板端: 优化布局和交互
- 移动端: 核心功能优先展示

## 🎨 UI/UX特性

- 现代化Material Design设计
- 深色/浅色主题切换
- 平滑的页面过渡动画
- 友好的错误提示和加载状态
- 键盘快捷键支持
- 无障碍访问支持

## 🔒 安全特性

- 前端输入验证
- XSS攻击防护
- CSRF令牌验证
- 敏感信息加密存储

## 📊 性能优化

- 组件懒加载
- 图片懒加载和压缩
- API请求缓存
- 虚拟滚动（大数据列表）
- Bundle大小优化

## 🧪 测试

### 单元测试

```bash
npm run test:unit
```

### 端到端测试

```bash
npm run test:e2e
```

### 测试覆盖率

```bash
npm run test:coverage
```

## 📚 API文档

后端API文档地址：http://localhost:8000/docs/

主要API端点：
- `/api/transactions/` - 交易记录管理
- `/api/budgets/` - 预算管理
- `/api/goals/` - 财务目标管理
- `/api/students/` - 学生管理
- `/api/finance/` - 财务管理

## 🐛 常见问题

### Q: 启动时出现类型错误
A: 确保已安装所有依赖，运行 `npm install` 重新安装

### Q: API请求失败
A: 检查后端服务是否启动，确认API地址配置正确

### Q: 图表显示异常
A: 检查数据格式是否正确，确认ECharts版本兼容性

### Q: 构建失败
A: 检查TypeScript类型定义，运行 `npm run type-check` 定位问题

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 支持

如遇到问题，请：
1. 查看本文档的常见问题部分
2. 搜索已有的 Issues
3. 创建新的 Issue 描述问题

---

**系统状态**: ✅ 可正常运行  
**前端地址**: http://localhost:5173  
**后端地址**: http://localhost:8000  
**最后更新**: 2024年11月
