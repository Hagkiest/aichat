from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'

# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台获取
SPARKAI_APP_ID = '5c183ce9'
SPARKAI_API_SECRET = 'NGViNTAxZjJiMmMxMGY2YzRmMDQ1OTNh'
SPARKAI_API_KEY = '943fdf11ac8acb25096a4c4ede92a5c8'

# 星火认知大模型的domain值
SPARKAI_DOMAIN = 'lite'

if __name__ == '__main__':
    # 初始化 Spark 大模型
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,  # 设置为 False，表示不使用流式输出
    )

    # 设定消息
    messages = [
        ChatMessage(role="system", content="你是一个知识渊博的人"),
        ChatMessage(role="user", content="你是谁")
    ]

    # 设置处理返回数据的方式
    handler = ChunkPrintHandler()

    # 生成回复
    a = spark.generate([messages], callbacks=[handler])

    # 打印 AI 回复
    print(a)

