class Paper(object):
    def __init__(self, href, title):
        self.herf = href
        self.title = title

    def __str__(self) -> str:
        return "title={title} herf={herf}".format(title=self.title, herf=self.herf)

class Issue(object):
    def __init__(self, href=None, title=None):
        self.herf:str = href
        self.title:str = title
        self.papers:list[Paper] = []

    def set_url(self, href):
        self.herf = href

    def add_paper(self, paper:Paper):
        self.papers.append(paper)

    def __str__(self) -> str:
        s = []
        for paper in self.papers:
            s.append(str(paper))
        return str(s)


class Volumes(object):
    def __init__(self, title):
        self.title = title
        self.issue = []