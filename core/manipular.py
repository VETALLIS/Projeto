import requests #importação de biblioteca requisições http e consumir API´s 
import urllib  #importação de biblioteca requisições http

class Manipular: #vai comparar a senha inserida com a senha criada para acessar a tela desejada.
    def comparar_criacao_senha(campo1, campo2):
        if campo1 != campo2:
            return f"As senhas não condizem uma com a outra."
        return None

    def validar_caracter_recuperar_senha(dados, field_name): #na tela recuperar senha, no campo senha ele  valida se há caractere especial
        special= ["!", "@", "#", "$","%", "&", "*", "-", "+", "=", "¨", "/", ";" "?", "°", "()", "§", "£", "¢", "¬", "^" "`", "|", "_"]
        try:
            for caractere in dados:
                if caractere in special:
                    return True
        except(TypeError, ValueError):
            return f"O campo {field_name} está faltando um caracter especial"
        return False
    
    def validar_min_caracter(dados,field_name): #valida se há no mínimo 3 caracteres pela variável min_carac, pelo len e manda mensagem caso nao atinja 3 carac
        min_carac= 3
        if len(dados) >= min_carac:
            return None
        else:
            return f"O campo {field_name} está muito curto"


    def validar_caracter(dados, field_name):
        """Retorna mensagem de erro se NÃO houver caractere especial, senão None."""
        special = set("!@#$%&*-+=¨/;?°()§£¢¬^`|_")

        if not isinstance(dados, str):
            return f"O campo {field_name} deve ser um texto"

        if any(c in special for c in dados):
            return None

        return f"O campo {field_name} está faltando um caractere especial"

    def validar_not_caracter(dados, field_name): #Valida se um campo NÃO tem caractere especial (nao pode ter) IS instance= 
    # serve para verificar se um objeto pertence a uma classe ou a um tipo de dado específico, verifica herança. Manda mesagem caso houver caractere especial
            if not isinstance(dados, str):
                return f"O campo {field_name} deve ser um texto"

            for caractere in dados:
                if not (caractere.isalnum() or caractere.isspace()):
                    return f"O campo {field_name} não pode conter caractere especial: '{caractere}'"

            return None
    
    def validar_vazio(dados, field_name):  # Verifica e manda mensagem de erro caso o campo estiver vazio e não puder
        if dados is None or str(dados).strip() == "":
            return f"O campo {field_name} é obrigatório."
        return None

        
    def validar_letra(dados, field_name): #Valida se SÓ HÁ letras e envia mensagem de erro caso contenha números
        for char in str(dados):
            if char.isdigit():
                return f"O campo {field_name} não pode conter números."
        return None

    def validar_numero(dados, field_name):  #verifica pelo char e o is digit se há número, manda mensagem de erro caso não tenha
        for char in str(dados):
            if char.isnumeric():
                return None
        return f"O campo {field_name} deve conter números."


    def validar_numero_negativo(dados, field_name): #float valida e aceita apenas números inteiros(maior que zero) e se há caractere numérico
        try:
            if float(dados) < 0:
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None
    
    def validar_cpf(dados, field_name, token): #API externa invertexto valida o cpf
        url = "https://api.invertexto.com/v1/validator"  # Endereço do endpoint de validação da API

        params={ # Parâmetros que vão na query string: token e value
            "token":token, # chave de acesso à API
            "value":dados # valor que será validado (o CPF)
        }
        try:  # Faz a requisição get para a apicom os parametros
            response = requests.get(url, params=params) 
            response.raise_for_status()
            data= response.json() # converte Json em dic python
            if data["valid"] != True: #resposta da API se é valido ou não
                return f'CPF invalido'
            return None #se estiver tudo certo

        except requests.exceptions.HTTPError as errh: #erro http
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc: #falha na conexão 
            print("Erro de conexão:", errc)
        except requests.exceptions.Timeout as errt: #api demorou p responder
            print("Timeout:",errt)
        except requests.exceptions.RequestException as err: #outro tipo de erro
            print ("Erro:", err)

        return False 
        
    def validar_cnpj(dados, field_name, token): #API externa invertexto valida o cnpj
        url = "https://api.invertexto.com/v1/validator"


        params={
            "token":token, #''
            "value":dados #''
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data= response.json()                               #''
            if data["valid"] != True:
                return f'CNPJ invalido'
            return None

        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão:", errc)                     #''
        except requests.exceptions.Timeout as errt:
            print("Timeout:",errt)
        except requests.exceptions.RequestException as err:
            print ("Erro:", err)

        return False
    
    def validar_email(dados, field_name, token): #API externa invertexto valida o email 
        base_url= "https://api.invertexto.com/v1/email-validator"
        email_encoded = urllib.parse.quote (dados) # codificação do email
             # safe garante que ate a barra seja codificada
        url= f"{base_url}/{email_encoded}"                    
        params = {"token": token}

        try:
            response = requests.get (url, params=params)
            response.raise_for_status()

            data = response.json()
            if data["valid_format"] != True or data["valid_mx"] == False or  data["disposable"] != False: 
                 # Inválido se: formato ruim, sem servidor de email (MX) ou descartável
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
        
    def validar_data(dados, field_name):#API externa invertexto valida A DATA
        meses = ['01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12',] #lista de meses válidos
        if len(dados) == 10: #caracteres da data 
            try:
                if int(dados[0:5]) >= 2026: #compara com 2026 e não aceita se a data for apos 2026
                    if dados[3:5] in meses: #pega as posicoes 3 e 4  e confere se esta dentre os numeros da lista de meses
                        if dados[4:6] in ['01', '03', '05', '07', '08', '10', '12']: #confere se o mês tem 31 dias                            if 0 < int(dados[0:2]) <= 31:
                                return None
                            else: #o dia não está entre 1 e 31
                                return f"O campo {field_name} está incorreto"
                        elif dados[4:6] in ['04', '06', '09', '11']: #se não, ve se tem 30 dias
                            if 0 < int(dados[0:2]) <= 30: 
                                return None
                            else:
                                return False
                        else: #fevereiro
                            if int(dados[8:]) == 28:
                                return None
                            else:
                                return False
                    else: # se o mês não está na lista de meses
                        return f"A {field_name} está com o mês incorreto"
            except ValueError as e:
                    (f"A {field_name} está com o ano incorreto")
        else:
            return f"O {field_name} não está de acordo com essa validação"
        return False