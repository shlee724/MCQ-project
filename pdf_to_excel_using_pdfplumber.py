#이건 일단 미완성


import os  
import pdfplumber  
import pandas as pd  


file_path = os.getcwd() 
pdf_name = "example.pdf"  
pdf_file_path = file_path + pdf_name  

# PDF 파일 열기  
pdf = pdfplumber.open(pdf_file_path)  

pages = pdf.pages  
print("총 페이지 수 : ", len(pages))  

tables = []  

# 1. 페이지에서 표 데이터 추출하기  
for each in pages:  
    table = each.extract_tables()  
    tables.extend(table)