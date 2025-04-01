import json
import time
from io import BytesIO
from pathlib import Path
from typing import Any


class DebugFileWriter:
    def __init__(self, base_path: Path, *rest_path: str) -> None:
        self.base_path = base_path
        self.full_path = base_path.joinpath(*rest_path)

    @property
    def enabled(self) -> bool:
        return self.base_path.exists()

    def write(self, content: Any, filename: str):
        filename = filename.format(time=round(time.time() * 1000))
        self.full_path.mkdir(parents=True, exist_ok=True)
        path = self.full_path / filename
        if isinstance(content, (bytes, bytearray)):
            data = content
        elif isinstance(content, BytesIO):
            data = content.getvalue()
        else:
            data = (
                content
                if isinstance(content, str)
                else json.dumps(content, ensure_ascii=False)
            ).encode("u8")
        path.write_bytes(data)
