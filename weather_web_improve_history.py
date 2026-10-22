import streamlit as st
import requests

st.title("天气查询")

# 初始化历史记录
if "history" not in st.session_state:
    st.session_state.history = []

# 侧边栏
with st.sidebar:
    st.header("使用说明")
    st.write("可以选择预设城市，或手动输入。")
    if st.button("清空历史"):
        st.session_state.history = []
        st.success("已清空历史记录")

# 下拉选择 + 手动输入
option = st.selectbox("选择查询方式", ["手动输入", "北京", "伦敦", "东京"])

if option == "手动输入":
    city = st.text_input("请输入城市名（英文）")
else:
    city_map = {"北京": "Beijing", "伦敦": "London", "东京": "Tokyo"}
    city = city_map[option]
    st.write(f"当前选择：{option}")

if st.button("查询"):
    if not city:
        st.warning("请输入或选择城市")
    else:
        with st.spinner("正在查询天气..."):
            url = f"https://wttr.in/{city}?format=j1"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                temp = data["current_condition"][0]["temp_C"]
                weather_desc = data["current_condition"][0]["weatherDesc"][0]["value"]

                # 保存到历史记录
                st.session_state.history.append({
                    "city": city,
                    "temp": temp,
                    "desc": weather_desc
                })

                # 两列显示当前结果
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("当前温度", f"{temp}°C")
                with col2:
                    st.write("**天气状况**")
                    st.write(weather_desc)

            except requests.RequestException as e:
                st.error(f"请求失败：{e}")
            except (KeyError, IndexError):
                st.error("返回数据格式异常")

# 显示历史记录
if st.session_state.history:
    st.subheader("查询历史（最近5条）")
    for item in reversed(st.session_state.history[-5:]):
        st.write(f"{item['city']}: {item['temp']}°C, {item['desc']}")