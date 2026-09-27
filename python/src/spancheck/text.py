import re
import unicodedata

_CURLY_QUOTES = {
    "“": '"',  # left double quotation mark
    "”": '"',  # right double quotation mark
    "‘": "'",  # left single quotation mark
    "’": "'",  # right single quotation mark
}

_HYPHEN_AT_LINEBREAK = re.compile(r"-\s*\n\s*")
_WHITESPACE_RUN = re.compile(r"\s+")


def normalize(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"normalize expects a string, got {type(text).__name__}")

    # basically if any input is not str, it should immediately call it out as a TypeError

    text = unicodedata.normalize("NFKC", text)
    # decomposes typographic ligatures like ﬁ into fi.

    for curly, straight in _CURLY_QUOTES.items():
        text = text.replace(curly, straight)

    # maps " " ' ' (Unicode smart quotes) to plain ASCII " and '

    text = text.replace("­", "")  # soft hyphen: drop entirely
    text = text.replace(" ", " ")  # non-breaking space: treat as space
    text = text.replace("•", "")  # bullet marker: list formatting, not content

    # En dashes (–) and em dashes (—) are left untouched: they're
    # distinct Unicode characters from a hyphen, carry real meaning (ranges,
    # parenthetical breaks), and never appear at a wrapped line break the
    # way ASCII hyphens do. Decision: normalize does not touch them.

    # A hyphen immediately followed by a line break was a PDF-wrapped word;
    # rejoin it without the hyphen. A hyphen NOT at a line break is a real
    # hyphen (e.g. "well-known") and must be left alone.
    text = _HYPHEN_AT_LINEBREAK.sub("", text)

    text = _WHITESPACE_RUN.sub(" ", text).strip()

    return text.lower()
