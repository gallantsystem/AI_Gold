import requests
from bs4 import BeautifulSoup
import datetime
import json
import os
import re

def get_soup(url):
    """
    URL에 접속하여 BeautifulSoup 객체를 반환합니다.
    브라우저처럼 보이게 하기 위해 좀 더 일반적인 헤더를 설정합니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.naver.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"접속 에러 ({url}): {e}")
        return None

def clean_price(text):
    """문자열에서 숫자와 콤마만 추출하여 리턴합니다."""
    if not text: return "정보 없음"
    cleaned = re.sub(r'[^0-9,]', '', text)
    return f"{cleaned}원" if cleaned else "정보 없음"

def scrape_naver_gold():
    """
    네이버 증권의 금시세 페이지를 활용합니다. (국내 순금 시세)
    이 방식은 여러 거래소의 기준점이 되어 가장 안정적입니다.
    """
    url = "https://finance.naver.com/marketindex/goldDetail.naver"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    
    try:
        # 네이버 금융의 금시세 텍스트 추출
        element = soup.select_one(".item_main .value")
        if element:
            return clean_price(element.get_text())
        return "추출 실패(Selector)"
    except:
        return "추출 실패"

def scrape_gold_korea():
    """한국금거래소 (대체 경로 - 모바일 인터페이스 등)"""
    url = "https://m.koreagoldx.co.kr/"
    soup = get_soup(url)
    if not soup: return "접속 실패"
    try:
        # 모바일 페이지는 구조가 단순하여 차단이 덜할 수 있습니다.
        element = soup.select_one(".price_list .price")
        return clean_price(element.get_text()) if element else "추출 실패"
    except:
        return "추출 실패"

def main():
    print(f"[{datetime.datetime.now()}] 안정적 경로를 통한 금시세 수집 시작...")
    
    # 네이버 시세와 기존 거래소 중 비교적 안정적인 경로를 조합합니다.
    # 개별 사이트 차단을 대비해 네이버 증권 데이터를 '기준 시세'로 활용하는 것을 권장합니다.
    prices = {
        "standard_reference": scrape_naver_gold(),  # 네이버 제공 기준 시세
        "korea_exchange": scrape_gold_korea(),      # 한국금거래소(모바일경로)
        "intl_gold": "준비 중"                       # 필요 시 국제 시세 추가 가능
    }

    # 결과 데이터 구조
    result_data = {
        "last_updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "prices": {
            "korea": prices["standard_reference"], # 대시보드 호환을 위해 키값 유지
            "standard": prices["standard_reference"],
            "jaeil": prices["korea_exchange"],
            "jongro": prices["standard_reference"]
        }
    }

    print("수집 결과:", json.dumps(result_data, indent=4, ensure_ascii=False))

    try:
        file_path = os.path.join(os.getcwd(), 'gold_price.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        print(f"파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"저장 에러: {e}")

if __name__ == "__main__":
    main()
