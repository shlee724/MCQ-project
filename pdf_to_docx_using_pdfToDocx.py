# 성능이 완전 개판이라 못쓸듯


from pdf2docx import Converter

# PDF 파일 경로
pdf_file = 'your_pdf_file.pdf'
# 변환된 Word 파일 경로
word_file = 'converted_word_file.docx'

# Converter 객체 생성
cv = Converter(pdf_file)

# PDF를 Word로 변환
cv.convert(word_file)

# 변환 프로세스 종료
cv.close()
