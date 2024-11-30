import requests, json

# 设置API请求的URL
url = "https://spark-api-open.xf-yun.com/v1/chat/completions"



# 设置请求头
headers = {
    "Authorization": "Bearer fhjXaCsmBduoQHEWasvW:RUkiuTCkAjvfkMLryqVT",  # 替换为你的API密钥
    "Content-Type": "application/json"
}
def getaireturn(que):
    # 请求的payload数据
    data = {
        "model": "lite",  # 选择模型
        "messages": [
            {"role": "user", "content":que}  # 用户输入消息
        ],
        "stream": False  # 启用流式请求
    }
    # 发起POST请求，开启流式传输
    response = requests.post(url, headers=headers, json=data, stream=True)

    # 确保请求成功
    if response.status_code == 200:
        # 使用 UTF-8 解码流式响应
        response.encoding = "utf-8"

        # 逐行读取流式响应
        for line in response.iter_lines(decode_unicode="utf-8"):
            if line:
                # 打印每一行AI的返回结果
                # print(line)
                # 解析JSON数据
                response_data = json.loads(line)
                # 提取choices列表中的第一个元素的message的content
                content = response_data["choices"][0]["message"]["content"]
                # 打印提取的content
                return(content)
                # 退出循环，只输出第一个content
                break
