### Deprecated
### use pandoc extension
### +east_asian_line_breaks
### instead

from panflute import *

import re
# Regular Expressions
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions

# 2000-206F General Punctuation
# 3000-303F 中日韓符號和標點
# 3040-309F 日文平假名 (V)
# 30A0-30FF 日文片假名 (V)
# 3100-312F 注音字母 (V)
# 31C0-31EF 中日韓筆畫
# 31F0-31FF 日文片假名語音擴展
# 3200-32FF 帶圈中日韓字母和月份 (V)
# 3400-4DBF 中日韓統一表意文字擴展 A (V)
# 4E00-9FFF 中日韓統一表意文字 (V)
# AC00-D7AF 諺文音節 (韓文)
# F900-FAFF 中日韓兼容表意文字 (V)
# FF00-FFEE Halfwidth and Fullwidth Forms
# http://unicode-table.com/cn/
# copied from https://github.com/huei90/pangu.node/blob/master/pangunode.js

import sys
import io
sys.stderr = io.TextIOWrapper(sys.stderr.buffer,encoding='utf8')

cjk_chars = re.compile( "([\u2000-\u206f\u3000-\u312F\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffee])")

def action(elem, doc):
    if isinstance(elem, Para):
      newContent = containers.ListContainer()
      for prev, curr in zip([None] + elem.content.list, elem.content):
        #print(prev, curr, file=sys.stderr)
        #print("==========", file=sys.stderr)
        if (prev and
            isinstance(curr, SoftBreak) and 
            "text" in prev.__slots__ and
            cjk_chars.match(prev.text[-1])
           ):
           pass
        else:
          newContent.append(curr)

      elem.content = newContent
      #print(elem.content, file=sys.stderr)
    
def finalize(doc):
    #print(doc.content, file=sys.stderr)
    pass

def main(doc=None):
    return run_filter(action, finalize=finalize, doc=doc)


# pandoc -f markdown-smart -t html-smart --filter pandoc-fix-CJK-filter.py source/_posts/Number-Theory-and-Public-Key-Cryptography-01-Time-Complexity-of-Arithmetic.md -o tmp
if __name__ == '__main__':
    main()