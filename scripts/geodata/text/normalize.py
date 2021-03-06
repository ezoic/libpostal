# -*- coding: utf-8 -*-
from geodata.text import _normalize
from geodata.text.tokenize import tokenize_raw
from geodata.text.token_types import token_types

from geodata.encoding import safe_decode

# String options
NORMALIZE_STRING_LATIN_ASCII = _normalize.NORMALIZE_STRING_LATIN_ASCII
NORMALIZE_STRING_TRANSLITERATE = _normalize.NORMALIZE_STRING_TRANSLITERATE
NORMALIZE_STRING_STRIP_ACCENTS = _normalize.NORMALIZE_STRING_STRIP_ACCENTS
NORMALIZE_STRING_DECOMPOSE = _normalize.NORMALIZE_STRING_DECOMPOSE
NORMALIZE_STRING_LOWERCASE = _normalize.NORMALIZE_STRING_LOWERCASE
NORMALIZE_STRING_TRIM = _normalize.NORMALIZE_STRING_TRIM
NORMALIZE_STRING_REPLACE_HYPHENS = _normalize.NORMALIZE_STRING_REPLACE_HYPHENS

DEFAULT_STRING_OPTIONS = NORMALIZE_STRING_LATIN_ASCII |  \
    NORMALIZE_STRING_DECOMPOSE | \
    NORMALIZE_STRING_TRIM | \
    NORMALIZE_STRING_REPLACE_HYPHENS | \
    NORMALIZE_STRING_STRIP_ACCENTS | \
    NORMALIZE_STRING_LOWERCASE

# Token options
NORMALIZE_TOKEN_REPLACE_HYPHENS = _normalize.NORMALIZE_TOKEN_REPLACE_HYPHENS
NORMALIZE_TOKEN_DELETE_HYPHENS = _normalize.NORMALIZE_TOKEN_DELETE_HYPHENS
NORMALIZE_TOKEN_DELETE_FINAL_PERIOD = _normalize.NORMALIZE_TOKEN_DELETE_FINAL_PERIOD
NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS = _normalize.NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS
NORMALIZE_TOKEN_DROP_ENGLISH_POSSESSIVES = _normalize.NORMALIZE_TOKEN_DROP_ENGLISH_POSSESSIVES
NORMALIZE_TOKEN_DELETE_OTHER_APOSTROPHE = _normalize.NORMALIZE_TOKEN_DELETE_OTHER_APOSTROPHE
NORMALIZE_TOKEN_SPLIT_ALPHA_FROM_NUMERIC = _normalize.NORMALIZE_TOKEN_SPLIT_ALPHA_FROM_NUMERIC
NORMALIZE_TOKEN_REPLACE_DIGITS = _normalize.NORMALIZE_TOKEN_REPLACE_DIGITS

DEFAULT_TOKEN_OPTIONS = NORMALIZE_TOKEN_REPLACE_HYPHENS | \
    NORMALIZE_TOKEN_DELETE_FINAL_PERIOD | \
    NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS | \
    NORMALIZE_TOKEN_DROP_ENGLISH_POSSESSIVES | \
    NORMALIZE_TOKEN_DELETE_OTHER_APOSTROPHE | \
    NORMALIZE_TOKEN_REPLACE_DIGITS


def remove_parens(tokens):
    new_tokens = []
    open_parens = 0
    for t, c in tokens:
        if c == token_types.PUNCT_OPEN:
            open_parens += 1
        elif c == token_types.PUNCT_CLOSE:
            if open_parens > 0:
                open_parens -= 1
        elif open_parens <= 0:
            new_tokens.append((t, c))
    return new_tokens


def normalize_string(s, string_options=DEFAULT_STRING_OPTIONS):
    s = safe_decode(s)
    if string_options & _normalize.NORMALIZE_STRING_LATIN_ASCII:
        normalized = _normalize.normalize_string_latin(s, string_options)
    else:
        normalized = _normalize.normalize_string_utf8(s, string_options)

    return normalized


def normalized_tokens(s, string_options=DEFAULT_STRING_OPTIONS,
                      token_options=DEFAULT_TOKEN_OPTIONS,
                      strip_parentheticals=True):
    '''
    Normalizes a string, tokenizes, and normalizes each token
    with string and token-level options.

    This version only uses libpostal's deterministic normalizations
    i.e. methods with a single output. The string tree version will
    return multiple normalized strings, each with tokens.

    Usage:
        normalized_tokens(u'St.-Barthélemy')
    '''
    normalized = normalize_string(s, string_options=string_options)

    # Tuples of (offset, len, type)
    raw_tokens = tokenize_raw(normalized)
    tokens = [(_normalize.normalize_token(normalized, t, token_options),
               token_types.from_id(t[-1])) for t in raw_tokens]

    if strip_parentheticals:
        return remove_parens(tokens)
    else:
        return tokens
