import PyPDF2
import re
from sql.sql_requests import insert_into_check


def check_tatenergosbyt(path):
    print('СЧЕТ Татэнергосбыт')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'tatenergosbyt'
    nomer = None
    nomer_date = None
    contragent = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    contract = None
    contract_date = None
    product = None
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
        # pattern_for_invoice = r'СЧЕТ \s+(.+?)от (\d+ \S+ \d+ г\.)'
        pattern_for_check = r'СЧЕТ (.*)'
        pattern_for_contragent = r'Гарантирующий Поставщик\s+(.+?)\n'
        pattern_for_payer = r'Плательщик\s+(.+?)\n'
        pattern_for_contract = r'Государственный \(Муниципальный\) Контракт\s+(.+?)\n'
        pattern_for_inn_kpp = r'ИНН/КПП (.+?)\n'
        match_for_check = re.search(pattern_for_check, text)
        match_for_contragent = re.search(pattern_for_contragent, text)
        match_for_payer = re.search(pattern_for_payer, text)
        match_for_contract = re.search(pattern_for_contract, text)
        matches_for_inn_kpp = re.findall(pattern_for_inn_kpp, text)

        if match_for_check:
            nomer = match_for_check.group(0).replace("  ", ' ').split(' ')[2]
            nomer_date = match_for_check.group(1).replace("  ", ' ').split(' ')[3::]
            nomer_date = ' '.join(nomer_date)
            print(nomer, nomer_date)
        else:
            print('NO match_for_invoice')
        if match_for_contragent:
            contragent = match_for_contragent.group(1)
            print(match_for_contragent.group(1))
        else:
            print('NO match_for_contragent')
        if match_for_payer:
            payer = match_for_payer.group(1)
            print(match_for_payer.group(1))
        else:
            print('NO match_for_payer')
        if match_for_contract:
            contract = match_for_contract.group(1).split(' ')[0]
            contract_date = match_for_contract.group(1).split(' ')[3]
            print(contract_date, contract)
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
            product = match_for_product.group(1).split(' руб. ')[0]
            result_price = match_for_product.group(1).split(' руб. ')[1]
            print(result_price)
            result_price, cent_result_price = result_price.split('.')[-2], result_price.split('.')[-1]
            result_price = result_price.split(' ')[1::]
            result_price = ''.join(result_price) + '.' + cent_result_price
            nds = match_for_product.group(1).split(' руб. ')[1]
            nds, cent_nds = nds.split('.')[1], nds.split('.')[2]
            cent_nds = cent_nds.split(' ')[0]
            nds = nds.split('%')[0].replace(' ', '')
            nds = ''.join(nds) + '.' + cent_nds
            print(nds)
            print(result_price)
            print(match_for_product.group(1))
        else:
            print('NO match_for_product')

        if matches_for_inn_kpp:
            print('@#@@@@')
            print(matches_for_inn_kpp)
            for i in matches_for_inn_kpp:
                if 'получателя' in i:
                    # inn_kpp =
                    # print(inn_kpp)
                    inn_contragent, kpp_contragent = i.split(' ')[1], i.split(' ')[3]
                    print(inn_contragent, kpp_contragent)
                elif 'плательщика' in i:
                    inn_payer = i.split(' ')[1]
                    print(inn_payer)
                # print(i)
        else:
            print('No matches_for_inn_kpp')

        pattern_for_checking_account = r'р/с (.*?)\n'
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print('111111')
            print(match_for_checking_account.group())
            checking_account = match_for_checking_account.group()[4:match_for_checking_account.group().find('в')]
            print(checking_account)
        # pattern_for_inn = r'ИНН (\d+) итог\s+(.*)'
        pattern_for_inn = r'ИНН (.*)'
        match_for_inn = re.search(pattern_for_inn, text)
        if match_for_inn:
            print(match_for_inn.group(0))
        else:
            print('NO match_for_inn')

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
        insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                          contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
    else:
        print('MB error check_tatenergosbyt')
        print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                          contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
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


def check_departament(path):
    print('СЧЕТ Департамент')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'departament'
    nomer = None
    nomer_date = None
    contragent = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    contract = None
    contract_date = None
    product = None
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

        pattern_for_contragent = r'Поставщик:ИНН (.*?), КПП (.*?),(.*?)\n'
        match_for_contragent= re.search(pattern_for_contragent, text)
        if match_for_contragent:
            print(1)
            contragent = match_for_contragent.group(0).split(' "')[1].replace('\n', '')
            inn_contragent = match_for_contragent.group(1)
            kpp_contragent = match_for_contragent.group(2)
            print(contragent)
            print(inn_contragent)
            print(kpp_contragent)

        pattern_for_nomer = r'Счет на оплату № (.*?) от (.*?) по контракту: (.*?)\n от (.*?)\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(2)
            nomer = match_for_nomer.group(1).replace(' ', '')
            nomer_date = match_for_nomer.group(2).replace(' ', '')
            contract = match_for_nomer.group(3).replace(' ', '')
            contract_date = match_for_nomer.group(4).replace(' ', '')
            print(nomer, nomer_date, contract, contract_date)

        pattern_for_inn_payer = r'Покупатель:ИНН (.*?), КПП (.*?),(.*?)\n(.*?)учреждение (.*?)\n'
        match_for_inn_payer = re.search(pattern_for_inn_payer, text)
        if match_for_inn_payer:
            print(3)
            inn_payer = match_for_inn_payer.group(1).replace(' ', '')
            payer = match_for_inn_payer.group(5)
            print(payer, inn_payer)
        ''''''''
        pattern_for_product = r'№ Товар Код Кол-во Ед. Цена в т.ч. НДС Всего\n(.*?)\n(.*?)ЦБ'
        match_for_product = re.search(pattern_for_product, text)
        if match_for_product:
            print(4)
            product = match_for_product.group(1) + match_for_product.group(2)
            print(product)
        ''''''''
        pattern_for_reuslt_price = r'Итого руб.: (.*?)\n'
        match_for_result_price = re.search(pattern_for_reuslt_price, text)
        if match_for_result_price:
            print(5)
            result_price = match_for_result_price.group(1).replace(' ', '')
            print(result_price)

        pattern_for_checking_account = r'Сч. № (.*?)\n'
        match_for_checking_account = re.findall(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(6)
            checking_account = match_for_checking_account[-1]
            checking_account = checking_account.replace(' ', '')
            print(checking_account)

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(7)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)

    if nomer:
        insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                          contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
    else:
        print('MB error check_departament')
        print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
              contract, contract_date, product, nds, result_price, checking_account, date_of_signing)


def check_vodokanal(path):
    print('СЧЕТ Водоканал')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'vodokanal'
    nomer = None
    nomer_date = None
    contragent = 'Водоканал'
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    contract = None
    contract_date = None
    product = None
    nds = None
    result_price = None
    checking_account = None
    date_of_signing = None
    for page in range(len(pdf_document.pages)):
        text = pdf_document.pages[page].extract_text()
        text = text.replace(r'\xa0', ' ').replace(r' \n', '').replace(' ', ' ').replace('\n', '>>>>>>><<<<<')
        text = re.sub(r"\s+", " ", text)
        text = text.replace('>>>>>>><<<<<', '\n')
        # print(text)

        pattern_for_nomer = r'Счет на оплат у № (.*?) о т (.*?)\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(1)
            nomer, nomer_date = match_for_nomer.group(1), match_for_nomer.group(2)
            print(nomer, nomer_date)

        pattern_for_inn_contragent = r'Пост авщик: (.*?), ИНН (.*?), КПП (.*?),'
        match_for_inn_contragent = re.search(pattern_for_inn_contragent, text)
        if match_for_inn_contragent:
            print(2)
            inn_contragent, kpp_contragent = match_for_inn_contragent.group(1), match_for_inn_contragent.group(2)
            print(inn_contragent, kpp_contragent)

        pattern_for_payer = r'Покупатель: (.*?), ИНН (.*?), КПП (.*?),'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(3)
            payer, inn_payer = match_for_payer.group(1), match_for_payer.group(2)
            print(payer, inn_payer)

        pattern_for_product = r'изм.Цена Сумма\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_product = re.search(pattern_for_product, text)
        if match_for_product:
            print(4)
            product = []
            # print(match_for_product.group(0))
            for i in range(1, 6):
                if 'Итого' in match_for_product.group(i):
                    break
                product.append(match_for_product.group(i))
            product = f'{product}'
            print(product)

        pattern_for_result_price = r'Сумма НДС: (.*?)\nВсег о к оплате: (.*?)\n'
        match_for_result_price = re.search(pattern_for_result_price, text)
        if match_for_result_price:
            print(5)
            nds, result_price = match_for_product.group(1), match_for_result_price.group(2)
            print(nds, result_price)

        pattern_for_checking_account = r'Счет № (.*?)\n'
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(6)
            checking_account = match_for_checking_account.group(1)
            print(checking_account)

        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(7)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)
        if nomer:
            insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer,
                              inn_payer,
                              contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
        else:
            print('MB error check_tatenergosbyt')
            print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                  contract, contract_date, product, nds, result_price, checking_account, date_of_signing)


def check_kazenergo(path):
    print('СЧЕТ Казэнерго')
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
    contract_date = None
    product = None
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

        pattern_for_nomer = r'Счет № (.*?) от (.*?).\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(1)
            nomer, nomer_date = match_for_nomer.group(1), match_for_nomer.group(2)
            print(nomer, nomer_date)

        pattern_for_payer = r'Покупатель:(.*?)\n'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(2)
            payer = match_for_payer.group(1)
            print(payer)

        pattern_for_contragent = r'ИНН / КПП продавца: (.*?) / (.*?)\n'
        match_for_contragent = re.search(pattern_for_contragent, text)
        if match_for_contragent:
            print(3)
            inn_contragent = match_for_contragent.group(1)
            kpp_contragent = match_for_contragent.group(2)
            print(inn_contragent)
            print(kpp_contragent)

        pattern_for_inn_payer = r'ИНН / КПП покупателя: (.*?) / (.*?)\n'
        match_for_inn_payer = re.search(pattern_for_inn_payer, text)
        if match_for_inn_payer:
            print(3)
            inn_payer = match_for_inn_payer.group(1).replace(' ', '')
            print(inn_payer)

        pattern_for_checking_account = r'РС (.*?) '
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(4)
            checking_account = match_for_checking_account.group(1)
            print(checking_account)

        pattern_for_dogovor = r'Договор: (.*?) от (.*?) Контракт: (.*?)\n'
        match_for_dogovor = re.search(pattern_for_dogovor, text)
        if match_for_dogovor:
            print(5)
            dogovor = match_for_dogovor.group(1)
            date_dogovor = match_for_dogovor.group(2)
            contract = match_for_dogovor.group(3)
            print(dogovor, date_dogovor, contract)

        pattern_for_reuslt_price = r'Всего к оплате (.*?),(.*?) (.*?),(.*?) (.*?)\n'
        match_for_result_price = re.search(pattern_for_reuslt_price, text)
        if match_for_result_price:
            print(6)
            nds = str(match_for_result_price.group(3) + '.' + match_for_result_price.group(4)).replace(' ', '')
            result_price = match_for_result_price.group(5).replace(' ', '')
            print(result_price, nds)
        ''''''''
        pattern_for_product = r'1 2 3 4 5 6 7 8 9 10 11\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
        match_for_product = re.search(pattern_for_product, text)
        if match_for_product:
            print(7)
            for i in range(1, 7):
                if 'C учетом долга' in match_for_product.group(i):
                    break
                print(match_for_product.group(i))
        ''''''''
        pattern_for_date_of_signing = r'СЕРТИФИКАТ ПОДПИСАН\n(.*?)\n(.*?)\n'
        match_for_date_signing = re.findall(pattern_for_date_of_signing, text)
        if match_for_date_signing:
            print(9)
            print(match_for_date_signing)
            date_of_signing = match_for_date_signing[-1]
            for i in date_of_signing:
                if '.' in i:
                    i = i.split('.')
                    day, month, year = i[0][-2:], i[1], i[2][0:4]
                    date_of_signing = '.'.join([day, month, year])
            print(date_of_signing)

        if nomer:
            insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer,
                              inn_payer,
                              contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
        else:
            print('MB error check_departament')
            print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                  contract, contract_date, product, nds, result_price, checking_account, date_of_signing)


def check_tatenergo(path):
    print('СЧЕТ Татэнерго')
    pdf_document = PyPDF2.PdfReader(path)
    name_table = 'tatenergo'
    contragent = 'ТАТЭНЕРГО'
    nomer = None
    nomer_date = None
    inn_contragent = None
    kpp_contragent = None
    payer = None
    inn_payer = None
    contract = None
    contract_date = None
    product = None
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
        print(text)
        pattern_for_nomer = r'СЧЕТ № (.*?) от (.*?).\n'
        match_for_nomer = re.search(pattern_for_nomer, text)
        if match_for_nomer:
            print(1)
            nomer, nomer_date = match_for_nomer.group(1), match_for_nomer.group(2)
            print(nomer, nomer_date)

        pattern_for_contragent = r'ИНН/КПП получателя: (.*?) (.*?)\n'
        match_for_contragent = re.search(pattern_for_contragent, text)
        if match_for_contragent:
            print(2)
            inn_contragent = match_for_contragent.group(1)
            kpp_contragent = match_for_contragent.group(2)
            print(inn_contragent)
            print(kpp_contragent)

        pattern_for_payer = r'(.*?)\nПлательщик:\n'
        match_for_payer = re.search(pattern_for_payer, text)
        if match_for_payer:
            print(2)
            payer = match_for_payer.group(1)
            print(payer)

        pattern_for_inn_payer = r'ИНН/КПП плательщика: (.*?) '
        match_for_inn_payer = re.search(pattern_for_inn_payer, text)
        if match_for_inn_payer:
            print(3)
            inn_payer = match_for_inn_payer.group(1)
            print(inn_payer)

        pattern_for_dogovor = r'Договор теплоснабжения № (.*?) от (.*?).\n'
        match_for_dogovor = re.search(pattern_for_dogovor, text)
        if match_for_dogovor:
            print(4)
            dogovor = match_for_dogovor.group(1)
            date_dogovor = match_for_dogovor.group(2)
            print(dogovor, date_dogovor)

        pattern_for_checking_account = r'р/с (.*?) '
        match_for_checking_account = re.search(pattern_for_checking_account, text)
        if match_for_checking_account:
            print(5)
            checking_account = match_for_checking_account.group(1)
            print(checking_account)

        pattern_for_code = r'напервойпозиции код(.*?) '
        match_for_code = re.search(pattern_for_code, text)
        if match_for_code:
            print(6)
            code = match_for_code.group(1)
            print(code)
        #
        if nomer:
            insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer,
                              inn_payer,
                              contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
        else:
            print('MB error check_departament')
            print(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                  contract, contract_date, product, nds, result_price, checking_account, date_of_signing)
# check_tatenergosbyt(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\tatenergosbyt\50 ав (2).pdf')
# check_tatenergosbyt(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\tatenergosbyt\110 э сч 05.23.pdf')

# check_departament(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\departament\152.22.23 Счет ЦБ00001196 от 31.01.2023 3098790,00.pdf')

# check_vodokanal(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\vodokanal\110 в сч 05.23.pdf')

# check_kazenergo(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\kazenergo\3 гим сч.pdf')

# check_tatenergo(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\tatenergo\азино т сч 05.23г.pdf')
