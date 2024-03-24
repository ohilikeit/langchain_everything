from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# Declare a chain
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 커뮤니티 중독자입니다. 시니컬하고 커뮤니티스러운 말투로 답변해주세요.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | ChatOpenAI(model="gpt-3.5-turbo")
