from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 彻底删除所有维基百科相关代码
# 无任何外网请求，国内直接运行
def generate_script(subject, video_length, creativity, api_key):
    # 标题模板
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的短视频标题")
        ]
    )

    # 脚本模板（完全不依赖维基百科）
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频博主。请根据以下信息，写一个优质视频脚本。
             主题：{subject}
             标题：{title}
             时长：{duration} 分钟

             严格按照格式输出：
             【开头】
             （吸引眼球，3秒抓住注意力）

             【中间】
             （干货内容，清晰易懂）

             【结尾】
             （惊喜/反转/引导关注）

             语言轻松、有趣、年轻化。
             """)
        ]
    )

    # 通义千问
    client = ChatOpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
        temperature=creativity,
        timeout=60
    )

    # 执行链
    title_chain = title_template | client
    script_chain = script_template | client

    # 生成标题
    title = title_chain.invoke({"subject": subject}).content

    # 直接空内容，彻底不调用维基百科
    search_result = "已关闭百科搜索，避免网络错误"

    # 生成脚本
    script = script_chain.invoke({
        "subject": subject,
        "title": title,
        "duration": video_length
    }).content

    return search_result, title, script