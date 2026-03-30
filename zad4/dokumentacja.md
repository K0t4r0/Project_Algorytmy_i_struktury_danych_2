# Dokumentacja — Wyjaśnienie algorytmu i implementacji w zad4.py

## Teoria algorytmu Dinica

W tym pliku zaimplementowano algorytm Dinica (Dinitza) do znajdowania maksymalnego przepływu w sieci przepływowej. Jest to jeden z najszybszych algorytmów dla grafów o dużej liczbie krawędzi i wierzchołków.

### Co to jest sieć przepływowa?
Sieć przepływowa to skierowany graf, w którym:
- Każda krawędź ma określoną przepustowość (capacity).
- Wyróżniamy dwa wierzchołki: źródło (source, np. "s") i ujście (sink, np. "t").
- Przepływ przez krawędź nie może przekroczyć jej przepustowości.
- Przepływ do każdego wierzchołka (poza źródłem i ujściem) jest zrównoważony.

### Zastosowania algorytmu Dinica
- Optymalizacja sieci transportowych i komputerowych.
- Rozwiązywanie problemów przydziału i matchingów.
- Analiza przepustowości systemów.

---

## Algorytm Dinica — opis działania

- **Idea:** Algorytm działa warstwowo. Najpierw buduje tzw. graf warstwowy (BFS), a następnie szuka ścieżek powiększających przepływ (DFS) tylko w obrębie tych warstw.
- **Teoria:** Dzięki podziałowi na warstwy i ograniczeniu przeszukiwania, algorytm działa bardzo szybko dla gęstych grafów. Złożoność czasowa: O(V^2 * E), gdzie V — liczba wierzchołków, E — liczba krawędzi.
- **Zalety:** Bardzo wydajny dla dużych sieci, prosty do implementacji.

---

## Implementacja w Pythonie — krok po kroku

- **Reprezentacja sieci:** Słownik słowników (`defaultdict(dict)`), gdzie kluczami są wierzchołki, a wartościami sąsiedzi i przepustowości krawędzi.
- **BFS:** Buduje graf warstwowy, przypisując każdemu wierzchołkowi poziom (odległość od źródła).
- **DFS:** Szuka ścieżek powiększających przepływ tylko w obrębie grafu warstwowego.
- **Dane wejściowe:** Liczba wierzchołków, liczba krawędzi, a następnie każda krawędź (skąd, dokąd, przepustowość).
- **Wyjście:** Program wypisuje maksymalny przepływ znaleziony przez algorytm Dinica.

#### Fragment kodu — kluczowe funkcje:
```python
from collections import defaultdict, deque

def bfs(graph, start, end):
    levels = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v, cap in graph[u].items():
            if cap > 0 and v not in levels:
                levels[v] = levels[u] + 1
                queue.append(v)
    return levels if end in levels else None

def dfs(graph, levels, u, end, flow):
    if u == end or flow == 0:
        return flow
    for v, cap in graph[u].items():
        if levels.get(v) == levels[u] + 1 and cap > 0:
            pushed = dfs(graph, levels, v, end, min(flow, cap))
            if pushed > 0:
                graph[u][v] -= pushed
                if u not in graph[v]: graph[v][u] = 0
                graph[v][u] += pushed
                return pushed
    return 0

def dinica(graph, start, end):
    max_flow = 0
    while True:
        levels = bfs(graph, start, end)
        if not levels:
            break
        while True:
            pushed = dfs(graph, levels, start, end, float('inf'))
            if pushed == 0:
                break
            max_flow += pushed
    print(f"max_flow: {max_flow}")
```

#### Fragment obsługi wejścia i uruchamiania algorytmu:
```python
line = input().split()
n, m = map(int, line)
graph = defaultdict(dict)
for _ in range(m):
    u, v, p = input().split()
    p = int(p)
    graph[u][v] = p
    if u not in graph[v]:
        graph[v][u] = 0

dinica(graph, "s", "t")
```

---

## Podsumowanie
Algorytm Dinica jest bardzo wydajnym narzędziem do znajdowania maksymalnego przepływu w sieciach. Dzięki warstwowej strukturze i efektywnemu przeszukiwaniu, sprawdza się w praktycznych zastosowaniach, gdzie liczy się szybkość i skalowalność.