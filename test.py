import re

string = '30 838.33 20% 6 167.67 37 006.00'
last_element = re.findall(r'\b\d+\s\d+\.\d{2}\b', string)[-1]

print(last_element)  # Output: 37 006.00