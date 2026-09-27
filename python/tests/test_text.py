import pytest

from spancheck import normalize

CASES = [
    # basic case and whitespace
    ("Hello World", "hello world"),
    ("  lots   of\n\nspace\t", "lots of space"),
    ("", ""),
    # typographic noise from PDFs
    ("ﬁve cards", "five cards"),                        # ligature fi
    ("“Draw” ‘two’", "\"draw\" 'two'"),  # curly quotes
    ("soft­hyphen", "softhyphen"),                      # soft hyphen
    ("non breaking", "non breaking"),                   # non-breaking space
    # hyphenation across line breaks
    ("resour-\nce cards", "resource cards"),
    ("resour-  \n  ce", "resource"),
    # a hyphen NOT at a line break must survive
    ("well-known rule", "well-known rule"),
    # bullet markers are list formatting, not content: stripped
    ("• Draw a card\n• Discard one", "draw a card discard one"),
    # en/em dashes carry real meaning and are left untouched
    ("Rounds 2–4", "rounds 2–4"),
    ("Score—high", "score—high"),
]


@pytest.mark.parametrize("raw, expected", CASES)
def test_normalize(raw, expected):
    assert normalize(raw) == expected


@pytest.mark.parametrize("raw", [raw for raw, _ in CASES])
def test_normalize_is_idempotent(raw):
    once = normalize(raw)
    assert normalize(once) == once


def test_known_limitation_real_hyphen_at_line_break():
    # A genuinely hyphenated word that happens to wrap gets joined.
    # Accepted for v1: Module 4's fuzzy alignment absorbs this.
    assert normalize("well-\nknown") == "wellknown"


def test_rejects_non_strings():
    with pytest.raises(TypeError):
        normalize(None)


def test_decision_bullets_are_stripped():
    # Bullet markers are PDF list-formatting artifacts, not part of the
    # underlying claim text, so normalize removes them entirely.
    assert normalize("• First rule\n• Second rule") == "first rule second rule"


def test_decision_en_and_em_dashes_are_preserved():
    # En dashes (ranges, e.g. "2-4") and em dashes (parenthetical breaks)
    # are distinct from a hyphen and carry real meaning, so normalize
    # leaves them untouched rather than folding them into "-".
    assert normalize("Draw 2–4 cards") == "draw 2–4 cards"
    assert normalize("Score—final") == "score—final"