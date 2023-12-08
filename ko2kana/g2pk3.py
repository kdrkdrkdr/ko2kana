# -*- coding: utf-8 -*-


import os, re, platform, sys, importlib
import subprocess

# import nltk
from jamo import h2j
from .special import jyeo, ye, consonant_ui, josa_ui, vowel_ui, jamo, rieulgiyeok, rieulbieub, verb_nieun, balb, palatalize, modifying_rieul
from .regular import link1, link2, link3, link4
from .utils import annotate, compose, group, gloss, parse_table, get_rule_id2text
from .english import convert_eng
from .korean import join_jamos, split_syllables
from .numerals import convert_num

 
class G2p(object):
    def __init__(self, use_konlpy=False, mecab_path=None):
        self.use_konlpy = use_konlpy
        self.mecab_path = mecab_path
        
        self.check_mecab()
        self.mecab = self.get_mecab()
        self.table = parse_table()

        # self.cmu = cmudict.dict() # for English

        self.rule2text = get_rule_id2text() # for comments of main rules
        self.idioms_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "idioms.txt")

    def load_module_func(self, module_name):
        tmp = __import__(module_name, fromlist=[module_name])
        return tmp

    def check_mecab(self):
        if self.use_konlpy:
            spam_spec = importlib.util.find_spec("konlpy")
            non_found = spam_spec is None
            if non_found:
                print(f'you have to install konlpy. install it...')
                p = subprocess.Popen([sys.executable, "-m", "pip", "install", 'konlpy'])
                p.wait()
            else:
                print("konlpy installed")
        else:
            if platform.system()=='Windows':
                spam_spec = importlib.util.find_spec("eunjeon")
                non_found = spam_spec is None
                if non_found:
                    print(f'you have to install eunjeon. install it...')
                    p = subprocess.Popen('pip install eunjeon')
                    p.wait()
            else:
                spam_spec = importlib.util.find_spec("mecab")
                non_found = spam_spec is None
                if non_found:
                    print(f'you have to install python-mecab-ko. install it...')
                    p = subprocess.Popen([sys.executable, "-m", "pip", "install", 'python-mecab-ko'])
                    p.wait()
                # else:
                    # print("mecab installed")


    def get_mecab(self):
        if self.use_konlpy:
            try:
                from konlpy.tag import Mecab
            except Exception as e:
                raise print(f'failed to load konlpy')
            try:
                if self.mecab_path:
                    return Mecab(self.mecab_path)
                else:
                    return Mecab()
            except Exception as e:
                raise print(f"failed to open konlpy.tag.Mecab")
        else:
            if platform.system() == 'Windows':
                try:
                    m = self.load_module_func('eunjeon')
                    return m.Mecab()
                except Exception as e:
                    raise print(f'you have to install eunjeon. "pip install eunjeon"')
            else:
                try:
                    m = self.load_module_func('mecab')
                    return m.MeCab()
                except Exception as e:
                    print("Failed to load python-mecab-ko:", e)


    def idioms(self, string, descriptive=False, verbose=False):
        '''Process each line in `idioms.txt`
        Each line is delimited by "===",
        and the left string is replaced by the right one.
        inp: input string.
        descriptive: not used.
        verbose: boolean.

        >>> idioms("지금 mp3 파일을 다운받고 있어요")
        지금 엠피쓰리 파일을 다운받고 있어요
        '''
        rule = "from idioms.txt"
        out = string

        with open(self.idioms_path, 'r', encoding="utf8") as f:
            for line in f:
                line = line.split("#")[0].strip()
                if "===" in line:
                    str1, str2 = line.split("===")
                    out = re.sub(str1, str2, out)
            gloss(verbose, out, string, rule)

        return out

    def __call__(self, string, descriptive=False, verbose=False, group_vowels=False, to_syl=True):
        '''Main function
        string: input string
        descriptive: boolean.
        verbose: boolean
        group_vowels: boolean. If True, the vowels of the identical sound are normalized.
        to_syl: boolean. If True, hangul letters or jamo are assembled to form syllables.

        For example, given an input string "나의 친구가 mp3 file 3개를 다운받고 있다",
        STEP 1. idioms
        -> 나의 친구가 엠피쓰리 file 3개를 다운받고 있다

        STEP 2. English to Hangul
        -> 나의 친구가 엠피쓰리 파일 3개를 다운받고 있다

        STEP 3. annotate
        -> 나의/J 친구가 엠피쓰리 파일 3개/B를 다운받고 있다

        STEP 4. Spell out arabic numbers
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 5. decompose
        -> 나의/J 친구가 엠피쓰리 파일 세개/B를 다운받고 있다

        STEP 6-9. Hangul
        -> 나의 친구가 엠피쓰리 파일 세개를 다운받꼬 읻따
        '''
        # 1. idioms
        string = self.idioms(string, descriptive, verbose)

        # 2 Convert English to Hangul
        string = convert_eng(string)

        # 3. annotate
        string = annotate(string, self.mecab)


        # 4. Spell out arabic numbers
        string = convert_num(string)

        # 5. decompose
        inp = h2j(string)

        # 6. special
        for func in (jyeo, ye, consonant_ui, josa_ui, vowel_ui, \
                     jamo, rieulgiyeok, rieulbieub, verb_nieun, \
                     balb, palatalize, modifying_rieul):
            inp = func(inp, descriptive, verbose)
        inp = re.sub("/[PJEB]", "", inp)

        # 7. regular table: batchim + onset
        for str1, str2, rule_ids in self.table:
            _inp = inp
            inp = re.sub(str1, str2, inp)

            if len(rule_ids)>0:
                rule = "\n".join(self.rule2text.get(rule_id, "") for rule_id in rule_ids)
            else:
                rule = ""
            gloss(verbose, inp, _inp, rule)

        # 8 link
        for func in (link1, link2, link3, link4):
            inp = func(inp, descriptive, verbose)

        # 8.5 Error Fix, 제 20항 적용 오류 해결
        inp_ = ""
        inp = split_syllables(inp.strip())
        i = 0
        while i < len(inp) - 4:
            if (inp[i:i+3] == 'ㅇㅡㄹ' or inp[i:i+3] == 'ㄹㅡㄹ') and inp[i+3] == ' ' and inp[i+4] == 'ㄹ':
                inp_ += inp[i:i+3] + ' ' + 'ㄴ'
                i += 5
            else:
                inp_ += inp[i]
                i += 1
        inp_ += inp[i:]
        inp = join_jamos(inp_)

        # 9. postprocessing
        if group_vowels:
            inp = group(inp)

        if to_syl:
            inp = compose(inp)
        return inp

if __name__ == "__main__":
    g2p = G2p(use_konlpy=True, mecab_ko_dic_path=r"/Volumes/NewVolumes/source/vits/mecab-ko-dic")
    a = g2p("나의 친구가 mp3 file 3개를 다운받고 있다")

    print(a)