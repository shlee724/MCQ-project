import fitz  # PyMuPDF

def modify_text_style(pdf_path, output_pdf_path, target_font, target_size, target_color, new_size, new_color):
    doc = fitz.open(pdf_path)
    
    # 타겟 색상과 새 색상을 RGB 튜플로 변환 (예: (1, 0, 0) -> 빨간색)
    #target_color_rgb = fitz.utils.getColor(target_color)
    #new_color_rgb = fitz.utils.getColor(new_color)
    
    for page in doc:
        text_instances = page.get_text("dict")['blocks']
        for instance in text_instances:
            if 'lines' in instance:
                for line in instance['lines']:
                    for span in line['spans']:
                        
                        color = span['color']
                        font = span['font']
                        size = span['size']


                        if font == target_font and size == target_size and color == target_color:
                            print("true")
                            # 기존 텍스트 삭제
                            rect = fitz.Rect(span['bbox'])
                            page.add_redact_annot(rect)
                            page.apply_redactions()
                            
                            # 새로운 스타일로 텍스트 추가
                            page.insert_text(rect.bl,  # 위치
                                             span['text'],  # 텍스트
                                             fontname="helv",  # 폰트 (helv는 Helvetica의 축약형)
                                             fontsize=new_size,  # 새 폰트 사이즈
                                             color=new_color)  # 새 색상
    
    doc.save(output_pdf_path)  # 수정된 PDF 저장

# 사용 예
pdf_path = 'your_pdf_file.pdf'
output_pdf_path = 'modified_pdf_file.pdf'
target_font = 'font000000002ac560db'  # 찾고자 하는 텍스트의 폰트
target_size = 13.5  # 찾고자 하는 텍스트의 사이즈
target_color = 26034  # 찾고자 하는 텍스트의 색깔
new_size = 11.25  # 변경할 텍스트의 새 사이즈
new_color = 0  # 변경할 텍스트의 새 색깔

modify_text_style(pdf_path, output_pdf_path, target_font, target_size, target_color, new_size, new_color)
