# from ko2kana import korean2katakana
from jaconv import alphabet2kata
from g2pk3 import G2p
g2p = G2p()

_letters = 'ㅏㅓㅗㅜㅡㅣㅐㅔ '
'''
초성: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ
중성: ㅏㅐ ㅑㅒ ㅓㅔ ㅕㅖ ㅗㅘㅙㅚ ㅛ ㅜ ㅝㅞㅟ ㅠ ㅡㅢ ㅣ
종성: ㄱㄴㄷㄹㅁㅂㅇ
'''
a = g2p('아애야얘어에여예오와왜외요우워웨위유으의이')
b = g2p('아애야얘어에여예오와왜외요우워웨위유으의이', group_vowels=True)

chosung = {
    'ㄲ':'k',
    'ㄸ':'t',
    'ㅃ':'p',
    'ㅆ':'s',
    'ㅉ':'z',

    'ㄱ':'g',
    'ㄴ':'n',
    'ㄷ':'d',
    'ㄹ':'r',
    'ㅁ':'m',
    'ㅂ':'b',
    'ㅅ':'s',
    'ㅇ':'*',
    'ㅈ':'z',
    'ㅊ':'ts',
    'ㅋ':'k',
    'ㅌ':'t',
    'ㅍ':'p',
    'ㅎ':'h',
}
# 아애야얘어에여예오와왜외요우워웨위유으의이
# 아에야예어에여예오와외외요우워외위유으의이
joongsung = {
    # ㅏㅐ ㅑㅒ ㅓㅔ ㅕㅖ ㅗㅘㅙㅚ ㅛ ㅜ ㅝㅞㅟ ㅠ ㅡㅢ ㅣ
    'ㅏ': 'a',
    'ㅐ': 'e',
    'ㅑ': 'ya',
    'ㅒ': 'ye',
    'ㅓ': 'o',
    'ㅔ': 'e',
    'ㅕ': 'yo',
    'ㅖ': 'ye',
    'ㅗ': 'o',
    'ㅘ': 'wa',
    'ㅙ': 'we',
    'ㅚ': 'we',
    'ㅛ': 'yo',
    'ㅜ': 'u',
    'ㅝ':'wo',
    'ㅞ':'we',
    'ㅟ':'wi',
    'ㅠ': 'yu',
    'ㅡ': '_u',
    'ㅢ': '_u_i',
    'ㅣ': 'i'
}
jongsung = {
    'ㄱ': 'ッ', 
    'ㄴ': 'ン',
    'ㄷ': 'ッ',
    'ㄹ': 'ー',
    'ㅁ': 'ンー',
    'ㅂ': 'ッ',
    'ㅇ': 'ンー',
}
# print(
#     alphabet2kata(
# """
# ga gi gu ge go
# na ni nu ne no
# da d'i d'u de do
# ra ri ru re ro
# ma mi mu me mo
# ba bi bu be bo
# sa shi su se so
# a i u e o
# za zi zu ze zo
# tsa tsi tsu tse tso
# ka ki ku ke ko
# ta t'i t'u te to
# pa pi pu pe po
# ha hi hu he ho
# wa ui wu oe wo

# """
#     )
# )