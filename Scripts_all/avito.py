from bs4 import BeautifulSoup
from selenium import webdriver


count = 0
user_search = input('Введите запрос - ')
driver = webdriver.Chrome()
with open(file='../result.txt', mode='w', encoding='utf-8') as file:
    file.write('link' + '\t' + 'title' + '\t' + 'price' + '\t' + 'description' + '\n')
while True:
    count += 1
    driver.get(f'https://www.avito.ru/rossiya?q={user_search}&p={count}')
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    result = soup.find_all('div', attrs={'class': 'description item_table-description'})
    if len(result) == 0:
        driver.quit()
        break
    for item in result:
        soup1 = BeautifulSoup(str(item), 'html.parser')
        price = str(soup1.find_all('div', attrs={'class': 'snippet-price-row'})[0].text).replace('\t', '').replace('\n', '')
        title = str(soup1.find_all('div', attrs={'class': 'snippet-title-row'})[0].text).replace('\t', '').replace('\n', '')
        link = 'https://www.avito.ru' + str(soup1.find_all('a', attrs={'class': 'snippet-link'})[0]).split('href="')[1].split('" itemprop="url"')[0]
        try:
            description = str(soup1.find_all('div', attrs={'class': 'snippet-text'})[0].text).replace('\t', '').replace(
                '\n', '')
            with open(file='../result.txt', mode='a', encoding='utf-8') as file:
                file.write(link + '\t' + title + '\t' + price + '\t' + description + '\n')
        except IndexError:
            with open(file='../result.txt', mode='a', encoding='utf-8') as file:
                file.write(link + '\t' + title + '\t' + price + '\n')
