# 第一阶段：项目初始化与环境搭建

## 1. 开发环境准备

### 操作系统与环境检查
- 确认操作系统（Windows/Mac/Linux）及版本
- 检查Python版本（建议3.8+）
- 检查Node.js版本（建议16+）
- 确认MySQL/MariaDB安装状态

### 开发工具选择与配置
- **IDE选择**：VS Code（推荐）或PyCharm
- **VS Code扩展安装**：
  - Python扩展（Python, Pylance）
  - Vue相关扩展（Volar, Vue VSCode Snippets）
  - Django扩展
  - MySQL管理扩展
  - GitLens（版本控制）
  - Thunder Client（API测试）

## 2. 项目目录结构创建

### 根目录规划
```
student_finance_system/     # 项目根目录
├── backend/               # Django后端项目
├── frontend/              # Vue.js前端项目
├── docs/                  # 项目文档
├── scripts/               # 部署和构建脚本
└── README.md             # 项目说明文档
```

### 后端目录结构初始化
```
backend/
├── config/               # Django项目配置
│   ├── __init__.py
│   ├── settings.py       # 项目设置
│   ├── urls.py          # 根URL配置
│   └── wsgi.py          # WSGI入口
├── apps/                 # 自定义应用目录
│   ├── users/           # 用户管理应用
│   ├── finance/         # 财务核心应用
│   └── common/          # 通用功能应用
├── static/              # 静态文件
├── media/               # 媒体文件
├── requirements/        # 依赖管理
│   ├── base.txt        # 基础依赖
│   ├── development.txt # 开发环境依赖
│   └── production.txt  # 生产环境依赖
├── manage.py           # Django管理脚本
└── requirements.txt    # 依赖清单（链接到requirements/base.txt）
```

### 前端目录结构初始化
```
frontend/
├── public/             # 静态公共文件
│   ├── index.html     # HTML模板
│   └── favicon.ico    # 网站图标
├── src/               # 源代码目录
│   ├── assets/        # 静态资源（图片、样式）
│   ├── components/    # Vue组件
│   │   ├── common/    # 通用组件
│   │   ├── finance/   # 财务相关组件
│   │   └── layout/    # 布局组件
│   ├── views/         # 页面组件
│   ├── router/        # 路由配置
│   ├── store/         # 状态管理（Vuex/Pinia）
│   ├── api/           # API接口封装
│   ├── utils/         # 工具函数
│   ├── App.vue        # 根组件
│   └── main.js        # 应用入口
├── package.json       # 项目配置和依赖
├── vite.config.js     # Vite构建配置
└── .env               # 环境变量配置
```

## 3. 开发环境配置

### Python虚拟环境配置
- 创建独立的Python虚拟环境
- 配置虚拟环境激活脚本
- 设置IDE使用虚拟环境解释器

### Node.js环境配置
- 初始化npm/yarn项目
- 配置包管理器镜像源（如需要）
- 设置前端开发服务器方法（如使用Vite）

### 数据库环境配置
- 创建开发用MySQL数据库
- 配置数据库连接参数
- 设置数据库字符集（utf8mb4）

## 4. 依赖管理文件创建

### 后端依赖管理
**requirements/base.txt** 包含：
- Django及Django REST Framework
- 数据库驱动（mysqlclient或PyMySQL）
- 认证相关（djangorestframework-simplejwt）
- 跨域支持（django-cors-headers）
- 其他工具库

**requirements/development.txt** 包含：
- 开发工具（调试器、代码检查工具）
- 测试框架
- 文档生成工具

### 前端依赖管理
**package.json** 配置：
- Vue 3及相关生态
- 路由管理（Vue Router）
- 状态管理（Pinia）
- UI组件库（Element Plus）
- 图表库（ECharts/vue-echarts）
- HTTP客户端（Axios）
- 构建工具（Vite）
- 开发工具（ESLint, Prettier）

## 5. 配置文件创建

### 后端配置文件
**config/settings.py** 分段配置：
- 基础设置（DEBUG, SECRET_KEY）
- 应用注册
- 数据库配置
- 静态文件配置
- 认证配置
- REST Framework配置
- 跨域配置

**环境变量管理**：
- 创建.env.example模板
- 开发环境.env文件
- 敏感信息隔离

### 前端配置文件
**vite.config.js** 配置：
- 开发服务器设置
- 代理配置（解决跨域）
- 构建选项
- 插件配置

**环境变量文件**：
- .env（开发环境）
- .env.production（生产环境）

## 6. 基础脚本创建

### 后端管理脚本
- 数据库迁移脚本
- 超级用户创建脚本
- 测试数据生成脚本

### 前端构建脚本
- 开发环境启动脚本
- 生产环境构建脚本
- 代码检查脚本

## 7. 版本控制初始化

### Git仓库初始化
- 创建.gitignore文件
- 初始化Git仓库
- 创建初始commit

**.gitignore配置**：
- Python虚拟环境目录
- Node.js依赖目录
- 数据库文件
- 日志文件
- 环境配置文件
- 编译输出目录

## 8. 文档创建

### 项目文档
**README.md** 包含：
- 项目简介
- 环境要求
- 安装步骤
- 运行说明
- 项目结构说明

### 开发文档
- 开发环境搭建指南
- 代码规范说明
- API接口文档模板
- 部署文档模板

## 9. 验证环境配置

### 环境验证步骤
1. 验证Python虚拟环境激活
2. 验证Django项目可启动
3. 验证Vue开发服务器可启动
4. 验证数据库连接正常
5. 验证前后端基础通信

### 成功标准
- 后端：`python manage.py runserver` 成功启动
- 前端：`npm run dev` 成功启动
- 数据库：能够成功连接和创建表
- 基础请求：前后端能够成功通信

这个阶段完成后，您将拥有一个结构清晰、配置完整的开发环境，为后续的功能开发奠定坚实基础。整个过程预计需要1-2天时间，具体取决于您的熟悉程度和环境条件。