class Conta:
    def __init__(self, numero, saldo, usuario):
        self.__numero = numero
        self.__saldo = saldo
        self.__usuario = usuario
        self.__agencia = "0001"
        self.__limite = 500
        self.__extrato = ""
        self.__numero_saques = 0
        self.__limite_saque_dia = 3

    @property
    def saldo(self):
        return self.__saldo 
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def usuario(self):
        return self.__usuario

    def imprimir_extrato(self):
        """
        Retorna o extrato da conta, mostrando todas as movimentações.

        Se não houve movimentações, retorna uma string informando que não foram realizadas movimentações.
        """    
        if not self.__extrato:
            return "Não foram realizadas movimentações."
        else:
            return self.__extrato

    def depositar(self, valor):
        """
        Adiciona um valor ao saldo da conta, atualizando o extrato e imprimindo o saldo.

        Args:
            valor (float): O valor a ser adicionado ao saldo da conta.

        Returns:
            int: Código de status do depósito:
                - 0: Se o valor for menor ou igual a zero.
                - saldo: Se o depósito for realizado com sucesso.
        """      
        if valor <= 0:
            return 0

        self.__saldo += valor
        self.__extrato += f"Depósito: R$ {valor:.2f}\n"
        return self.__saldo

    def sacar(self, valor):
        """
        Realiza um saque do saldo da conta, atualizando o extrato e o número de saques.

        Args:
            valor (int): O valor a ser sacado do saldo da conta.

        Returns:
            int: Código de status do saque:
                - 0: Se o valor for menor ou igual a zero.
                - -1: Se o valor for maior que o saldo disponível.
                - -2: Se o valor exceder o limite de saque permitido.
                - -3: Se o número de saques diários exceder o limite permitido.
                - saldo: Se o saque for realizado com sucesso.
        """        
        if valor <= 0:
            return 0

        if valor > self.__saldo:
            return -1

        if valor > self.__limite:
            return -2

        if self.__numero_saques >= self.__limite_saque_dia:
            return -3

        self.__saldo -= valor
        self.__extrato += f"Saque: R$ {valor:.2f}\n"
        self.__numero_saques += 1
        return self.__saldo


class Usuario:
    def __init__(self, cpf, nome):
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = ''
        self.__endereco = ''
            
    @property
    def nome(self):
        return self.__nome
    
    @property
    def cpf(self):
        return self.__cpf 

    def data_nascimento(self, data):
        if isinstance(data, str):
            self.__data_nascimento = data
        else:
            raise ValueError("O nome deve ser uma string")
    
    def endereco(self, endereco):
        self.__endereco = endereco
        return self.__endereco

def menu(opcao):
    if opcao > 2:
        return "Erro !!!"
    menu = [f"""
    -----------------------------------
    !!! DIO BANK - MÓDULO GERENCIAL !!!
    -----------------------------------
    [a] Acessar Conta
    [l] Listar Contas
    [n] Nova Conta
    [c] Cadastrar Usuário
    [x] Sair
    => """, f"""
    -----------------------------------
      !!! DIO BANK - MÓDULO CONTA !!!
    -----------------------------------
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [x] Menu Principal
    => """]
    return menu[opcao]

# usuario = Usuario(123,'Jud')
# conta = Conta(1, 0, usuario)
menu_opcao = 0
conta_atual = ""
contas_numeracao = 0
contas = []
usuarios = []

def verificacao_entrada(numero):
    if numero.isdigit():
        return True
    else:
        print("!!! Erro >>> Entrada inválida, digite apenas números! Operação Cancelada!")
        return False

while True:

    if menu_opcao == 0:
        opcao = input(menu(menu_opcao)).lower()

        if opcao == "a":
            entrada = input("Digite o número da conta:")
            if verificacao_entrada(entrada):
                for conta in contas:
                    if conta.numero == int(entrada):
                        conta_atual = conta
                        menu_opcao = 1
                        break                

        elif opcao == "l":
            if len(contas) == 0:
                print("Não existem contas cadastradas!")
            else:
                for conta in contas:
                    print(f"Numero: {conta.numero}")   
                    print(f"Nome: {conta.usuario.nome}")   
                    print(f"CPF: {conta.usuario.cpf}")   

        elif opcao == "n":
            entrada = input("Digite o número do CPF do usuário da nova conta:")
            if verificacao_entrada(entrada):
                cpf = int(entrada)
                nao_encontrado = True
                for usuario in usuarios:
                    if usuario.cpf == cpf:
                        contas_numeracao += 1
                        conta = Conta(numero=contas_numeracao, saldo=0, usuario=usuario)
                        contas.append(conta)
                        nao_encontrado = False
                        break
                if nao_encontrado: 
                    print('Número de CPF inexistente no banco de dados de clientes!')            
            
        elif opcao == "c":             
            entrada = input("Digite o CPF do novo cliente (apenas números):")
            if verificacao_entrada(entrada):
                cpf = int(entrada)
                existe_cpf = any(usuario.cpf == cpf for usuario in usuarios)
                if(existe_cpf):
                    print("CPF já cadastrado na Base de Dados! Operação cancelada!")                
                else:
                    nome = input("Digite o nome do novo cliente:")      
                    usuario = Usuario(cpf=cpf, nome=nome)  
                    usuarios.append(usuario)

        elif opcao == "x":
            break
    elif menu_opcao == 1:
        opcao = input(menu(menu_opcao)).lower()
        if opcao == "d":
            entrada = input("Informe o valor para depositar: ")
            if verificacao_entrada(entrada):
                valor = float(entrada)
                result = conta_atual.depositar(valor=valor)
                print(f"Depósito concluído com sucesso. O salto autal é R$ {result}" if result else "!!! Erro >>> Valor inválido.")

        elif opcao == "s":
            entrada = input("Informe o valor para sacar: ")
            if verificacao_entrada(entrada):
                valor = float(entrada)
                result = conta_atual.sacar(valor=valor)
                mensagens = {
                            -1: "!!! Erro >>> Você não tem saldo suficiente.",
                            -2: "!!! Erro >>> O valor do saque excede o limite diário.",
                            -3: "!!! Erro >>> Número máximo de saques diários excedido."
                        }
                print(mensagens.get(result, f"Saque realizado com sucesso. O saldo atual é R$ {result}."))

        elif opcao == "e":
            print("\n::::::::::::::::: EXTRATO :::::::::::::::::")
            print(conta_atual.imprimir_extrato())

        elif opcao == "x":
            menu_opcao = 0

        else:
            print("Opção inválida! Selecione novamente a operação desejada.")
