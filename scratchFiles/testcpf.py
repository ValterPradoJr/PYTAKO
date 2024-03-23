def valida_cpf(cpf):
    if cpf.isdigit() and len(cpf) == 11:
        numbers = [int(digit) for digit in cpf if digit.isdigit()]
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
    else:
        return False
    
print(valida_cpf('03535635012'))