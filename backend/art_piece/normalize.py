def normalize_name(value: str) -> str:
    return value.strip().title() if value else value

def normalize_sentence(value: str) -> str:
    return value.strip().capitalize() if value else value