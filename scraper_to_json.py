import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import re

def get_soup(url):
    """
    URL에 접속하여 BeautifulSoup 객체를 반환합니다.
    브라우저처럼 보이기 위해 헤더를 보강합니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        # 인코딩 설정을 자동으로 맞춥니다.
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"접속 에러 ({url}): {e}")
        return None

def clean_price(text):
    """문자열에서 숫자와 콤마만 추출합니다."""
    if not text: return "추출 실패"
    # 숫자와 ,만 남기고 제거
    cleaned = re.sub(r'[^0-9,]', '', text)
    return f"{cleaned}원" if cleaned else "추출 실패"

def scrape_korea_gold_exchange():
    """한국금거래소 - 실시간 시세 테이블 분석"""
    url = "https://www.koreagoldx.co.kr/"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    try:
        # 현재 메인 페이지의 '내가 살 때' 순금 가격 (정확한 클래스 구조 반영)
        element = soup.select_one("ul.price_list li:nth-child(1) dd.price")
        if not element:
            element = soup.select_one(".price_box .price")
        return clean_price(element.get_text())
    except:
        return "추출 실패"

def scrape_standard_gold():
    """한국표준금거래소"""
    url = "https://www.goldbars.co.kr/"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    try:
        # 오늘 금시세 - 살때 가격
        element = soup.select_one(".today_price_list .buy_price")
        if not element:
            element = soup.select_one(".price_table_box .buy")
        return clean_price(element.get_text())
    except:
        return "추출 실패"

def scrape_jaeil_gold():
    """제일금거래소"""
    url = "http://goldcafe.co.kr/"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    try:
        # 메인 시세 테이블의 24k 살때 가격
        element = soup.select_one(".price_table tr:nth-child(2) td:nth-child(2)")
        return clean_price(element.get_text())
    except:
        return "추출 실패"

def scrape_jongro_gold():
    """종로금거래소"""
    url = "http://www.jongrogold.com/"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    try:
        # 메인 비주얼 옆 시세 정보
        element = soup.select_one(".main_price_box .price")
        if not element:
            element = soup.select_one(".today_price_area dd")
        return clean_price(element.get_text())
    except:
        return "추출 실패"

def main():
    print(f"[{datetime.datetime.now()}] 금시세 수집 시작 (24K 1돈 기준)")
    
    prices = {
        "korea": scrape_korea_gold_exchange(),
        "standard": scrape_standard_gold(),
        "jaeil": scrape_jaeil_gold(),
        "jongro": scrape_jongro_gold()
    }

    result_data = {
        "last_updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "prices": prices
    }

    print("수집 완료:", json.dumps(result_data, indent=4, ensure_ascii=False))

    try:
        file_path = os.path.join(os.getcwd(), 'gold_price.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        print(f"파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"저장 에러: {e}")

if __name__ == "__main__":
    main()
