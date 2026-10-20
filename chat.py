import requests
import os

def chat(question):
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        print("请先设置环境变量 API_KEY")
        return

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "user", "content": question}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        print(reply)
    except requests.RequestException as e:
        print(f"请求失败：{e}")
    except (KeyError, IndexError):
        print("返回数据格式异常")

if __name__ == "__main__":
    question = input("请输入你的问题：")
    chat(question)