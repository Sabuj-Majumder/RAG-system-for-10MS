chat_history = []

def add_to_memory(user_input: str, model_output: str):
    chat_history.append(f"User: {user_input}\nAssistant: {model_output}")

def get_short_term_context() -> str:
    return "\n".join(chat_history[-5:])
