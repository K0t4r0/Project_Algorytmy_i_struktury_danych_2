
# Dokumentacja — Wyjaśnienie algorytmów i implementacji w ZAD2.py

## Teoria algorytmów — wprowadzenie

Graf to zbiór wierzchołków (punktów) połączonych krawędziami (liniami). W informatyce grafy służą do modelowania sieci, tras, relacji i wielu innych problemów. Często chcemy znaleźć najkrótszą drogę między dwoma punktami — do tego służą algorytmy najkrótszej ścieżki.

### 1. Algorytm Dijkstry

- **Zastosowanie:** Szukamy najkrótszej drogi w grafie, gdzie wszystkie krawędzie mają nieujemne (czyli dodatnie lub zero) wagi.
- **Jak działa:** 
   - Zaczynamy od wierzchołka startowego.
   - Ustawiamy jego odległość na 0, reszty na nieskończoność.
   - Wybieramy wierzchołek o najmniejszej odległości (kolejka priorytetowa).
   - Aktualizujemy odległości do sąsiadów, jeśli znajdziemy krótszą drogę.
   - Powtarzamy, aż odwiedzimy wszystkie wierzchołki lub znajdziemy cel.
- **Zalety:** Szybki, prosty, bardzo wydajny dla dużych grafów bez ujemnych wag.
- **Ograniczenia:** Nie działa poprawnie, jeśli są krawędzie o ujemnej wadze.

### 2. Algorytm Bellmana-Forda-Moore’a

- **Zastosowanie:** Szukamy najkrótszej drogi w grafie, gdzie mogą być krawędzie o ujemnej wadze.
- **Jak działa:** 
   - Ustawiamy odległości na nieskończoność, start na 0.
   - Przez (n-1) iteracji relaksujemy wszystkie krawędzie: jeśli znajdziemy krótszą drogę, aktualizujemy odległość.
   - Na końcu sprawdzamy, czy istnieje cykl o ujemnej długości (jeśli tak, nie ma sensu szukać najkrótszej drogi).
- **Zalety:** Działa dla grafów z ujemnymi wagami, wykrywa cykle ujemne.
- **Ograniczenia:** Wolniejszy niż Dijkstra, szczególnie dla dużych grafów.

### 3. Algorytm Floyda-Warshalla

- **Zastosowanie:** Chcemy znać najkrótsze drogi między wszystkimi parami wierzchołków.
- **Jak działa:** 
   - Tworzymy macierz odległości (każda komórka to odległość między dwoma wierzchołkami).
   - Iteracyjnie sprawdzamy, czy przejście przez trzeci wierzchołek daje krótszą drogę.
   - Wykrywamy cykle ujemne.
- **Zalety:** Daje pełną informację o wszystkich ścieżkach.
- **Ograniczenia:** Zużywa dużo pamięci i czasu dla dużych grafów.

#### Przykład grafu:
Wyobraź sobie mapę miasta, gdzie punkty to skrzyżowania, a krawędzie to ulice z określoną długością. Algorytmy pomagają znaleźć najkrótszą trasę z punktu A do B.


### Przykład fragmentu kodu (dodawanie krawędzi):
```python
from collections import defaultdict
graph = defaultdict(dict)
# Dodawanie krawędzi:
graph[1][2] = 8  # z wierzchołka 1 do 2, waga 8
```

#### Fragment obsługi wejścia и uruchamiania algorytmow:
```python
n, m = map(int, input().split())
graph = defaultdict(dict)
for _ in range(m):
   w1, w2, g = map(int, input().split())
   if g < 0:
      hasNegative = True
   graph[w1][w2] = g
v, u = map(int, input().split())
- **Wyjście:** Program wypisuje najkrótszą drogę lub informuje o braku ścieżki/cyklu ujemnym.
if hasNegative:
   print("Dijkstra: the graph contains negative weights")
else:
   dijkstra(graph, v, u, n)
moorea_bellmana(graph, n, v, u)

```

### Kod każdego algorytmu:

#### Dijkstra:
```python
def dijkstra(graph, start, end, n):
   distances = {node: float('inf') for node in range(1, n+1)}
   parents = {node: None for node in range(1, n+1)}
   distances[start] = 0
   priority_queue = [(0, start)]
   while priority_queue:
      current_distance, current_node = heapq.heappop(priority_queue)
      if current_distance > distances[current_node]:
         continue
      for neighbor, weight in graph.get(current_node, {}).items():
         distance = current_distance + weight
         if distance < distances[neighbor]:
            distances[neighbor] = distance
            parents[neighbor] = current_node
            heapq.heappush(priority_queue, (distance, neighbor))
   if distances[end] == float('inf'):
      print("Dijkstra: no path")
      return
   print(f"Dijkstra: the shortest way from {start} to {end}: {distances[end]}")
```

#### Bellman-Ford-Moore:
```python
def moorea_bellmana(graph, n, start, end):
   distances = {node: float('inf') for node in range(1, n + 1)}
   distances[start] = 0
   for _ in range(n - 1):
      for u in graph:
         for v, weight in graph[u].items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
               distances[v] = distances[u] + weight
   for u in graph:
      for v, weight in graph[u].items():
         if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            print("Bellman-Ford-Moore: the graph contains a negative cycle")
            return
   if distances[end] == float('inf'):
      print("Bellman-Ford-Moore: no path")
   else:
      print(f"Bellman-Ford-Moore: the shortest way from {start} to {end}: {distances[end]}")
```

#### Floyd-Warshall:
```python
def floyd_warshall(graph, n, start, end, w):
   INF = float('inf')
   dist = [[INF]*(n+1) for _ in range(n+1)]
   nxt = [[None]*(n+1) for _ in range(n+1)]
   for u in graph:
      for v, weight in graph[u].items():
         if weight < dist[u][v]:
            dist[u][v] = weight
            nxt[u][v] = v
   for k in range(1, n+1):
      for i in range(1, n+1):
         for j in range(1, n+1):
            if dist[i][k] != INF and dist[k][j] != INF and dist[i][j] > dist[i][k] + dist[k][j]:
               dist[i][j] = dist[i][k] + dist[k][j]
               nxt[i][j] = nxt[i][k]
   for i in range(1, n+1):
      if dist[i][i] < 0:
         print("Floyd-Warshall: the graph contains a negative cycle")
         return
   print("Floyd-Warshall: ")
   # ...dalsza część kodu wypisuje wyniki i ścieżki...
```

---

## Składnia Pythona i jej zalety

- **Czytelność:** Kod jest prosty, łatwy do zrozumienia nawet dla początkujących.
- **Struktury danych:** Słowniki, listy, kolejki priorytetowe (`heapq`) pozwalają szybko i wygodnie operować na grafach.
- **Dynamiczne typowanie:** Nie trzeba deklarować typów zmiennych, co przyspiesza pisanie kodu.
- **Bogate biblioteki:** Python ma gotowe narzędzia do obsługi grafów, kolejek, macierzy, co upraszcza implementację.

---

## Podsumowanie

Dokumentacja i kod pozwalają zrozumieć, jak działają algorytmy najkrótszej ścieżki, jak je zaimplementować i kiedy je stosować.  
Nawet jeśli nie masz doświadczenia z grafami, dzięki wyjaśnieniom i przykładom możesz zrozumieć, jak działa program i jak rozwiązuje typowe problemy z trasami, sieciami czy relacjami.  
Python jest idealnym językiem do nauki i prototypowania algorytmów, a przedstawione rozwiązania są uniwersalne i mogą być użyte w wielu dziedzinach informatyki.
