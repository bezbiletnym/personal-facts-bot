import requests, bs4, yaml, os
from classes.article import Article
import dotenv

def get_last_url() -> str:
    url = ''
    try:
        with open(file=LAST_URL_FILE) as f:
            file_data = yaml.safe_load(f)
            f.close()
            url = file_data.get('LAST_URL', '')
    except Exception as err:
        print(f"Unable to read last_url file: {repr(err)}")
    return url


def write_last_url(url: str):
    try:
       with open(file=LAST_URL_FILE, mode='w') as f:
           yaml.safe_dump(data={'LAST_URL': url}, stream=f)
           f.close()
    except Exception as err:
        print(f"Unable to write to last_url file: {repr(err)}")


def get_new_article() -> Article:
    response = requests.get(url=ARCHIVE_URL)
    data = response.content

    soup = bs4.BeautifulSoup(markup=data, features="html.parser")
    last_article_url = soup.find(name='article').a['href']
    if last_article_url == last_url:
        print("No new article is found, getting a random one...")
        last_article_url = get_random_article_url()
        is_from_archive = False
    else:
        print(f"Last article is {last_article_url}")
        is_from_archive = True
    article = Article(url=last_article_url, is_from_archive=is_from_archive)
    return article


def get_random_article_url():
    response = requests.get(url=RANDOM_URL)
    return response.links.get('shortlink', {}).get('url', '')


def send_tg_message(token: str, chat_id: int, article: Article) -> bool:
    tg_api_link = f"https://api.telegram.org/bot{token}/"
    message = f"<b>{article.header}</b>\n{article.url}"
    if article.pic is None:
        response = requests.post(url=f'{tg_api_link}sendMessage',
                                 json={'chat_id': chat_id,
                                        'text': message,
                                        'parse_mode': 'HTML',})
    else:
        response = requests.post(url=f'{tg_api_link}sendPhoto',
                                 json={'chat_id': chat_id,
                                        'caption': message,
                                        'parse_mode': 'HTML',
                                        'photo': article.pic,})
    print(response.content)
    return response.ok


ARCHIVE_URL='https://nowiknow.com/archives/'
RANDOM_URL='https://nowiknow.com/?random'
LAST_URL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "last_url.yaml")
dotenv.load_dotenv()
try_counter = 0
last_url = get_last_url()
new_article = get_new_article()

while try_counter < 5:
    try_counter += 1

    print(f"Attempt to send message #{try_counter}")
    send_result = send_tg_message(token=os.environ.get('BOT_TOKEN', ''), chat_id=int(os.environ.get('CHAT_ID', 0)), article=new_article)
    print("Message is sent" if send_result else "Something is wrong")
    if send_result:
        if new_article.is_from_archive:
            write_last_url(new_article.url)
        break

print("Script is finished")