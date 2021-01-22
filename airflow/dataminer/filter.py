import re

# stopwords support constant and regexpr
stopwords = [
    "많이",
    "조금",
    # re.compile(r"""""")
]

retype = type(re.compile(''))

def filterStopwords(x):
    for item in stopwords:
        if isinstance(item, retype):
            if (re.match(item, x)):
                return False
        else:
            if item == x:
                return False
    return True