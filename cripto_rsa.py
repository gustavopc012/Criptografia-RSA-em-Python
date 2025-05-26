import math
import os

# Máximo Divisor Comum
def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Para calcular d, usando o algoritmo de Euclides
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Substituindo letras da mensagem por números de acordo com o alfabeto A-Z + espaço, iniciando em A = 2 e indo até espaço = 28
def codificar_mensagem(mensagem):
    tabela = {chr(i + 65): i + 2 for i in range(26)}
    tabela[' '] = 28
    mensagem = mensagem.upper()

    for char in mensagem:
        if char not in tabela:
            raise ValueError(f"Caractere inválido: '{char}'. Use apenas letras A-Z e espaço.")

    return [tabela[char] for char in mensagem]

def decodificar_mensagem(codigos):
    tabela = {i + 2: chr(i + 65) for i in range(26)}
    tabela[28] = ' '
    return ''.join([tabela[c] for c in codigos])

# Para gerar uma chave pública, inicialmente se escolhe dois primos diferentes e um expoente relativamente primo/coprimo, para ser coprimo eles tem que ter apenas 1 como fator comum
def gerar_chave_publica():
    p = int(input("Digite um numero primo p: "))
    q = int(input("Digite um numero primo q: "))
    e = int(input("Digite um expoente e relativamente primo a (p-1)(q-1): "))

    if not (eh_primo(p) and eh_primo(q)):
        print("p e q precisam ser primos.")
        return

    # Aqui é feito calculo para gerar as chaves, é necessário a multiplicação dos números primos para gerar o n que será usado na próxima etapa
    n = p * q

    if(n <= 28):
        print("\n")
        print("Digite valores para p e q de forma que p * q >= 28.")
        return

    # Para os valores de e e d que servem tanto para a chave pública e privada, respectivamente, verifica-se phi para ver se eles são coprimos de n    
    phi = (p - 1) * (q - 1)
    # O número e é escolhido livremente, porém ele precisa ser coprimo de phi, por isso a verificação usando o mdc que deve ser 1 para que sejam coprimos
    if mdc(e, phi) != 1:
        print("e não é relativamente primo a (p-1)(q-1).")
        return

    with open("chave_publica.txt", "w") as f:
        f.write(f"{n} {e}")

    # Chaves públicas n e e geradas
    print("Chave pública gerada e salva em chave_publica.txt")

def encriptar():
    mensagem = input("Digite a mensagem (A-Z e espaço): ")
    n = int(input("Digite o valor de n da chave pública: "))
    e = int(input("Digite o valor de e da chave pública: "))

    # Chama a função de codificação para aplicar a criptografia pedida na mensagem usando o alfabeto de A-Z + espaço
    codigos = codificar_mensagem(mensagem)
    # Para encriptar é aplicada a fórmula que usa os números das chaves públicas, sendo cifra = mensagem ^ chave pública e mod chave pública n
    cifra = [pow(m, e, n) for m in codigos]

    with open("mensagem_encriptada.txt", "w") as f:
        f.write(' '.join(map(str, cifra)))

    print("Mensagem encriptada salva em mensagem_encriptada.txt")

def desencriptar():    
    p = int(input("Digite o valor de p: "))
    q = int(input("Digite o valor de q: "))
    e = int(input("Digite o valor de e: "))

    # Aqui é feito cálculo para gerar as chaves, é necessário a multiplicação dos números primos para gerar o n que será usado na próxima etapa
    n = p * q
    # Para os valores de e e d que servem tanto para a chave pública e privada, respectivamente, verifica-se phi para ver se eles são coprimos de n    
    phi = (p - 1) * (q - 1)
    # Nessa criptografia, d precisa ser o inverso modular de e, o que quer dizer que a multiplicação de d x e tem que ser 1 e tem que resultar em 1 novamente se calcularmos o mod de phi(n), como: (e x d) mod phi(n) = 1    
    d = modinv(e, phi)
    # O d é calculado usando o algoritmo de Euclides

    if not os.path.exists("mensagem_encriptada.txt"):
        print("Arquivo mensagem_encriptada.txt não encontrado.")
        return

    with open("mensagem_encriptada.txt", "r") as f:
        cifra = list(map(int, f.read().split()))

    # Para desencriptar, o inverso da fórmula é aplicado, usando os números das chaves privadas
    # Sendo mensagem' = cifra ^ chave privada d mod chave privada n
    decodificada = [pow(c, d, n) for c in cifra]
    mensagem = decodificar_mensagem(decodificada)

    with open("mensagem_desencriptada.txt", "w") as f:
        f.write(mensagem)

    print("Mensagem desencriptada salva em mensagem_desencriptada.txt")

def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Gerar chave pública")
        print("2 - Encriptar")
        print("3 - Desencriptar")
        print("4 - Sair")

        opcao = input("Opção: ")

        if opcao == '1':
            gerar_chave_publica()
        elif opcao == '2':
            encriptar()
        elif opcao == '3':
            desencriptar()
        elif opcao == '4':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()