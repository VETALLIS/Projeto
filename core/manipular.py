# ==== Importação da bibliotecas necessaria para validação ===== #
import requests
import urllib

# ======= Criação da classe de manipulação =====#
class Manipular:
    # ====== Preparação de dados para gravação no banco
    def preparar_banco(dados):
        pass

    # ===== Validação de caracteres especiais ===== #
    def validar_caracter(dados, field_name):
        especial= ["!", "@", "#", "$","%", "&", "*",] # Define os caracteres especiais
        try:
            for caractere in dados: # Percore os dados e verifica se há caracteres especiais
                if caractere in especial:
                    return None
        except(TypeError, ValueError): # Retorna se houver erro
            return f"O campo {field_name} está faltando um caracter especial"
        return f"O campo {field_name} não contem caracteres especiais"
    
    # ===== Validação de campos vazios =====#
    def validar_vazio(dados, field_name):
        if dados is None or str(dados).strip() == "": # Verifica se esta vazio
            return f"O campo {field_name} é obrigatório."
        return None
    
    # ===== Validação de numero negartivos ===== #
    def validar_numero_negativo(dados, field_name):
        try:
            if float(dados) < 0: # Verifica se o numero é menor do que zero
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None
    
    # ======= Validação de CPF, usando a API do Invertexto ====== #
    def validar_cpf(dados, field_name, token):
        url = "https://api.invertexto.com/v1/validator" 

        params={
            "token":token,
            "value":dados
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data= response.json()
            if data["valid"] != True:
                return f'Cpf invalido'
            return None

        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:",errt)
        except requests.exceptions.RequestException as err:
            print ("Erro:", err)

        return False
    

    # ======= Validação de email, com a API do Invertexto ====== #
    def validar_email(dados, field_name, token):
        base_url= "https://api.invertexto.com/v1/email-validator"
        email_encoded = urllib.parse.quote (dados)
        url= f"{base_url}/{email_encoded}"
        params = {"token": token}

        try:
            response = requests.get (url, params=params)
            response.raise_for_status()

            data = response.json()
            if data["valid_format"] != True or data["valid_mx"] == False or  data["disposable"] != False:
                return f'Email invalido'
            return None

        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:",errt)
        except requests.exceptions.RequestException as err:
            print ("Erro:", err)

            return False
        
    # ======= Validação de datas ======= 
    def validar_data(dados, field_name):
        meses = ['01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12',] # Define os meses do ano
        if field_name == "data": # Faz a verificação da data
            print("data", dados["data"])
            if len(dados) == 10:
                for data in dados:
                    if not(data.isdigit() or data == "/"):
                        return f"O campo {field_name} está escrito de forma incorreta"
                        break
                    else:
                        data_correta = True
                if data_correta == True:
                    if int(dados[6:]) >= 2025:
                        if dados[3:5] in meses:
                            if dados[3:5] in ['01', '03', '05', '07', '08', '10', '12']:
                                if 0 < int(dados[0:2]) <= 31:
                                    return True
                                else:
                                    return f"O campo {field_name} está incorreto"
                            elif dados[3:5] in ['04', '06', '09', '11']:
                                if 0 < int(dados[0:2]) <= 30:
                                    return True
                                else:
                                    return False
                            else:
                                if int(dados[0:2]) == 28:
                                    return True
                                else:
                                    return False
                        else:
                            return f"A {field_name} está com o mês incorreto"
                    else:
                        return f"A {field_name} está com o ano incorreto"
                else:
                    return f"A {field_name} está com a data incorreta"
            else:
                return f"O {field_name} não está de acordo com essa validação"
        else:
            return ("erro no nome")