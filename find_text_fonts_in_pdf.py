import fitz  # PyMuPDF

def print_text_attributes(pdf_path,output_file_path):
    # 출력 파일 열기(쓰기 모드)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        # PDF 파일 열기
        doc = fitz.open(pdf_path)
        
        for page_num, page in enumerate(doc):
            # 페이지의 텍스트 블록을 얻기 (블록에는 텍스트와 그 위치가 포함됨)
            text_instances = page.get_text("dict")['blocks']
            
            for instance in text_instances:
                if 'lines' in instance:  # 텍스트가 있는 경우만 처리
                    for line in instance['lines']:
                        for span in line['spans']:
                            text = span['text']
                            font = span['font']  # 폰트 이름
                            size = span['size']  # 폰트 크기
                            bold = 'Bold' in font  # 굵기 체크 (단순화된 방법)
                            bbox = span['bbox']  # 텍스트 박스 좌표
                            
                            print(f"Page {page_num+1}: '{text}'")
                            print(f"    Font: {font}, Size: {size}, Bold: {bold}")
                            print(f"    Text Box: {bbox}")
                            print("    BBox Left-Top: ({}, {}), Right-Bottom: ({}, {})\n".format(bbox[0], bbox[1], bbox[2], bbox[3]))
                            # 파일에 정보 쓰기
                            f.write(f"Page {page_num+1}: '{text}'\n")
                            f.write(f"    Font: {font}, Size: {size}, Bold: {bold}\n")
                            f.write(f"    Text Box: {bbox}\n")
                            f.write("    BBox Left-Top: ({}, {}), Right-Bottom: ({}, {})\n\n".format(bbox[0], bbox[1], bbox[2], bbox[3]))

# PDF 파일 경로
pdf_path = 'your_pdf_file.pdf'
# 출력할 텍스트 파일의 경로
output_file_path = 'output_text_attributes.txt'
print_text_attributes(pdf_path, output_file_path)
