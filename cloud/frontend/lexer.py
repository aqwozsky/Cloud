import re
import logging

# Loglama ayarları
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Token türleri
KEYWORDS = {'print', 'if', 'else', 'while', 'function', 'import', 'as', 'and', 'or', 'not', 'True', 'False', 'pass'}
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),  # Tamsayı ve kayan nokta sayıları
    ('STRING',   r'\'[^\']*\'|\"[^\"]*\"'),  # String ifadeler
    ('IDENTIFIER', r'[A-Za-z_]\w*'),  # Değişken isimleri
    ('OPERATOR', r'[+\-*/=<>]'),  # Operatörler
    ('PUNCTUATION', r'[;,.()]'),  # Noktalama işaretleri
    ('SKIP', r'[ \t]+'),  # Boşluklar
    ('NEWLINE', r'\n'),  # Yeni satır
    ('MISMATCH', r'.'),  # Hiçbir eşleşme olmadığında
]

def tokenize(source_code):
    tokens = []
    line_num = 1

    # Token regex'ini oluştur
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
    
    for match in re.finditer(token_regex, source_code):
        type = match.lastgroup
        value = match.group()

        if type == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif type == 'IDENTIFIER' and value.lower() in KEYWORDS:
            type = value.lower()
        elif type == 'NEWLINE':
            line_num += 1
            continue
        elif type == 'SKIP':
            continue
        elif type == 'MISMATCH':
            logging.error(f'Hatalı token: {value} line {line_num}')
            raise RuntimeError(f'{value} beklenmedik bir token bulundu. Satır: {line_num}')

        logging.debug(f'Token bulundu: {type}, {value}')
        tokens.append(Token(type, value))

    tokens.append(Token('EOF', None))
    return tokens

# Örnek kullanım
if __name__ == "__main__":
    source_code = """
print("Hello, World!")
if x == 5:
    print("x is 5")
"""
    try:
        tokens = tokenize(source_code)
        print(tokens)
    except RuntimeError as e:
        logging.error(e)
