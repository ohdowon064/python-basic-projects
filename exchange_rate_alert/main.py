from datetime import datetime

import requests


# 클래스(Class) 정의: 환율 정보와 관련된 기능을 담는 설계도
class ExchangeRateAlert:
    """
    API를 통해 환율 정보를 가져오고 표시하는 기능을 담당하는 클래스임.
    - API_URL: 데이터를 가져올 서버의 주소
    - TARGET_CURRENCIES: 사용자에게 보여줄 주요 통화 목록
    """

    # 클래스 변수: 모든 객체가 공유하는 값
    API_URL = "https://api.frankfurter.app/latest"
    TARGET_CURRENCIES = ["KRW", "USD", "EUR", "JPY", "CNY", "ZWL"]

    # fetch_rates 메서드: API 서버에 환율 정보를 요청하고 결과를 반환함.
    def fetch_rates(self, base_currency):
        """
        지정된 기본 통화를 기준으로 최신 환율 정보를 가져옴.
        - base_currency: 기준이 되는 통화 코드 (예: 'USD')
        - 반환값: 성공 시 환율 데이터(dict), 실패 시 None
        """
        # try-except 예외 처리: 네트워크 연결 문제 등 예상치 못한 오류에 대비함.
        try:
            # f-string을 이용해 요청할 URL을 동적으로 만듦.
            params = {"from": base_currency}
            # requests 라이브러리를 사용해 API에 GET 요청을 보냄.
            response = requests.get(self.API_URL, params=params)

            # 응답 상태 코드가 200(성공)인지 확인함.
            response.raise_for_status()  # 200이 아니면 예외를 발생시킴.

            # JSON 형식의 응답 데이터를 파이썬 딕셔너리로 변환하여 반환함.
            return response.json()

        except requests.exceptions.HTTPError as e:
            # 존재하지 않는 통화 코드를 입력했을 때의 오류 처리
            if e.response.status_code == 404:
                print(f"오류: '{base_currency}'는 유효하지 않은 통화 코드입니다.")
            else:
                print(f"HTTP 오류가 발생했습니다: {e}")
            return None
        except requests.exceptions.RequestException as e:
            # 인터넷 연결 문제 등 네트워크 관련 오류 처리
            print(f"네트워크 오류가 발생했습니다: {e}")
            return None
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")
            return None

    # display_rates 메서드: 가져온 환율 정보를 보기 좋게 출력함.
    def display_rates(self, data):
        """
        API로부터 받은 환율 데이터를 화면에 출력함.
        - data: fetch_rates로부터 받은 딕셔너리 데이터
        """
        # if 조건문: 데이터가 유효한지 확인함.
        if not data or "rates" not in data:
            print("환율 정보를 가져오는 데 실패했습니다.")
            return

        base = data.get("base", "N/A")
        date_str = data.get("date", "N/A")

        # 날짜 형식을 보기 좋게 변환
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y년 %m월 %d일")
        except ValueError:
            formatted_date = date_str

        print("\n" + "=" * 30)
        print(f" 기준 통화: {base}")
        print(f" 기준 날짜: {formatted_date}")
        print("=" * 30)

        rates = data["rates"]

        # for 반복문: 미리 정해둔 주요 통화 목록을 순회하며 환율을 출력함.
        for currency in self.TARGET_CURRENCIES:
            # 기준 통화와 같은 경우는 건너뜀 (continue)
            if currency == base:
                continue

            rate = rates.get(currency)
            # if 조건문: 해당 통화 정보가 있는지 확인
            if rate:
                print(f"  1 {base} = {rate:.2f} {currency}")

        print("=" * 30)


# 함수(Function) 정의: 프로그램의 전체적인 흐름을 제어함.
def main():
    """
    프로그램의 메인 로직을 실행하는 함수.
    """
    # 클래스로부터 객체(Object)를 생성
    viewer = ExchangeRateViewer()

    print("실시간 환율 정보 알리미에 오신 것을 환영합니다.")

    # while 반복문: 사용자가 종료를 원할 때까지 계속 실행됨.
    while True:
        print("\n확인하고 싶은 기준 통화의 코드를 입력하세요.")
        base_currency = input(
            " (예: KRW, USD, JPY... | 종료하려면 'q' 입력)\n> "
        ).upper()

        if base_currency == "Q":
            print("프로그램을 종료합니다.")
            break

        # 클래스의 메서드를 호출하여 환율 정보를 가져옴.
        rate_data = viewer.fetch_rates(base_currency)

        # 가져온 데이터가 있을 경우에만 출력 메서드를 호출함.
        if rate_data:
            viewer.display_rates(rate_data)


# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출함.
if __name__ == "__main__":
    main()
