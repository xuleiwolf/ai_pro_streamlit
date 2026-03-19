import streamlit as st

st.title("欢迎来到我的AI应用网站 💡")
st.write("撒花🎈🎈🎈")
st.write("")

column1,column2 = st.columns([1,1])
with column1:
    "##### 承蒙遇见👊👊👊"

with column2:
    st.image("头像.jpg", width=200)

st.write("")
"##### 个人简介:"
"90后程序员一枚"



