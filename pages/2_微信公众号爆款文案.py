import streamlit as st
import sys
from pathlib import Path
# 自动获取上级目录（线上/本地都通用）
sys.path.append(str(Path(__file__).parent.parent))
# 现在可以安全导入
from 应用工具包 import utils2

st.header("微信公众号爆款文案AI写作助手 ✏️")
with st.sidebar:
    api_key = st.text_input("请输入百度千问密钥：", type="password")
    st.markdown("[获取百度千问密钥，有免费额度的](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)")

theme = st.text_input("主题")
submit = st.button("开始写作")

if submit and not api_key:
    st.info("请输入你的百度千问密钥")
    st.stop()
if submit and not theme:
    st.info("请输入生成内容的主题")
    st.stop()
if submit:
    with st.spinner("AI正在努力创作中，请稍等..."):
        result = utils2.generate_xiaohongshu(theme, api_key)
    st.divider()
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("##### 公众号标题1")
        st.write(result.titles[0])
        st.markdown("##### 公众号标题2")
        st.write(result.titles[1])
        st.markdown("##### 公众号标题3")
        st.write(result.titles[2])
        st.markdown("##### 公众号标题4")
        st.write(result.titles[3])
        st.markdown("##### 公众号标题5")
        st.write(result.titles[4])
    with right_column:
        st.markdown("##### 公众号正文")
        st.write(result.content)

