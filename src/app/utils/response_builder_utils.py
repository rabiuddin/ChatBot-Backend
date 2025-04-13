from src.app.utils.encryption_utils import encrypt

class ResponseBuilder:
    def __init__(self):
        self.response = {
            "success": None,
            "data": None,
            "error": None,
            "statusCode": None
        }

    def set_success(self, success):
        self.response["success"] = success
        return self
    def set_data(self, data):
        data = encrypt(data)
        self.response["data"] = data
        return self
    def set_msg_chat_data(self, data):
        self.response["data"] = data
        return self
    def set_error(self, error):
        self.response["error"] = error
        return self
    def setStatusCode(self, statusCode):
        self.response["statusCode"] = statusCode
        return self
    def build(self):
        return self.response