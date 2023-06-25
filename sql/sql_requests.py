import sqlite3


def insert_into_check(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract, contract_date,
                      product, nds, result_price, checking_account, date_of_signing):
    conn = None
    try:
        print(f'INSERT check {name_table}')
        res = (nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract, contract_date, product,
               nds, result_price, checking_account, date_of_signing)
        request = f'INSERT INTO {name_table} (nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, ' \
                  f'inn_payer, contract, contract_date, product, nds, result_price, checking_account, date_of_signing) ' \
                  f'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        conn = sqlite3.connect(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\sql\check.db')
        cur = conn.cursor()
        cur.execute(request, res)
        conn.commit()
        print('INSERT SUCCESS')
    except Exception as e:
        print(f'Error INSERT check {name_table}')
        print(e)
    finally:
        if conn:
            conn.close()


def insert_into_invoice(name_table, invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer,
                        number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing):
    conn = None
    try:
        print(f'INSERT invoice {name_table}')
        res = (invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, number_dogovor, dogovor_date,
               quantity_of_items, nds, result_price, checking_account, date_of_signing)
        request = f'INSERT INTO {name_table} (invoice_number, invoice_date, contragent, inn_contragent, kpp_contragent, payer, ' \
                  f'inn_payer, number_dogovor, dogovor_date, quantity_of_items, nds, result_price, checking_account, date_of_signing) ' \
                  f'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        conn = sqlite3.connect(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\sql\invoice.db')
        cur = conn.cursor()
        cur.execute(request, res)
        conn.commit()
        print(f'INSERT invoice SUCCESS {name_table}')
    except Exception as e:
        print('Error invoice')
        print(e)
    finally:
        if conn:
            conn.close()


def insert_into_act(name_table, nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract,
                    date_contract, dogovor, nds, result_price, checking_account, date_of_signing):
    conn = None
    try:
        print(f'INSERT act {name_table}')
        res = (nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, inn_payer, contract,
               date_contract, dogovor, nds, result_price, checking_account, date_of_signing)
        request = f'INSERT INTO {name_table} (nomer, nomer_date, contragent, inn_contragent, kpp_contragent, payer, ' \
                  f'inn_payer, contract,date_contract, dogovor, nds, result_price, checking_account, date_of_signing) ' \
                  f'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        conn = sqlite3.connect(r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\sql\act.db')
        cur = conn.cursor()
        cur.execute(request, res)
        conn.commit()
        print(f'INSERT invoice SUCCESS {name_table}')
    except Exception as e:
        print('Error invoice')
        print(e)
    finally:
        if conn:
            conn.close()
