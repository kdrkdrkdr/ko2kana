from .japanese import japanese_to_romaji_with_accent
from .korean import (
    join_jamos, j2hcj, h2j,
    latin_to_hangul,
    number_to_hangul,
    g2pk,
)
import re
import jaconv


pre_repl = {
    'ㄲ': 'ㅋ',
    'ㄸ': 'ㅌ',
    'ㅃ': 'ㅍ',
    'ㅆ': 'ㅅ',
    'ㅉ': 'ㅊ',
    
    'ㅙ': 'ㅗ/ㅔ',
    'ㅚ': 'ㅗ/ㅣ',
    'ㅘ': 'ㅜㅏ',
    'ㅝ': 'ㅜ/ㅓ',
    'ㅞ': 'ㅜ/ㅔ',
    'ㅟ': 'ㅜ*ㅣ',
    'ㅢ': 'ㅡ*ㅣ',

    'ㅒ': 'ㅣ*ㅔ',
    'ㅖ': 'ㅣ*ㅔ',
    'ㅕ': 'ㅛ',
    'ㅑ': 'ㅣ*ㅏ',
    'ㅛ': 'ㅣ*ㅗ',

    'ㅓ': 'ㅏ',
    'ㅐ': 'ㅔ',
    'ㅡ': 'ㅜ',

    # '||//ㅎ': 'ㄹ',
}
# ァ, ィ, ゥ, ェ, ォ, ャ, ュ, ョ

post_repl = {
    'j': 'z',
    'si': 'shi',
    'cu': 'tsu',
    'c': 'ch',

    'i*a': 'ya',
    'i*u': 'yu',
    'i*o': 'yo',
    'i*e': 'ye',

    'ty': 'ti*',
    'dy': 'di*',

    '*a': 'ァ',
    '*i': 'ィ',
    '*u': 'ゥ',
    '*e': 'ェ',
    '*o': 'ォ',

    'ti': 'ティ',
    'tu': 'トゥ',
    'di': 'ディ',
    'du': 'ドゥ',

    'chy': 'chiy',
    'chiye': 'chie',
}

def get_word_list(text):
    text = latin_to_hangul(text)
    text = number_to_hangul(text)
    text = g2pk(text)
    text = j2hcj(h2j(text))
    text = re.sub(r'([\u3131-\u3163])$', r'\1.', text)
    return list(join_jamos(text.replace('  ', ' ')[:-1]))


def korean2katakana(text):
    word_lst = get_word_list(text)
    text = '/' + text.replace('/', ' ').replace('|', ' ').replace('^', ' ').replace('  ', ' ').replace(' ', '^')
    new_lst = []

    for i, s in enumerate(word_lst):
        dh = list(j2hcj(h2j(s)))
        if len(dh) == 3:
            if dh[-1] == 'ㄴ':
                dh[-1] = 'ㄴ'
                
            elif dh[-1] == 'ㅁ' or dh[-1] == 'ㅇ':
                dh[-1] = 'ㄴ|'
            
            elif dh[-1] == 'ㄹ':
                dh[-1] = '||/'

            else: # ㄱ ㄷ ㅂ
                dh[-1] = dh[-1]

        
        dh.append('/')
        new_lst.extend(dh)

    kr = ''.join(new_lst)
    for k, v in pre_repl.items():
        kr = kr.replace(k, v)

    kr2ro = japanese_to_romaji_with_accent(kr)

    for k, v in post_repl.items():
        kr2ro = kr2ro.replace(k, v)
    
    result = jaconv.alphabet2kata(kr2ro)
    result = result.replace('/', '').replace('|', 'ー').replace('^', '')
    return result


if __name__ == '__main__': 
    print(korean2katakana("안녕하세요")) # -> アンニョンーハセヨ