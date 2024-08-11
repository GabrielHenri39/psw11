import re
from django.contrib import messages
from django.contrib.messages import constants




def calcular_digitos_verificadores(cnpj):
    """Calcula os dígitos verificadores de um CNPJ.

    Args:
        cnpj: Os primeiros 12 dígitos do CNPJ.

    Returns:
        tuple: Uma tupla com os dois dígitos verificadores.
    """

    multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma_1 = sum(int(digito) * multiplicador for digito, multiplicador in zip(cnpj, multiplicadores_1))
    resto_1 = soma_1 % 11
    digito_1 = resto_1 if resto_1 <= 9 else 0

    cnpj += str(digito_1)
    soma_2 = sum(int(digito) * multiplicador for digito, multiplicador in zip(cnpj, multiplicadores_2))
    resto_2 = soma_2 % 11

    digito_2 = resto_2 if resto_2 <= 9 else 0
    print(f'digito 1 {digito_1} digito 2 {digito_2}')

    return str(digito_1) + str( digito_2)

    
def valida_cnpj(request, cnpj):  # type: ignore
    """Valida um CNPJ brasileiro.

    Args:
        cnpj (str): O número do CNPJ a ser validado.

    Returns:
        tuple: Uma tupla (bool, str), onde o primeiro elemento indica se o CNPJ é válido e o segundo é uma mensagem de erro.
    """

    cnpj = re.sub(r'[^0-9]', '', cnpj) # type: ignore

    if len(cnpj) != 14: # type: ignore
        messages.add_message(request,constants.ERROR,'CNPJ inválido:  deve conter 14 dígitos')
        return False
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14: # type: ignore
        messages.add_message(request,constants.ERROR,"CNPJ inválido: todos os dígitos são iguais")
        return False

   
    
    digitos_verificadores_calculados = calcular_digitos_verificadores(cnpj[:12]) # type: ignore
    if digitos_verificadores_calculados != cnpj[-2:]: # type: ignore
          # Verifica os dígitos verificadores
        messages.add_message(request, constants.ERROR, "CNPJ inválido: dígitos verificadores incorretos")
        return False
    return True


def valida_site(request,site):
      # type: ignore
    """Valida um site.

    Args:
        site (str): O site a ser validado.

    Returns:
        tuple: Uma tupla (bool, str), onde o primeiro elemento indica se o site é válido e o segundo é uma mensagem de erro.
    """

    if len(site) < 4:
        messages.add_message(request, constants.ERROR, 'Site inválido: deve conter pelo menos 4 caracteres')
        return False
    if not site.startswith('http://') and not site.startswith('https://'):
        messages.add_message(request, constants.ERROR, 'Site inválido: deve começar com "http://" ou "https://"')
        return False
    return True