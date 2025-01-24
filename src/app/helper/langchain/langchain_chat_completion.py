from src.app.config.config import Config
from src.app.models.prompt_model import PromptRequest
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class LangchainService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'): 
            self.initialized = True
            try:
                self.config = Config()
                self.model = None
                self.workflow = StateGraph(state_schema=MessagesState)

                self.workflow.add_edge(START, "model")
                self.workflow.add_node("model", self.call_model)
                self.langchain_config = {"configurable": {"thread_id": "abc123"}}

                self.app = self.workflow.compile(checkpointer=MemorySaver())

                self.trimmer = trim_messages(
                    max_tokens=5,
                    strategy="last",
                    include_system=True,
                    token_counter=len,
                    allow_partial=False,
                    start_on="human",
                )

            except Exception as e:
                print(f"Initialization failed: {e}")

    def call_model(self, state: MessagesState):
        try:
            # Create a chat prompt template
            trimmed_messages = self.trimmer.invoke(state["messages"])
            prompt_template = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a helpful assistant."),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )
            # Construct the prompt and invoke the model
            prompt = prompt_template.invoke({"messages": trimmed_messages})
            response = self.model.invoke(prompt)
            return {"messages": response}
        except Exception as e:
            raise RuntimeError(f"Model invocation failed: {e}")

    def __set_model(self, model: str):
        try:
            if model in self.config.get_gemini_allowed_models():
                self.model = ChatGoogleGenerativeAI(
                    model=model,
                    api_key=self.config.get_gemini_api_key(),
                    max_tokens=self.config.get_max_tokens(),
                    temperature=self.config.get_model_temperature(),
                )
            elif model in self.config.get_openai_allowed_models():
                self.model = ChatOpenAI(
                    model=model,
                    api_key=self.config.get_openai_api_key(),
                    max_tokens=self.config.get_max_tokens(),
                    temperature=self.config.get_model_temperature(),
                )
            else:
                raise ValueError(
                    f"Model '{model}' is not allowed. Allowed models: {self.config.get_gemini_allowed_models() + self.config.get_openai_allowed_models()}"
                )
        except Exception as e:
            raise RuntimeError(f"Error setting model: {e}")

    def langchain_chat_completion(self, request: PromptRequest):
        try:
            # Set the model
            self.__set_model(request.model)

            # Create HumanMessage from the request
            input_messages = [HumanMessage(request.prompt)]

            # Invoke the workflow and pass input messages
            output = self.app.invoke({"messages": input_messages}, self.langchain_config)

            # Extract assistant's response from the output
            assistant_message = output["messages"][-1].content

            return assistant_message
        except Exception as e:
            return f"Sorry, the Chat Completion services are currently down. Try again later.\nException: {e}"
