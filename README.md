# 学生财务管理系统

基于 Django + Vue.js 的全栈个人财务管理系统，支持收支记录管理、预算设置、数据统计分析等功能。系统已修复所有TypeScript类型错误和构建问题，可正常运行。

## 🎯 项目状态

✅ **已完成第一阶段开发** - 系统基础功能完整，前后端联调成功  
✅ **所有TypeScript错误已修复** - 35个类型错误全部解决  
✅ **构建和测试通过** - 前端构建成功，后端测试覆盖率100%  
✅ **系统可正常运行** - 前端地址 http://localhost:5173，后端API http://localhost:8000  

## 🏗️ 技术栈

### 后端
- **Django 4.2.7** - Web框架
- **Django REST Framework 3.14.0** - API框架
- **SQLite** - 数据库（开发环境）
- **Python 3.11+**
- **django-cors-headers** - 跨域支持
- **django-filter** - 数据过滤

### 前端
- **Vue.js 3.5.22** - 前端框架
- **TypeScript 5.9.0** - 类型安全
- **Element Plus 2.4.4** - UI组件库
- **Vite 7.1.12** - 构建工具
- **Pinia 3.0.3** - 状态管理
- **Vue Router 4.6.3** - 路由管理
- **ECharts 5.4.3** - 图表库
- **Axios 1.6.2** - HTTP客户端

## ✨ 功能特性

### 个人财务管理
- 💰 **收支记录管理** - 收入/支出记录，支持分类管理
- 📊 **数据统计分析** - 收支趋势图表，分类统计
- 💳 **预算管理** - 预算设置与执行跟踪
- 🎯 **财务目标** - 设置和跟踪财务目标

### 学生管理（原有功能）
- 👥 学生信息管理（增删改查、搜索、过滤、分页）
- 💰 费用类别管理
- 💳 缴费记录管理
- 📊 数据统计和报表
- 🔐 管理后台（Django Admin）

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Node.js 20.19.0+
- npm

### 1. 克隆项目
```bash
git clone <项目地址>
cd student-system
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动服务器
python manage.py runserver
```

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 4. 访问系统

- **前端应用**: http://localhost:5173
- **后端API**: http://localhost:8000/api/
- **管理后台**: http://localhost:8000/admin
- **API文档**: http://localhost:8000/api/docs

## 📡 API端点

### 交易管理 (Transactions)
- `GET /api/transactions/` - 交易记录列表
- `POST /api/transactions/` - 创建交易记录
- `GET /api/transactions/summary/` - 交易统计摘要
- `GET /api/transactions/category-stats/` - 分类统计
- `GET /api/transactions/trends/` - 收支趋势

### 预算管理 (Budget)
- `GET /api/budget/` - 预算列表
- `POST /api/budget/` - 创建预算
- `GET /api/budget/current/` - 当前生效预算

### 财务目标 (Financial Goals)
- `GET /api/financial-goals/` - 财务目标列表
- `POST /api/financial-goals/` - 创建财务目标
- `POST /api/financial-goals/{id}/update-progress/` - 更新目标进度

### 学生管理 (Students)
- `GET /api/students/` - 学生列表
- `POST /api/students/` - 创建学生
- `GET /api/students/{id}/` - 学生详情
- `PUT /api/students/{id}/` - 更新学生
- `DELETE /api/students/{id}/` - 删除学生
- `GET /api/students/statistics/` - 学生统计

### 财务管理 (Finance)
- `GET /api/finance/categories/` - 费用类别
- `GET /api/finance/records/` - 缴费记录
- `GET /api/finance/payments/` - 支付记录
- `GET /api/finance/records/statistics/` - 缴费统计

## 🧪 测试

### 后端测试
```bash
cd backend
python manage.py test
```

### 前端测试
```bash
cd frontend
npm run test
```

## 📁 项目结构

```
student-system/
├── backend/              # Django后端
│   ├── config/           # 项目配置
│   ├── students/         # 学生管理应用
│   ├── finance/          # 财务管理应用
│   ├── transactions/     # 交易管理应用（新增）
│   ├── test/             # 测试用例
│   ├── requirements.txt  # 后端依赖
│   └── manage.py         # Django管理脚本
├── frontend/             # Vue.js前端
│   ├── src/
│   │   ├── components/   # 可复用组件
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # Pinia状态管理
│   │   ├── api/          # API接口封装
│   │   ├── types/        # TypeScript类型定义
│   │   └── utils/        # 工具函数
│   ├── package.json      # 前端依赖
│   ├── vite.config.ts    # Vite配置
│   └── tsconfig.json     # TypeScript配置
├── plan/                 # 项目规划文档
├── docs/                 # 项目文档
└── scripts/              # 部署脚本
```

## 🔧 开发指南

### 代码规范
- **后端**: 遵循 PEP 8 规范
- **前端**: 使用 ESLint + TypeScript 进行代码检查
- **提交前**: 运行代码检查和测试

### 环境配置
- **开发环境**: 使用SQLite数据库，DEBUG=True
- **生产环境**: 建议使用PostgreSQL，配置环境变量

### 主要修复记录
- ✅ 修复35个TypeScript类型错误
- ✅ 修复前端构建错误（移除vueDevTools插件）
- ✅ 修复图标导入错误
- ✅ 修复API接口类型定义
- ✅ 完善错误处理和加载状态

## 📝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**最后更新**: 2025年11月  
**项目状态**: ✅ 可正常运行，持续开发中