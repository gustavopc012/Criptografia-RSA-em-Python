import math

letras_para_numeros = {
    'A': 2, 'B': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7, 'G': 8,
    'H': 9, 'I': 10, 'J': 11, 'K': 12, 'L': 13, 'M': 14,
    'N': 15, 'O': 16, 'P': 17, 'Q': 18, 'R': 19, 'S': 20,
    'T': 21, 'U': 22, 'V': 23, 'W': 24, 'X': 25, 'Y': 26,
    'Z': 27, ' ': 28
}

numeros_para_letras = {v: k for k, v in letras_para_numeros.items()}

def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def calcular_phi(p, q):
    return (p - 1) * (q - 1)

def mod_inverso(e, phi):
    x0, x1 = 0, 1
    resto0, resto1 = phi, e

    while resto1 != 0:
        quociente = resto0 // resto1
        x0, x1 = x1, x0 - quociente * x1
        resto0, resto1 = resto1, resto0 - quociente * resto1

    if resto0 > 1:
        return None
    return x0 + phi if x0 < 0 else x0

def gerar_chave_publica_manual(p, q, e):
    if not (eh_primo(p) and eh_primo(q)):
        print("Erro: p e q devem ser primos.")
        return False

    phi = calcular_phi(p, q)
    if mdc(e, phi) != 1:
        print(f"Erro: e = {e} não é coprimo com φ(n) = {phi}.")
        return False

    n = p * q
    d = mod_inverso(e, phi)
    if d is None:
        print("Erro: não foi possível calcular o inverso modular.")
        return False

    retornar_chaves(n, e, d, p, q)
    return True

def criptografar_mensagem(mensagem, e, n):
    criptografada = []
    for letra in mensagem:
        if letra not in letras_para_numeros:
            print(f"Caractere inválido: {letra}")
            continue
        m = letras_para_numeros[letra]
        c = pow(m, e, n)
        criptografada.append(str(c))

    with open("criptografada.txt", "w") as file:
        file.write(" ".join(criptografada))
    return " ".join(criptografada)

def descriptografar_string(texto_criptografado, p, q, e):
    phi_n = calcular_phi(p, q)
    d = mod_inverso(e, phi_n)
    if d is None:
        return "Erro: e não tem inverso modular."

    n = p * q
    partes = texto_criptografado.split()
    mensagem = []

    for valor in partes:
        if not valor.strip():
            continue
        c = int(valor)
        m = pow(c, d, n)
        letra = numeros_para_letras.get(m, '?')
        mensagem.append(letra)

    resultado = "".join(mensagem)
    with open("msg_descriptografada.txt", "w") as file:
        file.write(resultado)
    return resultado

def retornar_chaves(n, e, d, p, q):
    with open("chaves.txt", "w") as file:
        file.write(f"Chave pública (n, e): ({n}, {e})\n")
        file.write(f"Chave privada (n, d): ({n}, {d})\n")
        file.write(f"p: {p}\nq: {q}\n")

def main():
    while True:
        print("\n" + "="*50)
        print("MENU PRINCIPAL - CRIPTOGRAFIA RSA".center(50))
        print("="*50)
        print("1 - Gerar chave pública")
        print("2 - Encriptar")
        print("3 - Desencriptar")
        print("4 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == '1':
            print("\n" + "="*50)
            print("GERAÇÃO DE CHAVES RSA".center(50))
            print("="*50)
            p = int(input("Digite p (primo): "))
            q = int(input("Digite q (primo): "))
            e = int(input("Digite e (expoente público): "))
            if gerar_chave_publica_manual(p, q, e):
                print("Chaves geradas e salvas em chaves.txt")

        elif opcao == '2':
            print("\n" + "="*50)
            print("CRIPTOGRAFIA DE MENSAGEM".center(50))
            print("="*50)
            mensagem = input("Mensagem (MAIÚSCULAS, sem acento): ").strip().upper()
            n = int(input("n (chave pública): "))
            e = int(input("e (expoente público): "))
            cripto = criptografar_mensagem(mensagem, e, n)
            print("Mensagem criptografada:")
            print(cripto)
            print("Salva em criptografada.txt")

        elif opcao == '3':
            print("\n" + "="*50)
            print("DESCRIPTOGRAFIA DE MENSAGEM".center(50))
            print("="*50)
            p = int(input("p (primo): "))
            q = int(input("q (primo): "))
            e = int(input("e (expoente público): "))

            print("\nDeseja desencriptar de:")
            print("1 - Digitar a mensagem criptografada")
            print("2 - Ler de um arquivo .txt")
            escolha = input("Escolha (1 ou 2): ").strip()

            if escolha == '1':
                texto = input("Mensagem criptografada: ").strip()
            elif escolha == '2':
                nome_arquivo = input("Nome do arquivo (ex: criptografada.txt): ").strip()
                try:
                    with open(nome_arquivo, "r") as file:
                        texto = file.read().strip()
                        print(f"Conteúdo lido: {texto}")
                except FileNotFoundError:
                    print("Arquivo não encontrado.")
                    continue
            else:
                print("Opção inválida.")
                continue

            resultado = descriptografar_string(texto, p, q, e)
            print("Mensagem descriptografada:")
            print(resultado)
            print("Salva em msg_descriptografada.txt")

        elif opcao == '4':
            print("Encerrando o programa. Até logo!")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
