import requests
from bs4 import BeautifulSoup
import datetime
import json

def get_soup(url):
    """
    URL에 접속하여 BeautifulSoup 객체를 반환합니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        # 타임아웃을 15초로 늘려 안정성을 확보합니다.
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"접속 에러 ({url}): {e}")
        return None

def scrape_korea_gold_exchange():
    """한국금거래소 시세 추출"""
    url = "https://www.koreagoldx.co.kr/"
    soup = get_soup(url)
    if not soup: return "데이터 없음"
    try:
        price = soup.select_one(".price_box .price_list li:first-child .price").text.strip()
        return price
    except:
        return "추출 실패"

def scrape_standard_gold():
    """한국표준금거래소 시세 추출"""
    url = "https://www.goldbars.co.kr/"
    soup = get_soup(url)
    if not soup: return "데이터 없음"
    try:
        price = soup.select_one(".today_price_list .buy_price").text.strip()
        return price
    except:
        return "추출 실패"

def scrape_jaeil_gold():
    """제일금거래소 시세 추출"""
    url = "http://goldcafe.co.kr/"
    soup = get_soup(url)
    if not soup: return "데이터 없음"
    try:
        price = soup.select_one(".price_table tr:nth-child(2) td:nth-child(2)").text.strip()
        return price
    except:
        return "추출 실패"

def scrape_jongro_gold():
    """종로금거래소 시세 추출"""
    url = "http://www.jongrogold.com/"
    soup = get_soup(url)
    if not soup: return "데이터 없음"
    try:
        price = soup.select_one(".main_price_box .price").text.strip()
        return price
    except:
        return "추출 실패"

def main():
    print(f"[{datetime.datetime.now()}] 금시세 데이터 수집 시작...")
    
    # 각 거래소의 데이터를 한 번씩만 수집합니다.
    prices = {
        "korea": scrape_korea_gold_exchange(),
        "standard": scrape_standard_gold(),
        "jaeil": scrape_jaeil_gold(),
        "jongro": scrape_jongro_gold()
    }

    # 최종 결과 데이터 구조 생성
    result_data = {
        "last_updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "prices": prices
    }

    # GitHub Actions 로그에서 확인할 수 있도록 출력
    print("수집된 데이터:")
    print(json.dumps(result_data, indent=4, ensure_ascii=False))

    # JSON 파일로 저장 (GitHub Actions가 이 파일을 커밋하게 됩니다)
    try:
        with open('gold_price.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        print("성공: gold_price.json 파일이 업데이트되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 에러 발생: {e}")

if __name__ == "__main__":
    main()
