# coding:utf-8
# _author_:Junjie
# date:2019/2/26


class ListSet:
    def __init__(self, content):
        self.content = content
        self.deal()

    def deal(self):
        result = []
        title_url_list = []
        for one in self.content:
            if one:
                try:
                    if (one[0], one[1]) not in title_url_list:
                        title_url_list.append((one[0], one[1]))
                        result.append(one)
                except:
                    pass
        self.content = result