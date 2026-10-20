import requests
import os

def chat(question, messages):          # ← 改动1：增加了 messages 参数
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        print("请先设置环境变量 API_KEY")
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages.append({"role": "user", "content": question})   # ← 改动2：把当前问题加入历史

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": messages                                 # ← 改动3：发送完整历史
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})  # ← 改动4：把回复也加入历史
        return reply
    except requests.RequestException as e:
        print(f"请求失败：{e}")
        return None
    except (KeyError, IndexError):
        print("返回数据格式异常")
        return None

if __name__ == "__main__":
    print("连续对话模式（输入 q 退出）")
    messages = []                                            # ← 改动5：创建历史列表

    while True:                                              # ← 改动6：加了循环
        question = input("\n你：")
        if question.strip().lower() == "q":                  # ← 改动7：支持输入 q 退出
            print("已退出")
            break

        reply = chat(question, messages)
        if reply:
            print(f"AI：{reply}")