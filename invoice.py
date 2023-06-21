import PyPDF2
import re
import os
from sql.sql_requests import insert_into_check, insert_into_invoice


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


        invoice_number = None
        invoice_date = None
        contragent = None
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
        pattern_for_invoice_number = r'СЧЁТ-ФАКТУРА № \n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_invoice_number = re.search(pattern_for_invoice_number, text)
        if match_for_invoice_number:
            invoice_number = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace('СЧЁТ-ФАКТУРА № ', '').split(' ')[0]
            invoice_date = match_for_invoice_number.group().replace('\n', '').replace('  ', '').replace('СЧЁТ-ФАКТУРА № ', '').replace(' "', '').split(' ')[2::]
            invoice_date = ' '.join(invoice_date)
            print(invoice_number, invoice_date)
        else:
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
        else:
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
        else:
            print('NO inn_contragent, kpp_contragent')
        pattern_payer = r'Покупатель\n(.*?)\n'
        match_payer = re.search(pattern_payer, text, re.DOTALL)
        if match_payer:
            payer = match_payer.group(1).replace('\n', '')
            print(payer)
        else:
            print('NO payer')

        pattern_inn_payer = r'ИНН/КПП продавца\n(.*?)\n'
        match_inn_payer = re.search(pattern_inn_payer, text)
        if match_inn_payer:
            inn_payer = match_inn_payer.group(1).replace('/', '')
            print(inn_payer)

        # index1 = find_enter(text, 111)
        # index2 = find_enter(text, 113)
        # number_dogovor = text[index1:index2]
        # print(number_dogovor)
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
            # print(matches_items)
            quantity_of_items = sum_numbers_in_list(matches_items)
            print(quantity_of_items)
        else:
            print('NO sum_items')

        pattern_for_resutl = r'Всего к оплате\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_result = re.search(pattern_for_resutl, text)

        if match_for_result:
            nds = match_for_result.group(3)
            result_price = match_for_result.group(4)
            print(result_price, nds)
        else:
            print('No result')

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

        insert_into_invoice(invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
         number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing)


    # if file_path:
    #     print(file_path)
# invoice_tatenergosbyt(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\all_items\50счетфактура.pdf')
# 50 исчет фактура
# all_documents('invoice')

