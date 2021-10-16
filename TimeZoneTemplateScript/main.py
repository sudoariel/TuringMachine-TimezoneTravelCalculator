import time

''' 
Entradas:
- Longitude cidade de origem (XXX) / 0 a 359 (9 bits)
- Horário cidade de origem (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Longitude cidade de destino (XXX) / 0 a 359 (9 bits)
- Duração da viagem (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Sentido da viagem (W ou E) / W ou E (caractere)

Saída:
- Horário de chegada no fuso horário da cidade de destino (HH:MM) / 00:00 a 23:59 (5 bits: 6 bits)
- Sinalizar chegar no mesmo dia, dia anterior ou dia seguinte (D-1, D0, D+1) / A, M, P (caractere)
'''

print("--- ENTRADA DA MÁQUINA ---")
long_origem = input("Longitude cidade de origem (0 - 359): ")
hora_origem = input("Horário cidade de origem (HH:MM): ")
long_dest = input("Longitude cidade de destino (0 - 359): ")
duracao = input("Duração da viagem (HH:MM): ")
sentido = input("Sentido da viagem (W ou E): ")

def is_hh_mm(t):
    try:
        time.strptime(t, '%H:%M')
    except:
        return False
    else:
        return True

assert int(long_origem) in range(0, 360) and int(long_dest) in range(0, 360)
assert sentido.upper() in "WE"
assert is_hh_mm(hora_origem) and is_hh_mm(duracao)

print("\n")
print("--- ENTRADA DA MÁQUINA CODIFICADA ---")
long_origem_bin = '{0:09b}'.format(int(long_origem))
hora_origem_bin = '{0:05b}:{1:06b}'.format(int(hora_origem.split(':')[0]), int(hora_origem.split(':')[1]))
long_dest_bin = '{0:09b}'.format(int(long_dest)) 
duracao_bin = '{0:05b}:{1:06b}'.format(int(duracao.split(':')[0]), int(duracao.split(':')[1]))
sentido_bin = sentido.upper()

print(f"Longitude cidade de origem ({long_origem}): {long_origem_bin}")
print(f"Horário cidade de origem ({hora_origem}): {hora_origem_bin}")
print(f"Longitude cidade de destino ({long_dest}): {long_dest_bin}")
print(f"Duração da viagem ({duracao}): {duracao_bin}")
print(f"Sentido da viagem ({sentido}): {sentido_bin}")