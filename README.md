# 学生管理系统

基于 Django + Vue.js 的全栈学生管理系统，支持学生信息管理、费用管理、缴费记录等功能。

## 技术栈

### 后端
- **Django 4.2.7** - Web框架
- **Django REST Framework** - API框架
- **SQLite** - 数据库（开发环境）
- **Python 3.11+**

### 前端
- **Vue.js 3** - 前端框架
- **TypeScript** - 类型安全
- **Element Plus** - UI组件库
- **Vite** - 构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理

## 功能特性

- 👥 学生信息管理（增删改查、搜索、过滤、分页）
- 💰 费用类别管理
- 💳 缴费记录管理
- 📊 数据统计和报表
- 🔐 管理后台（Django Admin）
- 📱 响应式设计

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 20.19.0+
- npm 或 yarn

### 后端设置

```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 前端设置

```bash
cd frontend
npm install
npm run dev
```

### 访问系统

- 前端应用: http://localhost:5173
- 后端API: http://localhost:8000/api/
- 管理后台: http://localhost:8000/admin

## API端点

### 学生管理
- `GET /api/students/` - 学生列表
- `POST /api/students/` - 创建学生
- `GET /api/students/{id}/` - 学生详情
- `PUT /api/students/{id}/` - 更新学生
- `DELETE /api/students/{id}/` - 删除学生
- `GET /api/students/statistics/` - 学生统计

### 财务管理
- `GET /api/finance/categories/` - 费用类别
- `GET /api/finance/records/` - 缴费记录
- `GET /api/finance/payments/` - 支付记录
- `GET /api/finance/records/statistics/` - 缴费统计

## 开发指南

### 代码规范
- 后端遵循 PEP 8 规范
- 前端使用 ESLint 和 TypeScript 进行代码检查
- 提交前运行代码检查和测试

### 项目结构

```
student-system/
├── backend/          # Django后端
│   ├── config/     # 项目配置
│   ├── students/   # 学生应用
│   ├── finance/    # 财务应用
│   └── requirements.txt
├── frontend/       # Vue.js前端
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── stores/      # 状态管理
│   │   └── api/         # API接口
│   └── package.json
└── docs/           # 文档
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。