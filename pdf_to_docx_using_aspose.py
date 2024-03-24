import aspose.words as aw

# Aspose.Words 초기화
license = aw.License()
license.set_license("Aspose.Words.lic")

# PDF 파일을 Word 파일로 변환
def pdf_to_word(pdf_file, word_file):
    # Load PDF
    doc = aw.Document(pdf_file)
    # Save as Word
    doc.save(word_file)

# PDF 파일과 Word 파일의 경로 설정
pdf_file = 'example.pdf'
word_file = 'example.docx'

# PDF를 Word로 변환
pdf_to_word(pdf_file, word_file)
