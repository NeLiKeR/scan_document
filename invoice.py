import PyPDF2
import re
import os


def check(path):
    print('СЧЕТ')
    pdf_document = PyPDF2.PdfReader(path)

    for page in range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ')
        # print(text)
        # pattern_for_invoice = r'СЧЕТ \s+(.+?)от (\d+ \S+ \d+ г\.)'
        pattern_for_invoice = r'СЧЕТ (.*)'
        pattern_for_contragent = r'Гарантирующий Поставщик\s+(.+?)\n'
        pattern_for_payer = r'Плательщик\s+(.+?)\n'
        pattern_for_contract = r'Государственный \(Муниципальный\) Контракт\s+(.+?)\n'
        match_for_invoice = re.search(pattern_for_invoice, text)
        match_for_contragent = re.search(pattern_for_contragent, text)
        match_for_payer = re.search(pattern_for_payer, text)
        match_for_contract = re.search(pattern_for_contract, text)
        if match_for_invoice:
            print(match_for_invoice.group(0))
        else:
            print('NO match_for_invoice')
        if match_for_contragent:
            print(match_for_contragent.group(1))
        else:
            print('NO match_for_contragent')
        if match_for_payer:
            print(match_for_payer.group(1))
        else:
            print('NO match_for_payer')
        if match_for_contract:
            print(match_for_contract.group(1))
        else:
            print('NO match_for_contract')
        # print(text)

        # if 'за электроэнергию(мощность)' in text:
        #     product = 'за электроэнергию(мощность)'
        #     pattern_for_product = r'за электроэнергию\(мощность\)\s+(.+?)\n'
        #     match_for_product = re.search(pattern_for_product, text)
        #     if match_for_product:
        #         print(product)
        #         print(match_for_product.group(1))
        pattern_for_product = r'1 2 3 4 5 6\n(.*?)\n'
        match_for_product = re.search(pattern_for_product, text, re.DOTALL)
        if match_for_product:
            print(match_for_product.group(1))
        else:
            print('NO match_for_product')

        # pattern_for_inn = r'ИНН (\d+) итог\s+(.*)'
        pattern_for_inn = r'ИНН (.*)'
        match_for_inn = re.search(pattern_for_inn, text)
        if match_for_inn:
            print(match_for_inn.group(0))
        else:
            print('NO match_for_inn')
        # first_nomer = text.find('№')+2
        # second_line = text[first_nomer:].find('\n') + first_nomer
        # take_nomer_docum = text[first_nomer:second_line]
        # third_line = text[text_nomer].find('\n') + text_nomer
        # if 'ТАТЭНЕРГОСБЫТ' in text[text_nomer:third_line]:
        #     contragent = 'ТАТЭНЕРГОСБЫТ'
        # else:
        #
        # print(f'Номер документа: {take_nomer_docum}')
        # print(f'Контрагент: {contragent}')
        # print(text)


def find_enter(string, max):
    index = 0
    count = 0
    while count < max:
        index = string.find('\n', index + 1)
        if index == -1:
            break
        count += 1

    return index


def sum_numbers_in_list(lst):
    total_sum = 0
    for string in lst:
        try:
            number = int(string)
            total_sum += number
        except ValueError:
            # Ignore non-numeric strings
            pass
    return total_sum


def invoice(path):
    print('СЧЕТ-ФАКТУРА')
    pdf_document = PyPDF2.PdfReader(path)

    for page in range(1):#range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '')
        # print(text)
        # index1 = find_enter(text, 7)
        # index2 = find_enter(text, 21)
        # invoice_number = text[index1:index2].replace('\n', '').replace('  ', '')
        # print(invoice_number)

        pattern_for_invoice_number = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_number = re.search(pattern_for_invoice_number, text)

        if match_for_invoice_number:
            invoice_number = match_for_invoice_number.group().replace('\n', '').replace('  ', '')
            print(invoice_number)

        else:
            print('NO invoice_number')
        # index1 = find_enter(text, 46)
        # index2 = find_enter(text, 48)
        # contagent = text[index1:index2]
        # print(contagent)
        pattern_contragent = r'Грузоотправитель и его адрес\n(.*?)\n'

        matched_text = re.search(pattern_contragent, text, re.DOTALL)
        if matched_text:
            contragent = matched_text.group(0)
            print(contragent, end='')
        else:
            print('NO contragent')

        # index1 = find_enter(text, 83)
        # index2 = find_enter(text, 85)
        # payer = text[index1:index2]
        # print(payer)
        pattern_payer = r'Покупатель\n(.*?)\n'
        match_payer = re.search(pattern_payer, text, re.DOTALL)
        if match_payer:
            payer = match_payer.group(0)
            print(payer, end='')
        else:
            print('NO payer')

        # index1 = find_enter(text, 111)
        # index2 = find_enter(text, 113)
        # number_dogovor = text[index1:index2]
        # print(number_dogovor)
        pattern_dogovor = r'Доп\. сведения:\n(.*?)\n'
        match_number_dogovor = re.search(pattern_dogovor, text, re.DOTALL)
        if match_number_dogovor:
            number_dogovor = match_number_dogovor.group()
            print(number_dogovor, end='')
        else:
            print('NO number_dogovor')
        # print(text)

        # pattern_items = r'кВт·ч\n(.*?)\n'
        # result_items = re.search(pattern_items, text, re.DOTALL)
        # if result_items:
        #     print('$$$$$')
        #     match_items = result_items.group()
        #     print(match_items)

        pattern_items = r'кВт·ч\n(\d+)'
        matches_items = re.findall(pattern_items, text)
        if matches_items:
            print(matches_items)
            sum_items = sum_numbers_in_list(matches_items)
            print(sum_items)
        else:
            print('NO sum_items')

        pattern_for_resutl = r'Всего к оплате\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_result = re.search(pattern_for_resutl, text)

        if match_for_result:
            result = match_for_result.group(4)
            print(result)
        else:
            print('No result')


def check_documents(path):
    pdf_document = PyPDF2.PdfReader(path)
    text = pdf_document.pages[0].extract_text()
    text = text.replace(r'\xa0', ' ').replace(r' \n', '')
    pattern_for_check = r'СЧЕТ (.*)'
    match_for_check = re.search(pattern_for_check, text)
    pattern_for_invoice = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
    match_for_invoice = re.search(pattern_for_invoice, text)

    if match_for_check:
        print(path)
        check(path)
        print('%%%%%%%%%')
    elif match_for_invoice:
        print(path)
        invoice(path)
        print('%%%%%%%')


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

    # if file_path:
    #     print(file_path)

# check(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\invoice\50 ав.pdf')
# invoice(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\invoice\50счетфактура.pdf')
all_documents('invoice')
