import re
import unicodedata
from g2p_en import G2p as G2pEn
from .g2pk3 import G2p as G2pKo
from .english import convert_eng

g2p_en = G2pEn()
g2p_ko = G2pKo()

ko_dict = {
    'ᄁ': 'ᄏ',
    'ᄄ': 'ᄐ',
    'ᄈ': 'ᄑ',
    'ᄊ': 'ᄉ',
    'ᄍ': 'ᄎ',
    'ᅢ': 'ᅦ',
    'ᅤ': 'ᅨ',
    'ᅥ': 'ᅩ',
    'ᅧ': 'ᅭ',
    'ᅫ': 'ᅬ',
    'ᅰ': 'ᅬ',
    'ᅳ': 'ᅮ',
    'ᅴ': 'ᅱ',

    '가': 'ガ',
    '갸': 'ギャ',
    '게': 'ゲ',
    '계': 'ギェ',
    '고': 'ゴ',
    '과': 'グァ',
    '괴': 'グェ',
    '교': 'ギョ',
    '구': 'グ',
    '궈': 'グォ',
    '귀': 'グィ',
    '규': 'ギュ',
    '기': 'ギ',

    '나': 'ナ',
    '냐': 'ニャ',
    '네': 'ネ',
    '녜': 'ニェ',
    '노': 'ノ',
    '놔': 'ヌァ',
    '뇌': 'ヌェ',
    '뇨': 'ニョ',
    '누': 'ヌ',
    '눠': 'ヌォ',
    '뉘': 'ヌィ',
    '뉴': 'ニュ',
    '니': 'ニ',

    '다': 'ダ',
    '댜': 'デャ',
    '데': 'デ',
    '뎨': 'ディェ',
    '도': 'ド',
    '돠': 'ドゥァ',
    '되': 'ドゥェ',
    '됴': 'デョ',
    '두': 'ドゥ',
    '둬': 'ドゥォ',
    '뒤': 'ドゥィ',
    '듀': 'デュ',
    '디': 'ディ',

    '라': 'ラ',
    '랴': 'リャ',
    '레': 'レ',
    '례': 'リェ',
    '로': 'ロ',
    '롸': 'ルァ',
    '뢰': 'ルェ',
    '료': 'リョ',
    '루': 'ル',
    '뤄': 'ルォ',
    '뤼': 'ルィ',
    '류': 'リュ',
    '리': 'リ',

    '마': 'マ',
    '먀': 'ミャ',
    '메': 'メ',
    '몌': 'ミェ',
    '모': 'モ',
    '뫄': 'ムァ',
    '뫼': 'ムェ',
    '묘': 'ミョ',
    '무': 'ム',
    '뭐': 'ムォ',
    '뮈': 'ムィ',
    '뮤': 'ミュ',
    '미': 'ミ',

    '바': 'バ',
    '뱌': 'ビャ',
    '베': 'ベ',
    '볘': 'ビェ',
    '보': 'ボ',
    '봐': 'ブァ',
    '뵈': 'ブェ',
    '뵤': 'ビョ',
    '부': 'ブ',
    '붜': 'ブォ',
    '뷔': 'ブィ',
    '뷰': 'ビュ',
    '비': 'ビ',

    '사': 'サ',
    '샤': 'シャ',
    '세': 'セ',
    '셰': 'シェ',
    '소': 'ソ',
    '솨': 'スァ',
    '쇠': 'スェ',
    '쇼': 'ショ',
    '수': 'ス',
    '숴': 'スォ',
    '쉬': 'スゥィ',
    '슈': 'シュ',
    '시': 'シ',

    '아': 'ア',
    '야': 'ヤ',
    '에': 'エ',
    '예': 'イェ',
    '오': 'オ',
    '와': 'ワ',
    '외': 'ウェ',
    '요': 'ヨ',
    '우': 'ウ',
    '워': 'ウォ',
    '위': 'ウィ',
    '유': 'ユ',
    '이': 'イ',

    '자': 'ザ',
    '쟈': 'ジャ',
    '제': 'ゼ',
    '졔': 'ジェ',
    '조': 'ゾ',
    '좌': 'ズァ',
    '죄': 'ズェ',
    '죠': 'ジョ',
    '주': 'ズ',
    '줘': 'ズォ',
    '쥐': 'ズィ',
    '쥬': 'ジュ',
    '지': 'ジ',

    '차': 'シァ',
    '챠': 'チァ',
    '체': 'ツェ',
    '쳬': 'チェ',
    '초': 'ツォ',
    '촤': 'チュァ',
    '최': 'チュェ',
    '쵸': 'チォ',
    '추': 'ツ',
    '춰': 'チュォ',
    '취': 'チュィ',
    '츄': 'チュ',
    '치': 'チ',

    '카': 'カ',
    '캬': 'キャ',
    '케': 'ケ',
    '켸': 'キェ',
    '코': 'コ',
    '콰': 'クァ',
    '쾨': 'クェ',
    '쿄': 'キョ',
    '쿠': 'ク',
    '쿼': 'クォ',
    '퀴': 'クィ',
    '큐': 'キュ',
    '키': 'キ',

    '타': 'タ',
    '탸': 'テャ',
    '테': 'テ',
    '톄': 'ティェ',
    '토': 'ト',
    '톼': 'トァ',
    '퇴': 'トェ',
    '툐': 'テョ',
    '투': 'トゥ',
    '퉈': 'トォ',
    '튀': 'トィ',
    '튜': 'テュ',
    '티': 'ティ',

    '파': 'パ',
    '퍄': 'ピャ',
    '페': 'ペ',
    '폐': 'ピェ',
    '포': 'ポ',
    '퐈': 'プァ',
    '푀': 'プェ',
    '표': 'ピョ',
    '푸': 'プ',
    '풔': 'プォ',
    '퓌': 'プィ',
    '퓨': 'ピュ',
    '피': 'ピ',

    '하': 'ハ',
    '햐': 'ヒャ',
    '헤': 'ヘ',
    '혜': 'ヒェ',
    '호': 'ホ',
    '화': 'ファ',
    '회': 'フェ',
    '효': 'ヒョ',
    '후': 'フ',
    '훠': 'フォ',
    '휘': 'フィ',
    '휴': 'ヒュ',
    '히': 'ヒ',

    'ᆨ': 'ッー',
    'ᆫ': 'ン',
    'ᆮ': 'ッ',
    'ᆯ': 'ー',
    'ᆷ': 'ンー',
    'ᆸ': 'ッー',
    'ᆼ': 'ンー'
}

def korean2katakana(text: str):
    text = unicodedata.normalize('NFD', g2p_ko(text))
    for h, k in ko_dict.items():
        text = text.replace(h, k)
    return unicodedata.normalize('NFKC', text)

ja_vowel_dict = {
    'AA': 'A-',
    'AE': 'A',
    'AH': 'A',
    'AO': 'O-',
    'AW': 'AU',
    'AX': 'E',
    'AXR': 'A-',
    'AY': 'AI',
    'EH': 'E',
    'ER': 'A-',
    'EY': 'EI',
    'IH': 'I',
    'IX': 'I',
    'IY': 'I-',
    'OW': 'O-',
    'OY': 'OI',
    'UH': 'U',
    'UW': 'U-',
    'UX': 'U-'
}

ja_dict = {
    'A': 'ア',
    'I': 'イ',
    'U': 'ウ',
    'E': 'エ',
    'O': 'オ',

    'B':  'ブ',
    'BA': 'バ',
    'BI': 'ビ',
    'BU': 'ブ',
    'BE': 'ベ',
    'BO': 'ボ',

    'CH':  'チ',
    'CHA': 'チャ',
    'CHI': 'チ',
    'CHU': 'チュ',
    'CHE': 'チェ',
    'CHO': 'チョ',

    'D':  'ド',
    'DA': 'ダ',
    'DI': 'ディ',
    'DU': 'ドゥ',
    'DE': 'デ',
    'DO': 'ド',

    'DH':  'ズ',
    'DHA': 'ザ',
    'DHI': 'ジ',
    'DHU': 'ズ',
    'DHE': 'ゼ',
    'DHO': 'ゾ',

    'F':  'フ',
    'FA': 'ファ',
    'FI': 'フィ',
    'FU': 'フ',
    'FE': 'フェ',
    'FO': 'フォ',

    'G':  'グ',
    'GA': 'ガ',
    'GI': 'ギ',
    'GU': 'グ',
    'GE': 'ゲ',
    'GO': 'ゴ',

    'HH':  'ヒ',
    'HHA': 'ハ',
    'HHI': 'ヒ',
    'HHU': 'フ',
    'HHE': 'へ',
    'HHO': 'ホ',

    'JH':  'ジ',
    'JHA': 'ジャ',
    'JHI': 'ジ',
    'JHU': 'ジュ',
    'JHE': 'ジェ',
    'JHO': 'ジョ',

    'K':  'ク',
    'KA': 'カ',
    'KI': 'キ',
    'KU': 'ク',
    'KE': 'ケ',
    'KO': 'コ',

    'L':  'ル',
    'LA': 'ラ',
    'LI': 'リ',
    'LU': 'ル',
    'LE': 'レ',
    'LO': 'ロ',

    'M':  'ム',
    'MA': 'マ',
    'MI': 'ミ',
    'MU': 'ム',
    'ME': 'メ',
    'MO': 'モ',

    'N':  'ン',
    'NA': 'ナ',
    'NI': 'ニ',
    'NU': 'ヌ',
    'NE': 'ネ',
    'NO': 'ノ',

    'NG':  'ング',
    'NGA': 'ンガ',
    'NGI': 'ンギ',
    'NGU': 'ング',
    'NGE': 'ンゲ',
    'NGO': 'ンゴ',

    'P':  'プ',
    'PA': 'パ',
    'PI': 'ピ',
    'PU': 'プ',
    'PE': 'ペ',
    'PO': 'ポ',

    'R':  'ル',
    'RA': 'ラ',
    'RI': 'リ',
    'RU': 'ル',
    'RE': 'レ',
    'RO': 'ロ',

    'S':  'ス',
    'SA': 'サ',
    'SI': 'シ',
    'SU': 'ス',
    'SE': 'セ',
    'SO': 'ソ',

    'SH':  'シュ',
    'SHA': 'シャ',
    'SHI': 'シ',
    'SHU': 'シュ',
    'SHE': 'シェ',
    'SHO': 'ショ',

    'T':  'ト',
    'TA': 'タ',
    'TI': 'ティ',
    'TU': 'トゥ',
    'TE': 'テ',
    'TO': 'ト',

    'TH':  'ス',
    'THA': 'サ',
    'THI': 'シ',
    'THU': 'ス',
    'THE': 'セ',
    'THO': 'ソ',

    'TS':  'ツ',
    'TSA': 'ツァ',
    'TSI': 'ツィ',
    'TSU': 'ツ',
    'TSE': 'ツェ',
    'TSO': 'ツォ',

    'V':  'ヴ',
    'VA': 'ヴァ',
    'VI': 'ヴィ',
    'VU': 'ヴ',
    'VE': 'ヴェ',
    'VO': 'ヴォ',

    'W':  'ウ',
    'WA': 'ワ',
    'WI': 'ウィ',
    'WU': 'ウ',
    'WE': 'ウェ',
    'WO': 'ヲ',

    'WH':  'ホウ',
    'WHA': 'ホワ',
    'WHI': 'ホウィ',
    'WHU': 'ホウ',
    'WHE': 'ホウェ',
    'WHO': 'ホヲ',

    'Y':  'イ',
    'YA': 'ヤ',
    'YI': 'イ',
    'YU': 'ユ',
    'YE': 'イェ',
    'YO': 'ヨ',

    'Z':  'ズ',
    'ZA': 'ザ',
    'ZI': 'ジ',
    'ZU': 'ズ',
    'ZE': 'ゼ',
    'ZO': 'ゾ',

    'ZH':  'ジ',
    'ZHA': 'ジャ',
    'ZHI': 'ジ',
    'ZHU': 'ジュ',
    'ZHE': 'ジェ',
    'ZHO': 'ジョ',
    
    '-': 'ー'
}

ja_xtu_list = ['CH', 'D', 'JH', 'K', 'P', 'SH', 'T']

def english2katakana(text: str, accent_char=''):
    def dump_buf(buf, no_xtu):
        if len(buf) == 0:
            return ''
        out = 'ッ' if not no_xtu and buf[0] in ja_xtu_list else ''
        for i in range(len(buf)):
            tail = ''.join(buf[i:])
            if tail in ja_dict:
                out += ja_dict[tail]
                break
            out += ja_dict.get(buf[i], buf[i])
        return out

    out = ''
    buf = []
    arpabets = g2p_en(text)
    no_xtu = True
    for i in arpabets:
        if '0' <= i[-1] <= '9':
            # vowel
            vowel = ja_vowel_dict.get(i[:-1], '')
            long_vowel = len(vowel) >= 2
            if len(vowel) >= 1:
                buf.append(vowel[0])
                out += dump_buf(buf, no_xtu or len(buf) > 2)
                no_xtu = long_vowel
            if i[-1] == '1':
                out += accent_char
            if long_vowel:
                out += ja_dict.get(vowel[1], '')
            buf = []
        elif i == ' ':
            # word boundary
            out += dump_buf(buf, no_xtu or len(buf) > 1) + ' '
            buf = []
            no_xtu = True
        else:
            # consonant
            # speically handle NG in the middle
            # if G or K follows, replace the sequence with N G or N K
            if len(buf) > 0 and buf[-1] == 'NG' and (i == 'G' or i == 'K'): 
                buf = buf[:-1] + ['N', i]
            else:
                buf.append(i)
    # trailing 
    out += dump_buf(buf, no_xtu or len(buf) > 1)
    return out

def toKana(text: str, accent_char=''):
    ko_replaced = re.sub(
        "[가-힣]+", 
        lambda x: korean2katakana(x.group(0)), 
        text
    )
    en_replaced = re.sub(
        "([a-zA-Z']+ *)*[a-zA-Z']+", 
        lambda x: english2katakana(x.group(0), accent_char), 
        ko_replaced
    )
    return en_replaced

if __name__ == '__main__':
    print(toKana('Hello. こんいちわ。안녕하세요.')) # ハロー. こんいちわ。アンニョンーハセヨ.