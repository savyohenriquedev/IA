# Gerador de Senhas Aleatórias
# Autor: Sávyo (Enrich)

import random  # Biblioteca para geração de números aleatórios
import string  # Biblioteca para conjuntos de caracteres (letras, dígitos, etc.)

def obter_configuracao_senha():
    """
    Solicita a pessoa as configurações da senha (comprimento e tipos de caracteres).
    Retorna uma tupla com o comprimento (int) e um dicionário de opções (bool).
    """
    # Exibe instruções claras para o usuário
    print("\n=== Configuração do Gerador de Senhas ===")
    print("Configure sua senha personalizada.")

    # Solicita o comprimento da senha, garantindo que seja um número inteiro válido
    while True:
        try:
            comprimento = int(input("Digite o comprimento da senha (mínimo 4): "))
            if comprimento < 4:
                print("Erro: O comprimento deve ser pelo menos 4 caracteres.")
                continue
            break
        except ValueError:
            print("Erro: Digite um número inteiro válido.")

    # Solicita os tipos de caracteres com validação de entrada (Sim/Não)
    # Usa um dicionário para armazenar as escolhas, facilitando expansão futura
    opcoes = {}
    perguntas = [
        ("colocar letras maiúsculas (A-Z)? (Sim/Não): ", "maiusculas"),
        ("colocar letras minúsculas (a-z)? (Sim/Não): ", "minusculas"),
        ("colocar números (0-9)? (Sim/Não): ", "numeros"),
        ("colocar símbolos (!@#$%)? (Sim/Não): ", "simbolos")
    ]

    for pergunta, chave in perguntas:
        while True:
            resposta = input(pergunta).strip().lower()
            if resposta in ["sim", "s", "não", "nao", "n"]:
                opcoes[chave] = resposta in ["sim", "s"]
                break
            print("Erro: Responda com 'Sim' ou 'Não' seu analfabeto!")

    # Verifica se pelo menos um tipo de caractere foi selecionado
    if not any(opcoes.values()):
        print("Nada selecionado. Ativando letras minúsculas por padrão.")
        opcoes["minusculas"] = True

    return comprimento, opcoes

def gerar_senha(comprimento, opcoes):
    """
    Gera uma senha aleatória com base no comprimento e nas opções fornecidas.
    Args:
        comprimento (int): Tamanho da senha.
        opcoes (dict): Dicionário com chaves 'maiusculas', 'minusculas', 'numeros',
                       'simbolos' e valores booleanos.
    Returns:
        str: Senha gerada.
    """
    # Cria um conjunto de caracteres disponíveis com base nas opções
    caracteres = ""
    if opcoes["maiusculas"]:
        caracteres += string.ascii_uppercase  # A-Z
    if opcoes["minusculas"]:
        caracteres += string.ascii_lowercase  # a-z
    if opcoes["numeros"]:
        caracteres += string.digits  # 0-9
    if opcoes["simbolos"]:
        caracteres += string.punctuation  # !@#$%, etc.

    # Gera a senha escolhendo caracteres aleatórios
    # Usa random.choice para uniformidade na seleção
    senha = "".join(random.choice(caracteres) for _ in range(comprimento))

    return senha

def main():
    """
    Função principal que coordena a execução do programa.
    Exibe um menu, coleta configurações, gera a senha e permite repetição.
    """
    print("\n=== Gerador de Senhas Aleatórias ===")
    print("Desenvolvido por Sávyo (Enrich)")

    while True:
        # Obtém as configurações do cara
        comprimento, opcoes = obter_configuracao_senha()

        # Gera e exibe a senha
        try:
            senha = gerar_senha(comprimento, opcoes)
            print(f"\nSenha gerada: {senha}")
        except Exception as e:
            # Tratamento genérico para erros inesperados (tipo caracteres vazios)
            print(f"Erro gerando senha: {e}")
            continue

        # Pergunta se o cara vai querer gerar outra senha
        while True:
            continuar = input("\nTu quer gerar outra senha? (Sim/Não): ").strip().lower()
            if continuar in ["sim", "s", "não", "nao", "n"]:
                break
            print("Erro: Responda com 'Sim' ou 'Não' seu analfabeto")

        if continuar in ["não", "nao", "n"]:
            print("Saindo. Valeu ai por usar meu código! ~Sávyo Enrich")
            break

if __name__ == "__main__":
    # Ponto de entrada do programa
    # Garante que main() só seja executado se o script for rodado diretamente
    main()