import PyPDF2
from PIL import Image
import pytesseract
import pandas as pd
import os

# PDF에서 텍스트 및 이미지 추출
def extract_text_and_images_from_pdf(pdf_path, output_folder):
    text_list = []
    image_list = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text_list.append(page.extractText())
            xObject = page['/Resources']['/XObject'].getObject()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].getData()
                    image = Image.frombytes("RGB", size, data)
                    image_path = os.path.join(output_folder, f"page_{page_num+1}_image_{obj[1:]}.png")
                    image.save(image_path)
                    image_list.append(image_path)
    return text_list, image_list

# Excel 파일로 저장
def save_to_excel(texts, images, excel_path):
    df = pd.DataFrame({'Text': texts, 'Image': images})
    df.to_excel(excel_path, index=False)

if __name__ == "__main__":
    pdf_path = "example.pdf"  # 변환할 PDF 파일 경로
    output_folder = "images"  # 이미지를 저장할 폴더 경로
    excel_path = "output.xlsx"  # 출력할 Excel 파일 경로

    # 이미지를 저장할 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # PDF에서 텍스트 및 이미지 추출
    text_list, image_list = extract_text_and_images_from_pdf(pdf_path, output_folder)

    # 텍스트 및 이미지의 경로를 열에 저장
    save_to_excel(text_list, image_list, excel_path)

    print("PDF를 Excel로 변환 완료!")