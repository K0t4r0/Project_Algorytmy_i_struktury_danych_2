# ZADANIE 1. Reprezentacja grafow i digrafow wazonych
# Dane wejsciowe: n - liczba wierzcholkow (numeracja od 0 do n)
#                 m - liczba krawedzi
#
# Dane wyjsciowe: macierz sasiedztwa,
#                 lista sasiadow,
#                 dwie tablice
n,m = map(int, input().split())

matrix = [[0 for _ in range(n)] for _ in range(n)]
di_matrix = [[0 for _ in range(n)] for _ in range(n)]
lista = {i: [] for i in range(n)}
di_lista = {i: [] for i in range(n)}
tab1, tab2, di_tab1, di_tab2 = [0], [], [0], [] 

for _ in range (m):
    w1,w2,g = map(int, input().split())

    matrix[w1][w2] = g
    matrix[w2][w1] = g
    di_matrix[w1][w2] = g

    lista[w1].append((w2, g))
    lista[w2].append((w1, g))
    di_lista[w1].append((w2,g))

for i in range(n):
    for (v, w) in lista[i]:
        tab2.append((v, w))
    tab1.append(len(tab2))

    for (v, w) in di_lista[i]:
        di_tab2.append((v, w))
    di_tab1.append(len(di_tab2))
    
print("--------Macierz Sasiedztwa-------")

for el in matrix:
    print(el)
print("--Skierowana Macierz Sasiedztwa--")
for el in di_matrix:
    print(el)

print("")

print("----------Lista Sasiadow---------")

for i, v in lista.items():
    print(f"{i}: {v}")
print("----Skierowana Lista Sasiadow----")
for i, v in di_lista.items():
    print(f"{i}: {v}")

print("")

print("-----------Dwie Tablice----------")

print("tab1:", tab1)
print("tab2:", tab2)
print("-----Skierowane Dwie Tablice-----")
print("tab1:", di_tab1)
print("tab2:", di_tab2)