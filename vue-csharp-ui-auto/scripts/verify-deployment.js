const http = require('http');
const https = require('https');
const { exec } = require('child_process');
const fs = require('fs');

console.log('开始验证部署...');

// 检查前端文件是否存在
const frontendPath = '/var/www/vue-csharp-frontend';
if (fs.existsSync(frontendPath)) {
    console.log('✅ 前端文件已部署到:', frontendPath);
    const files = fs.readdirSync(frontendPath);
    console.log('前端文件:', files);
} else {
    console.log('❌ 前端文件未找到:', frontendPath);
}

// 检查后端服务
function checkBackend() {
    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/api/health',
        method: 'GET',
    };

    const req = http.request(options, (res) => {
        console.log(`后端服务状态码: ${res.statusCode}`);
        
        res.on('data', (d) => {
            console.log('后端健康检查响应:', d.toString());
        });
        
        res.on('end', () => {
            console.log('✅ 后端服务验证完成');
        });
    });

    req.on('error', (e) => {
        console.error('❌ 后端服务连接失败:', e.message);
    });

    req.end();
}

// 检查系统服务状态
function checkServiceStatus(serviceName) {
    exec(`systemctl is-active ${serviceName}`, (error, stdout, stderr) => {
        if (error) {
            console.log(`❌ ${serviceName} 服务未运行:`, stderr);
            return;
        }
        console.log(`✅ ${serviceName} 服务状态:`, stdout.trim());
    });
}

// 检查 Nginx 配置
function checkNginx() {
    exec('nginx -t', (error, stdout, stderr) => {
        if (error) {
            console.log('❌ Nginx 配置有误:', stderr);
            return;
        }
        console.log('✅ Nginx 配置正确:', stdout);
    });
}

// 执行所有检查
checkBackend();
checkServiceStatus('vue-csharp-backend');
checkNginx();

console.log('部署验证完成');