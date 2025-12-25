# Vue + C# UI 自动化测试项目

本项目展示了如何构建一个完整的Vue前端 + C#后端架构，并配置GitHub Actions实现UI自动化测试的完整流程。

## 项目结构

```
vue-csharp-ui-auto/          # 根仓库
├── Frontend/                # Vue 前端项目（Vue3）
│   ├── src/
│   │   ├── components/      # 测试目标组件（如登录、表单）
│   │   ├── views/           # 测试目标页面（如首页、用户页）
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js       # Vite配置文件
├── Backend/                 # C# 后端项目（ASP.NET Core）
│   ├── Controllers/         # 接口控制器（如 UserController）
│   ├── Models/              # 数据模型
│   ├── Services/            # 业务服务
│   ├── Program.cs
│   └── appsettings.json
├── UiAutoTest/              # UI 自动化测试脚本（Python+Selenium）
│   ├── test_vue_page.py     # 测试 Vue 前端页面的脚本
│   └── requirements.txt     # 测试依赖
└── .github/
    └── workflows/
        └── ui-auto-test.yml # GitHub Actions 配置文件
```

## 核心功能

### 前端 (Vue3)
- 登录页面：用户登录验证
- 首页：展示用户信息
- 表单页面：数据提交功能
- 使用Axios与后端API通信
- 包含测试专用标识(data-testid)便于自动化测试

### 后端 (C# ASP.NET Core)
- 健康检查API：`/api/health`
- 认证API：`/api/auth/login`
- 数据提交API：`/api/data/submit`
- 使用内存数据库进行测试
- 支持跨域请求(CORS)

### UI自动化测试
- Vue登录页面 + C#接口联动测试
- Vue表单提交功能测试
- 页面导航功能测试
- 生成HTML测试报告

## GitHub Actions 工作流

工作流配置实现了以下步骤：
1. 拉取代码
2. 配置C#运行环境
3. 启动C#后端服务
4. 配置Node.js环境
5. 启动Vue前端服务
6. 安装Chrome浏览器和驱动
7. 配置Python环境
8. 安装测试依赖
9. 运行UI自动化测试
10. 上传测试报告和日志

## 本地开发

### 前端运行
```bash
cd Frontend
npm install
npm run serve
```

### 后端运行
```bash
cd Backend
dotnet run
```

### 测试运行
```bash
cd UiAutoTest
pip install -r requirements.txt
python test_vue_page.py
```

## 关键配置说明

1. **跨域配置**：后端已配置允许Vue前端访问API
2. **测试数据**：预设了测试用户`test_user`/`test_pass123`
3. **端口配置**：前端8080，后端5000
4. **测试标识**：Vue组件包含data-testid便于定位元素

## 部署到GitHub

1. 初始化Git仓库
```bash
git init
git add .
git commit -m "初始化Vue+C#项目，添加UI自动化测试脚本和GitHub Actions配置"
git remote add origin https://github.com/你的用户名/vue-csharp-ui-auto.git
git push -u origin main
```

2. 推送后，GitHub Actions会自动运行UI自动化测试

## 避坑指南

1. 前后端服务启动地址：C#后端需绑定0.0.0.0:5000，Vue前端需通过--host 0.0.0.0启动
2. 服务启动等待时间：Vue启动较慢，需设置足够等待时间
3. Vue元素定位：优先使用id/data-testid，避免用class
4. C#测试环境配置：使用内存数据库，避免污染生产数据