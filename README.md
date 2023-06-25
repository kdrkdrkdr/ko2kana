# ko2kana
Tools for writing Korean pronunciation in katakana.

Replace Korean with Katakana so that you can read Korean in the TTS Japanese model.
Typically, when you create a multilingual TTS, you organize the text with an IPA cleaner. 
However, this method is awkward, inaccurate and if the pronunciation symbol is insufficient or absent, the voice is missing.
Therefore, only phonemes present in the TTS data were made close to the pronunciation of other languages.


## Requirements
* python >= 3.8
* jamo
* g2pk2
* cmake
* pyopenjtalk


## Installation
```bash
pip install ko2kana
```

## Usage

```python
from ko2kana import korean2katakana
s = korean2katakana("안녕하세요.")
print(s) 
'アンニョンーハセヨ'
```


## References
If you use our software for research, please cite:
```
@misc{kim2023ko2kana,
  author = {Kim, Gyeongmin},
  title = {ko2kana},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kdrkdrkdr/ko2kana}}
}```