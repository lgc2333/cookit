import time
from collections.abc import Iterator, MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Optional, TypeVar, Union, overload
from typing_extensions import override

if TYPE_CHECKING:
    from os import stat_result

TF = TypeVar("TF", str, bytes)


class FileCacheManager(MutableMapping[str, TF]):
    @overload
    def __init__(
        self: "FileCacheManager[str]",
        cache_dir: Union[str, Path],
        /,
        text_mode: Literal[True],
        max_size: Optional[int] = None,
        ttl: Optional[int] = None,
        encoding: str = "utf-8",
    ) -> None: ...
    @overload
    def __init__(
        self: "FileCacheManager[bytes]",
        cache_dir: Union[str, Path],
        /,
        text_mode: bool = False,
        max_size: Optional[int] = None,
        ttl: Optional[int] = None,
    ) -> None: ...
    def __init__(
        self,
        cache_dir: Union[str, Path],
        /,
        text_mode: bool = False,
        max_size: Optional[int] = None,
        ttl: Optional[int] = None,
        encoding: str = "utf-8",
    ):
        self.cache_dir = cache_dir if isinstance(cache_dir, Path) else Path(cache_dir)
        self.text_mode = text_mode
        self.max_size = max_size
        self.ttl = ttl
        self.encoding = encoding

    def purge(self):
        if (not self.cache_dir.exists()) or ((not self.max_size) and (not self.ttl)):
            return

        files: list[tuple[Path, stat_result]] = [
            (x, x.stat()) for x in self.cache_dir.iterdir() if x.is_file()
        ]
        files.sort(key=lambda x: x[1].st_mtime)
        files_len = len(files)

        should_unlink: set[Path] = set()
        if self.max_size and files_len > self.max_size:
            should_unlink.update(x[0] for x in files[: files_len - self.max_size])

        if self.ttl:
            out_time = time.time() - self.ttl
            index = next(
                (i for i, x in enumerate(files) if x[1].st_mtime >= out_time),
                files_len,
            )
            should_unlink.update(path for path, _ in files[:index])

        for path in should_unlink:
            path.unlink(missing_ok=True)

    @override
    def __getitem__(self, key: str) -> TF:
        self.purge()
        if (not (path := (self.cache_dir / key)).exists()) or (not path.is_file()):
            raise KeyError(key)
        return path.read_text(self.encoding) if self.text_mode else path.read_bytes()  # type: ignore

    @override
    def __setitem__(self, key: str, value: TF) -> None:
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)
        path = self.cache_dir / key
        (
            path.write_text(value, self.encoding)  # type: ignore
            if self.text_mode
            else path.write_bytes(value)  # type: ignore
        )
        self.purge()

    @override
    def __delitem__(self, key: str) -> None:
        (self.cache_dir / key).unlink(missing_ok=True)

    @override
    def __iter__(self) -> Iterator[str]:
        self.purge()
        return (x.name for x in self.cache_dir.iterdir() if x.is_file())

    @override
    def __len__(self) -> int:
        self.purge()
        return len([x for x in self.cache_dir.iterdir() if x.is_file()])

    @override
    def __contains__(self, key: Any) -> bool:
        if not isinstance(key, str):
            return False
        self.purge()
        return (self.cache_dir / key).exists()
