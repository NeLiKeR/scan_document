import PyPDF2
import re
from sql.sql_requests import insert_into_check, insert_into_act


def act_kazenergo(path):
    print("АКТ Казэнерго")
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'kazenergo'
    contragent = 'Казэнерго'
    nomer = None
    nomer_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    contract = None
    date_contract = None
    dogovor = None
    nds = None
    result_price = None
    checking_account = None
    date_of_signing = None
    for page in range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        # text = " ".join(re.findall(r'[A-Za-z]+', text))
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        # print(text)

        pattern_for_nomer = r'№ (.*?) \nот (.*?)\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(1)
            nomer = match_for_nomer.group(1)
            nomer_date = match_for_nomer.group(2)
            print(nomer, nomer_date)

        pattern_for_payer = r'льное учреждение (.*?) далее'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(2)
            payer = match_for_payer.group(1)
            print(payer)

        pattern_for_contract = r'Основание:\n \nКонтракт: (.*?) Договор: \n (.*?)\n \nот (.*?).\n'
        match_for_contract = re.search(pattern_for_contract, text)
        if match_for_contract:
            print(3)
            contract = match_for_contract.group(1)
            dogovor = match_for_contract.group(2)
            date_contract = match_for_contract.group(3)
            print(contract, dogovor, date_contract)

        pattern_for_result_price = r'Всего к оплате:\n(.*?)\n-\n(.*?)\n(.*?)\n'
        match_for_result_price = re.search(pattern_for_result_price, text)
        if match_for_result_price:
            print(4)
            result_price = match_for_result_price.group(3)
            nds = match_for_result_price.group(2)
            print(result_price, nds)

        pattern_for_checking_account = r'р/с (.*?),'
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(5)
            checking_account = match_for_checking_account.group(1)
            print(checking_account)

        pattern_for_inn_contragent = r'ИНН\n(.*?)\nКПП\n(.*?)\n'
        match_for_inn_contragent = re.findall(pattern_for_inn_contragent, text)
        if match_for_inn_contragent:
            print(6)
            inn_contragent = match_for_inn_contragent[0][0]
            kpp_contragent = match_for_inn_contragent[0][1]
            inn_payer = match_for_inn_contragent[1][0]
            print(inn_contragent, kpp_contragent, inn_payer)

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

        if nomer:
            insert_into_act(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract,
               date_contract, dogovor, nds, result_price, checking_account, date_of_signing)
        else:
            print('MB error invoice_departament')
            print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract,
               date_contract, dogovor, nds, result_price, checking_account, date_of_signing)


act_kazenergo(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\kazenergo\110 т акт 05.23.pdf')