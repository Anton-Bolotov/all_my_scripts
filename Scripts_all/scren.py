from bs4 import BeautifulSoup
from selenium import webdriver


def create_list_of_links(list_with_url):
    with open(file='input.txt', mode='r', encoding='utf-8') as file:
        for url in file:
            url = url.replace('\n', '')
            list_with_url.append(url)
        return list_with_url


def main(list_with_url):
    url = create_list_of_links(list_with_url=list_with_url)
    driver = webdriver.Chrome()
    count = 0
    while True:
        try:
            driver.get(url[count])
            count += 1
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            if 'Soubor byl smazán' in str(soup):
                print(url[count - 1] + '\t' + 'Удалить')
            elif 'Súbor bol vymazaný' in str(soup):
                print(url[count - 1] + '\t' + 'Удалить')
            elif 'Plik został usunięty' in str(soup):
                print(url[count - 1] + '\t' + 'Удалить')
            else:
                try:
                    result = str(soup.find_all('div', attrs={'id': 'snippet--commentsSnippet'})[0].text).split('\n')[1]
                    if '(' in result:
                        print(url[count - 1] + '\t' + result)
                except IndexError:
                    input('Решите капчу и нажмите Enter')
                    count -= 1
        except IndexError:
            driver.quit()
            break


if __name__ == '__main__':
    some_list = []
    main(list_with_url=some_list)

