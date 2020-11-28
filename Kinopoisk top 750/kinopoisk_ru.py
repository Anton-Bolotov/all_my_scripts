from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
count = 0
number = 0
print('№' + '\t' + 'Ссылка' + '\t' + 'Название' + '\t' + 'Название на английском' + '\t' + 'Год' + '\t' + 'Страна' + '\t' + 'Жанр')
while True:
    if count >= 27:
        driver.quit()
        break
    count += 1
    url = f'https://www.kinopoisk.ru/popular/films/?page={count}&sort=popularity&quick_filters=films&tab=all'

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result = soup.find_all('a', attrs={'class': 'selection-film-item-meta__link'})
    for urls in result:
        number += 1
        soup_2 = BeautifulSoup(str(urls), 'html.parser')
        link = 'https://www.kinopoisk.ru' + str(urls).split('href="')[1].split('"><p')[0]
        title_name = soup_2.find('p', attrs={'class': 'selection-film-item-meta__name'}).text
        eng_name = soup_2.find('p', attrs={'class': 'selection-film-item-meta__original-name'}).text
        year = eng_name[-5:]
        country = soup_2.find_all('span', attrs={'class': 'selection-film-item-meta__meta-additional-item'})[0].text
        genre = soup_2.find_all('span', attrs={'class': 'selection-film-item-meta__meta-additional-item'})[0].text
        print(str(number) + '\t' + link + '\t' + title_name + '\t' + eng_name + '\t' + year + '\t' + country + '\t' + genre)
