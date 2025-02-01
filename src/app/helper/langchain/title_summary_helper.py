from src.app.config.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

config = Config()

def get_chat_summary(message: str):
    try:
        model = ChatGoogleGenerativeAI(
            model='gemini-1.5-flash',
            api_key=config.get_gemini_api_key(),
            max_tokens=config.get_max_tokens(),
            temperature=config.get_model_temperature(),
        )
        messages = [
            SystemMessage("Based on the following message you have to suggest a title to name the chat / conversation. Provide only one concise title without any quotation marks nothing more nothing less, only plain text, but you can add spaces:"),
            HumanMessage(message)
        ]

        res = model.invoke(messages)

        response = res.content

        return response
    except Exception as e:
        return f"Sorry the OpenAI  services are currently down, try again later.\nException: {e}"