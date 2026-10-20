import requests

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp = data["current_condition"][0]["temp_C"]
        weather_desc = data["current_condition"][0]["weatherDesc"][0]["value"]

        print(f"{city} 当前温度：{temp}°C")
        print(f"天气状况：{weather_desc}")
    except requests.Timeout:
        print("请求超时，请检查网络后重试")
    except requests.RequestException as e:
        print(f"请求失败：{e}")
    except (KeyError, IndexError):
        print("返回数据格式异常，无法解析天气信息")

if __name__ == "__main__":
    while True:
        city = input("请输入城市名（英文，如 Beijing）：").strip()
        if city:
            break
        print("城市名不能为空，请重新输入")
    get_weather(city)

"""
原始版本：
if __name__ == "__main__":
    city = input("请输入城市名（英文，如 Beijing）：")
    get_weather(city)
"""
