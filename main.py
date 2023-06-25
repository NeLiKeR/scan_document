import PyPDF2
import re
import os

from act import act_kazenergo
from invoice import invoice_tatenergosbyt, invoice_departament, invoice_vodokanal, invoice_kazenergo
from check import check_tatenergosbyt, check_departament, check_vodokanal, check_kazenergo


def check_documents(path):
    pdf_document = PyPDF2.PdfReader(path)
    text = pdf_document.pages[0].extract_text()
    text = text.replace(r'\xa0', ' ').replace(r' \n', '')
    pattern_for_check_1 = r'СЧЕТ (.*)'
    # pattern_for_invoice = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
    pattern_for_tatenergosbyt_check_2 = r'АО "ТАТЭНЕРГОСБЫТ"'
    pattern_for_tatenergosbyt_invoice_1 = r'СЧЁТ-ФАКТУРА'
    pattern_for_tatenergosbyt_invoice_2 = r'ТАТЭНЕРГОСБЫТ'
    pattern_for_departament_check = r', Акционерное общество "Департамент'
    pattern_for_departament_invoice = r'Счет-фак тур'
    pattern_for_vodokanal_check_1 = r'"Водоканал"'
    pattern_for_vodokanal_check_2 = r'Счет на оп'
    match_for_tatenergosbyt_check_1 = re.search(pattern_for_check_1, text)
    match_for_tatenergosbyt_check_2 = re.search(pattern_for_tatenergosbyt_check_2, text)
    match_for_tatenergosbyt_invoice_1 = re.search(pattern_for_tatenergosbyt_invoice_1, text)
    match_for_tatenergosbyt_invoice_2 = re.search(pattern_for_tatenergosbyt_invoice_2, text)
    match_for_departament_check = re.search(pattern_for_departament_check, text)
    match_for_departament_invoice = re.search(pattern_for_departament_invoice, text)
    match_for_vodokanal_check_1 = re.search(pattern_for_vodokanal_check_1, text)
    match_for_vodokanal_check_2 = re.search(pattern_for_vodokanal_check_2, text)
    if match_for_tatenergosbyt_check_2 and match_for_tatenergosbyt_check_1:
        print(path)
        check_tatenergosbyt(path)
        print('%%%%%%%%%')
    elif match_for_tatenergosbyt_invoice_1 and match_for_tatenergosbyt_invoice_2:
        print(path)
        invoice_tatenergosbyt(path)
        print('%%%%%%%')
    elif match_for_departament_check:
        print(path)
        check_departament(path)
        print("%%%%%%%%%%%")
    elif match_for_departament_invoice:
        print(path)
        invoice_departament(path)
        print('%%%%%%%%%%')
    elif 'Счет на оп' in text and 'Во доканал' in text:
        print(path)
        check_vodokanal(path)
        print("%%%%%%%%%%%")
    elif r'Счет-фактура №' in text and 'Водоканал' in text:
        print(path)
        invoice_vodokanal(path)
        print('%%%%%%%%%%')
    elif r'Счет №' in text and 'Казэнерго':
        print(path)
        check_kazenergo(path)
        print('%%%%%%%%%%')
    elif r'СЧЁТ-ФАКТУРА № ' in text and 'Казэнерго' in text:
        print(path)
        invoice_kazenergo(path)
        print('%%%%%%%%%%')
    elif r'Акт о передаче результатов' in text and 'Казэнерго' in text:
        print(path)
        act_kazenergo(path)
        print('%%%%%%%%%')





def all_documents(path):
    # Получаем список всех файлов в папке
    file_list = os.listdir(path)
    file_path = None
    # Проходимся по каждому файлу
    for file_name in file_list:
        # Проверяем, что файл имеет расширение .pdf
        if file_name.endswith('.pdf'):
            # Полный путь к файлу
            file_path = os.path.join(path, file_name)
            # Делаем что-то с PDF-файлом, например, выводим его название
            print(file_name)
            check_documents(file_path)


all_documents(r'all_items')
