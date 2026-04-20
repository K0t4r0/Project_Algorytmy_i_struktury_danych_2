# Dokumentacja — Wyjaśnienie algorytmu i implementacji w zad5.py

## Teoria i zastosowanie

Otoczka wypukła (convex hull) to najmniejszy wypukły wielokąt, który zawiera wszystkie zadane punkty na płaszczyźnie. Jest to fundamentalny problem w geometrii obliczeniowej, wykorzystywany m.in. w grafice komputerowej, robotyce, GIS, analizie obrazów i wielu innych dziedzinach.

W pliku zad5.py zaimplementowano dwa klasyczne algorytmy wyznaczania otoczki wypukłej:
- **Algorytm Grahama (Graham scan)**
- **Algorytm Jarvisa (Jarvis march, gift wrapping)**

---

## Algorytm Grahama

- **Idea:** Sortujemy punkty według kąta względem punktu o najmniejszej współrzędnej y (a w razie remisu — x). Następnie przechodzimy po posortowanych punktach, budując otoczkę stosując test orientacji (czy skręcamy w lewo, prawo, czy idziemy prosto).
- **Złożoność:** O(n log n) — dominuje sortowanie.
- **Zalety:** Szybki, prosty, odporny na duże zbiory punktów.

---

## Algorytm Jarvisa

- **Idea:** Zaczynamy od punktu najbardziej lewego (najmniejsze x), a następnie „owijamy” zbiór punktów, wybierając zawsze taki, który jest najbardziej na lewo względem obecnej krawędzi otoczki.
- **Złożoność:** O(nh), gdzie h to liczba punktów na otoczce.
- **Zalety:** Bardzo prosty, dobry dla małych h (gdy większość punktów leży wewnątrz otoczki).

---

## Implementacja w Pythonie — krok po kroku

- **Wejście:** Liczba punktów n, a następnie n wierszy z dwoma liczbami całkowitymi (współrzędne x, y).
- **Wyjście:** Współrzędne punktów otoczki wypukłej wyznaczonej przez oba algorytmy.
- **Wizualizacja:** Program rysuje punkty oraz obie otoczki na jednym wykresie (matplotlib).

#### Kluczowe fragmenty kodu:
```python
def graham_scan(points):
	n = len(points)
    if n < 3: return points

    start_point = min(points, key=lambda p: (p[1], p[0]))
    
    points_without_start = [p for p in points if p != start_point]

    sorted_points = sorted(
        points_without_start, 
        key=lambda p: (math.atan2(p[1] - start_point[1], p[0] - start_point[0]), dist_sq(start_point, p))
    )

    hull = [start_point]
    for p in sorted_points:
        while len(hull) >= 2 and get_orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)
    
    return hull
```
```python
def jarvis(points):
	    n = len(points)
    if n < 3: return points
    
    start_point = min(points, key=lambda p: (p[0], p[1])) 

    hull = []
    p = start_point
    while True:
        hull.append(p)

        q = None

        for r in points:
            if r == p:
                continue
            if q is None:
                q = r
                continue

            orientation = get_orientation(p, q, r)

            if orientation == 2 or (orientation == 0 and dist_sq(p, r) > dist_sq(p, q)):
                q = r
        p = q

        if p == start_point:
            break

    return hull
```

#### Przykład użycia:
```python
n = int(input())
points_array = [tuple(map(int, input().split())) for _ in range(n)]
hull_g = graham_scan(points_array)
hull_j = jarvis(points_array)
print("--- Graham ---\n", hull_g)
print("--- Jarvis ---\n", hull_j)
show(points_array, hull_g, hull_j)
```

---

## Podsumowanie
Plik zad5.py pozwala porównać dwa klasyczne algorytmy wyznaczania otoczki wypukłej. Wyniki są prezentowane zarówno tekstowo, jak i graficznie, co ułatwia analizę i zrozumienie działania obu metod.
