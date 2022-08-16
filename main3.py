import time

start_time = time.time()
import sys

# sys.path.append('/usr/lib/python3/dist-packages/beautifulsoup4')
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By



#set chromodriver.exe path
driver = webdriver.Chrome(executable_path="/Users/obaylan/PycharmProjects/scrapLegalNet/venv/chromedriver")
#implicit wait
driver.implicitly_wait(0.5)
#maximize browser
driver.maximize_window()
#launch URL
driver.get(' https://legalbank.net/arama/mahkeme-kararlari')
#identify element


def next_page():
    element = driver.find_element(By.XPATH,'//*[@id="content_content_pgr_btnPagerNext"]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.find_element(By.XPATH,'//*[@id="content_content_pgr_btnPagerNext"]').click();
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    return soup


def get_data(links, num):
    cnt=0
    for link in links:
        html_text = requests.get(link).content.decode('utf-8')
        text = BeautifulSoup(html_text, 'lxml')
        try:
            res = text.find('div', class_='belge').text
        except:
            res = 'NO BELGE'
        last_char = str(num)+ str(cnt)+ ".txt"
        print(last_char)
        # print('Last character : ', last_char)
        with open(last_char, "w") as file:
            file.write(str(res))
            file.close()
        cnt = cnt+1
        # except IOError:
        #     print(last_char)


content = requests.get(' https://legalbank.net/arama/mahkeme-kararlari').content
soup = BeautifulSoup(content, 'lxml')
results = soup.find_all('div', class_='result')
result_a = []
links_list = []
# for result in results:
#     result_a.append(list(result.a.attrs.values())[0])
# for each in result_a:
#     links_list.append(f'{"https://legalbank.net/"}{each}')

# sub_lists = np.array_split(links_list, 2)

# pool = Pool()
# result1 = pool.apply_async(get_data, [sub_lists[0]])
# result2 = pool.apply_async(get_data, [sub_lists[1]])
# answer1 = result1.get()
# answer2 = result2.get()
get_data(links_list, 1)
for i in range(2, 2612):
    next_page()
print("--- %s seconds ---" % (time.time() - start_time))
for i in range(2612, 261812):
    soup = next_page()
    results = soup.find_all('div', class_='result')
    result_a = []
    links_list = []
    for result in results:
        result_a.append(list(result.a.attrs.values())[0])
    for each in result_a:
        links_list.append(f'{"https://legalbank.net/"}{each}')

    sub_lists = np.array_split(links_list, 2)

    pool = Pool()
    result1 = pool.apply_async(get_data, [sub_lists[0]])
    result2 = pool.apply_async(get_data, [sub_lists[1]])
    answer1 = result1.get()
    answer2 = result2.get()


    get_data(links_list, i)

    print("--- %s seconds ---" % (time.time() - start_time), " COUNT=", i)

#close browser
driver.quit()
