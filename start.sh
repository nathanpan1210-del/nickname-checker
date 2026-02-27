#!/bin/bash
cd "$(dirname \"$0\")\"

echo \"📦 安装依赖...\"
pip install -r requirements.txt

echo \"🚀 启动服务...\"
python src/app.py