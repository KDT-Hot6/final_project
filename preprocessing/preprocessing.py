import re

def preprocessing(text):
    hangle = re.compile('[^ ㄱ-ㅣ가-힣]+')
    return hangle.sub('', text)