# -*- coding: utf-8 -*-
"""
UNIFEI - Universidade Federal de Itajuba.

LaQC - Laboratorio de Quimica Computacional

autores:
    Astrubal (calculo gerador dos spectros)
    Rogerio (interface com usuario)
"""
import math
import sys
import platform
from pathlib import Path
import numpy as np


# Constant
A = 1.30629744736E8
FACT1 = 1.0E7
FACT2 = 1.0E0
SIGMA = 3099.6


def head_msg():
    """
    Mensagem de cabeçalho.

    Returns
    -------
    None.

    """
    print()
    print("-".center(79, "-"))
    print(f'{"|":<1} {"UNIFEI - Universidade Federal de Itajubá":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Laboratório de Química Computacional":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print(f'{"|":<1} {">>> digite [sair] para encerrar o programa <<<":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print("-".center(79, "-"))
    print(f'{"|":<1} {"Gráfico UV-VIS de Cálculo dos Estados Excitados":^75} '
          f'{"|":>1}')
    print("-".center(79, "-"))
    print()


def get_separador():
    """
    Captura o separador de caminho de acordo com o sistema operacional.

    Returns
    -------
    separador : string
        Caracter separador.

    """
    separador = "/"
    sistema_operacional = platform.system()
    if sistema_operacional == 'Linux':
        separador = "/"
    else:
        separador = "\\"

    return separador


def file_exist(file=""):
    """
    Verifica se o arquivo existe.

    Parameters
    ----------
    file : txt
        Nome do arquivo e/ou diretório

    Returns
    -------
    Bool
        True, existe; False, não existe.

    """
    arq_existe = False
    if len(file) > 0:
        path = Path(file)
        arq_existe = path.exists()

    return arq_existe


def tchau():
    """
    Saindo e dizendo Tchau!.

    Returns
    -------
    None.

    """
    print("")
    print("-".center(79, "-"))
    print(f'{"|":<1} {"UNIFEI - Universidade Federal de Itajubá":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Laboratório de Química Computacional":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print(f'{"|":<1} {"Tchau!!!!":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print("-".center(79, "-"))
    print("")
    sys.exit()


def questions(type_of_fit, type_of_average, wave_numbers,
              wave_numbers_interval=0.5):
    """
    Questões que o usuário deve responder antes da execução dos procedimentos.

    Parameters
    ----------
    type_of_fit : TYPE
        Tipo de ajuste a ser feito (gaussiano ou lorentziano).
    type_of_average : TYPE
        Tipo de média a ser usada para geração do gráfico resumo.
    wave_numbers : TYPE
        Vetor que indica a faixa de número de onda a ser utilizada no cálculo.
    wave_numbers_interval : TYPE
        Intervalo entre as faixas de onda.

    Returns
    -------
    tyoe_of_fit, type_of_average, wave_numbers, wave_numbers_interval.

    """
    val = input("Tipo do ajuste (gaussian or lorentzian) "
                "[gaussian]".ljust(57, ".") + ": ").strip()
    if val != "":
        if val in ['gaussian', 'lorentzian']:
            type_of_fit = val
        else:
            if val == "sair":
                tchau()
            else:
                print(f" + Tipo de ajuste inválido ({val}), usando ({'gaussian'})")
                type_of_fit = "gaussian"

    val = input("Números de onda (100-800) [100-800]".
                ljust(57, ".") + ": ").strip()
    values = [100, 800]
    if val != "":
        if val == "sair":
            tchau()
        else:
            try:
                values = [int(i) for i in val.split("-")]
            except ValueError:
                print(f" + Wave numbers invalid ({val}), using ({'100-800'})")
                values[0] = 100
                values[1] = 800

    val = input("Intervalo dos números de onda [10.0]".ljust(57, ".") + ": ")
    if val != "":
        if val == "sair":
            tchau()
        else:
            try:
                wave_numbers_interval = float(val)
                wave_numbers = list(np.arange(values[0],
                                              values[1]+1, wave_numbers_interval))
            except ValueError:
                print(f" + Intervalo inválido ({val}), usando ({'10'})")
                wave_numbers_interval = 10

    val = input("Tipo de média (aritmética) [aritmética]".
                ljust(57, ".") + ": ").strip()
    if val != "":
        if val in ['aritmética']:
            type_of_average = val
        else:
            if val == "sair":
                tchau()
            else:
                print(f" + Tipo de média inválida ({val}),"
                      "usando ({'aritmética'})")
                type_of_average = 'aritmética'

    # Retorno
    return type_of_fit, type_of_average, wave_numbers, wave_numbers_interval


def get_arquivos(local, tipo=".log"):
    """
    Lista dos arquivos .log no diretorio especificado.

    Returns
    -------
    list_files : array
        Lista com o nome de todos os arquivos encontrados.

    """
    list_files = []

    path = Path(local)

    # List of all files with extension .log
    list_files = [log_file.name for log_file in path.iterdir()
                  if log_file.is_file() if log_file.suffix == tipo]

    return list_files


def get_arquivos_gaussian(local, tipo=".log"):
    """
    Lista dos arquivos .log no diretorio especificado.

    Já realiza tratamento de verificação da expressão "Normal termination" para o Gaussian.

    Returns
    -------
    list_files : array
        Lista com o nome de todos os arquivos encontrados.

    """
    list_files = []

    path = Path(local)

    # List of all files with extension .log
    for log_file in path.iterdir():
        if log_file.is_file() and log_file.suffix == tipo:
            if normal_termination(log_file):
                list_files.append(log_file.name)

    return list_files


def normal_termination(local_log):
    """
    Verifica a presença da expressão 'Normal termination of Gaussian 09'.

    Parameters
    ----------
    local_log : TYPE
        DESCRIPTION.

    Returns
    -------
    continuar : TYPE
        DESCRIPTION.

    """
    continuar = False
    with open(local_log) as f_arquivo:
        for line in f_arquivo:
            if "Normal termination of Gaussian 09" in line:
                continuar = True

    return continuar


def extract_data_orca():
    """
    Extraindo dados de estados excitados no arquivo de saída do Orca.

    Returns
    -------
    None.

    """
    excited_states = []
    list_num_excited_state = []

    try:
        local_files = input("Local dos arquivos".ljust(57, ".") + ": ").strip()
        if local_files.strip() != "":
            if local_files[-1] != get_separador():
                local_files = local_files + get_separador()

            if file_exist(local_files):
                list_log = get_arquivos(local_files, '.out')

                for log in list_log:
                    local_log = local_files + log
                    print(f" - Extraindo estado excitado do arquivo: {log}")
                    num_excited_state = 0
                    with open(local_log, 'r', encoding='utf-8') as f_arquivo:
                        secao_encontrada = False

                        for line in f_arquivo:
                            txt_linha = line.strip()
                            if txt_linha.startswith("ABSORPTION SPECTRUM VIA "
                                                    "TRANSITION ELECTRIC "
                                                    "DIPOLE MOMENTS"):
                                secao_encontrada = True
                            else:
                                if len(txt_linha) == 0 and secao_encontrada:
                                    break

                            if secao_encontrada:
                                resto = []
                                for i in txt_linha.split(" "):
                                    if i != "":
                                        resto.append(i)

                                try:
                                    int(resto[0])
                                    num_excited_state = num_excited_state + 1
                                    comprimento_onda = resto[2]
                                    forca_oscilador = resto[3]
                                    excited_states.append([comprimento_onda,
                                                           forca_oscilador])
                                except ValueError:
                                    continue
                        list_num_excited_state.append(num_excited_state)
                        f_arquivo.close()

                # Saving data
                f_input = open("input.dat", "w")

                # Número total de estados estrutura
                f_input.write(f"{len(list_log):<4d}\n")

                # Número de estados excitados em cada estrutura
                val_num_excited_state = " ".join(str(i) for i in
                                                 list_num_excited_state)
                f_input.write(f"{val_num_excited_state}\n")

                # Valores de número de onda e força do oscilador
                for item in excited_states:
                    valor_itens = "  ".join(str(i) for i in item)
                    f_input.write(f"{valor_itens}\n")
                f_input.close()
                print("")
    except OSError as msg_err:
        print(f" + Erro: {msg_err}")


def extract_data_gaussian():
    """
    Extraindo dados de estados excitados no arquivo de saída do Gaussian.

    Returns
    -------
    None.

    """
    excited_states = []
    list_num_excited_state = []

    try:
        local_files = input("Local dos arquivos".ljust(57, ".") + ": ").strip()
        if local_files.strip() != "":
            if local_files[-1] != get_separador():
                local_files = local_files + get_separador()

            if file_exist(local_files):
                list_log = get_arquivos_gaussian(local_files, '.log')

                # Extraindo dados
                for log in list_log:
                    local_log = local_files + log
                    print(f" - Extraindo estado excitado do arquivo: {log}")
                    num_excited_state = 0
                    with open(local_log, "r") as f_arquivo:
                        secao_encontrada = False

                        for line in f_arquivo:
                            txt_linha = line.strip()

                            if txt_linha.startswith("(Enter /scr/programs/g09/l914.exe)"):
                                secao_encontrada = True
                            else:
                                if txt_linha.startswith("Leave Link") and secao_encontrada:
                                    break

                            if secao_encontrada:
                                if txt_linha.startswith("Excited State"):
                                    num_excited_state = num_excited_state + 1

                                    # restante da linha
                                    restante = txt_linha.split(":")[1]

                                    resto = []
                                    for i in restante.split(" "):
                                        if i != "":
                                            resto.append(i)
                                    comprimento_onda = resto[3]
                                    forca_oscilador = resto[5].replace("f=", "")
                                    excited_states.append([comprimento_onda, forca_oscilador])

                        list_num_excited_state.append(num_excited_state)
                        f_arquivo.close()

                # Saving data
                f_input = open("input.dat", "w")
                f_input.write(f"{len(list_log):<4d}\n")
                f_input.write(f'{" ".join(str(i) for i in list_num_excited_state)}\n')
                for item in excited_states:
                    f_input.write(f'{"  ".join(str(i) for i in item)}\n')
                f_input.close()
                print("")
            else:
                print(" + Caminho não existe. Saindo!")
                sys.exit()

        else:
            print(" + Caminho não informado!")
            sys.exit()
    except OSError as msg_err:
        print(f" + Erro: {msg_err}")


def fit_gaussian(type_of_average, wave_numbers):
    """
    Ajuste gaussian.

    Parameters
    ----------
    type_of_average : TYPE
        DESCRIPTION.
    wave_numbers : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    average = {}
    dados_spectrum = []

    try:
        f_spectrum_gaussian = open("spectrum_gaussian.dat", "w")

        with open("input.dat", "r") as f_input:
            # m_valor representa a quantidade de estruturas que terão os espectros UV-VIS calculados
            m_valor = int(f_input.readline())
            # n_valor representa a quantidade de estados excitados para cada estrutura
            n_valor = [int(i) for i in f_input.readline().split(" ")]

            maxn = max(n_valor)
            eigenvalue = [[0.0]*maxn for i in np.arange(0, m_valor)]
            strength = [[0.0]*maxn for i in np.arange(0, m_valor)]

            for j in range(0, m_valor):
                for i in range(0, n_valor[j]):
                    read_line = f_input.readline()
                    if (read_line.strip()) != "":
                        values = [float(i) for i in read_line.split("  ")]
                        # Comprimento de onda
                        eigenvalue[j][i] = values[0]
                        # Força do oscilador
                        strength[j][i] = values[1]
        f_input.close()

        for j in range(0, m_valor):
            for nm_valor in wave_numbers:
                spectrum = 0.0
                for i in range(0, n_valor[j]):
                    if type_of_average == 'aritmética':
                        vlr_spectrum = A * (strength[j][i] / (FACT1/SIGMA)) * \
                            math.exp(-(((1.0/nm_valor) - (1.0/eigenvalue[j][i]))/(FACT2/SIGMA))**2)
                        spectrum = spectrum + vlr_spectrum

                # Registra os valores calculados para cada número de onda
                # para depois calcular desvio padrão e erro
                dados_spectrum.append([nm_valor, spectrum])
                f_spectrum_gaussian.write(f"{nm_valor:<4f}   {spectrum:>6.10f}\n")

                if nm_valor in average:
                    average[nm_valor] = average[nm_valor] + spectrum
                else:
                    average[nm_valor] = spectrum

            f_spectrum_gaussian.write("\n")

        f_spectrum_gaussian.close()
        print("")
        print("Aquivo spectrum_gaussian.dat gerado!")

        # Calculating and saving average
        if type_of_average == 'aritmética':
            for key in average.keys():
                average[key] = average[key] / m_valor

        with open("average_spectrum.dat", "w") as f_average:
            for key, value in average.items():
                f_average.write(f"{key:<4f}   {value:>6.10f}\n")
        f_average.close()
        print("Arquivo average_spectrum.dat gerado!")

        # Calculando erro padrão
        np.savetxt("dados_spectrum.txt", dados_spectrum, fmt="%6.10f", delimiter=";")
        medias_spectrum = [[i, average[i]] for i in average]
        np.savetxt("medias.txt", medias_spectrum, fmt="%6.10f", delimiter=";")

        # Calculo do desvio padrão e erro
        calcula_dp_erro(medias_spectrum, dados_spectrum)
    except OSError as msg_err:
        print(f"Erro: {msg_err}")
    except ZeroDivisionError:
        print(f"Divisão por zero: {A} * ({strength[j][i]} / "
              "({fact1}/{sigma})) * math.exp(-(((1.0/{nm})-"
              "(1.0/{eigenvalue[j][i]}))/({fact2}/{sigma}))**2)")


def calcula_dp_erro(medias_spectrum, dados_spectrum):
    """
    Cálculo do desvio padrão e erro padrão.

    Returns
    -------
    None.

    """
    vlr_dp = []
    for i in medias_spectrum:
        num_onda = i[0]
        vlr_spec = i[1]
        qtde = 0
        diferenca = 0
        for j in dados_spectrum:
            if j[0] == num_onda:
                diferenca = diferenca + ((vlr_spec - j[1])**2)
                qtde += 1
        vlr_dp.append[[num_onda, diferenca/qtde]]



def fit_lorentzian(type_of_average, wave_numbers):
    """
    Ajuste lorentzian.

    Parameters
    ----------
    type_of_average : TYPE
        DESCRIPTION.
    wave_numbers : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    average = {}

    try:
        f_spectrum_lorentzian = open("spectrum_lorentzian.dat", "w")

        with open("input.dat", "r") as f_input:
            m_valor = int(f_input.readline())
            n_valor = [int(i) for i in f_input.readline().split(" ")]

            maxn = max(n_valor)
            eigenvalue = [[0.0]*maxn for i in range(0, m_valor)]
            strength = [[0.0]*maxn for i in range(0, m_valor)]

            for j in range(0, m_valor):
                for i in range(0, n_valor[j]):
                    read_line = f_input.readline()
                    if (read_line.strip()) != "":
                        values = [float(i) for i in read_line.split("  ")]
                        eigenvalue[j][i] = values[0]
                        strength[j][i] = values[1]
        f_input.close()

        for j in range(0, m_valor):
            for nm_valor in wave_numbers:
                spectrum = 0.0
                for i in range(0, n_valor[j]):
                    if type_of_average == 'aritmética':
                        spectrum = spectrum + A * (strength[j][i] / (FACT1/SIGMA)) * \
                                   (1 / (((nm_valor - eigenvalue[j][i])**2) + 1))

                f_spectrum_lorentzian.write(f"{nm_valor:<4f}   {spectrum:>6.12f}\n")

                if nm_valor in average:
                    average[nm_valor] = average[nm_valor] + spectrum
                else:
                    average[nm_valor] = spectrum

            f_spectrum_lorentzian.write("\n")

        f_spectrum_lorentzian.close()
        print("")
        print("Arquivo spectrum_lorentzian.dat gerado!")

        # Calculating and saving average
        if type_of_average == 'aritmética':
            for key in average.keys():
                average[key] = average[key] / m_valor

        with open("average.dat", "w") as f_average:
            for key, value in average.items():
                f_average.write(f"{key:<4f}   {value:>6.12f}\n")
        f_average.close()
        print("Arquivo average.dat gerado!")
    except OSError as msg_err:
        print(f'Erro ao ajustar como modelo lorentzian: {msg_err}')
    except ValueError as msg_err:
        print(f'Erro ao ajustar como modelo lorentzian: {msg_err}')


def main(type_of_fit, type_of_average, wave_numbers, wave_numbers_interval):
    """
    Função principal.

    Parameters
    ----------
    type_of_fit : TYPE
        tipo de ajuste.
    type_of_average : TYPE
        tipo de media a ser calculada.
    wave_numbers : TYPE
        faixa de números de onda.
    wave_numbers_interval : TYPE
        intervalo para a faixa de número de onda.

    Returns
    -------
    None.

    """
    type_of_fit, type_of_average, wave_numbers, wave_numbers_interval = questions(type_of_fit,
                                                                                  type_of_average, wave_numbers,
                                                                                  wave_numbers_interval)

    if type_of_fit == "gaussian":
        fit_gaussian(type_of_average, wave_numbers)
    elif type_of_fit == "lorentzian":
        fit_lorentzian(type_of_average, wave_numbers)


if __name__ == "__main__":
    type_of_app = "Gaussian"
    type_of_fit = "gaussian"
    type_of_average = 'aritmética'
    wave_numbers_interval = 10
    wave_numbers = list(np.arange(100, 801, wave_numbers_interval))

    head_msg()

    if file_exist("input.dat"):
        main(type_of_fit, type_of_average, wave_numbers, wave_numbers_interval)
    else:
        val = input("O input.dat não existe. Deseja gerá-lo? "
                    "(S or N) [N]".ljust(57, ".") + ": ")
        if (val in ['n', 's', 'N', 'S']):
            if (val in ["N", "n"]):
                tchau()
            else:
                val = input("Origem do arquivo de saída (Gaussian ou Orca) "
                            "[Gaussian]".ljust(57, ".") + ": ").strip()
                if val == "sair":
                    tchau()

                if val != "":
                    type_of_app = val

                if type_of_app == "Gaussian":
                    extract_data_gaussian()
                    main(type_of_fit, type_of_average, wave_numbers,
                         wave_numbers_interval)
                else:
                    if type_of_app == "Orca":
                        extract_data_orca()
                        main(type_of_fit, type_of_average, wave_numbers,
                             wave_numbers_interval)
                    else:
                        print(f' + Valor ({val}) inválido!')
        else:
            print(' + Valor ({val}) inválido!')