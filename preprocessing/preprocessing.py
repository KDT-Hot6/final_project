import re

# 한글만 추출
def preprocessing(text):
    hangle = re.compile('[^ ㄱ-ㅣ가-힣]+')
    return hangle.sub('', text)


#
# def 