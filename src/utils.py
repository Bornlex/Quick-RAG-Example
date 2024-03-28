class SearchParameters:
    text_method: str = 'text'
    vector_method: str = 'vector'


def format_exception(e: Exception):
    return f"{type(e).__name__}: {str(e)}"
