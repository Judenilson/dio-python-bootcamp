class Conta:
    def __init__(self, saldo):
        self.__saldo = saldo
        self.__limite = 500
        self.__extrato = ""
        self.__numero_saques = 0
        self.__limite_saque_dia = 3

    def saldo(self):
        """
        Imprime o saldo atual da conta em um formato legível.
        """   
        print("-------------------------------------------")
        print(f"Saldo: R$ {self.__saldo:.2f}")
        print("-------------------------------------------")

    def imprimir_extrato(self):
        """
        Imprime o extrato da conta, mostrando todas as movimentações e o saldo atual.

        Se não houver movimentações, informa que não foram realizadas movimentações.
        """    
        print("\n::::::::::::::::: EXTRATO :::::::::::::::::")

        if not self.__extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(self.__extrato)

        self.saldo()

    def depositar(self, valor):
        """
        Adiciona um valor ao saldo da conta, atualizando o extrato e imprimindo o saldo.

        Args:
            valor (float): O valor a ser adicionado ao saldo da conta.

        Returns:
            int: Código de status do depósito:
                - 0: Se o valor for menor ou igual a zero.
                - 1: Se o depósito for realizado com sucesso.
        """      
        if valor <= 0:
            return 0

        self.__saldo += valor
        self.__extrato += f"Depósito: R$ {valor:.2f}\n"
        self.saldo()
        return 1

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
                - 1: Se o saque for realizado com sucesso.
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
        self.saldo()
        return 1


menu = """

!!! DIO BANK !!!

[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair

=> """

conta = Conta(0)

while True:

    opcao = input(menu).lower()

    if opcao == "d":
        entrada = input("Informe o valor para depositar: ")
        if entrada.isdigit():
            valor = float(entrada)
            result = conta.depositar(valor=valor)
            print("Depósito concluído com sucesso." if result else "!!! Erro >>> Valor inválido.")
        else:
            print("!!! Erro >>> Entrada inválida, digite apenas números!")

    elif opcao == "s":
        entrada = input("Informe o valor para sacar: ")
        if entrada.isdigit():
            valor = float(entrada)
            result = conta.sacar(valor=valor)
            mensagens = {
                        -1: "!!! Erro >>> Você não tem saldo suficiente.",
                        -2: "!!! Erro >>> O valor do saque excede o limite diário.",
                        -3: "!!! Erro >>> Número máximo de saques diários excedido.",
                        1: "Saque realizado com sucesso."
                    }
            print(mensagens.get(result, "!!! Erro >>> Valor inválido."))
        else:
            print("!!! Erro >>> Entrada inválida, digite apenas números!")

    elif opcao == "e":
        conta.imprimir_extrato()

    elif opcao == "x":
        break

    else:
        print("Opção inválida! Selecione novamente a operação desejada.")
