menu = '''
    [D]: Depositar
    [S]: Sacar
    [E]: Extrato
    [Q]: Sair
'''
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).upper()

    if opcao == 'D':
        deposito = float(input('Informe o valor a ser depositado: '))
        if deposito <= 0:
            print('O valor nao pode ser menor ou igual a Zero')
        else:
            saldo += deposito
            extrato.append(f'+{deposito:.2f}')

    elif opcao == 'S':
        saque = float(input('Informe o valor que deseja sacar: '))

        if saque > saldo:
            print(f'Valor solicitado é maior que o saldo atual: {saldo:.2f}')
            
        elif saque > limite:
            print(f'Saque maior que o limite diario por operacao de R$ 500,00')

        elif numero_saques > LIMITE_SAQUES:
            print(f'O limite de 3 saques diarios foi exedido.')
        
        elif saque > 0:
            saldo -= saque
            numero_saques += 1
            extrato.append(f'-{saque:.2f}')

        else:
            print(f'Operecao falho!')


    elif opcao == 'E':
        if extrato is None:
            print(' Essa conta nao teve movimentacao...')
        else:
            for valor in extrato:
                print(f'{valor}')
        print(f'Saldo e: R${saldo:.2f}')

    elif opcao == 'Q':
        print('Saiu')
        break
    else:
        print('Operacao invalida, por favor selecione novamente a operacao desejada')