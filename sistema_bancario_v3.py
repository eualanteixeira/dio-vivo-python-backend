from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:

    def __init__(self, cpf: int) -> None:
        self.cpf = cpf
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: int, endereco: str) -> None:
        super().__init__(cpf)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historio = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historio
    
    def sacar(self ,valor: float) -> float:
        saldo = self.saldo
                
        if self._valor_maior_que_saldo(valor,saldo):
                print(f'Valor solicitado é maior que o saldo atual: {saldo:.2f}')
        
        elif self._valor_maior_que_zero(valor):
            self._saldo -= valor
            print(f'Saque realizado no valor de R${valor:.2f}')
            return True

        else:
            print(f'Operacao falhou!')

        return False
    
    @staticmethod
    def _valor_maior_que_saldo(valor,saldo):
        if valor > saldo:
            return True
        
    @staticmethod
    def _valor_maior_que_zero(valor):
        if valor > 0:
            return True
        
    def depositar(self, valor):
        if self._valor_maior_que_zero(valor):
            self._saldo += valor
            print(f'Deposito realizado no valor de {valor:.2f}')
            return True
        else:
            print('O valor nao pode ser menor ou igual a Zero')
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'Saque']
        )
        if self._valor_maior_que_limite(valor,self.limite):
            print(f'Saque maior que o limite diario por operacao de R$ {self.limite}')

        elif ContaCorrente._numero_saque_maior_limite_saques(numero_saques, self.limite_saque):
            print(f'O limite de {self.limite} saques diarios foi exedido.')

        else:
            return super().sacar(valor)
        
        return False

    @classmethod
    def _valor_maior_que_limite(cls,valor,limite):
        if valor > limite:
            return True
    
    @classmethod
    def _numero_saque_maior_limite_saques(cls,numero_saques,limite_saques):
        if numero_saques > limite_saques:
            return True
        


    def __str__(self) -> str:
        return f'''
            Agencia: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente.nome}
        '''

class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self,):
        return self._transacoes
     
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if isinstance(conta, ContaCorrente):
            sucesso = conta.sacar(self.valor)

            if sucesso:
                conta.historico.adicionar_transacao(self)

        else:
            print("Saque disponivel apenas para conta corrente. ")

class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = '''
    [D]: Depositar
    [S]: Sacar
    [E]: Extrato
    [CU]: Cadastrar Usuario
    [CC]: Cadastrar Conta
    [LC]: Listar Contas
    [EX]: Sair
'''
    return input(menu).upper()

def filtrar_cliente(cpf, clientes):
    clientes_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrado[0] if clientes_filtrado else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente nao possui conta')
        return
    return cliente.contas[0]

def depositar(cpf, clientes, valor):
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente nao encontrado')
        return
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(cpf, clientes, valor):
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente nao encontrado')
        return
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def extrato_bancario(cpf, clientes):
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente nao encontrado')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    transacoes = conta.historico.transacoes
    extrato = ''

    if not transacoes:
        extrato = 'Nao ha movimentacoes'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: {transacao['valor']:.2f} - {transacao['data']}"
    print(extrato)  
    print(f'\tSaldo: R$ {conta.saldo:.2f}')  

def criar_conta(cpf: int, numero_conta, clientes, contas: list):

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente nao encontrada')
        return
    
    conta = ContaCorrente.nova_conta(numero_conta, cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')
    
def listar_contas(contas):

    for conta in contas:
        print('=' * 100)
        print(conta)

def criar_cliente(cpf, clientes: list):
    
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Cliente encontrado')
        return
    
    nome = input('Informe seu nome completo: ')
    data_nascimento = input('Informe a data de nascimento no formato DD/MM/AAAA: ')
    endereco =  input('Informe o endereco, rua, numero - bairro - cidade/sigla, estado: ')

    novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)

    clientes.append(novo_cliente)

    print('Cliente criado com sucesso!')

def main():
    clientes = []
    contas = []

    
    try:
        while True:
            opcao = menu()

            if opcao == 'D':
                cpf = int(input('Informe o CPF do cliente: '))
                valor = float(input('Informe o valor a ser depositado: '))
                depositar(cpf, clientes, valor)

            elif opcao == 'S':
                cpf = int(input('Informe o CPF do cliente: '))
                valor = float(input('Informe o valor a ser sacado: '))
                sacar(cpf, clientes, valor) 

            elif opcao == 'E':
                cpf = int(input('Informe o CPF do cliente: '))
                extrato_bancario(cpf, clientes)

            elif opcao == 'CU':
                cpf = int(input('Informe o CPF do cliente: '))
                criar_cliente(cpf, clientes)
                
            elif opcao == 'CC':
                numero_conta = len(contas) + 1
                cpf = int(input('Informe o CPF do cliente: '))
                criar_conta(cpf, numero_conta, clientes, contas)
                
            elif opcao == 'LC':
                listar_contas(contas)
                
            elif opcao == 'EX':
                break

    except Exception as e:
        print(f'Erro: {e}')

main()

