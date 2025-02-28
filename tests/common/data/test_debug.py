import json
from pathlib import Path

from cookit import DebugFileWriter


def test_debug_file_writer(tmp_path: Path):
    # Test enabled states
    writer = DebugFileWriter(tmp_path, "subdir")
    assert writer.enabled is True

    non_existent = tmp_path / "nonexistent"
    writer_disabled = DebugFileWriter(non_existent, "subdir")
    assert writer_disabled.enabled is False

    # Test different content types
    content_bytes = b"bytes content"
    writer.write(content_bytes, "test.bin")
    assert (tmp_path / "subdir/test.bin").read_bytes() == content_bytes

    content_str = "text content"
    writer.write(content_str, "test.txt")
    assert (tmp_path / "subdir/test.txt").read_text("utf-8") == content_str

    content_json = {"key": "value"}
    writer.write(content_json, "test.json")
    assert json.loads((tmp_path / "subdir/test.json").read_text()) == content_json

    # Test directory creation
    nested_writer = DebugFileWriter(tmp_path, "subdir", "nested")
    nested_writer.write("content", "test.txt")
    assert (tmp_path / "subdir/nested/test.txt").exists()

    # Test timestamp in filename
    root_writer = DebugFileWriter(tmp_path)
    root_writer.write("content", "test_{time}.txt")
    files = list(tmp_path.glob("test_*.txt"))
    assert len(files) == 1
    assert files[0].read_text() == "content"
