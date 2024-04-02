from pdf2image import convert_from_path
import cv2, os
from PIL import Image
from reportlab.pdfgen import canvas
 
def pdf_to_image(pdf_path, image_path):
    # Convert the PDF to a list of PIL images
    images = convert_from_path(pdf_path, poppler_path=r'C:\poppler-24.02.0\Library\bin')
 
    # Loop through each image
    for i, image in enumerate(images):
        # Save the image
        image.save(image_path + str(i) + '.png', "PNG")
 
def change_target_text_in_image(image_num, target_top_left_x, target_top_left_y, target_bottom_right_x, target_bottom_right_y, text):
    # Load the image
    image_path = 'page'+str(image_num)+'.png'
    img = cv2.imread(image_path)
    
    x, y, width, height = target_top_left_x, target_top_left_y, (target_bottom_right_x - target_top_left_x), (target_bottom_right_y - target_top_left_y)
    
    # Create a red rectangle to cover the desired portion of the image
    red = (0, 0, 255)
    img[y:y + height, x:x + width] = red
    
    # Write text on the red rectangle using a white color
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (x + int(width / 4), y + int(height / 2))
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    # Save the resulting image
    cv2.imwrite('redacted_image_with_text'+str(image_num)+'.png', img)

def images_to_pdf(output_pdf_path):
    image_num = 0
    images = []

    # 이미지 파일 찾기
    while True:
        image_path = f'redacted_image_with_text{image_num}.png'
        if os.path.exists(image_path):
            images.append(image_path)
            image_num += 1
        else:
            break  # 이미지가 더 이상 존재하지 않으면 종료

    if not images:
        print("No images found.")
        return

    # 첫 번째 이미지를 기준으로 PDF의 크기 설정
    first_image = Image.open(images[0])
    width, height = first_image.size

    # PDF 파일 생성
    c = canvas.Canvas(output_pdf_path, pagesize=(width, height))

    for image_path in images:
        c.drawImage(image_path, 0, 0, width, height)
        c.showPage()  # 다음 페이지로 넘어가기

    c.save()
    print(f"Created PDF with {len(images)} images.")

"""
def image_to_pdf():
    # Open the image file
    image = Image.open('redacted_image_with_text'+str(image_num)+'.png')
    
    # Save the image as a PDF file
    image.save("redacted_pdf_file.pdf", "PDF")
"""

# Specify the coordinates for the redaction
top_left_x = 531
top_left_y = 297
bottom_right_x = 972
bottom_right_y = 325
text = "xxx@gmail.com"

# Example usage
pdf_to_image('sample_resume.pdf', 'page')

change_target_text_in_image(0,top_left_x, top_left_y, bottom_right_x, bottom_right_y, text)

images_to_pdf("redacted_pdf_file.pdf")


