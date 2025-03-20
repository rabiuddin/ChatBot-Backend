from fastapi import APIRouter
from src.app.config.DB_connection import DatabaseConnection
from src.app.utils.response_builder_utils import ResponseBuilder
from src.app.models.message_summary_model import UpdateTitle
from src.app.helper.langchain import title_summary_helper

router = APIRouter()

connection = DatabaseConnection().create_connection()
cursor = connection.cursor()

@router.get("/title-summary/{message}")
def get_chat_summary(message: str):
    try:
        response = title_summary_helper.get_chat_summary(message)
        response_builder = ResponseBuilder().set_success(True).set_msg_chat_data(response).build()
        return response_builder
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI summary services are currently down, try again later.\nExeption: {e}").build()

@router.get("/")
def get_all_chats():
    global connection, cursor
    try:
        cursor.execute("SELECT * FROM Chats")
        
        chats = cursor.fetchall()

        chat_list = [{"id": chat[0], "title": chat[1],"created_at":chat[2]} for chat in chats]

        response = ResponseBuilder().set_success(True).set_msg_chat_data(chat_list).build()
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response

@router.get("/{id}")
def get_chat(id: int):
    global connection, cursor

    try:
        cursor.execute("SELECT * FROM Chats WHERE ID = %s", (id,))
        chat = cursor.fetchone()
        response = ResponseBuilder().set_success(True).set_msg_chat_data(chat).build()
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response

@router.post("/")
def create_chat():
    global connection, cursor

    try:
        cursor.execute("INSERT INTO Chats (ID) VALUES (DEFAULT)")
        connection.commit()

        chatId = cursor.lastrowid

        cursor.execute("SELECT * FROM Chats WHERE ID = %s", (chatId,))
        res = cursor.fetchone()

        chat = {"id": res[0], "title": res[1], "created_at": res[2]}

        response = ResponseBuilder().set_success(True).set_msg_chat_data({"chat": chat}).build()
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response

@router.delete("/{id}")
def delete_chat(id: int):
    global connection, cursor

    try:
        cursor.execute("DELETE FROM Chats WHERE ID = %s", (id,))
        connection.commit()

        response = ResponseBuilder().set_success(True).set_data("Chat deleted successfully").build()
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response

@router.put("/")
def update_chat_title(chatID: int, title: str):
    global connection, cursor

    try:
        cursor.execute("UPDATE Chats SET title = %s WHERE ID = %s", (title, chatID))
        connection.commit()

        response = ResponseBuilder().set_success(True).set_data("Chat title updated successfully").build()
    except Exception as e:
        return ResponseBuilder().set_success(False).set_data(f"").set_error(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").build()

    return response






