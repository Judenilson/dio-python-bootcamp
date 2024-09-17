class Conta:
    def __init__(self, numero, saldo, usuario):
        self.numero = numero
        self.usuario = usuario
        self.agencia = "0001"
        self._saldo = saldo
        self._limite = 500
        self._extrato = ""
        self._numero_saques = 0
        self._limite_saque_dia = 3

    @property
    def saldo(self):
        return self._saldo 
    
    @property
    def extrato(self):
        return self._extrato    
    
    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

    def imprimir_extrato(self, saldo, /, *, extrato):
        """
        Retorna o extrato da conta, mostrando todas as movimentações.

        Se não houve movimentações, retorna uma string informando que não foram realizadas movimentações.
        """
        response = extrato
        response += f"----------------- Saldo: R$ {saldo:.2f}\n"
        if not extrato:
            return "Não foram realizadas movimentações."
        else:
            return response

    def depositar(self, valor, /):
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

        self._saldo += valor
        self._extrato += f"Depósito: R$ {valor:.2f}\n"
        return self._saldo

    def sacar(self, *, valor):
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

        if valor > self._saldo:
            return -1

        if valor > self._limite:
            return -2

        if self._numero_saques >= self._limite_saque_dia:
            return -3

        self._saldo -= valor
        self._extrato += f"Saque: R$ {valor:.2f}\n"
        self._numero_saques += 1
        return self._saldo


class Usuario:
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
            
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
                    print("------------------------------------")
                    print(f"Numero: {conta.numero}")   
                    print(f"Nome: {conta.usuario.nome}")   
                    print(f"CPF: {conta.usuario.cpf}")   
                    print(f"Data de Nascimento: {conta.usuario.data_nascimento}")   
                    print(f"Endereço: {conta.usuario.endereco}")   
                    print("------------------------------------")

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
                    data_nascimento = input("Digite a data de nascimento do cliente (dd-mm-aaaa):")      
                    endereco = input("Digite o endereco do cliente:")      
                    usuario = Usuario(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)  
                    usuarios.append(usuario)

        elif opcao == "x":
            break
    elif menu_opcao == 1:
        opcao = input(menu(menu_opcao)).lower()
        if opcao == "d":
            entrada = input("Informe o valor para depositar: ")
            if verificacao_entrada(entrada):
                valor = float(entrada)
                result = conta_atual.depositar(valor)
                print(f"Depósito concluído com sucesso. O salto autal é R$ {result}" if result else "!!! Erro >>> Valor inválido.")

        elif opcao == "s":
            entrada = input("Informe o valor para sacar: ")
            if verificacao_entrada(entrada):
                valor = float(entrada)
                result = conta_atual.sacar(valor=valor)
                mensagens = {
                            -1: "!!! Erro >>> Você não tem saldo suficiente.c",
                            -2: "!!! Erro >>> O valor do saque excede o limite diário.",
                            -3: "!!! Erro >>> Número máximo de saques diários excedido."
                        }
                print(mensagens.get(result, f"Saque realizado com sucesso. O saldo atual é R$ {result}."))

        elif opcao == "e":
            print("\n::::::::::::::::: EXTRATO :::::::::::::::::")
            print(conta_atual.imprimir_extrato(conta_atual.saldo, extrato=conta_atual.extrato))

        elif opcao == "x":
            menu_opcao = 0

        else:
            print("Opção inválida! Selecione novamente a operação desejada.")
