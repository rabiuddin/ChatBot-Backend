import time
import logging
from openai import OpenAI
from src.app.config import Config
from src.app.models.assistant_prompt_model import AssistantPrompt

class MergeStackService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MergeStackService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = Config()
            self.client = OpenAI(api_key=self.config.get_openai_api_key())
            self.assistant = None
            self.vector_store = None
            self.thread = None
            self.initialized = True

    def get_assistant(self):
        if not self.assistant:
            self.assistant = self.client.beta.assistants.create(
                name="Company Policy Assistant",
                instructions="You are an expert of Company policies. You are asked to provide information about the company policies to the employees.",
                model="gpt-4o",
                tools=[{"type": "file_search"}],
            )
        return self.assistant

    def get_vector_store(self):
        if not self.vector_store:
            self.vector_store = self.client.beta.vector_stores.create(
                name="Company Policy Vector Store"
            )
        return self.vector_store

    def merge_stack_assistant(self, request: AssistantPrompt):
        try:
            self.get_assistant()
            self.get_vector_store()

            if not self.thread:
                self.thread = self.client.beta.threads.create()

            file_path = "/home/rabi/AI Internship/ChatBot-Backend/src/app/files/mergestack.txt"
            with open(file_path, "rb") as file:
                document = self.client.beta.vector_stores.files.upload_and_poll(
                    vector_store_id=self.vector_store.id,
                    file=file
                )

            self.assistant = self.client.beta.assistants.update(
                assistant_id=self.assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
            )

            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=request.prompt,
            )

            run = self.client.beta.threads.runs.create_and_poll(
                assistant_id=self.assistant.id,
                thread_id=self.thread.id
            )

            while run.status != "completed":
                time.sleep(0.5)
                run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)

            response = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            return response.data[0]

        except Exception as e:
            logging.error("MergeStack service encountered an error: %s", e)
            return f"Sorry, the MergeStack services are currently down. Try again later.\nException: {e}"

