# Dokumentacja — Wyjaśnienie algorytmów i implementacji w zad3.py

## Teoria algorytmów przepływu w sieciach

W tym pliku zaimplementowano dwa fundamentalne algorytmy przepływu w sieciach: Forda-Fulkersona oraz Edmondsa-Karpa. Są one wykorzystywane do znajdowania maksymalnego przepływu w sieci przepływowej, czyli takiej, gdzie każda krawędź ma określoną przepustowość (capacity), a celem jest przesłanie jak największej ilości „przepływu” od źródła (source) do ujścia (sink).

### Co to jest sieć przepływowa?
Sieć przepływowa to skierowany graf, w którym:
- Każda krawędź ma określoną przepustowość (maksymalną ilość „przepływu”, którą można przez nią przesłać).
- Mamy wyróżnione dwa wierzchołki: źródło (source) i ujście (sink).
- Przepływ przez krawędź nie może przekroczyć jej przepustowości.
- Przepływ do każdego wierzchołka (poza źródłem i ujściem) jest zrównoważony: suma przepływów wchodzących = suma wychodzących.

### Zastosowania algorytmów przepływu
Algorytmy te mają szerokie zastosowanie:
- Optymalizacja sieci transportowych (np. ruch uliczny, rurociągi).
- Rozwiązywanie problemów przydziału (np. przydział zadań do pracowników).
- Analiza sieci komputerowych.
- Rozwiązywanie problemów dwudzielnych (np. matching w grafach).

---

## Algorytm Forda-Fulkersona

- **Idea:** Szukamy ścieżek od źródła do ujścia, po których można przesłać przepływ, i „wpychamy” przez nie tyle, ile się da. Powtarzamy, aż nie znajdziemy już żadnej ścieżki z wolną przepustowością.
- **Teoria:** Algorytm działa iteracyjnie, każda ścieżka zwiększa całkowity przepływ. W praktyce, jeśli przepustowości są całkowite, algorytm zawsze się zakończy.
- **Ograniczenia:** Może być powolny, jeśli wybieramy ścieżki nieoptymalnie (np. przy dużych liczbach lub cyklach).

```python
def dfs(u, sink, flow, visited, graph):
    visited.add(u)
    if u == sink:
        return flow
    for v in graph[u]:
        capacity = graph[u][v]
        if v not in visited and capacity > 0:
            pushed = dfs(v, sink, min(flow, capacity), visited, graph)
            if pushed > 0:
                graph[u][v] -= pushed
                if u not in graph[v]: 
                    graph[v][u] = 0
                graph[v][u] += pushed
                return pushed
    return 0

def ford_fulkerson(graph, source, sink):
    max_flow = 0
    while True:
        visited = set()
        pushed = dfs(source, sink, float('inf'), visited, graph)
        if pushed == 0:
            break
        max_flow += pushed
    return max_flow
```

---

## Algorytm Edmondsa-Karpa

- **Idea:** To ulepszona wersja Forda-Fulkersona, gdzie ścieżki są wybierane za pomocą BFS (Breadth-First Search), czyli zawsze najkrótsza możliwa ścieżka w liczbie krawędzi.
- **Teoria:** Dzięki BFS algorytm działa szybciej i ma gwarantowaną złożoność O(V * E^2), gdzie V to liczba wierzchołków, a E — krawędzi.
- **Zalety:** Zawsze wybiera najkrótszą ścieżkę, co zapobiega „zawieszaniu się” na cyklach i przyspiesza działanie.

```python
def bfs(source, sink, graph):
    queue = deque([source])
    visited = set([source])
    parent = {}
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            capacity = graph[u][v]
            if v not in visited and capacity > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return parent
    return None

def edmonds_karp(graph, source, sink):
    max_flow = 0
    while True:
        parent = bfs(source, sink, graph)
        if parent is None:
            break
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            if u not in graph[v]:
                graph[v][u] = 0
            graph[v][u] += path_flow
            v = u
        max_flow += path_flow
    return max_flow
```

---

## Implementacja w Pythonie — krok po kroku

- **Reprezentacja sieci:** Używamy słownika słowników (`defaultdict(dict)`), gdzie kluczami są wierzchołki, a wartościami sąsiedzi i przepustowości krawędzi.
- **Dane wejściowe:** Program pobiera liczbę wierzchołków, krawędzi, a następnie każdą krawędź (skąd, dokąd, przepustowość).
- **Wywołanie algorytmów:** Tworzymy kopię sieci, aby oba algorytmy mogły działać niezależnie.
- **Wyjście:** Program wypisuje maksymalny przepływ znaleziony przez oba algorytmy.

#### Fragment obsługi wejścia i uruchamiania algorytmów:
```python
n, m = map(int, input().split())
siec = defaultdict(dict)
for _ in range(m):
    w1, w2, p = input().split()
    siec[w1][w2] = int(p)
siec_copy = copy.deepcopy(siec)
print(ford_fulkerson(siec, 's', 't'))
print(edmonds_karp(siec_copy, 's', 't'))
```

---

## Składnia Pythona i jej zalety

- **Czytelność:** Kod jest prosty, łatwy do zrozumienia nawet dla początkujących.
- **Struktury danych:** Słowniki, listy, kolejki (`deque`) pozwalają wygodnie operować na sieciach.
- **Dynamiczne typowanie:** Nie trzeba deklarować typów zmiennych, co przyspiesza pisanie kodu.
- **Bogate biblioteki:** Python ma gotowe narzędzia do obsługi grafów, kolejek, macierzy, co upraszcza implementację.

---

## Podsumowanie

Dokumentacja i kod pozwalają zrozumieć, jak działają algorytmy przepływu w sieciach, jak je zaimplementować i kiedy je stosować.  
Nawet jeśli nie masz doświadczenia z sieciami przepływowymi, dzięki wyjaśnieniom i przykładom możesz zrozumieć, jak działa program i jak rozwiązuje typowe problemy z optymalizacją przepływu.  
Python jest idealnym językiem do nauki i prototypowania algorytmów, a przedstawione rozwiązania są uniwersalne i mogą być użyte w wielu dziedzinach informatyki.
