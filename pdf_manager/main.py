# 이 프로그램 실행 전 터미널에 아래 명령어 입력해서
# 필수 라이브러리 설치해야 함.
# pip install PyPDF2 pdf2docx

import os

from pdf2docx import Converter
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


# 클래스(Class): PDF 처리 관련 모든 기능(메서드)을 담은 설계도임.
class PdfManager:
    """
    PDF 파일을 처리하는 다양한 기능을 제공하는 클래스입니다.
    - PDF 합치기, 분리하기, 순서 변경하기, Word로 변환하기
    """

    # 1. 여러 PDF 파일 합치는 기능임.
    def merge_pdfs(self):
        print("\n--- PDF 합치기 ---")
        try:
            # input(): 사용자에게 파일 경로 입력받음.
            # .split(','): 쉼표 기준으로 잘라 리스트(list)로 만듦.
            file_paths = input(
                "합칠 PDF 파일들의 경로를 쉼표(,)로 구분하여 입력하세요:\n> "
            ).split(",")

            # strip()으로 각 경로 앞뒤 공백 제거함.
            file_paths = [path.strip() for path in file_paths]

            # PdfMerger 객체 생성함.
            merger = PdfMerger()

            # for 반복문: 리스트의 각 파일 경로에 대해 반복함.
            for path in file_paths:
                if not os.path.exists(path):
                    # 존재 안 하는 파일에 대한 예외 처리임.
                    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
                merger.append(path)

            output_filename = input(
                "저장할 파일 이름을 입력하세요 (예: result.pdf):\n> "
            )
            merger.write(output_filename)
            merger.close()

            # f-string: 변수 값을 문자열 안에 포함시킴.
            print(f"성공! '{output_filename}' 파일로 저장되었습니다.")

        except FileNotFoundError as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 2. PDF 파일 페이지별로 분리하는 기능임.
    def split_pdf(self):
        print("\n--- PDF 분리하기 ---")
        try:
            file_path = input("분리할 PDF 파일의 경로를 입력하세요:\n> ")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

            reader = PdfReader(file_path)
            total_pages = len(reader.pages)

            print(f"총 {total_pages}페이지의 문서를 분리합니다.")

            # for 반복문과 range(): 페이지 수만큼 반복함.
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                # os.path.splitext: 파일 이름과 확장자를 분리함.
                base_name, _ = os.path.splitext(file_path)
                output_filename = f"{base_name}_page_{i + 1}.pdf"

                with open(output_filename, "wb") as f:
                    writer.write(f)

            print(f"성공! 총 {total_pages}개의 파일로 분리되었습니다.")

        except FileNotFoundError as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 3. PDF 페이지 순서 변경하는 기능임.
    def reorder_pdf(self):
        print("\n--- PDF 페이지 순서 변경 ---")
        try:
            file_path = input("순서를 변경할 PDF 파일의 경로를 입력하세요:\n> ")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            print(
                f"총 {total_pages}페이지의 문서입니다. 페이지 번호는 1부터 시작합니다."
            )

            order_str = input(
                f"새로운 페이지 순서를 쉼표(,)로 구분하여 입력하세요 (예: 3,1,2,{total_pages}):\n> "
            )

            # list comprehension과 int() 써서 문자열 리스트를 숫자 리스트로 변환함.
            new_order = [int(p.strip()) for p in order_str.split(",")]

            # 유효성 검사임.
            if len(new_order) != total_pages or sorted(new_order) != list(
                range(1, total_pages + 1)
            ):
                raise ValueError(
                    "페이지 번호가 잘못되었습니다. 모든 페이지를 중복 없이 입력해야 합니다."
                )

            writer = PdfWriter()
            # 사용자는 1부터 시작하는 번호 입력하지만, 실제 인덱스는 0부터 시작하므로 1을 빼줘야 함.
            for page_num in new_order:
                writer.add_page(reader.pages[page_num - 1])

            output_filename = input(
                "저장할 파일 이름을 입력하세요 (예: reordered.pdf):\n> "
            )
            with open(output_filename, "wb") as f:
                writer.write(f)

            print(
                f"성공! 페이지 순서가 변경되어 '{output_filename}'으로 저장되었습니다."
            )

        except (FileNotFoundError, ValueError) as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 4. PDF를 Word(.docx)로 변환하는 기능임.
    def convert_to_docx(self):
        print("\n--- PDF를 Word 파일로 변환 ---")
        try:
            pdf_path = input("변환할 PDF 파일의 경로를 입력하세요:\n> ")

            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

            base_name, _ = os.path.splitext(pdf_path)
            docx_path = f"{base_name}.docx"

            print(
                f"'{docx_path}' 파일로 변환을 시작합니다. 파일 크기에 따라 시간이 걸릴 수 있습니다..."
            )

            # Converter 클래스 이용해 객체 생성함.
            cv = Converter(pdf_path)
            cv.convert(docx_path)
            cv.close()

            print(f"성공! '{docx_path}' 파일로 변환되었습니다.")

        except FileNotFoundError as e:
            print(f"오류: {e}")
        except Exception as e:
            # 라이브러리 자체에서 발생하는 오류 처리함.
            print(f"변환 중 오류가 발생했습니다: {e}")


# 함수(Function): 프로그램 전체 흐름을 제어하는 메인 함수임.
def main():
    # 클래스로부터 객체(Object) 생성함.
    manager = PdfManager()

    # while 반복문: 사용자가 종료 선택할 때까지 계속 실행함.
    while True:
        # print(): 사용자에게 보여줄 메뉴 출력함.
        print("\n" + "=" * 30)
        print("    나만의 PDF 처리 프로그램")
        print("=" * 30)
        print("1. PDF 파일 합치기")
        print("2. PDF 파일 분리하기")
        print("3. PDF 페이지 순서 변경하기")
        print("4. PDF를 Word 파일로 변환하기")
        print("5. 종료")
        print("=" * 30)

        choice = input("원하는 작업의 번호를 선택하세요: ")

        # if/elif/else 조건문: 사용자 선택에 따라 다른 기능 호출함.
        if choice == "1":
            manager.merge_pdfs()
        elif choice == "2":
            manager.split_pdf()
        elif choice == "3":
            manager.reorder_pdf()
        elif choice == "4":
            manager.convert_to_docx()
        elif choice == "5":
            print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
            break  # while 루프 빠져나감.
        else:
            print("잘못된 번호입니다. 1~5 사이의 숫자를 입력해주세요.")


# 이 스크립트 파일이 직접 실행될 때만 main() 함수 호출함.
if __name__ == "__main__":
    main()
