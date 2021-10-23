import time
import re
''' 
Entradas:
- Longitude cidade de origem (XXX)(W ou E) / 0 a 180 (8 bits)
- Horário cidade de origem (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Longitude cidade de destino (XXX)(W ou E) / 0 a 180 (8 bits)
- Duração da viagem (HH:MM) / 00:00 a 23:59 (6 bits: 6 bits)
- Sentido da viagem (W ou E) / W ou E (caractere)

Saída:
- Horário de chegada no fuso horário da cidade de destino (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Sinalizar chegar no mesmo dia, dia anterior ou dia seguinte (D-1, D0, D+1) / A, M, P (caractere)
'''

print("--- ENTRADA DA MÁQUINA ---")
long_origem = input("Longitude cidade de origem (0 - 180)(W ou E): ")
hora_origem = input("Horário cidade de origem (HH:MM): ")
long_dest = input("Longitude cidade de destino (0 - 180)(W ou E): ")
duracao = input("Duração da viagem (HH:MM): ")
sentido = input("Sentido da viagem (W ou E): ")


def is_hh_mm(t):
    try:
        time.strptime(t, '%H:%M')
    except:
        return False
    else:
        return True


long_origem_array = re.split('(\D+)', long_origem)
long_origem_ang = long_origem_array[0]
long_origem_dir = long_origem_array[1]

long_dest_array = re.split('(\D+)', long_dest)
long_dest_ang = long_dest_array[0]
long_dest_dir = long_dest_array[1]

assert int(long_origem_ang) in range(0, 181) and int(long_dest_ang) in range(
    0, 181)
assert sentido.upper() in "WE" and long_origem_dir.upper(
) in "WE" and long_dest_dir.upper() in "WE"
assert is_hh_mm(hora_origem) and is_hh_mm(duracao)

print("\n")
print("--- ENTRADA DA MÁQUINA CODIFICADA ---")
long_origem_ang_bin = '{0:08b}'.format(int(long_origem_ang))
hora_origem_bin = '{0:05b}:{1:06b}'.format(int(hora_origem.split(':')[0]),
                                           int(hora_origem.split(':')[1]))
long_dest_ang_bin = '{0:08b}'.format(int(long_dest_ang))
duracao_bin = '{0:06b}:{1:06b}'.format(int(duracao.split(':')[0]),
                                       int(duracao.split(':')[1]))
sentido_bin = sentido.upper()
long_origem_dir_bin = long_origem_dir.upper()
long_dest_dir_bin = long_dest_dir.upper()

print(
    f"Longitude cidade de origem ({long_origem}): {long_origem_ang_bin}{long_origem_dir_bin}"
)
print(f"Horário cidade de origem ({hora_origem}): {hora_origem_bin}")
print(
    f"Longitude cidade de destino ({long_dest}): {long_dest_ang_bin}{long_dest_dir_bin}"
)
print(f"Duração da viagem ({duracao}): {duracao_bin}")
print(f"Sentido da viagem ({sentido}): {sentido_bin}")
''' 
Fita de entrada:
AAAAAAAAB#CCCCC:DDDDDD#EEEEEEEED#FFFFFF:GGGGGG#H

- Longitude cidade de origem AAAAAAAAB
AAAAAAAA - representação binária de 8 bits do ângulo entre 0 e 180.
B - caractere W ou E representando oeste ou leste respectivamente.
- Horário cidade de origem CCCCC:DDDDDD
CCCCC - representação binária de 5 bits das horas entre 0 e 23.
DDDDDD - representação binária de 6 bits dos minutos entre 0 e 59.
- Longitude cidade de destino
EEEEEEEE - representação binária de 8 bits do ângulo entre 0 e 180.
D - caractere W ou E representando oeste ou leste respectivamente.
- Duração da viagem
FFFFFF - representação binária de 6 bits das horas entre 0 e 23.
GGGGGG - representação binária de 6 bits dos minutos entre 0 e 59.
- Sentido da viagem 
B - caractere W ou E representando oeste ou leste respectivamente.

Saída:
X#YYYYY:ZZZZZZ
- Sinalização do dia de chegada
X - caracteres A, M ou P representando dia anterior, mesmo dia ou próximo dia.
- Horário de chegada no fuso horário da cidade de destino
YYYYY - representação binária de 5 bits das horas entre 0 e 23.
ZZZZZZ - representação binária de 6 bits dos minutos entre 0 e 59.

'''

print("\n")
print("--- FITA DE ENTRADA DA MÁQUINA ---")
fita_entrada = [
    long_origem_ang_bin + long_origem_dir_bin, hora_origem_bin,
    long_dest_ang_bin + long_dest_dir_bin, duracao_bin, sentido_bin
]
fita_entrada = "#".join(fita_entrada)
print(fita_entrada)


# Passo 1: Somar hora de origem na duração
def somar_duracao(fita):
    fita = fita.split("#")
    duracao_hora = fita[3].split(":")[0]
    duracao_minutos = fita[3].split(":")[1]
    origem_hora = fita[1].split(":")[0]
    origem_minutos = fita[1].split(":")[1]
    soma_minutos = bin(int(duracao_minutos, 2) + int(origem_minutos, 2))
    # Verificar se a soma é maior que 59
    if int(soma_minutos, 2) > 59:
        # Subtrair 60 da soma dos minutos
        soma_minutos = bin(int(soma_minutos, 2) - 60)
        # Acrescentar 1 hora na duração
        duracao_hora = bin(int(duracao_hora, 2) + 1)

    soma_horas = bin(int(duracao_hora, 2) + int(origem_hora, 2))
    duracao_somada = '{0:06b}:{1:06b}'.format(int(soma_horas, 2),
                                              int(soma_minutos, 2))
    fita[3] = duracao_somada
    return "#".join(fita)

fita_entrada = somar_duracao(fita_entrada)
print("--- FITA APÓS PASSO 1 ---")
print(fita_entrada)
