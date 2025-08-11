from contextlib import nullcontext as _nullcontext
from typing_extensions import deprecated


@deprecated("Use `contextlib.nullcontext` directly instead")
class nullcontext(_nullcontext): ...  # noqa: N801
