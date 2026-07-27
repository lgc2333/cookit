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

Search before adding utilities: `rg -n "keyword|related_term" cookit`.

- `common/`: General utilities, with no external dependencies; text, math/unit/time formatting, async helpers, signals, debug files, data helpers, decorator collectors.
- `pyd/`: Pydantic v1 & v2 compatibility and helpers; validation, dump, config, validators, model decorators.
- `jinja/`: Jinja helpers and filters; filters and filter registration.
- `loguru/`: Loguru helpers; suppress/log exception helpers.
- `nonebot/`: NoneBot helpers; plugin loading checks, command arg dependencies, localstore guard, Alconna recall/reply helpers.
- `pw/`: Playwright helpers; screenshots, route groups, real-file routers, Jinja screenshot rendering.

## Rules

- Keep test coverage as high as possible to avoid dead code. Code included in the current runtime's coverage scope should be covered unless it is version-specific, dependency-gated, or an intentional error path that is impractical to trigger safely.

## Gotchas

### Playwright

- `pytest-playwright-asyncio` needs session-scoped asyncio settings; keep `asyncio_default_fixture_loop_scope` and `asyncio_default_test_loop_scope` as `session`.

### NoneBot2

- Some coverage misses are expected in one runtime, such as Pydantic v1/v2 branches and Python-version fallbacks.
