from flask import Flask, request, Response
import requests
import logging

app = Flask(__name__)

# 代理配置
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

@app.route('/api/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    try:
        # 构建目标 URL
        target_url = f"https://api.openai.com/{path}"

        # 获取请求头和数据
        headers = {key: value for key, value in request.headers.items() if key.lower() != 'host'}
        data = request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None
        params = request.args if request.method == 'GET' else None

        # 发起请求
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            params=params,
            proxies=proxies  # 使用代理
        )

        # 构建响应
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.RequestException as e:
        logging.error(f"转发请求时出错: {e}")
        return Response(
            "转发请求时发生错误。",
            status=500
        )
    except Exception as e:
        logging.error(f"意外错误: {e}")
        return Response(
            "发生了意外错误。",
            status=500
        )

if __name__ == '__main__':
    app.run(debug=True)
