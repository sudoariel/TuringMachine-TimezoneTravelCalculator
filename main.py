''' 

Entradas:
- Longitude cidade de origem (XXX) 0 a 359 (9 bits)
- Horário cidade de origem (HH:MM) 00:00 a 23:59 (5 bits: 6 bits)
- Longitude cidade de destino (XXX) 0 a 359 (9 bits)
- Duração da viagem (HH:MM) 00:00 a 23:59 (5 bits: 6 bits)
- Sentido da viagem (W ou E) W ou E 

Saída:
- Horário de chegada no fuso horário da cidade de destino (HH:MM) 00:00 a 23:59 (5 bits: 6 bits)
- Sinalizar chegar no mesmo dia, dia anterior ou dia seguinte (D-1, D0, D+1) A, M, P 

'''

long_origem = input("Longitude cidade de origem (0 - 359): ")
hora_origem = input("Horário cidade de origem (HH:MM): ")
long_dest = input("Longitude cidade de destino (0 - 359): ")
duracao = input("Duração da viagem (HH:MM): ")
sentido = input("Sentido da viagem (W ou E): ")

