from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langserve import add_routes
from chain import chain
from chat import chain as chat_chain


from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/prompt/playground")


# prompt 생성 router 추가
add_routes(app, chain, path="/prompt")


class InputChat(BaseModel):
    """Input for the chat endpoint"""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ..., description="The chat message representing the current conversation"
    )


# 채팅 인터페이스 라우터 추가
add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
