import PyPDF2
import re
from sql.sql_requests import insert_into_invoice


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


def invoice_tatenergosbyt(path):
    print('СЧЕТ-ФАКТУРА Татэнергосбыт')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'tatenergosbyt'
    contragent = None
    invoice_number = None
    invoice_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    number_dogovor = None
    dogovor_date = None
    quantity_of_items = None
    result_price = None
    checking_account = None
    nds = None
    date_of_signing = None
    for page in range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        # text = " ".join(re.findall(r'[A-Za-z]+', text))
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        # print(text)
        # index1 = find_enter(text, 7)
        # index2 = find_enter(text, 21)
        # invoice_number = text[index1:index2].replace('\n', '').replace('  ', '')
        # print(invoice_number)

        pattern_for_invoice_number = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_number = re.search(pattern_for_invoice_number, text)
        if match_for_invoice_number:
            invoice_number = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace('СЧЁТ-ФАКТУРА № ', '').split(' ')[0]
            invoice_date = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace('СЧЁТ-ФАКТУРА № ', '').replace(' "', '').split(' ')[2::]
            invoice_date = ' '.join(invoice_date)
            print(invoice_number, invoice_date)
        elif not inn_contragent:
            print('NO invoice_number')
        # index1 = find_enter(text, 46)
        # index2 = find_enter(text, 48)
        # contagent = text[index1:index2]
        # print(contagent)

        pattern_contragent = r'Грузоотправитель и его адрес\n(.*?)\n'
        matched_text = re.search(pattern_contragent, text, re.DOTALL)
        if matched_text:
            contragent = matched_text.group(1).replace('\n', '')
            print(contragent)
        elif not contragent:
            print('NO contragent')
        # print(text)
        # index1 = find_enter(text, 83)
        # index2 = find_enter(text, 85)
        # payer = text[index1:index2]
        # print(payer)
        pattern_inn_contragent = r'ИНН/КПП продавца\n(.*?)\n(.*?)\n(.*?)'
        match_inn_contragent = re.search(pattern_inn_contragent, text)
        if match_inn_contragent:
            inn_contragent = match_inn_contragent.group(1).replace('/', '')
            kpp_contragent = match_inn_contragent.group(2)
            print(inn_contragent, kpp_contragent)
        elif not inn_contragent:
            print('NO inn_contragent, kpp_contragent')

        pattern_payer = r'Покупатель\n(.*?)\n'
        match_payer = re.search(pattern_payer, text, re.DOTALL)
        if match_payer:
            payer = match_payer.group(1).replace('\n', '')
            print(payer)
        elif not payer:
            print('NO payer')

        pattern_inn_payer = r'ИНН/КПП покупателя\n(.*?)\n'
        match_inn_payer = re.search(pattern_inn_payer, text)
        if match_inn_payer:
            inn_payer = match_inn_payer.group(1).replace('/', '')
            print(inn_payer)

        pattern_dogovor = r'Доп\. сведения:\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_number_dogovor = re.search(pattern_dogovor, text, re.DOTALL)
        if match_number_dogovor:
            number_dogovor = match_number_dogovor.group(1).replace('\n', '').replace('Договор: ', '').replace('№', '').split(' ')[0]
            dogovor_date = match_number_dogovor.group(1).replace('\n', '').replace('Договор: ', '').replace('№', '').split(' ')[3]
            index_checking_account = match_number_dogovor.group(4).find('Р/сч ') + 5
            checking_account = match_number_dogovor.group(4)[index_checking_account::]
            print(number_dogovor)
            print(dogovor_date)
            print(checking_account)
        elif not checking_account:
            print('NO number_dogovor')

        pattern_items = r'кВт·ч\n(\d+)'
        matches_items = re.findall(pattern_items, text)
        if matches_items:
            # print(matches_items)
            quantity_of_items = sum_numbers_in_list(matches_items)
            print(quantity_of_items)
        elif not quantity_of_items:
            print('NO sum_items')

        pattern_for_result = r'Всего к оплате\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_result = re.search(pattern_for_result, text)
        if match_for_result:
            nds = match_for_result.group(3)
            result_price = match_for_result.group(4)
            print(result_price, nds)
        elif not result_price:
            print('No result')

        pattern_for_items = r'-\n-\n-\n-\n-\n-\n'

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(6)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)
    if invoice_number:
        insert_into_invoice(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
         number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)
    else:
        print('MB error invoice_tatenergosbyt')
        print(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
         number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)


def invoice_departament(path):
    print('СЧЕТ-ФАКТУРА Департамент')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'departament'
    contragent = None
    invoice_number = None
    invoice_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    number_dogovor = None
    dogovor_date = None
    quantity_of_items = None
    result_price = None
    checking_account = None
    nds = None
    date_of_signing = None
    for page in range(1):  # range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        # text = " ".join(re.findall(r'[A-Za-z]+', text))
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        # print(text)
        contragent = 'ДЕПАРТАМЕНТ'
        pattern_for_nomer = r'Счет-фак тура № (.*?) от (.*?)\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(1)
            invoice_number = match_for_nomer.group(1)
            invoice_date = match_for_nomer.group(2).replace('(1)', '')
            print(invoice_number)
            print(invoice_date)

        pattern_for_inn_contragent = r'ИНН/КПП продавца (.*?)\n'
        match_for_inn_contragent = re.search(pattern_for_inn_contragent, text)
        if match_for_inn_contragent:
            print(2)
            inn_contragent, kpp_contragent = match_for_inn_contragent.group(1).split('/')
            print(inn_contragent, kpp_contragent)

        pattern_for_payer = r'Наименование покупателя (.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(3)
            payer = match_for_payer.group(2) + match_for_payer.group(3) + match_for_payer.group(4)
            print(payer)

        pattern_for_inn_payer = r'ИНН/КПП покупателя (.*?)\n'
        match_for_inn_payer = re.search(pattern_for_inn_payer, text)
        if match_for_inn_payer:
            print(4)
            inn_payer, kpp_payer = match_for_inn_payer.group(1).split('/')
            print(inn_payer, kpp_payer)

        pattern_for_result_price = r'Всего к оплате (.*?) X без НДС (.*?)\n'
        match_for_result_price = re.search(pattern_for_result_price, text)
        if match_for_result_price:
            print(5)
            result_price = match_for_result_price.group(2)
            print(result_price)

        pattern_for_item = r'А 1 1а 1б 2 2а 3 4 5 6 7 8 9 10 10а 11 12 12а\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_item = re.search(pattern_for_item, text)
        if match_for_item:
            print(6)
            new_pattern_for_item = r'[а-яА-Я](.*)'
            item = match_for_item.group(1)
            new_match_for_item = re.search(new_pattern_for_item, item)

            item = new_match_for_item.group(0) + match_for_item.group(2) + match_for_item.group(3) + \
                   match_for_item.group(4) + match_for_item.group(5) + match_for_item.group(6) + ' году'
            print(item)

        pattern_number_dogovor = r'\((.*?)\)(.*?) от (\d+\.\d+\.\d+)'
        match_for_number_dogovor = re.search(pattern_number_dogovor, text)
        if match_for_number_dogovor:
            print(7)
            number_dogovor = match_for_number_dogovor[2].strip()
            dogovor_date = match_for_number_dogovor[3]
            print("Номер:", number_dogovor)
            print("Дата:", dogovor_date)
            # number_dogovor = match_for_number_dogovor.group(1)
            # dogovor_date = match_for_number_dogovor.group(2)
            # print(number_dogovor, dogovor_date)

        pattern_for_checking_account = r'Расчетный счет (.*?) в'
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(7)
            checking_account = match_for_checking_account.group(1)
            print(checking_account)

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(8)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)
    if invoice_number:
        insert_into_invoice(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
     number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)
    else:
        print('MB error invoice_departament')
        print(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
              number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)


def invoice_vodokanal(path):
    print('СЧЕТ-ФАКТУРА Водоканал')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'vodokanal'
    contragent = 'Водоканал'
    invoice_number = None
    invoice_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    number_dogovor = None
    dogovor_date = None
    quantity_of_items = None
    result_price = None
    checking_account = None
    nds = None
    date_of_signing = None
    for page in range(1):  # range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        # text = " ".join(re.findall(r'[A-Za-z]+', text))
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        # print(text)

        pattern_for_invoice_nomer = r'Счет-фактура № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_nomer = re.search(pattern_for_invoice_nomer, text)
        if match_for_invoice_nomer:
            print(1)
            invoice_number, invoice_date = match_for_invoice_nomer.group(1), match_for_invoice_nomer.group(4)
            print(invoice_date, invoice_number)

        pattern_for_inn_contragent = r'ИНН/КПП продавца\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_inn_contragent = re.search(pattern_for_inn_contragent, text)
        if match_for_inn_contragent:
            print(2)
            inn_contragent, kpp_contragent = match_for_inn_contragent.group(1), match_for_inn_contragent.group(3)
            print(inn_contragent, kpp_contragent)

        pattern_for_payer = r'Покупатель\n(.*?)\n'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(3)
            payer = match_for_payer.group(1)
            print(payer)

        pattern_for_inn_payer = r'ИНН/КПП покупателя\n(.*?)\n'
        match_for_inn_payer = re.search(pattern_for_inn_payer, text)
        if match_for_inn_payer:
            print(4)
            inn_payer = match_for_inn_payer.group(1)
            print(inn_payer)

        pattern_for_product = r'\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\nИД: '
        match_for_product = re.findall(pattern_for_product, text)
        if match_for_product:
            print(5)
            product = ''
            product_list = []
            # print(match_for_product)
            for i in match_for_product:
                for j in i:
                    if j == '-':
                        break
                    product += j + ' '
                product = product.replace('  ', ' ')
                product_list.append(product)
                product = ''
            print(product_list)
            product = f'{product_list}'
        pattern_for_result_price = r'X\n(.*?)\n(.*?)\n(.*?)'
        match_for_result_price = re.search(pattern_for_result_price, text)
        if match_for_result_price:
            print(6)
            nds, result_price = match_for_result_price.group(1), match_for_result_price.group(2)
            print(result_price, nds)

        pattern_for_number_dogovor = r'Договор, \n(.*?), \n(.*?), '
        match_for_number_dogovor = re.search(pattern_for_number_dogovor, text)
        if match_for_number_dogovor:
            print(7)
            number_dogovor, dogovor_date = match_for_number_dogovor.group(1), match_for_number_dogovor.group(2)
            print(number_dogovor, dogovor_date)

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(8)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)

        if invoice_number:
            insert_into_invoice(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent,
                                payer, inn_payer,
                                number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account,
                                date_of_signing)
        else:
            print('MB error invoice_departament')
            print(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer,
                  inn_payer,
                  number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)


def invoice_kazenergo(path):
    print('СЧЕТ-ФАКТУРА Казэнерго')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'kazenergo'
    contragent = 'Казэнерго'
    invoice_number = None
    invoice_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    number_dogovor = None
    dogovor_date = None
    quantity_of_items = None
    result_price = None
    checking_account = None
    nds = None
    date_of_signing = None
    for page in range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        print(text)
        pattern_for_invoice_number = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_number = re.search(pattern_for_invoice_number, text)
        if match_for_invoice_number:
            print(1)
            invoice_number = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace('СЧЁТ-ФАКТУРА № ', '').split(
                ' ')[0]
            invoice_date = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace(
                'СЧЁТ-ФАКТУРА № ', '').replace(' "', '').split(' ')[2::]
            invoice_date = ' '.join(invoice_date)
            print(invoice_number, invoice_date)

        pattern_inn_contragent = r'ИНН/КПП продавца\n(.*?)\n(.*?)\n(.*?)'
        match_inn_contragent = re.search(pattern_inn_contragent, text)
        if match_inn_contragent:
            print(2)
            inn_contragent = match_inn_contragent.group(1).replace('/', '')
            kpp_contragent = match_inn_contragent.group(2)
            print(inn_contragent, kpp_contragent)

        pattern_payer = r'Покупатель\n(.*?)\n'
        match_payer = re.search(pattern_payer, text, re.DOTALL)
        if match_payer:
            print(3)
            payer = match_payer.group(1).replace('\n', '')
            print(payer)

        pattern_inn_payer = r'ИНН/КПП продавца\n(.*?)\n'
        match_inn_payer = re.search(pattern_inn_payer, text)
        if match_inn_payer:
            print(4)
            inn_payer = match_inn_payer.group(1).replace('/', '')
            print(inn_payer)

        pattern_for_resutl = r'Всего к оплате\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_result = re.search(pattern_for_resutl, text)
        if match_for_result:
            print(5)
            nds = match_for_result.group(3)
            result_price = match_for_result.group(4)
            print(result_price, nds)

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(6)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)

    if invoice_number:
        insert_into_invoice(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
         number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)
    else:
        print('MB error invoice_tatenergosbyt')
        print(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
         number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)


def invoice_tatenergo(path):
    print('СЧЕТ-ФАКТУРА Татэнерго')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'departament'
    contragent = 'Татэнерго'
    for page in range(1):  # range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        # text = " ".join(re.findall(r'[A-Za-z]+', text))
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        print(text)

        pattern_for_invoice_number = r'Счет-фактура № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_number = re.search(pattern_for_invoice_number, text)
        if match_for_invoice_number:
            print(1)
            invoice_number = match_for_invoice_number.group(1)
            invoice_date = match_for_invoice_number.group(4)
            print(invoice_number, invoice_date)

        pattern_inn_contragent = r'ИНН/КПП продавца\n(.*?) \n(.*?)\n(.*?)\n(.*?)'
        match_inn_contragent = re.search(pattern_inn_contragent, text)
        if match_inn_contragent:
            print(2)
            inn_contragent = match_inn_contragent.group(1)
            kpp_contragent = match_inn_contragent.group(3)
            print(inn_contragent, kpp_contragent)

        pattern_payer = r'Покупатель\n(.*?)\n'
        match_payer = re.search(pattern_payer, text, re.DOTALL)
        if match_payer:
            print(3)
            payer = match_payer.group(1)
            print(payer)

        pattern_inn_payer = r'ИНН/КПП покупателя\n(.*?)\n'
        match_inn_payer = re.search(pattern_inn_payer, text)
        if match_inn_payer:
            print(4)
            inn_payer = match_inn_payer.group(1)
            print(inn_payer)

        pattern_for_result = r'Всего к оплате\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_result = re.search(pattern_for_result, text)
        if match_for_result:
            print(5)
            nds = match_for_result.group(3)
            result_price = match_for_result.group(4)
            print(result_price, nds)


# invoice_departament(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\departament\151.22.23 ЦБ000173865 от 28.03.2023 128671,20.pdf')

# invoice_tatenergosbyt(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\all_items\50счетфактура.pdf')
# 50 исчет фактура

# invoice_vodokanal(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\vodokanal\110 в сф 05.23.pdf')

# invoice_kazenergo(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\kazenergo\110 т сф 05.23.pdf')

invoice_tatenergo(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\tatenergo\12 шк 05.23 тепло.pdf')