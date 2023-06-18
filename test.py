import PyPDF2
import re


text1 = 'pageTag={"Ndog": "57044 Э", "KodDog": 279167, "KodDoc": 2022508019, "NomDoc":\n' \
        '"3538/70", "RYM": 2023.06}\n' \
        'СЧЕТ N 3538/70  от 15 июня 2023 г.\n' \
        'Гарантирующий Поставщик  АО "ТАТЭНЕРГОСБЫТ"\n' \
        'fdsafadsf'

text2 = 'pageTag={"Ndog": "57044 Э", "KodDog": 279167, "KodDoc": 2010749692, "NomDoc": "44700"}\n' \
        'СЧЕТ  № 44700 от 14 июня 2023 г.\n' \
        'Гарантирующий Поставщик  АКЦИОНЕРНОЕ ОБЩЕСТВО "ТАТЭНЕРГОСБЫТ"'\


pattern = r'СЧЕТ (.*)\n'
match_for_invoice1 = re.search(pattern, text1)
match_for_invoice2 = re.search(pattern, text2)

if match_for_invoice1:
    print(match_for_invoice1.group())

if match_for_invoice2:
    print(match_for_invoice2.group())
