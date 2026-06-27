from functools import partial


def camel_case(string: str, upper_first: bool = False) -> str:
    """Convert a snake_case string to camelCase or PascalCase."""
    pfx, *rest = string.split("_")
    if upper_first:
        pfx = pfx.capitalize()
    sfx = "".join(x.capitalize() for x in rest)
    return f"{pfx}{sfx}"


pascal_case = partial(camel_case, upper_first=True)


def full_to_half(text: str) -> str:
    """Convert full-width ASCII characters and spaces to half-width forms."""
    return "".join(
        chr(ord(char) - 0xFEE0) if "\uff01" <= char <= "\uff5e" else char
        for char in text
    ).replace("\u3000", " ")


def escape_single_quotes(value: str) -> str:
    """Escape single quotes for embedding text in quoted literals."""
    return value.replace("'", "\\'")


def escape_double_quotes(value: str) -> str:
    """Escape double quotes for embedding text in quoted literals."""
    return value.replace('"', '\\"')


def escape_backticks(value: str) -> str:
    """Escape backticks for embedding text in template literals."""
    return value.replace("`", "\\`")
