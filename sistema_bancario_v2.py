#versao 2
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

def depositar(saldo: float, valor: float, extrato:list,/,):
    
    if valor > 0:
        saldo += valor
        extrato.append(f'R$ +{valor:.2f}')
        print(f'Deposito realizado no valor de {valor:.2f}')
    else:
        print('O valor nao pode ser menor ou igual a Zero')
    return saldo, extrato

def sacar(*,saldo: float, valor: float, extrato: list, limite: float, numero_saques: int, limite_saques: float) -> float:
    if _valor_maior_que_saldo(valor,saldo):
            print(f'Valor solicitado é maior que o saldo atual: {saldo:.2f}')
            
    elif _valor_maior_que_limite(valor,limite):
        print(f'Saque maior que o limite diario por operacao de R$ {limite}')

    elif _numero_saque_maior_limite_saques(numero_saques,limite_saques):
        print(f'O limite de {limite} saques diarios foi exedido.')
    
    elif _valor_maior_que_zero(valor):
        saldo -= valor
        numero_saques += 1
        extrato.append(f'R$ -{valor:.2f}')
        print(f'Saque realizado no valor de R${valor:.2f}')

    else:
        print(f'Operecao falho!')
    return saldo, extrato

def _valor_maior_que_saldo(valor,saldo):
    if valor > saldo:
        return True
    
def _valor_maior_que_limite(valor,limite):
    if valor > limite:
        return True
    
def _numero_saque_maior_limite_saques(numero_saques,limite_saques):
    if numero_saques > limite_saques:
        return True
    
def _valor_maior_que_zero(valor):
    if valor > 0:
        return True

def extrato_bancario(saldo: float, /, *, extrato: list):
    if extrato:
        for valor in extrato:
            print(f'{valor}')
        print(f'Saldo e: R${saldo:.2f}')
    else:
        print('Essa conta nao teve movimentacao...')
    
def criar_usuario(usuarios: list, nome: str, cpf: int, data_nascimento: str, endereco: str):
    usuario_exite = _filtrar_usuario(cpf, usuarios)
    if usuario_exite:
        print(f'Usuario, {usuario_exite} ja possui cadastro')
    else:
        usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'enderco': endereco})
        print('Usuario cadastrado')

def _filtrar_usuario(cpf: int, usuarios: list):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario['nome']
        
def criar_conta(contas: list, agencia: str, usuarios: str, cpf: int):
    usuario = _filtrar_usuario(cpf,usuarios)
    if usuario:
        contas.append({'agencia': agencia, 'numero_conta': _numero_conta(contas), 'usuario': usuario })  
        print('Conta cadastrada com sucesso.')
    else:
        print('Usuario nao possui cadastro!')

def _numero_conta(contas: list):
    conta = len(contas) + 1
    return conta  

def listar_contas(contas: list):
    for conta in contas:
        if conta:
            print(f"Agencia: {conta['agencia']}\nConta: {conta['numero_conta']}\nUsuario: {conta['usuario']}\n")
        else:
            print('Nenhuma conta cadastada...')

# def sair():
#     print('Saiu')
#     break


# sair 

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    usuarios = []
    contas = []
    
    try:
        while True:
            opcao = menu()

            if opcao == 'D':
                valor = float(input('Informe o valor a ser depositado: '))
                saldo, extrato = depositar(float(saldo), float(valor), extrato)

            elif opcao == 'S':
                valor = float(input('Informe o valor que deseja sacar: '))

                saldo, extrato = sacar(
                    saldo=float(saldo),
                    valor=float(valor),
                    extrato=extrato,
                    limite=float(limite),
                    numero_saques=int(numero_saques),
                    limite_saques=LIMITE_SAQUES
                )
            elif opcao == 'E':
                extrato = extrato_bancario(
                    saldo,
                    extrato=extrato,
                )
            
            elif opcao == 'CU':
                nome = input('Informe seu nome completo: ')
                cpf = input('Infome seu CPF, "apenas numeros": ')
                data_nascimento = input('Informe a data de nascimento no formado DD/MM/AAA: ')
                endereco =  input('Informe o endereco, rua, numero - bairro - cidade/sigla, estado: ')
                criar_usuario(usuarios, nome, cpf, data_nascimento, endereco)

            elif opcao == 'CC':
                cpf = input('Infome seu CPF, "apenas numeros": ')
                criar_conta(contas, AGENCIA, usuarios, cpf)

            elif opcao == 'LC':
                listar_contas(contas)

            elif opcao == 'EX':
                break

    except Exception as e:
        print(f'Erro: {e}')

main()

