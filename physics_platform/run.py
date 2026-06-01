"""
应用启动入口
============

本文件是整个 Flask 应用的启动脚本。

运行方式：
    cd physics_platform
    python run.py

启动后访问：
    http://localhost:5000

参数说明：
    debug=True    → 开启调试模式（代码修改后自动重启，显示错误详情）
    host='0.0.0.0' → 监听所有网络接口（局域网内其他设备也可访问）
    port=5000     → 监听端口号

注意：
    - debug=True 仅用于开发环境！
    - 生产环境应使用 Gunicorn：gunicorn -w 4 -b 0.0.0.0:5000 run:app
    - 生产环境需修改 SECRET_KEY 为随机密钥

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

from app import create_app

# 创建 Flask 应用实例
app = create_app()

if __name__ == '__main__':
    # 仅在直接运行此文件时启动开发服务器
    # 被其他文件 import 时不会启动
    app.run(debug=True, host='0.0.0.0', port=5000)
