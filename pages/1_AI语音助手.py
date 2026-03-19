import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 页面配置
st.set_page_config(page_title="💬 DeepSeek AI 助手", page_icon="🤖")
st.title("💬 克隆 ChatGPT")

# 侧边栏
with st.sidebar:
    api_key = st.text_input("请输入 DeepSeek Key：", type="password")
    st.markdown("[获取DeepSeek key](https://platform.deepseek.com/usage)")

# 初始化会话历史
if "store" not in st.session_state:
    st.session_state.store = {}
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
    ]

# 渲染历史消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------- 核心 AI 函数（新版官方标准写法）--------------------------
def get_chain(api_key):
    # 模型
    model = ChatOpenAI(
        model="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )
    # 提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好、专业的AI助手。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    # 链式组合
    chain = prompt | model
    return chain

# 获取会话历史
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

# -------------------------- 用户输入 --------------------------
prompt = st.chat_input("请输入你的问题...")
if prompt:
    if not api_key:
        st.warning("⚠️ 请输入 DeepSeek API Key")
        st.stop()

    # 显示用户消息
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    # AI 回复
    with st.spinner("🤖 AI 思考中..."):
        try:
            chain = get_chain(api_key)
            # 带记忆的链
            with_history = RunnableWithMessageHistory(
                chain,
                get_session_history=get_session_history,
                input_messages_key="input",
                history_messages_key="history"
            )
            response = with_history.invoke(
                {"input": prompt},
                config={"configurable": {"session_id": "streamlit_chat"}}
            )
            ai_msg = response.content

        except Exception as e:
            ai_msg = f"❌ 错误：{str(e)}"

    # 显示 AI 回复
    st.session_state.messages.append({"role": "ai", "content": ai_msg})
    st.chat_message("ai").write(ai_msg)