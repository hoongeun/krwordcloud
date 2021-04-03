# 카테고리가 올바르지 않을 때


class InvalidCategory(Exception):
    def __init__(self, category):
        self.message = f'{category} is Invalid Category.'

    def __str__(self):
        return self.message

# 실행시간이 너무 길어서 데이터를 얻을 수 없을 때


class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return self.message
