from src.app.config import Config
from src.app.models.prompt_model import PromptRequest
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from typing_extensions import List, TypedDict
from langchain import hub

config = Config()

class MergeStackAssistant:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MergeStackAssistant, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'): 
            self.initialized = True
            try:
                self.model = ChatOpenAI(
                    model='gpt-4',
                    api_key=config.get_openai_api_key(),
                    max_tokens=config.get_max_tokens(),
                    temperature=config.get_model_temperature(),
                )

                graph_builder = StateGraph(self.State).add_sequence([self.retrieve, self.generate])
                graph_builder.add_edge(START, "retrieve")
                self.graph = graph_builder.compile()

                self.trimmer = trim_messages(
                    max_tokens=5,
                    strategy="last",
                    include_system=True,
                    token_counter=len,
                    allow_partial=False,
                    start_on="human",
                )

                # Initialize the embedding model
                embedding_model = OpenAIEmbeddings(model= "text-embedding-3-small",api_key=config.get_openai_api_key())

                loader = PyPDFLoader(file_path="src/app/files/mergeStack policy.pdf")
                docs = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                all_splits = text_splitter.split_documents(docs)

                self.vector_store = InMemoryVectorStore(embedding_model)
                _ = self.vector_store.add_documents(all_splits)

                self.prompt = hub.pull("rlm/rag-prompt")


            except Exception as e:
                print(f"Initialization failed: {e}")

    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str

    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}


    def generate(self, state: State):
           
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke(
            {
                "question": state["question"] + " Give me the output in a nice Markdown format.", 
                "context": docs_content
            }
        )
        response = self.model.invoke(messages)
        return {"answer": response.content}

    def merge_stack_assistant(self, request: PromptRequest):
        try:
            response = self.graph.invoke({"question": request.prompt})

            assistant_message = response["answer"]

            return assistant_message
        except Exception as e:
            return f"Sorry, the MergeStack AI services are currently down. Try again later.\nException: {e}"
