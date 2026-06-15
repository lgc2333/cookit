# AGENTS.md

`cookit` is a project-unrelated utility library.

## Commands

```bash
uv sync -U
uv run pytest
uv run ruff check .
uv run ruff format .
uv run basedpyright
```

## Structure

- `common/`: General utilities, with no external dependencies.
- `pyd/`: Pydantic v1 & v2 compatibility and helpers.
- `jinja/`: Jinja helpers and filters.
- `loguru/`: Loguru helpers.
- `nonebot/`: NoneBot helpers.
- `pw/`: Playwright helpers.

## Rules

### Testing Rules

- Add or update tests for changed public helpers.
- Tests should make the helper's intended behavior obvious from the test name and assertions.
- When touching tested code, check coverage with `uv run pytest --cov=cookit --cov-report=term-missing`.
- Code included in the current runtime's coverage scope should be covered unless it is version-specific, dependency-gated, or an intentional error path that is impractical to trigger safely.

## Gotchas

### Testing Gotchas

- `pytest-playwright-asyncio` needs session-scoped asyncio settings; keep `asyncio_default_fixture_loop_scope` and `asyncio_default_test_loop_scope` as `session`.
- Playwright tests require browser binaries. Run `uv run playwright install chromium` if Chromium is missing.
- NoneBot plugin helper modules may require `require("plugin_name")` before import; use the `app` fixture when NoneBot must be initialized.
- `UniMessage.of` may need a current bot/adapter; create a fake bot and set the current bot context instead of mocking it.
- Some coverage misses are expected in one runtime, such as Pydantic v1/v2 branches and Python-version fallbacks.
