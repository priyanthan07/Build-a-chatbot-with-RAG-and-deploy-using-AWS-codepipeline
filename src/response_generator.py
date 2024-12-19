from src.data_preparation import get_sentence_window_engine, get_sentence_window_index

def get_rag_engine():
    index_dir = ".src/sentence_index"
    sw_index = get_sentence_window_index(index_dir, sentence_window_size=3)
    sw_engine = get_sentence_window_engine(sw_index)
    return sw_engine

def chat(user_response, sw_engine):
    window_response = sw_engine.query(user_response)
    return window_response.response


