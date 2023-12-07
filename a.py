import re

def replace_multiple(input_str, replacement_dict):
    pattern = re.compile("|".join([re.escape(k) for k in replacement_dict.keys()]))
    print("|".join([re.escape(k) for k in replacement_dict.keys()]))
    result = pattern.sub(lambda m: replacement_dict[m.group(0)], input_str)
    return result

# 테스트
original_text = "apple, cat, elephant"
replacement_dict = {"a": "b", "c": "d", "e": "f"}

result = replace_multiple(original_text, replacement_dict)
print(result)

import jaconv