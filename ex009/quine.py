#! /usr/bin/env python
apostrophe = '\''
src = '''#! /usr/bin/env python
apostrophe = {1}\{1}{1}
src = {1}{1}{1}{0}{1}{1}{1}
print src.format(src, apostrophe),
'''
print src.format(src, apostrophe),
