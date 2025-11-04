from pathlib import Path
from typing import List




def list_py_files(root: str) -> List[Path]:
    p = Path(root)
    return [f for f in p.rglob('*.py') if f.is_file()]