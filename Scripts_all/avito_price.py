from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
some_list = []
count = 0

with open(file='../result.txt', mode='w', encoding='utf-8') as file:
    file.write('Url' + '\t' + 'Price' + '\t' + 'Views' + '\n')

with open(file='../input.txt', mode='r', encoding='utf-8') as ff:
    for url in ff:
        url = url.replace('\n', '')
        some_list.append(url)
while True:
    driver.get(some_list[count])
    count += 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if count == int(len(some_list)):
        break
    try:
        price_fresh = soup.find_all('span', attrs={'class': 'price-value-string js-price-value-string'})[0].get_text()
        final_price = str(price_fresh).replace('\n', '').replace('\t', '').replace('  ', '')
        views_fresh = soup.find('div', attrs={'class': 'title-info-metadata-item title-info-metadata-views'})
        final_views = str(views_fresh).split('</i>')[1].split('</div>')[0]
        with open(file='../result.txt', mode='a', encoding='utf-8') as file:
            file.write(some_list[count - 1] + '\t' + final_price + '\t' + final_views + '\n')
    except IndexError:
        if 'Доступ временно заблокирован' in str(soup):
            input('Нужно ввести капчу и нажать Enter')
            count -= 1
        else:
            with open(file='../result.txt', mode='a', encoding='utf-8') as file:
                file.write(some_list[count - 1] + '\t' + 'С этой ссылкой что-то не то, проверь вручную\n')
driver.quit()
