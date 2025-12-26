#!/bin/bash

# Vue + C# 应用启动脚本

echo "开始部署 Vue + C# 应用..."

# 启动后端服务
echo "启动后端服务..."
sudo systemctl daemon-reload
sudo systemctl enable vue-csharp-backend
sudo systemctl start vue-csharp-backend

# 检查后端服务状态
if sudo systemctl is-active --quiet vue-csharp-backend; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 重启 Nginx
echo "重启 Nginx..."
sudo systemctl reload nginx

# 检查服务是否正常运行
echo "等待服务启动..."
sleep 10

# 检查后端健康检查端点
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务无法访问"
    exit 1
fi

echo "✅ Vue + C# 应用部署完成！"
echo "前端: http://localhost"
echo "后端: http://localhost:5000"
echo "健康检查: http://localhost:5000/api/health"