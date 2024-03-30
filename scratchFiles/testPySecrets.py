import secrets

# Função para gerar token único
def generate_token():
    return secrets.token_urlsafe(4).upper()

print(generate_token())

test_var = 'upper'
test_var2 = 'upper213'
test_var3 = '31231'

print(test_var.upper())
print(test_var2.upper())
print(test_var3.upper())