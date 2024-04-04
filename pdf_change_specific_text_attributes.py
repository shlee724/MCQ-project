import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ImageDraw, ImageFont

def create_high_resolution_text_image(text, font_path, font_size, color, image_num, dpi=(300, 300), padding=(10, 10)):
    """텍스트를 고해상도 이미지로 변환합니다. 배경은 투명 처리합니다."""
    scale_factor = dpi[0] / 96  # 일반적인 화면 DPI 대비 스케일 팩터
    font_size_scaled = int(font_size * scale_factor)  # 폰트 사이즈 조정
    font = ImageFont.truetype(font_path, font_size_scaled)
    
    # 텍스트 실제 크기 계산
    text_width, text_height = font.getsize(text)
    image_size = (int(text_width + 2 * padding[0]), int(text_height + 2 * padding[1]))
    
    image = Image.new('RGBA', image_size, (0, 0, 0, 0))  # 투명 배경 생성
    draw = ImageDraw.Draw(image)
    
    # 텍스트를 이미지 중앙에 위치시키기
    text_position = (padding[0], padding[1])
    draw.text(text_position, text, font=font, fill=color + (255,))  # RGBA로 색상 지정
    
    # 저장할 이미지 파일 경로 지정
    image_path = f'high_res_text_image/img_{image_num}.png'
    image.save(image_path, dpi=dpi)  # 이미지 저장
    
    return image_path

def insert_text_image(page, image_path, position, doc):
    """이미지를 PDF에 삽입"""
    #doc = fitz.open(pdf_path)
    img = fitz.open(image_path)
    #rect = fitz.Rect(position, (position[0] + img[0].rect.width, position[1] + img[0].rect.height))
    rect = fitz.Rect(position[0], position[1], position[0] + img[0].rect.width, position[1] + img[0].rect.height)
    page.insert_image(rect, filename=image_path)

def modify_text_style(pdf_path, output_pdf_path, target_font, target_size, target_color, new_size, new_color):
    doc = fitz.open(pdf_path)
    image_num = 0
      
    for page in doc:
        text_instances = page.get_text("dict")['blocks']
        for instance in text_instances:
            if 'lines' in instance:
                for line in instance['lines']:
                    for span in line['spans']:
                        
                        color = span['color']
                        font = span['font']
                        size = span['size']
                        text = span['text']

                        if font == target_font and (size == target_size or size == 11.25):  #정답선지이거나 오답선지이거나
                            print("true")
                            # 기존 텍스트 삭제
                            rect = fitz.Rect(span['bbox'])
                            page.add_redact_annot(rect)
                            page.apply_redactions()
                            
                            # 커스텀 폰트 이용해 이미지 생성
                            font_path = "fonts/UntitledTTF.ttf"
                            font_size = 15
                            color = (0, 0, 0)  # 검은색
                            image_path = create_high_resolution_text_image(text, font_path, font_size, color, image_num)
                            image_num += 1

                            #정답 선지이면 포지션 재조정, 정답 선지가 아니면 기존의 포지션 유지
                            if size == target_size and color == target_color:   #정답선지
                                position = (rect.bl*1.125 + rect.tl*12.375)/13.5 # 삽입 위치
                            else:                                               #오답선지
                                position = rect.tl

                            insert_text_image(page, image_path, position, doc)  #이미지화된 텍스트 삽입

    
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