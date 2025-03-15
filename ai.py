from langchain_community.llms.ollama import Ollama
from flask import *
from flask_login import *

def gpt_stream(model, history):
    # 定义一个函数，用于从GPT模型中获取流式数据
    host="0.0.0.0"
    port="11434" #默认的端口号为11434
    # 创建一个Ollama对象，用于与GPT模型进行交互
    deepseek=Ollama(base_url=f"http://{host}:{port}", model=model,temperature=0)
    chunks = []
    # 遍历GPT模型的流式数据
    for chunk in deepseek.stream(history):
        chunks.append(chunk)
        # 将每个数据块添加到chunks列表中，并返回
        yield chunk

# 定义_gpt_api函数
def _gpt_api():
    # 判断当前用户是否已登录
    if current_user.is_authenticated:
        # 如果已登录，则返回gpt_stream函数的返回值，并设置mimetype为"text/plain"
        return Response(gpt_stream(request.form.get("model"),json.loads(request.form.get("history"))), mimetype="text/plain")
    else:
        # 如果未登录，则返回提示信息
        return "Please Login First!"