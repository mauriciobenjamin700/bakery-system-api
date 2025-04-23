from random import choice, shuffle
from string import ascii_lowercase, ascii_uppercase, digits


def generate_random_password(length: int = 10) -> str:
    """
    Gera uma senha aleatória de tamanho especificado, contendo letras maiúsculas,
    minúsculas, números e caracteres especiais.

    - Args:
        - length (int): Tamanho da senha (default=10)

    - Returns:
        - str: Senha aleatória
    """
    if length < 8:
        raise ValueError(
            "O comprimento mínimo da senha deve ser 8 para incluir todos os tipos de caracteres."
        )

    # Garantir pelo menos um caractere de cada tipo
    password = [
        choice(ascii_lowercase),  # Pelo menos uma letra minúscula
        choice(ascii_uppercase),  # Pelo menos uma letra maiúscula
        choice(digits),  # Pelo menos um número
        choice(["@", "-", "!", "?"]),  # Pelo menos um caractere especial
    ]

    # Preencher o restante da senha com caracteres aleatórios
    all_characters = ascii_lowercase + ascii_uppercase + digits
    password += [choice(all_characters) for _ in range(length - 4)]

    # Embaralhar os caracteres para evitar padrões previsíveis
    shuffle(password)

    return "".join(password)


if __name__ == "__main__":
    print(generate_random_password(10))
