# pytest playwright currently doesn't support asyncio
# so i won't write pytest based tests for it

from ..utils import auto_import_tests

auto_import_tests(__file__, __package__)
