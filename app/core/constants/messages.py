ERROR_INVALID_FORMAT_TYPE_DATE = "Datas devem ser strings ou datetimes"
ERROR_INVALID_FORMAT_TYPE_ID = "ID deve ser uma string"
ERROR_INVALID_FORMAT_TYPE_NAME = "Nome deve ser uma string"
ERROR_INVALID_FORMAT_TYPE_EMAIL = "Email deve ser uma string"
ERROR_INVALID_FORMAT_TYPE_PHONE = "Telefone deve ser uma string"
ERROR_INVALID_FORMAT_TYPE_PASSWORD = "Senha deve ser uma string"

ERROR_REQUIRED_FIELD_ID = "ID é obrigatório"
ERROR_REQUIRED_FIELD_NAME = "Nome é obrigatório"
ERROR_REQUIRED_FIELD_EMAIL = "Email é obrigatório"
ERROR_REQUIRED_FIELD_PHONE = "Número de telefone é obrigatório"
ERROR_REQUIRED_FIELD_PASSWORD = "Senha é obrigatória"
ERROR_REQUIRED_FIELD_LEVEL = "Nível é obrigatório"
ERROR_REQUIRED_FIELD_CPF_CNPJ = "CPF ou CNPJ é obrigatório"
ERROR_REQUIRED_FIELD_PIX_KEY_TYPE = "Tipo de Pix Key é obrigatório"
ERROR_REQUIRED_FIELD_PIX_KEY = "Pix Key é obrigatório"


ERROR_INVALID_EMAIL = "Email inválido"
ERROR_INVALID_PHONE = "Número de telefone inválido"
ERROR_INVALID_CPF_CNPJ = "CPF ou CNPJ inválido"
ERROR_INVALID_PIX_KEY_TYPE = "Tipo de Pix Key inválido"
ERROR_INVALID_PIX_KEY = "Pix Key inválido"
ERROR_INVALID_LEVEL = "Nível inválido"

ERROR_DATE_INVALID_FORMAT_MASK = "Data deve ter o formato YYYY-MM-DD HH:MM:SS"

ERROR_EMAIL_INVALID_FORMAT_TYPE = "Email deve ser uma string"
ERROR_EMAIL_INVALID_FORMAT_MASK = "Email deve ter um formato válido"
ERROR_PASSWORD_INVALID_FORMAT_TYPE = "Senha deve ser uma string"
ERROR_PASSWORD_INVALID_FORMAT_MIN_LENGTH = (
    "Senha deve ter pelo menos 8 caracteres"
)
ERROR_PASSWORD_INVALID_FORMAT_MAX_LENGTH = (
    "Senha deve ter no máximo 255 caracteres"
)
ERROR_PASSWORD_INVALID_FORMAT_DIGIT = "Senha deve ter pelo menos um dígito"
ERROR_PASSWORD_INVALID_FORMAT_LOWERCASE = (
    "Senha deve ter pelo menos uma letra minúscula"
)
ERROR_PASSWORD_INVALID_FORMAT_UPPERCASE = (
    "Senha deve ter pelo menos uma letra maiúscula"
)
ERROR_PASSWORD_INVALID_FORMAT_SPECIAL_CHARACTER = (
    "Senha deve ter pelo menos um caractere especial"
)
ERROR_IS_ADMIN_INVALID_FORMAT_TYPE = "Is Admin deve ser um boolean"
ERROR_NAME_INVALID_FORMAT_TYPE = "Nome deve ser uma string"
ERROR_NAME_INVALID_FORMAT_MIN_LENGTH = "Nome deve ter pelo menos 2 caracteres"
ERROR_PHONE_INVALID_FORMAT_TYPE = "Telefone deve ser uma string"
ERROR_PHONE_INVALID_FORMAT_LENGTH = (
    "Telefone deve ter pelo menos 11 dígitos no formato (XX) 9XXXX-XXXX"
)
ERROR_USERNAME_INVALID_FORMAT_TYPE = "Nome de usuário deve ser uma string"
ERROR_USERNAME_INVALID_FORMAT_MIN_LENGTH = (
    "Nome de usuário deve ter pelo menos 2 caracteres sem espaços"
)

ERROR_DATABASE_USER_ALREADY_EXISTS = "Usuário já existe"
ERROR_DATABASE_USER_NOT_FOUND = "Usuário não encontrado"
ERROR_DATABASE_USERS_NOT_FOUND = "Usuários não encontrados"
ERROR_DATABASE_INGREDIENT_ALREADY_EXISTS = "Ingrediente já cadastrado"
ERROR_DATABASE_INGREDIENT_NOT_FOUND = "Ingrediente não encontrado"
ERROR_DATABASE_INGREDIENTS_NOT_FOUND = "Ingredientes não encontrados"
ERROR_DATABASE_INGREDIENT_BATCH_NOT_FOUND = (
    "Lote de ingrediente não encontrado"
)
ERROR_DATABASE_PRODUCT_ALREADY_EXISTS = "Produto já cadastrado"
ERROR_DATABASE_PRODUCT_NOT_FOUND = "Produto não encontrado"
ERROR_DATABASE_PRODUCTS_NOT_FOUND = "Produtos não encontrados"
ERROR_PORTION_NOT_FOUND = "Porção não encontrada"
ERROR_DATABASE_PRODUCT_BATCH_NOT_FOUND = "Lote de produto não encontrado"

SERVER_ERROR = "Erro interno do servidor"

MESSAGE_USER_ADD_SUCCESS = "Usuário adicionado com sucesso"
MESSAGE_USER_DELETE_SUCCESS = "Usuário deletado com sucesso"
MESSAGE_INGREDIENT_DELETE_SUCCESS = "Ingrediente deletado com sucesso"
MESSAGE_INGREDIENT_BATCH_DELETE_SUCCESS = (
    "Lote de ingrediente deletado com sucesso"
)

ERROR_TOKEN_CLAIMS_INVALID = "Token inválido"
ERROR_TOKEN_EXPIRED = "Token expirado"
ERROR_TOKEN_REQUIRED = "Token obrigatório"
ERROR_ACCESS_USER_UNAUTHORIZED = "Usuário não autorizado"

ERROR_NOT_ENOUGH_INGREDIENTS = "Ingredientes insuficientes"
ERROR_NOT_ENOUGH_PRODUCTS = "Produtos insuficientes"
ERROR_NOT_ENOUGH_PRODUCT_BATCHES = "Lotes de produtos insuficientes"
ERROR_NOT_ENOUGH_PRODUCT_IN_STOCK = "Produto insuficiente em estoque"
ERROR_NOT_ENOUGH_INGREDIENT_BATCHES = "Lotes de ingredientes insuficientes"
ERROR_NOT_ENOUGH_INGREDIENT_IN_STOCK = "Ingrediente insuficiente em estoque"
ERROR_NOT_ENOUGH_PORTIONS = "Porções insuficientes"
