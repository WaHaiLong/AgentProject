# 部署说明

## 自动部署到服务器

本项目配置了自动部署到服务器的GitHub Actions工作流，使用自托管运行器。

### 部署流程

1. 当您在代码库中创建一个版本标签（格式为 `v*.*.*`）时，会自动触发部署流程
2. 工作流文件：`.github/workflows/deploy.yml`
3. 部署目标：自托管服务器（使用 `self-hosted` 运行器）

### 部署架构

- **后端**：C# ASP.NET Core 应用，部署到 `/opt/vue-csharp-app/backend`
- **前端**：Vue.js SPA，部署到 `/var/www/vue-csharp-frontend`
- **反向代理**：使用 Nginx，将前端请求代理到后端API
- **服务管理**：使用 systemd 管理后端服务

### 部署配置

- **后端服务**：运行在 `http://localhost:5000`
- **前端服务**：通过 Nginx 在 `http://localhost:80` 提供
- **API 代理**：Nginx 将 `/api/` 路径的请求代理到后端

### 手动部署

如果您需要手动部署，可以：

1. 创建一个标签并推送：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. 或者在 GitHub 界面创建一个新的 Release

### 服务器要求

服务器需要预装以下组件：
- .NET 8.0 SDK
- Node.js 18
- Nginx
- systemd
- sudo 权限

### GitHub Secrets 配置

为了安全地部署，您需要在 GitHub 仓库设置中配置以下 Secrets：
- `DB_CONNECTION_STRING`: 数据库连接字符串
- `JWT_SECRET_KEY`: JWT 密钥
- `JWT_ISSUER`: JWT 发行者
- `JWT_AUDIENCE`: JWT 受众

### 部署后验证

部署完成后，您可以通过以下方式验证部署：
- 前端：访问服务器IP的80端口
- 后端健康检查：`http://<server-ip>/api/health`