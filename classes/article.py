import requests, bs4

class Article: # Class for keeping an article data
    header: str
    url: str
    pic: str
    is_from_archive: bool

    def __init__(self, url: str, is_from_archive: bool):
        self.url = url
        self.is_from_archive = is_from_archive
        self.header, self.pic = self._get_article_data()

    def _get_article_data(self):
        response = requests.get(url=self.url)
        data = response.content
        soup = bs4.BeautifulSoup(markup=data, features="html.parser")
        article_block = soup.find(name='article')
        header = article_block.header.h1.text
        try:
            pic = article_block.div.find(name='img', recursive=True)['src']
        except Exception as err:
            print(repr(err))
            pic = None
        return header, pic



