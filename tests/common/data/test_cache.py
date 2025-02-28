import asyncio
from pathlib import Path


async def test_file_cache_manager(tmp_path: Path):
    from cookit import FileCacheManager

    bytes_cache = FileCacheManager(tmp_path, max_size=2, ttl=1)

    bytes_cache["test"] = b"test"
    assert "test" in bytes_cache
    assert bytes_cache.get("test") == b"test"

    bytes_cache["test"] = b"test test"
    assert "test" in bytes_cache
    assert bytes_cache.get("test") == b"test test"

    await asyncio.sleep(0.01)
    bytes_cache["test2"] = b"test2"
    assert "test2" in bytes_cache
    assert bytes_cache.get("test2") == b"test2"

    await asyncio.sleep(0.01)
    bytes_cache["test3"] = b"test3"
    assert "test3" in bytes_cache
    assert bytes_cache.get("test3") == b"test3"

    assert "test2" in bytes_cache
    assert bytes_cache.get("test2") == b"test2"

    assert "test" not in bytes_cache
    assert bytes_cache.get("test") is None

    await asyncio.sleep(0.5)

    await asyncio.sleep(0.01)
    bytes_cache["test4"] = b"test4"
    assert "test4" in bytes_cache
    assert bytes_cache.get("test4") == b"test4"

    assert "test" not in bytes_cache
    assert bytes_cache.get("test") is None
    assert "test2" not in bytes_cache
    assert bytes_cache.get("test2") is None

    await asyncio.sleep(0.5)

    assert "test" not in bytes_cache
    assert bytes_cache.get("test") is None
    assert "test2" not in bytes_cache
    assert bytes_cache.get("test2") is None
    assert "test3" not in bytes_cache
    assert bytes_cache.get("test3") is None
    assert "test4" in bytes_cache
    assert bytes_cache.get("test4") == b"test4"

    await asyncio.sleep(0.5)

    assert "test" not in bytes_cache
    assert bytes_cache.get("test") is None
    assert "test2" not in bytes_cache
    assert bytes_cache.get("test2") is None
    assert "test3" not in bytes_cache
    assert bytes_cache.get("test3") is None
    assert "test4" not in bytes_cache
    assert bytes_cache.get("test4") is None

    text_cache = FileCacheManager(tmp_path, text_mode=True, max_size=2, ttl=1)

    text_cache["test_text"] = "test测试测试"
    assert "test_text" in text_cache
    assert text_cache.get("test_text") == "test测试测试"
    assert bytes_cache.get("test_text") == "test测试测试".encode()
