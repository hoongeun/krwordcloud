import re
import datetime


def parse_datetime(dtstr: str):
    min_ago = re.search("^([0-5]?[0-9])분전", dtstr)
    if min_ago:
        return datetime.now()
        - datetime.timedelta(minutes=int(min_ago.group()[0]))
    replaced = dtstr.replace("오전", "AM").replace("오후", "PM")
    return datetime.datetime.strptime(f"{replaced} GTM+0900",
                                      "%Y.%m.%d. %p %H:%M GTM%z")
