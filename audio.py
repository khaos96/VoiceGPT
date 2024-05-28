import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


async def main():
    bot = Chatbot(cookiePath='cookies.json')
    response = await bot.ask(prompt=input("Ask Bing AI a Question..."),conversation_style=ConversationStyle.creative)
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    print("Bot response:", bot_response)
    await bot.close()

    if __name__ == "__main__":
        asyncio.run(main())