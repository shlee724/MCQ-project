import fitz  # PyMuPDF

def save_all_text_attributes_to_file(pdf_path, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        doc = fitz.open(pdf_path)
        
        for page_num, page in enumerate(doc):
            text_instances = page.get_text("dict")['blocks']
            
            for instance in text_instances:
                if 'lines' in instance:
                    for line in instance['lines']:
                        for span in line['spans']:
                            # 텍스트와 관련된 주요 속성 추출
                            text = span['text']
                            font = span['font']  # 폰트 이름
                            size = span['size']  # 폰트 크기

                            print(text.__class__)
                            print(font.__class__)
                            print(size.__class__)

                            bold = 'Bold' in font or 'bold' in font.lower()  # 굵기
                            italic = 'Italic' in font or 'italic' in font.lower()  # 기울기
                            color = span['color']  # 텍스트 색상
                            underline = span['flags'] & 4 != 0  # 밑줄 여부
                            bbox = span['bbox']  # 텍스트 박스 좌표

                            print(color.__class__)

                            # 파일에 정보 쓰기
                            f.write(f"Page {page_num+1}: '{text}'\n")
                            f.write(f"    Font: {font}, Size: {size}, Bold: {bold}, Italic: {italic}, Color: {color}, Underline: {underline}\n")
                            f.write(f"    Text Box: {bbox}\n")
                            f.write("    BBox Left-Top: ({}, {}), Right-Bottom: ({}, {})\n\n".format(bbox[0], bbox[1], bbox[2], bbox[3]))

# PDF 파일 경로
pdf_path = 'your_pdf_file.pdf'
# 출력할 텍스트 파일의 경로
output_file_path = 'output_all_text_attributes.txt'
save_all_text_attributes_to_file(pdf_path, output_file_path)
