import time
import logging
from openai import OpenAI
from src.app.config import Config
from src.app.models.assistant_prompt_model import AssistantPrompt
import os

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

            self.assistant = self.client.beta.assistants.create(
                name="Company Policy Assistant",
                instructions="You are an expert of Company policies. You are asked to provide information about the company policies to the employees.",
                model="gpt-4o",
                tools=[{"type": "file_search"}],
            )

            self.vector_store = self.client.beta.vector_stores.create(
                name="Company Policy Vector Store"
            )

            # Get the current file's directory (mergestack_helper.py)
            current_file_directory = os.path.dirname(__file__)

            # Traverse up to the project root
            project_root = os.path.abspath(os.path.join(current_file_directory, "../../.."))

            # Construct the path to the `files` directory
            directory_path = os.path.join(project_root, "app", "files")

            # Print or use the `files_directory`
            print(directory_path)

            file_name = "mergeStack policy.pdf"
            file_path = os.path.join(directory_path, file_name)
            # Putting the file 
            with open(file_path, "rb") as file:
                document = self.client.beta.vector_stores.files.upload_and_poll(
                    vector_store_id=self.vector_store.id,
                    file=file
                )

            self.assistant = self.client.beta.assistants.update(
                assistant_id=self.assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
            )

            self.thread = None
            self.initialized = True

    def get_assistant(self):
        return self.assistant

    def get_vector_store(self):
        return self.vector_store

    def merge_stack_assistant(self, request: AssistantPrompt):
        try:
            if not self.thread:
                self.thread = self.client.beta.threads.create()

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

