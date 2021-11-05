import time
import re
''' 
Entradas:
- Horário cidade de origem (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Duração da viagem (HH:MM) / 00:00 a 23:59 (7 bits: 7 bits)
- Longitude cidade de origem (XXX)(W ou E) / 0 a 180 (8 bits)
- Longitude cidade de destino (XXX)(W ou E) / 0 a 180 (8 bits)
- Sentido da viagem (W ou E) / W ou E (caractere)

Saída:
- Horário de chegada no fuso horário da cidade de destino (HH:MM) / 00:00 a 23:59 (6 bits: 6 bits)
- Sinalizar chegar no mesmo dia, dia anterior ou dia seguinte (D-1, D0, D+1) / A, M, P (caractere)
'''

print("--- ENTRADA DA MÁQUINA ---")
hora_origem = input("Horário cidade de origem (HH:MM): ")
duracao = input("Duração da viagem (HH:MM): ")
long_origem = input("Longitude cidade de origem (0 - 180)(W ou E): ")
long_dest = input("Longitude cidade de destino (0 - 180)(W ou E): ")
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
duracao_bin = '{0:07b}:{1:07b}'.format(int(duracao.split(':')[0]),
                                       int(duracao.split(':')[1]))
sentido_bin = sentido.upper()
long_origem_dir_bin = long_origem_dir.upper()
long_dest_dir_bin = long_dest_dir.upper()

print(f"Horário cidade de origem ({hora_origem}): {hora_origem_bin}")
print(f"Duração da viagem ({duracao}): {duracao_bin}")
print(
    f"Longitude cidade de origem ({long_origem}): {long_origem_ang_bin}{long_origem_dir_bin}"
)

print(
    f"Longitude cidade de destino ({long_dest}): {long_dest_ang_bin}{long_dest_dir_bin}"
)
print(f"Sentido da viagem ({sentido}): {sentido_bin}")
''' 
Fita de entrada:
CCCCC:DDDDDD#FFFFFFF:GGGGGGG#AAAAAAAAB#EEEEEEEED#H

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
GGGGGGG - representação binária de 7 bits dos minutos entre 0 e 59.
- Sentido da viagem 
B - caractere W ou E representando oeste ou leste respectivamente.

Saída:
X#YYYYYY:ZZZZZZ
- Sinalização do dia de chegada
X - caracteres A, M ou P representando dia anterior, mesmo dia ou próximo dia.
- Horário de chegada no fuso horário da cidade de destino
YYYYY - representação binária de 6 bits das horas entre 0 e 23.
ZZZZZZ - representação binária de 6 bits dos minutos entre 0 e 59.
'''

print("\n")
print("--- FITA DE ENTRADA DA MÁQUINA ---")
fita_entrada = [
    hora_origem_bin, duracao_bin, long_origem_ang_bin + long_origem_dir_bin, 
    long_dest_ang_bin + long_dest_dir_bin, sentido_bin]
fita_entrada = "#".join(fita_entrada)
print(fita_entrada)

# Passo 1: Somar hora de origem na duração
def somar_duracao(fita):
    fita = fita.split("#")
    duracao_hora = fita[1].split(":")[0]
    duracao_minutos = fita[1].split(":")[1]
    origem_hora = fita[0].split(":")[0]
    origem_minutos = fita[0].split(":")[1]
    soma_minutos = bin(int(duracao_minutos, 2) + int(origem_minutos, 2))
    # Verificar se a soma é maior que 59
    if int(soma_minutos, 2) > 59:
        # Subtrair 60 da soma dos minutos
        soma_minutos = bin(int(soma_minutos, 2) - 60)
        # Acrescentar 1 hora na duração
        duracao_hora = bin(int(duracao_hora, 2) + 1)

    soma_horas = bin(int(duracao_hora, 2) + int(origem_hora, 2))
    duracao_somada = '{0:07b}:{1:07b}'.format(int(soma_horas, 2),
                                              int(soma_minutos, 2))
    fita[0] = "bbbbb:bbbbbb"
    fita[1] = duracao_somada
    return "#".join(fita)

fita_entrada = somar_duracao(fita_entrada)
print("--- FITA APÓS PASSO 1 (SOMA ORIGEM + DURAÇÃO) ---")
print(fita_entrada)

# Passo 2: Converter longitude de origem e destino em horas
# HOrigem = Origem / 15 (4 bits)
# HDestino = Destino / 15 (4 bits)
def converter_long_horas(fita):
    fita = fita.split("#")
    long_origem = fita[2][:-1]
    long_origem_dec = int(long_origem, 2)
    long_destino = fita[3][:-1]
    long_destino_dec = int(long_destino, 2)
    horigem_dec = long_origem_dec // 15
    hdestino_dec = long_destino_dec // 15
    horigem_resto = long_origem_dec % 15
    hdestino_resto = long_destino_dec % 15
    fita[2] = "{0:08b}".format(horigem_resto) + fita[2][-1]
    fita[3] = "{0:08b}".format(hdestino_resto) + fita[3][-1]
    fita = "#".join(fita) + "#"
    fita += "{0:04b}".format(horigem_dec) + "#"
    fita += "{0:04b}".format(hdestino_dec)
    return fita
fita_entrada = converter_long_horas(fita_entrada)
print("--- FITA APÓS PASSO 2 (CONVERSÃO LONGITUDE/HORA) ---")
print(fita_entrada)

# Passo 3: Diferença de hora local
#  W -> E (E) HOrigem + HDestino -> dia +0 (output M)
#  W -> E (W) 24 - (HOrigem + HDestino) -> dia +1 (output P)
#  E -> W (E) 24 - (HOrigem + HDestino) -> dia -1 (output A)
#  E -> W (W) HOrigem + HDestino -> dia +0 (output M)
# Uma viagem feita entre dois locais em um mesmo hemisfério, será feita nesse mesmo hemisfério.
#  W -> W (E) HOrigem - HDestino -> dia +0 (output M)
#  W -> W (W) HDestino - HOrigem -> dia +0 (output M)
#  E -> E (E) HDestino - HOrigem -> dia +0 (output M)
#  E -> E (W) HOrigem - HDestino -> dia +0 (output M)

def dif_hora_local(fita):
    fita = fita.split("#")
    horigem = int(fita[5], 2)
    hdestino = int(fita[6], 2)
    HLO = fita[2][-1]
    HLD = fita[3][-1]
    HDIR = fita[4]
    
    hresult = 0
    dresult = ""

    if HLO == "W" and HLD == "E" and HDIR == "E":
        hresult = horigem + hdestino
        dresult = "M"
    elif HLO == "W" and HLD == "E" and HDIR == "W":
        hresult = 24 -(horigem + hdestino)
        dresult = "P"
    elif HLO == "E" and HLD == "W" and HDIR == "E":
        hresult = 24 - (horigem + hdestino)
        dresult = "A"
    elif HLO == "E" and HLD == "W" and HDIR == "W":
        hresult = horigem + hdestino
        dresult = "M"
    elif HLO == "W" and HLD == "W" and HDIR == "E":
        hresult = horigem - hdestino
        dresult = "M"
    elif HLO == "W" and HLD == "W" and HDIR == "W":
        hresult = hdestino - horigem
        dresult = "M"
    elif HLO == "E" and HLD == "E" and HDIR == "E":
        hresult = hdestino - horigem
        dresult = "M"
    elif HLO == "E" and HLD == "E" and HDIR == "W":
        hresult = horigem - hdestino
        dresult = "M"
    
    fita = dresult + "#" + "#".join(fita) + "#" + HLO + HLD + HDIR + "#" + "{0:05b}".format(hresult)
    return fita
fita_entrada = dif_hora_local(fita_entrada)
print("--- FITA APÓS PASSO 3 (CÁLCULO DA DIFERENÇA DE HORA LOCAL) ---")
print(fita_entrada)

# Passo 4:
# Se movimento E: somar HResultado na soma da duração/origem (hora)
# Se movimento W: subtrair HResultado da soma da duração/origem (hora)
def detectar_movimento(fita):
    fita = fita.split("#")
    hresult = int(fita[9], 2)
    hora = int(fita[2].split(":")[0], 2)
    
    hora_final = 0
    if fita[5] == "E":
        hora_final = hresult + hora
    elif fita[5] == "W":
        hora_final = hora - hresult
    
    hora_final_bin = "{0:07b}".format(hora_final)
    fita[2] = hora_final_bin + ":" + fita[2].split(":")[1]
    return "#".join(fita)

fita_entrada = detectar_movimento(fita_entrada)
print("--- FITA APÓS PASSO 4 (DETECTAR MOVIMENTO E/W E AJUSTAR HORA) ---")
print(fita_entrada)

# Passo 5:
# Verificar se hora da soma final é maior que 23:
#   true: subtrair 24 da hora
#       se dia não é P:
#          ou  A -> M
#          ou  M -> P
#       verifica novamente

def ajustar_dia(fita):
    fita = fita.split("#")
    hora = int(fita[2].split(":")[0], 2)
    dia = fita[0]
    while(hora > 23):
        hora -= 24
        if dia == "A":
            dia = "M"
        elif dia == "M":
            dia = "P"
    fita[0] = dia
    hora_final_bin = "{0:07b}".format(hora)
    fita[2] = hora_final_bin + ":" + fita[2].split(":")[1]
    return "#".join(fita)

def limpar_fita(fita):
    fita = fita.split("#")
    dia = fita[0]
    hora = int(fita[2].split(":")[0], 2)
    minutos = int(fita[2].split(":")[1], 2)
    hora_bin = "{0:05b}".format(hora)
    minutos_bin = "{0:06b}".format(minutos)
    return dia + "#" + hora_bin + ":" + minutos_bin


fita_entrada = ajustar_dia(fita_entrada)
fita_entrada = limpar_fita(fita_entrada)
print("--- FITA APÓS PASSO 5 (AJUSTAR DIA E LIMPAR FITA) ---")
print(fita_entrada)
