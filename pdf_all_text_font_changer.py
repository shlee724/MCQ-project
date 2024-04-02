import fitz  # PyMuPDF

def change_text_to_default_font(input_pdf_path, output_pdf_path):
    # PDF 문서 열기
    doc = fitz.open(input_pdf_path)
    
    # 첫 페이지에서 사용된 첫 번째 폰트 찾기
    first_page = doc[0]
    fonts = first_page.get_fonts()
    if not fonts:
        print("No fonts found on the first page. Exiting.")
        return
    default_font = fonts[0][0]  # 첫 번째 폰트의 이름을 기본 폰트로 사용
    
    # 각 페이지를 순회하면서 텍스트의 폰트 변경
    # 각 페이지를 순회하면서 텍스트의 폰트 변경
    for page in doc:
        # 페이지의 텍스트 블록들을 얻어옴
        text_instances = page.get_text("dict")["blocks"]
        
        # 기존의 모든 텍스트를 제거
        page.clean_contents()
        
        # 텍스트 블록들을 순회하면서 기본 폰트로 텍스트 추가
        for instance in text_instances:
            if instance["type"] == 0:  # Type 0은 텍스트를 의미
                # 'text' 키가 존재하는지 확인
                if "text" in instance:
                    text = instance["text"]
                    rect = fitz.Rect(instance["bbox"])
                    # 기본 폰트와 폰트 크기 지정하여 텍스트 추가
                    page.insert_text(rect.tl, text, fontname=default_font, fontsize=11)

    # 변경된 문서를 새 파일로 저장
    doc.save(output_pdf_path)
    doc.close()

# 사용 예시
input_pdf_path = 'example.pdf'
output_pdf_path = 'your_output_pdf_with_default_font.pdf'

change_text_to_default_font(input_pdf_path, output_pdf_path)

