import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, font_path, font_size, color=(0,0,0)):
    """텍스트를 이미지로 변환"""
    font = ImageFont.truetype(font_path, font_size)
    size = font.getsize(text)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    draw.text((0, 0), text, font=font, fill=color)
    image_path = 'text_image.png'
    image.save(image_path)
    return image_path

def insert_text_image(pdf_path, output_pdf_path, image_path, position):
    """이미지를 PDF에 삽입"""
    doc = fitz.open(pdf_path)
    page = doc[0]  # 첫 페이지에 삽입
    img = fitz.open(image_path)
    rect = fitz.Rect(position, (position[0] + img[0].rect.width, position[1] + img[0].rect.height))
    page.insert_image(rect, filename=image_path)
    doc.save(output_pdf_path)
    doc.close()


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
                        text = span['text']


                        if font == target_font and size == target_size and color == target_color:
                            print("true")
                            # 기존 텍스트 삭제
                            rect = fitz.Rect(span['bbox'])
                            page.add_redact_annot(rect)
                            page.apply_redactions()
                            
                            # 사용 예
                            font_path = "path/to/your/custom/font.ttf"
                            font_size = 11.25
                            color = (0, 0, 0)  # 검은색
                            image_path = create_text_image(text, font_path, font_size, color)

                            pdf_path = 'your_pdf_file.pdf'
                            output_pdf_path = 'modified_pdf_file.pdf'
                            position = (100, 100)  # 삽입 위치
                            insert_text_image(pdf_path, output_pdf_path, image_path, position)
    
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
