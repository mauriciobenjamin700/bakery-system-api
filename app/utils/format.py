def clean_format_name(name: str):
    """
    Desformata um nome

    - Args:
        - name:: str: Nome que será desformatado

    - Return:
        - str: Nome desformatado
    """
    return name.strip().upper()

def clean_format_phone(phone: str):
    """
    Desformata um número de telefone

    - Args:
        - phone:: str: Número de telefone que será desformatado ex((89) 91212-1212)

    - Return
        - str: Número de telefone desformatado (89912121212)


    """
    return "".join([number for number in phone if number.isnumeric()])


def format_name(name: str) -> str:
    """
    Formata um nome

    - Args:
        - name:: str: Nome que será formatado

    - Return:
        - str: Nome formatado
    """
    return name.strip().title()


def format_phone(number: str) -> str:
    """
    Formata um número de telefone

    - Args:
        - number:: str: Número de telefone que será formatado

    - Return:
        - str: Número de telefone formatado ex((89) 91212-1212)
    """
    number = "".join([number for number in number if number.isnumeric()])
    return f"({number[:2]}) {number[2:7]}-{number[7:]}"
