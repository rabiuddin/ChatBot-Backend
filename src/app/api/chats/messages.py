from fastapi import APIRouter
from src.app.config.DB_connection import DatabaseConnection
from src.app.utils.response_builder_utils import ResponseBuilder
from src.app.models.message_model import MessageRequest

router = APIRouter()

connection = DatabaseConnection().create_connection()
cursor = connection.cursor()

@router.get("/{chatID}")
def get_all_messages(chatID: int):
    try:
        cursor.execute("SELECT * FROM Messages WHERE ChatID = %s", (chatID,))
        messages = cursor.fetchall()
        message_list = [{"ChatID": message[1], "HumanMessage": message[2], "AIMessage": message[3]} for message in messages]

        response = ResponseBuilder().set_success(True).set_msg_chat_data(message_list).build()
    except Exception as e:
        response = ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response

@router.post("/")
def add_message(message: MessageRequest):
    if message.ChatID == "":
        response = ResponseBuilder().set_success(False).set_data("Please provide a ChatID.").build()
        return response
    elif message.HumanMessage == "":
        response = ResponseBuilder().set_success(False).set_data("Please provide a HumanMessage.").build()
        return response
    elif message.AIMessage == "":
        response = ResponseBuilder().set_success(False).set_data("Please provide a AIMessage.").build()
        return response
    
    try:
        cursor.execute("INSERT INTO Messages (ChatID, HumanMessage, AIMessage) VALUES (%s, %s, %s)", (message.ChatID, message.HumanMessage, message.AIMessage))
        connection.commit()
        response = ResponseBuilder().set_success(True).set_msg_chat_data({"ChatID": message.ChatID, "HumanMessage": message.HumanMessage, "AIMessage": message.AIMessage}).build()

        return response
    except Exception as e:
        response = ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

        return response
