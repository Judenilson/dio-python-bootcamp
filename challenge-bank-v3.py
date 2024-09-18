from abc import ABC, abstractmethod
from datetime import datetime


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor <= 0:
            return False

        self._saldo += valor
        print("Depósito realizado com sucesso!")
        return True

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido!")
            return False

        if valor > self._saldo:
            print("Saldo insuficiente!")
            return False

        self._saldo -= valor
        print("Saque realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if (valor > self._limite) or (numero_saques >= self._limite_saques):
            print("Limite diário excedido!")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C:     {self.numero}
            Titular: {self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def add_transacao(self, transacao):
        agora = datetime.now()
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": agora.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, endereco, cpf, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        status = conta.depositar(self.valor)

        if status:
            conta.historico.add_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        status = conta.sacar(self.valor)

        if status:
            conta.historico.add_transacao(self)


""" ---->  FRONT-END  <----- """


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


def verificacao_entrada(numero):
    if numero.isdigit():
        return True
    else:
        print("!!! Erro >>> Entrada inválida, digite apenas números! Operação Cancelada!")
        return False


def depositar(conta):
    entrada = input("Informe o valor para depositar: ")
    if verificacao_entrada(entrada):
        valor = float(entrada)
        transacao = Deposito(valor)
        cliente = conta.cliente
        cliente.realizar_transacao(conta, transacao)


def sacar(conta):
    entrada = input("Informe o valor para sacar: ")
    if verificacao_entrada(entrada):
        valor = float(entrada)
        transacao = Saque(valor)
        cliente = conta.cliente
        cliente.realizar_transacao(conta, transacao)


def exibir_extrato(conta):
    print("\n::::::::::::::::: EXTRATO :::::::::::::::::")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não existem movimentações!")
        return

    extrato = ""
    for transacao in transacoes:
        extrato += f"\n{transacao['data']}\t{transacao['tipo']}\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")


def acessar_conta(contas):
    entrada = input("Digite o número da conta:")
    if verificacao_entrada(entrada):
        for conta in contas:
            if conta.numero == int(entrada):
                return (conta, 1)
        print("!!! Erro >>> conta inexistente!")
        return ("", 0)


def listar_contas(contas):
    if len(contas) == 0:
        print("Não existem contas cadastradas!")
    else:
        for conta in contas:
            print(conta)


def cadastrar_nova_conta(clientes, contas):
    entrada = input("Digite o número do CPF do usuário da nova conta:")
    if verificacao_entrada(entrada):
        cpf = int(entrada)
        for cliente in clientes:
            if cliente.cpf == cpf:
                contas_numeracao = len(contas) + 1
                conta = ContaCorrente.nova_conta(numero=contas_numeracao, cliente=cliente)
                cliente.contas.append(conta)
                contas.append(conta)
                return conta
        print('Número de CPF inexistente no banco de dados de clientes!')
        return False


def cadastrar_novo_cliente(clientes):
    entrada = input("Digite o CPF do novo cliente (apenas números):")
    if verificacao_entrada(entrada):
        cpf = int(entrada)
        existe_cpf = any(cliente.cpf == cpf for cliente in clientes)
        if (existe_cpf):
            print("CPF já cadastrado na Base de Dados! Operação cancelada!")
        else:
            nome = input("Digite o nome do novo cliente:")
            data_nascimento = input(
                "Digite a data de nascimento do cliente (dd-mm-aaaa):")
            endereco = input(
                "Digite o endereco do cliente (logradouro, Nro - Bairro - Cidade/Sigla Estado):")
            cliente = PessoaFisica(
                cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
            clientes.append(cliente)


def main():
    menu_opcao = 0
    conta_atual = ""
    contas = []
    clientes = []

    while True:

        if menu_opcao == 0:
            opcao = input(menu(menu_opcao)).lower()
            if opcao == "a":
                conta_atual, menu_opcao = acessar_conta(contas)
            elif opcao == "l":
                listar_contas(contas)
            elif opcao == "n":
                cadastrar_nova_conta(clientes, contas)
            elif opcao == "c":
                cadastrar_novo_cliente(clientes)
            elif opcao == "x":
                break
            else:
                print("Opção inválida! Selecione novamente a operação desejada.")
        elif menu_opcao == 1:
            opcao = input(menu(menu_opcao)).lower()
            if opcao == "d":
                depositar(conta_atual)
            elif opcao == "s":
                sacar(conta_atual)
            elif opcao == "e":
                exibir_extrato(conta_atual)
            elif opcao == "x":
                menu_opcao = 0
            else:
                print("Opção inválida! Selecione novamente a operação desejada.")


main()
