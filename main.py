from japanese import japanese_to_romaji_with_accent
from korean import (
    join_jamos, j2hcj, h2j,
    latin_to_hangul,
    number_to_hangul,
    g2pk,
)
import re
import jaconv


repl_lst = {
    'ㄲ': 'ㅋ',
    'ㄸ': 'ㅌ',
    'ㅃ': 'ㅍ',
    'ㅆ': 'ㅅ',
    'ㅉ': 'ㅊ',
    'ㅓ': 'ㅗ',
    'ㅐ': 'ㅔ',
    'ㅡ': 'ㅜ',
    'ㄹㄹ':'ㄹ',
    'ㅙ': 'ㅗㅐ',
    'ㅚ': 'ㅗㅣ',
    'ㅝ': 'ㅜㅓ',
    'ㅞ': 'ㅜㅔ',
    'ㅟ': 'ㅜㅣ',
    'ㅢ': 'ㅡㅣ',
    'ㅒ': 'ㅣㅐ',
    'ㅕ': 'ㅣㅓ',
    'ㅖ': 'ㅣㅔ',
    'ㄹㅡㄹ':'루',
}


def get_word_list(text):
    text = latin_to_hangul(text)
    text = number_to_hangul(text)
    text = g2pk(text)
    text = '|'.join(text)
    text = j2hcj(h2j(text))
    text = re.sub(r'([\u3131-\u3163])$', r'\1.', text)
    return list(join_jamos(text.replace('  ', ' ')[:-1]))


def korean2katakana(text):
    word_lst = get_word_list(text)
    new_lst = []

    for s in word_lst:
        dh = list(j2hcj(h2j(s)))
        if len(dh) == 3:
            if dh[-1] in ['ㅁ', 'ㄴ', 'ㅇ']:
                dh[-1] = 'ㄴ'
            elif dh[-1] == 'ㄹ':
                dh[-1] = '루'
            else: # ㄱ ㄷ ㅂ
                dh[-1] = ''

        new_lst.extend(dh)

    kr = ''.join(new_lst)
    
    for k, v in repl_lst.items():
        kr = kr.replace(k, v)
            
    print('kr: ', kr)
    kr2ro = japanese_to_romaji_with_accent(kr).replace('si', 'shi').replace('c', 'ts') \
                                              .replace('ti', 'ティー').replace('tu', 'トゥー') \
                                              .replace('di', 'ディー').replace('du', 'ドゥー')
    result = jaconv.alphabet2kata(kr2ro).replace('|', '')
    return result

print(korean2katakana("안녕하세요."))