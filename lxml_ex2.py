import requests
from lxml.html import fromstring
#from pandas import Series, DataFrame
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
url = 'https://web.kangnam.ac.kr/'
response = requests.get(url, headers=headers) #유저 에이전트 적용

doc = fromstring(response.text)

result = doc.xpath('//*[@id="portal_main_notice2_list"]/li[1]/ul')

titles = result[0].xpath('.//li/div/a[@class="txt"]/text()')
second = result[0].text_content().replace('\t','') #test_content로 xpath또 지정 안해줘도 바로 문자열 뽑아줄 수 있다.
# df = pd.DataFrame(second, columns=['title'])
# print(df)
test = []
apple = {'\t': '', '\n':'', '\r':''}

for a in range(len(titles)):
    transtable = titles[a].maketrans(apple)
    test.append(titles[a].translate(transtable))


df = pd.DataFrame(test, columns=['title'])
print(df)



# test = []
# for b in range(len(titles)):
#     test.append(titles[b])
# print(len(titles)) #따로 하위 태크의 xpath를 설정해서 크롤링
# for a in range(len(titles)):
#     print(test[a])

# total = []
# for title in result: #하위 태그를 설정하지 않아도 text만 크롤링 가능
#     total.append(title.text_content())
# print(total)

