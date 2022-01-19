#from typing import get_args
import requests
from lxml.html import fromstring, tostring

def main():
    session = requests.Session()
    #세션이란 : 세션정보를 갖고 흐름이 끊기지 않도록(로그인이 계속외어있는 상태
    response = session.get("https://kin.naver.com/search/list.nhn?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC")
    #스크랩핑 대상 url

    #링크 리스트 획득
    urls = scrape_news_list_page(response)

    #print(urls)

    for name, url in urls.items():
        #url 출력
        print(name, url)

def scrape_news_list_page(response):
    urls = {}
    #urls 딕셔너리 선언
    print("response = ",response.content)
    #태그정보 문자열 저장
    root = fromstring(response.content)
    print("root = ", root)
    #for a in root.xpath('//ul[@class="basic1"]/li/dl/dt/a[@class="_nclicks:kin.txt _searchListTitleAnchor"]'): #제목이랑 url 모두 크롤링
    for a in root.xpath('//ul[@class="basic1"]/li/dl/dd[@class="txt_inline"]'):
        #구조에 따라서 바꿔줘야함 원하는 부분의 class가 있는 하위 테그를 집어넣어주면됨
        #이건 링크 크롤링이 안됨 날짜만 가능

        #print(tostring(a, pretty_print=True))
        name, url = extract_contents(a)
        #딕셔너리 삽입
        urls[name] = url

    return urls

def extract_contents(dom):
    #링크주소
    link = dom.get("href")

    name = dom.text_content()

    return name, link

if __name__ == '__main__':
    main()