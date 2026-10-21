import streamlit as st
import requests

st.title("天气查询")

with st.form("weather_form"):
    city = st.text_input("请输入城市名（英文，如 Beijing）")
    submitted = st.form_submit_button("查询")

if submitted:
    if not city:
        st.warning("请输入城市名")
    else:
        url = f"https://wttr.in/{city}?format=j1"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            temp = data["current_condition"][0]["temp_C"]
            weather_desc = data["current_condition"][0]["weatherDesc"][0]["value"]

            st.success(f"{city} 当前温度：{temp}°C")
            st.write(f"天气状况：{weather_desc}")
        except requests.RequestException as e:
            st.error(f"请求失败：{e}")
        except (KeyError, IndexError):
            st.error("返回数据格式异常")