#엑셀로 텍스트는 잘 변환되는데, 이미지가 셀에 들어가지 않고 셀 밖에서 노는 문제때문에 이미지의 포지션 이슈가 생김



import fitz  # PyMuPDF
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
import io
import tempfile

def pdf_to_excel(pdf_path, excel_path):
    doc = fitz.open(pdf_path)
    wb = Workbook()
    ws = wb.active

    for page_num, page in enumerate(doc):
        # 페이지의 텍스트 블록과 이미지 블록을 추출합니다.
        text_blocks = page.get_text("blocks")
        image_blocks = page.get_images(full=True)

        # 이미지 블록의 xref를 추출하여 위치를 찾습니다.
        image_xrefs = {xref[0] for xref in image_blocks}

        # 모든 블록을 하나의 리스트로 병합합니다.
        blocks = text_blocks + [(img[0], 0, 0, 0, 0, "image", img[0]) for img in image_blocks]

        # 블록을 y 위치에 따라 정렬합니다.
        blocks.sort(key=lambda block: block[1])

        for block in blocks:
            if block[5] == "image" and block[0] in image_xrefs:
                # 이미지를 처리합니다.
                for img in image_blocks:
                    if img[0] == block[0]:
                        image_bytes = doc.extract_image(img[0])['image']
                        # 이미지를 임시 파일로 저장합니다.
                        image_pil = PILImage.open(io.BytesIO(image_bytes))
                        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        image_pil.save(temp_img.name)
                        img = Image(temp_img.name)
                        ws.add_image(img, 'A' + str(ws.max_row + 1))  # 이미지 삽입
            else:
                # 텍스트를 셀에 추가합니다.
                ws.append([block[4]])

    wb.save(excel_path)

pdf_path = 'your_pdf_file.pdf'  # PDF 파일 경로
excel_path = 'output_excel_file.xlsx'  # Excel 파일 경로

pdf_to_excel(pdf_path, excel_path)
