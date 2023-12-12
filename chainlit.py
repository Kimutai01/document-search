import chainlit as cl

from orchestrator import generate_agent

agent = generate_agent()
from llama_index import Document


@cl.on_chat_start
async def factory():
    cl.user_session.set("chat_engine", agent)
    




@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("chat_engine") 
    response = await cl.make_async(agent.stream_chat)(message.content)

    response_message = cl.Message(content="")

    for token in response.response_gen:
        await response_message.stream_token(token=token)

    if response.response_txt:
        response_message.content = response.response_txt

    await response_message.send()