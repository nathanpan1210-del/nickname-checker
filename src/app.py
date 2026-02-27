from flask import Flask, jsonify, request, render_template_string
from .db import check_nickname, get_all

app = Flask(__name__)

# HTML前端页面
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>花名查重系统</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #666;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #eee;
            border-radius: 10px;
            font-size: 18px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        #result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            display: none;
        }
        #result.duplicate {
            background: #fee;
            color: #c00;
            border: 2px solid #fcc;
        }
        #result.similar {
            background: #fff3e0;
            color: #e65100;
            border: 2px solid #ffcc80;
        }
        #result.available {
            background: #e8f5e9;
            color: #2e7d32;
            border: 2px solid #a5d6a7;
        }
        .tips {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌸 花名查重系统</h1>
        <div class="input-group">
            <label>请输入你想取的花名：</label>
            <input type="text" id="nickname" placeholder="例如：星辰大海" maxlength="20">
        </div>
        <button onclick="check()">查询花名</button>
        <div id="result"></div>
        <div class="tips">
            <strong>查重规则：</strong><br>
            • 完全重复 → 花名重复，请重新取<br>
            • 2字以上相似 → 花名相似，建议重取<br>
            • 不重复不相似 → 花名可用
        </div>
    </div>

    <script>
        async function check() {
            const nickname = document.getElementById('nickname').value.trim();
            if (!nickname) {
                alert('请输入花名');
                return;
            }

            const result = document.getElementById('result');
            result.style.display = 'block';
            result.className = '';
            result.innerHTML = '查询中...';

            try {
                const res = await fetch('/api/check', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({nickname})
                });
                const data = await res.json();

                result.className = data.status;
                result.innerHTML = data.message;

                if (data.similar_to) {
                    result.innerHTML += `<br><small>相似花名：${data.similar_to}</small>`;
                }
            } catch (e) {
                result.innerHTML = '查询失败，请重试';
            }
        }

        // 回车键提交
        document.getElementById('nickname').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') check();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """前端页面"""
    return render_template_string(HTML_PAGE)

@app.route('/api/check', methods=['POST'])
def check():
    """查重API"""
    data = request.json
    nickname = data.get('nickname', '').strip()
    if not nickname:
        return jsonify({"status": "error", "message": "请输入花名"})
    result = check_nickname(nickname)
    return jsonify(result)

@app.route('/api/names', methods=['GET'])
def get_names():
    """获取所有花名"""
    return jsonify(get_all())

if __name__ == '__main__':
    app.run(debug=True)