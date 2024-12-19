import os
import openai 
from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core import load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, StorageContext

from dotenv import load_dotenv
from llama_index.core.postprocessor import MetadataReplacementPostProcessor # type: ignore
from llama_index.core.indices.postprocessor import SentenceTransformerRerank # type: ignore

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_sentence_window_index(index_dir, sentence_window_size):
    
    documents = SimpleDirectoryReader(input_files = ["src/introduction-to-natural-language-processing.pdf"]).load_data()
    document = Document(text="\n\n".join([doc.text for doc in documents]))
    
    Node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=sentence_window_size,
        window_metadata_key="window",
        original_text_metadata_key="original_sentence",
    )

    Settings.llm = OpenAI()
    Settings.embed_model = "local:BAAI/bge-small-en-v1.5"
    Settings.node_parser = Node_parser

    if not os.path.exists(index_dir):
        sentence_index = VectorStoreIndex.from_documents([document])
        sentence_index.storage_context.persist(persist_dir=index_dir)
        
    else:
        sentence_index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_dir))
    return sentence_index


def get_sentence_window_engine(sentence_index):
    
    postprocessor = MetadataReplacementPostProcessor(target_metadata_key="window",)
    rerank = SentenceTransformerRerank(top_n=2, model="BAAI/bge-reranker-base") 
    sentence_window_engine = sentence_index.as_query_engine(similarity_top_k=6, node_postprocessors=[postprocessor, rerank])
    
    return sentence_window_engine