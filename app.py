from flask import Flask, request, Response
import requests

app = Flask(__name__)

TARGET_URL = "https://openai.com"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # 构建目标 URL
    url = f"{TARGET_URL}/{path}"

    # 获取请求方法
    method = request.method

    # 获取请求头和数据
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_data()

    # 发起请求
    response = requests.request(method, url, headers=headers, data=data, params=request.args)

    # 构建响应
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
