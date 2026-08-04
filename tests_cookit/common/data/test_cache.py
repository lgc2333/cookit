import os
import time
from pathlib import Path

import pytest


def test_file_cache_reads_and_overwrites_bytes(tmp_path: Path):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path)

    cache["avatar"] = b"old"
    assert cache["avatar"] == b"old"

    cache["avatar"] = b"new"

    assert cache["avatar"] == b"new"
    assert cache.get("missing") is None
    with pytest.raises(KeyError, match="missing"):
        _ = cache["missing"]


def test_file_cache_reads_text_with_configured_encoding(tmp_path: Path):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path, text_mode=True, encoding="utf-8")

    cache["message"] = "hello 测试"

    assert cache["message"] == "hello 测试"
    assert (tmp_path / "message").read_bytes() == "hello 测试".encode()


def test_file_cache_behaves_like_mutable_mapping(tmp_path: Path):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path)
    cache["a"] = b"a"
    cache["b"] = b"b"
    (tmp_path / "directory").mkdir()

    assert len(cache) == 2
    assert set(cache) == {"a", "b"}
    assert "a" in cache
    assert b"a" not in cache

    del cache["a"]

    assert "a" not in cache
    del cache["missing"]
    assert set(cache) == {"b"}


def test_file_cache_purge_keeps_newest_files_when_max_size_is_reached(
    tmp_path: Path,
):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path, max_size=2)
    old_file = tmp_path / "old"
    mid_file = tmp_path / "mid"
    new_file = tmp_path / "new"

    old_file.write_bytes(b"old")
    mid_file.write_bytes(b"mid")
    new_file.write_bytes(b"new")
    os.utime(old_file, (1000, 1000))
    os.utime(mid_file, (2000, 2000))
    os.utime(new_file, (3000, 3000))

    cache.purge()

    assert not old_file.exists()
    assert mid_file.read_bytes() == b"mid"
    assert new_file.read_bytes() == b"new"


def test_file_cache_purge_removes_expired_files(tmp_path: Path):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path, ttl=60)
    expired_file = tmp_path / "expired"
    fresh_file = tmp_path / "fresh"
    now = time.time()

    expired_file.write_bytes(b"expired")
    fresh_file.write_bytes(b"fresh")
    os.utime(expired_file, (now - 120, now - 120))
    os.utime(fresh_file, (now, now))

    cache.purge()

    assert not expired_file.exists()
    assert fresh_file.read_bytes() == b"fresh"


def test_file_cache_purge_is_noop_without_limits(tmp_path: Path):
    from cookit import FileCacheManager

    cache = FileCacheManager(tmp_path)
    cache["item"] = b"item"

    cache.purge()

    assert cache["item"] == b"item"


def test_file_cache_creates_missing_parent_directory(tmp_path: Path):
    from cookit import FileCacheManager

    cache_dir = tmp_path / "missing" / "cache"
    cache = FileCacheManager(cache_dir)

    cache["item"] = b"item"

    assert cache_dir.is_dir()
    assert cache["item"] == b"item"
