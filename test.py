import tabula
import pandas as pd

# Path to your PDF file
pdf_path = r'C:\Users\566a5\PycharmProjects\Работа\new_scan_doc\tatenergosbyt\50 ав (2).pdf'

# Path to your PDF file

# Open the PDF file
tables = tabula.read_pdf(pdf_path, pages="all")

# Iterate over extracted tables
for table in tables:
    # Convert the table to a Pandas DataFrame
    df = pd.DataFrame(table)

    # Perform further operations with the DataFrame
    # For example, you can print the table or manipulate the data
    print(df)