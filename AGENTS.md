# AGENTS.md

`cookit` is a project-unrelated utility library.

## Commands

NOTE: The following command are expected to be run under the plugin repo root rather than the workspace root.

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

- Keep test coverage as high as possible to avoid dead code. Code included in the current runtime's coverage scope should be covered unless it is version-specific, dependency-gated, or an intentional error path that is impractical to trigger safely.

## Gotchas

## Playwright

- `pytest-playwright-asyncio` needs session-scoped asyncio settings; keep `asyncio_default_fixture_loop_scope` and `asyncio_default_test_loop_scope` as `session`.
- Playwright tests require browser binaries. Run `uv run playwright install chromium` if Chromium is missing.

### NoneBot2

- NoneBot plugin helper modules may require `require("plugin_name")` before import; use the `app` fixture when NoneBot must be initialized.
- Alconna/UniMessage helpers may need `current_bot`, `current_event`, and `current_state`; exercise them inside a matcher with `app.test_matcher()` and `ctx.receive_event()` instead of mocking context.
- Some coverage misses are expected in one runtime, such as Pydantic v1/v2 branches and Python-version fallbacks.
