import ast
from typing import List, Tuple




class CodeChunk:
    def __init__(self, name: str, source: str, file_path: str, start_lineno: int, end_lineno: int):
        self.name = name
        self.source = source
        self.file_path = file_path
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno


    def to_dict(self):
        return {
            'name': self.name,
            'source': self.source,
            'file_path': self.file_path,
            'start_lineno': self.start_lineno,
            'end_lineno': self.end_lineno,
        }

def extract_functions_from_file(path: str) -> List[CodeChunk]:

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = getattr(node, 'lineno', None)
            end = getattr(node, 'end_lineno', None)
            if start and end:
                src_lines = text.splitlines()
                source = '\n'.join(src_lines[start - 1:end])
                name = node.name
                chunks.append(CodeChunk(name=name, source=source, file_path=path, start_lineno=start, end_lineno=end))

    return chunks
