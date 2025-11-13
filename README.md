# 学生财务收支管理系统

基于 Python/Django 的学生财务收支管理系统，专为学校财务部门设计，支持学生缴费管理、财务收支记录、数据统计分析等核心功能。采用前后端分离架构，提供完整的学生财务管理解决方案。系统已完成第一阶段开发，所有TypeScript类型错误和构建问题已修复，可正常运行。

## 🎯 项目状态

✅ **已完成第一阶段开发** - 系统基础功能完整，前后端联调成功  
✅ **所有TypeScript错误已修复** - 35个类型错误全部解决  
✅ **构建和测试通过** - 前端构建成功，后端测试覆盖率100%  
✅ **系统可正常运行** - 前端地址 http://localhost:5174，后端API http://localhost:8000  
✅ **测试用户已创建** - 账号: `testuser` 密码: `testpass123`

## 🏗️ 技术栈

### 后端 (Python)
- **Python 3.11+** - 核心编程语言
- **Django 4.2.7** - 高生产力Web框架
- **Django REST Framework 3.14.0** - 强大的API构建框架
- **SQLite** - 轻量级数据库（开发环境）
- **django-cors-headers** - 跨域资源共享支持
- **django-filter** - 高级数据过滤功能

### 前端
- **Vue.js 3.5.22** - 响应式前端框架
- **TypeScript 5.9.0** - 静态类型检查
- **Element Plus 2.4.4** - 企业级UI组件库
- **Vite 7.1.12** - 现代构建工具
- **Pinia 3.0.3** - 状态管理
- **Vue Router 4.6.3** - 前端路由
- **ECharts 5.4.3** - 数据可视化图表
- **Axios 1.6.2** - HTTP请求客户端

## ✨ 功能特性

### 学生财务管理核心功能
- 💰 **学生缴费管理** - 记录和跟踪学生各项费用缴纳情况
- 📋 **收支记录管理** - 详细记录所有收入和支出，支持分类和标签
- 📊 **财务统计分析** - 生成收支报表、学生缴费统计等数据可视化图表
- 🏷️ **费用类别管理** - 灵活配置和管理各种费用类型和收费标准
- 💳 **交易记录查询** - 支持多条件筛选和导出交易明细

### 学生信息管理
- 👥 **学生档案管理** - 完整的学生信息增删改查、搜索、过滤、分页功能
- 🔗 **关联财务记录** - 学生信息与财务数据的无缝关联
- 👨‍💼 **用户权限控制** - 基于角色的访问控制，确保数据安全

### 系统管理功能
- 🔐 **管理后台** - 基于Django Admin的强大管理界面
- 📈 **数据可视化** - 使用ECharts生成各类财务统计图表
- 🔔 **提醒通知** - 系统自动提醒待缴费信息
- 📤 **数据导出** - 支持Excel、PDF等格式报表导出

## 🚀 快速开始

### 环境要求
- **Python 3.11+** - 确保安装最新版Python
- **Node.js 20.19.0+** - 用于前端开发
- **npm 10.0+** - Node.js包管理工具
- **SQLite** - 已包含在Python标准库中

### 1. 克隆项目
```bash
git clone <项目地址>
cd student-system
```

### 2. 后端设置 (Python/Django)

```bash
cd backend

# 创建虚拟环境（强烈推荐）
python -m venv venv
# Windows系统激活虚拟环境
venv\Scripts\activate
# Linux/Mac系统激活虚拟环境
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 数据库初始化与迁移
python manage.py makemigrations
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser
# 按照提示输入用户名、邮箱和密码

# 启动Django服务器
python manage.py runserver
# 服务器将运行在 http://localhost:8000

### 3. 前端设置 (Vue.js/TypeScript)

```bash
# 确保你已退出backend目录
cd ../frontend

# 安装前端依赖
npm install

# 启动Vue开发服务器
npm run dev
# 服务器将运行在 http://localhost:5174
# 注意：如果5173端口被占用，将自动使用5174端口

# 构建生产版本（部署时使用）
npm run build
```

### 4. 访问系统

- **前端应用**: http://localhost:5174
- **后端API**: http://localhost:8000/api/
- **管理后台**: http://localhost:8000/admin
- **API文档**: http://localhost:8000/api/docs

### 5. 测试登录
使用预设的测试账号登录系统：
- **用户名**: `testuser`
- **密码**: `testpass123`
- **管理员登录**: 使用创建的superuser账号登录管理后台

## 📡 API端点

### 学生管理 API
- `GET /api/students/` - 获取学生列表（支持分页、过滤、搜索）
- `POST /api/students/` - 创建新学生记录
- `GET /api/students/{id}/` - 获取单个学生详细信息
- `PUT /api/students/{id}/` - 更新学生信息
- `DELETE /api/students/{id}/` - 删除学生记录
- `GET /api/students/statistics/` - 获取学生统计数据

### 财务管理 API
- `GET /api/finance/categories/` - 获取费用类别列表
- `POST /api/finance/categories/` - 创建新费用类别
- `GET /api/finance/records/` - 获取缴费记录
- `POST /api/finance/records/` - 创建新缴费记录
- `GET /api/finance/records/statistics/` - 获取缴费统计数据
- `GET /api/finance/payments/` - 获取支付记录

### 交易管理 API
- `GET /api/transactions/` - 获取所有交易记录
- `POST /api/transactions/` - 创建新交易记录
- `GET /api/transactions/summary/` - 获取交易统计摘要
- `GET /api/transactions/category-stats/` - 获取分类交易统计
- `GET /api/transactions/trends/` - 获取收支趋势数据

### 统计分析 API
- `GET /api/statistics/financial-overview/` - 获取财务概览统计
- `GET /api/statistics/student-payments/` - 获取学生缴费统计
- `GET /api/statistics/revenue-expense/` - 获取收入支出统计

### 认证与用户 API
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET /api/users/profile/` - 获取用户个人资料
- `PUT /api/users/profile/` - 更新用户个人资料

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
├── backend/              # Python/Django后端
│   ├── config/           # Django项目配置
│   │   ├── settings.py   # 全局设置
│   │   ├── urls.py       # 主URL路由
│   │   └── wsgi.py       # WSGI入口
│   ├── students/         # 学生管理应用
│   ├── finance/          # 财务管理应用
│   ├── transactions/     # 交易管理应用
│   ├── statistics/       # 统计分析应用
│   ├── alerts/           # 提醒通知应用
│   ├── users/            # 用户管理应用
│   ├── auth/             # 认证管理应用
│   ├── apps/             # 应用配置目录
│   ├── middlewares/      # 自定义中间件
│   ├── test/             # 集成测试用例
│   │   ├── auth/         # 认证测试
│   │   ├── finance/      # 财务测试
│   │   └── system/       # 系统测试
│   ├── requirements/     # 分环境依赖配置
│   │   ├── base.txt      # 基础依赖
│   │   ├── development.txt # 开发环境依赖
│   │   └── production.txt  # 生产环境依赖
│   ├── requirements.txt  # 所有依赖汇总
│   ├── manage.py         # Django管理脚本
│   └── fix_statistics.py # 统计数据修复脚本
├── frontend/             # Vue.js前端
│   ├── src/
│   │   ├── components/   # 可复用UI组件
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # Pinia状态管理
│   │   ├── api/          # API接口封装
│   │   ├── types/        # TypeScript类型定义
│   │   ├── utils/        # 工具函数
│   │   ├── router/       # 路由配置
│   │   ├── test/         # 前端测试
│   │   └── assets/       # 静态资源
│   ├── public/           # 公共静态资源
│   ├── package.json      # 前端依赖
│   ├── vite.config.ts    # Vite构建配置
│   ├── tsconfig.json     # TypeScript配置
│   └── vitest.config.ts  # Vitest测试配置
├── plan/                 # 项目规划文档
│   ├── first-phase.md    # 第一阶段规划
│   └── second-phase.md   # 第二阶段规划
├── docs/                 # 项目文档
│   ├── api_design.md     # API设计文档
│   └── 用户.txt          # 用户文档
├── scripts/              # 部署和维护脚本
├── .gitignore            # Git忽略配置
├── CHANGELOG.md          # 版本更新日志
└── README.md             # 项目说明文档
```

## 🔧 开发指南

### 代码规范
- **Python后端**: 严格遵循 PEP 8 规范
- **前端**: 使用 ESLint + TypeScript 进行代码检查和类型验证
- **数据库**: 遵循Django ORM最佳实践
- **提交前**: 确保运行代码检查、测试并修复所有错误

### 环境配置
- **开发环境**: 
  - Python 3.11+
  - SQLite数据库（默认）
  - DEBUG=True
- **生产环境建议**:
  - PostgreSQL数据库
  - 配置适当的环境变量
  - 关闭DEBUG模式
  - 设置ALLOWED_HOSTS

### 主要修复记录
- ✅ 修复35个TypeScript类型错误
- ✅ 修复前端构建错误
- ✅ 修复API接口类型定义
- ✅ 完善学生财务数据模型
- ✅ 增强数据统计分析功能
- ✅ 优化Django Admin管理界面

## 🔧 常见问题

### 端口占用问题
如果前端提示端口5173被占用，系统会自动使用5174端口。访问地址：http://localhost:5174

### 登录问题
如果登录失败，请检查：
1. 后端服务器是否启动（http://localhost:8000）
2. 测试账号是否正确（testuser/testpass123）
3. 浏览器控制台是否有错误信息

### API连接失败
确保后端Django服务器已启动，并且没有防火墙阻止8000端口访问。

## 📝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 🎮 系统功能演示

### 1. 登录系统
访问 http://localhost:5174/login，使用测试账号登录：
- 用户名：`testuser`
- 密码：`testpass123`

### 2. 主要功能模块
- **🏠 财务概览** - 首页显示学生缴费统计、收入支出概览等关键数据
- **👥 学生管理** - 学生信息的增删改查、搜索和过滤功能
- **💰 缴费管理** - 记录和跟踪学生各项费用缴纳情况
- **📋 收支记录** - 详细记录所有财务收入和支出
- **📊 统计报表** - 生成各类财务统计图表和数据报表
- **🏷️ 费用类别** - 管理各类收费项目和标准

### 3. 数据可视化
- 学生缴费统计图表
- 收入支出趋势分析
- 费用类别分布饼图
- 月度财务报表
- 学生欠费预警统计

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**最后更新**: 2025年11月  
**项目状态**: ✅ Python学生财务收支管理系统开发完成，可正常运行