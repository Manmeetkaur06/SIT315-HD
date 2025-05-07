"""SHA‑256 helper."""
from pathlib import Path, PurePath
import hashlib

def hash_file(p: str | PurePath) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
