import pdfplumber
import pandas as pd

def convert_pdf_to_excel(pdf_path, excel_path):
    # PDF 파일을 엽니다.
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        
        # 엑셀 파일에 쓸 준비를 합니다. with 문을 사용합니다.
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for i, page in enumerate(pages):
                # 페이지의 텍스트를 추출합니다.
                text = page.extract_text()
                if text:
                    # 텍스트를 줄바꿈으로 분리하여 DataFrame으로 변환합니다.
                    df = pd.DataFrame(text.split('\n'), columns=['Text'])
                    # 데이터프레임을 엑셀 시트로 저장합니다. 각 페이지마다 별도의 시트에 저장됩니다.
                    df.to_excel(writer, sheet_name=f'Page_{i + 1}', index=False)

# 사용 예시
pdf_path = 'your_pdf_file.pdf' # 변환할 PDF 파일 경로
excel_path = 'output_excel_file.xlsx' # 저장할 Excel 파일 경로

convert_pdf_to_excel(pdf_path, excel_path)
