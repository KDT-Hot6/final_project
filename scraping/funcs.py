import re

def remove_space(text):
    text1 = re.sub('&nbsp;| &nbsp;|\n|\t|\r','',text)
    text2 = re.sub(',', '', text1)
    return text2


def extract_empathy(text):
    text1 = re.sub(' |\n', '', text)
    text2 = re.findall("\d+", text1)[0]
    return text2


def extract_feature(text):
    feature_list = []
    
    for feature in text.split('\n'):
        if re.findall('\d+', feature):
            idx = feature.index('(')
            feature_list.append(feature[:idx])
    return ' '.join(feature_list)


def extract_score(text):
    _1, s1, s2, s3, _2  = text.split("\n")
    return str(round((float(s1[1:]) + float(s2[2:]) + float(s3[3:])) / 3, 1))