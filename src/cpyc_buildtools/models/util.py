
def sanitize(s: str) -> str:
    if not s.endswith('\n'):
        return s.replace('\r', '') + '\n'
    return s.replace('\r', '')
    