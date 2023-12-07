from g2pk3 import G2p
import unicodedata
from g2pk3.korean import join_jamos
g2p = G2p()

'''
ᄁ,ᄏ
ᄄ,ᄐ
ᄈ,ᄑ
ᄊ,ᄉ
ᄍ,ᄎ
ᆨ,ッ
ᆫ,ン
ᆮ,ッ
ᆯ,ー
ᆷ,ンー
ᆸ,ッ
ᆼ,ンー
'''

text = ''
text = g2p(text)
text = unicodedata.normalize('NFD', text)
f = open('repl.csv', 'r', encoding='utf-8').read().split('\n')
for i in f:
    k, v = i.split(',')
    text = text.replace(k, v)
print(text)