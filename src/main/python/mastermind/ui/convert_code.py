from mastermind.jvm import ConvertCode


def parse_code(raw: str, c: int, d: int) -> int | None:
    raw = raw.strip()

    if len(raw) != d or not raw.isdigit():
        return None

    for ch in raw:
        if not (1 <= int(ch) <= c):
            return None

    return int(ConvertCode.toIndex(c, d, int(raw)))


def display(index: int, c: int, d: int) -> str:
    return str(int(ConvertCode.toCode(c, d, index)))
