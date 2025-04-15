import MeCab


def char_split(text: str) -> str:
    return '\n'.join([' '.join(line) for line in text.splitlines()])


def mecab_split(text: str) -> str:
    mecab = MeCab.Tagger("-Owakati")
    return '\n'.join([' '.join(mecab.parse(line).split()) for line in text.splitlines()])
