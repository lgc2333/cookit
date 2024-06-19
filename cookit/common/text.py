def camel_case(string: str, upper_first: bool = False) -> str:
    pfx, *rest = string.split("_")
    if upper_first:
        pfx = pfx.capitalize()
    sfx = "".join(x.capitalize() for x in rest)
    return f"{pfx}{sfx}"


def full_to_half(text: str) -> str:
    return "".join(
        chr(ord(char) - 0xFEE0) if "\uff01" <= char <= "\uff5e" else char
        for char in text
    ).replace("\u3000", " ")


def escape_single_quotes(value: str) -> str:
    return value.replace("'", "\\'")


def escape_double_quotes(value: str) -> str:
    return value.replace('"', '\\"')


def escape_backticks(value: str) -> str:
    return value.replace("`", "\\`")
