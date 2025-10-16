# 이 프로그램 실행 전 터미널에 아래 명령어 입력해서
# 필수 라이브러리 설치해야 함.
# pip install PyPDF2 pdf2docx

# os와 glob 대신 pathlib의 Path 객체를 사용함.
from pathlib import Path

from pdf2docx import Converter
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


# 클래스(Class): PDF 처리 관련 모든 기능(메서드)을 담은 설계도임.
class PdfTool:
    """
    PDF 파일을 처리하는 다양한 기능을 제공하는 클래스입니다.
    - PDF 합치기, 분리하기, 순서 변경하기, Word로 변환하기
    """

    # 1. 특정 디렉토리 안의 모든 PDF 파일을 합치는 기능임.
    def merge_pdfs(self):
        print("\n--- PDF 합치기 ---")
        try:
            # input(): 사용자에게 디렉토리 경로를 입력받음.
            dir_path_str = input(
                "PDF 파일들이 있는 디렉토리(폴더)의 경로를 입력하세요:\n> "
            ).strip()
            # 입력받은 경로 문자열로 Path 객체를 생성함.
            dir_path = Path(dir_path_str)

            # Path.is_dir(): 해당 경로가 디렉토리인지 확인.
            if not dir_path.is_dir():
                # 디렉토리가 아니거나 없으면 에러 발생시킴.
                raise NotADirectoryError(f"유효한 디렉토리 경로가 아닙니다: {dir_path}")

            # Path.glob('*.pdf'): 디렉토리 내의 모든 .pdf 파일을 찾아 리스트로 만듦.
            # sorted(): 파일들을 이름순으로 정렬함.
            pdf_files = sorted(dir_path.glob("*.pdf"))

            if not pdf_files:
                print("해당 디렉토리에 PDF 파일이 없습니다.")
                return

            print("\n다음 파일들을 이름순으로 병합합니다:")
            for f in pdf_files:
                # Path.name: 전체 경로에서 파일 이름만 추출함.
                print(f"- {f.name}")

            # PdfMerger 객체 생성함.
            merger = PdfMerger()

            # for 반복문: 찾은 각 PDF 파일(Path 객체)에 대해 반복함.
            for pdf in pdf_files:
                merger.append(pdf)

            output_filename = input(
                "저장할 파일 이름을 입력하세요 (예: result.pdf):\n> "
            )
            output_path = Path(output_filename)
            merger.write(output_path)
            merger.close()

            # Path.resolve(): 파일의 절대 경로를 가져옴.
            absolute_path = output_path.resolve()
            print(f"성공! '{output_path.name}' 파일로 저장되었습니다.")
            print(f"저장된 전체 경로: {absolute_path}")

        except (NotADirectoryError, FileNotFoundError) as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 2. PDF 파일 페이지별로 분리하는 기능임.
    def split_pdf(self):
        print("\n--- PDF 분리하기 ---")
        try:
            file_path_str = input("분리할 PDF 파일의 경로를 입력하세요:\n> ")
            file_path = Path(file_path_str)

            if not file_path.exists():
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

            reader = PdfReader(file_path)
            total_pages = len(reader.pages)

            print(f"총 {total_pages}페이지의 문서를 분리합니다.")

            # for 반복문과 range(): 페이지 수만큼 반복함.
            output_files = []
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                # Path.stem: 확장자를 제외한 파일 이름.
                base_name = file_path.stem
                output_filename = f"{base_name}_page_{i + 1}.pdf"
                output_path = Path(output_filename)
                output_files.append(output_path)

                with open(output_path, "wb") as f:
                    writer.write(f)

            print(f"성공! 총 {total_pages}개의 파일로 분리되었습니다.")
            # 저장된 파일들의 절대 경로를 출력하도록 수정함.
            for f_path in output_files:
                print(f"저장된 파일 경로: {f_path.resolve()}")

        except FileNotFoundError as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 3. PDF 페이지 순서 변경하는 기능임.
    def reorder_pdf(self):
        print("\n--- PDF 페이지 순서 변경 ---")
        try:
            file_path_str = input("순서를 변경할 PDF 파일의 경로를 입력하세요:\n> ")
            file_path = Path(file_path_str)

            if not file_path.exists():
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
            output_path = Path(output_filename)
            with open(output_path, "wb") as f:
                writer.write(f)

            absolute_path = output_path.resolve()
            print(
                f"성공! 페이지 순서가 변경되어 '{output_path.name}'으로 저장되었습니다."
            )
            # 절대 경로 출력 추가함.
            print(f"저장된 전체 경로: {absolute_path}")

        except (FileNotFoundError, ValueError) as e:
            print(f"오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류가 발생했습니다: {e}")

    # 4. PDF를 Word(.docx)로 변환하는 기능임.
    def convert_to_docx(self):
        print("\n--- PDF를 Word 파일로 변환 ---")
        try:
            pdf_path_str = input("변환할 PDF 파일의 경로를 입력하세요:\n> ")
            pdf_path = Path(pdf_path_str)

            if not pdf_path.exists():
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

            # Path.with_suffix(): 파일의 확장자만 변경함.
            docx_path = pdf_path.with_suffix(".docx")

            print(
                f"'{docx_path.name}' 파일로 변환을 시작합니다. 파일 크기에 따라 시간이 걸릴 수 있습니다..."
            )

            # Converter 클래스 이용해 객체 생성함. 라이브러리가 문자열을 요구할 수 있으므로 str()로 변환.
            cv = Converter(str(pdf_path))
            cv.convert(str(docx_path))
            cv.close()

            absolute_path = docx_path.resolve()
            print(f"성공! '{docx_path.name}' 파일로 변환되었습니다.")
            # 절대 경로 출력 추가함.
            print(f"저장된 전체 경로: {absolute_path}")

        except FileNotFoundError as e:
            print(f"오류: {e}")
        except Exception as e:
            # 라이브러리 자체에서 발생하는 오류 처리함.
            print(f"변환 중 오류가 발생했습니다: {e}")


# 함수(Function): 프로그램 전체 흐름을 제어하는 메인 함수임.
def main():
    # 클래스로부터 객체(Object) 생성함.
    tool = PdfTool()

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
            tool.merge_pdfs()
        elif choice == "2":
            tool.split_pdf()
        elif choice == "3":
            tool.reorder_pdf()
        elif choice == "4":
            tool.convert_to_docx()
        elif choice == "5":
            print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
            break  # while 루프 빠져나감.
        else:
            print("잘못된 번호입니다. 1~5 사이의 숫자를 입력해주세요.")


# 이 스크립트 파일이 직접 실행될 때만 main() 함수 호출함.
if __name__ == "__main__":
    main()
