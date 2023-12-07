import re
from jamo import h2j, j2h
import os


############## Hangul ##############
def parse_table():
    '''Parse the main rule table'''
    with open(os.path.dirname(os.path.abspath(__file__)) + '/table.csv', 'r', encoding='utf8') as f:
        lines = f.read().splitlines()
        onsets = lines[0].split(",")
        table = []
        for line in lines[1:]:
            cols = line.split(",")
            coda = cols[0]
            for i, onset in enumerate(onsets):
                cell = cols[i]
                if len(cell) == 0: continue
                if i == 0:
                    continue
                else:
                    str1 = f"{coda}{onset}"
                    if "(" in cell:
                        str2 = cell.split("(")[0]
                        rule_ids = cell.split("(")[1][:-1].split("/")
                    else:
                        str2 = cell
                        rule_ids = []

                    table.append((str1, str2, rule_ids))

    return table


############## Preprocessing ##############
def annotate(string, mecab):
    tokens = mecab.pos(string)
    if string.replace(" ", "") != "".join(token for token, _ in tokens):
        return string
    blanks = [i for i, char in enumerate(string) if char == " "]

    tag_seq = []
    for token, tag in tokens:
        tag = tag.split("+")[-1]
        if tag == "NNBC":  # bound noun
            tag = "B"
        else:
            tag = tag[0]
        tag_seq.append("_" * (len(token) - 1) + tag)
    tag_seq = "".join(tag_seq)

    for i in blanks:
        tag_seq = tag_seq[:i] + " " + tag_seq[i:]

    annotated = ""
    for char, tag in zip(string, tag_seq):
        annotated += char
        if char == "의" and tag == "J":
            annotated += "/J"
        elif tag == "E":
            if h2j(char)[-1] in "ᆯ":
                annotated += "/E"
        elif tag == "V":
            if h2j(char)[-1] in "ᆫᆬᆷᆱᆰᆲᆴ":
                annotated += "/P"
        elif tag == "B":  # bound noun
            annotated += "/B"

    return annotated


############## Postprocessing ##############
def compose(letters):
    # insert placeholder
    letters = re.sub("(^|[^\u1100-\u1112])([\u1161-\u1175])", r"\1ᄋ\2", letters)

    string = letters # assembled characters
    # c+v+c
    syls = set(re.findall("[\u1100-\u1112][\u1161-\u1175][\u11A8-\u11C2]", string))
    for syl in syls:
        string = string.replace(syl, j2h(*syl))

    # c+v
    syls = set(re.findall("[\u1100-\u1112][\u1161-\u1175]", string))
    for syl in syls:
        string = string.replace(syl, j2h(*syl))

    return string


def group(inp):
    '''For group_vowels=True
    Contemporarily, Korean speakers don't distinguish some vowels.
    '''
    inp = inp.replace("ᅢ", "ᅦ")
    inp = inp.replace("ᅤ", "ᅨ")
    inp = inp.replace("ᅫ", "ᅬ")
    inp = inp.replace("ᅰ", "ᅬ")

    return inp


############## Utilities ##############
def get_rule_id2text():
    '''for verbose=True'''
    with open(os.path.dirname(os.path.abspath(__file__)) + '/rules.txt', 'r', encoding='utf8') as f:
        rules = f.read().strip().split("\n\n")
        rule_id2text = dict()
        for rule in rules:
            rule_id, texts = rule.splitlines()[0], rule.splitlines()[1:]
            rule_id2text[rule_id.strip()] = "\n".join(texts)
    return rule_id2text


def gloss(verbose, out, inp, rule):
    '''displays the process and relevant information'''
    if verbose and out != inp and out != re.sub("/[EJPB]", "", inp):
        print(compose(inp), "->", compose(out))
        print("\033[1;31m", rule, "\033[0m")




