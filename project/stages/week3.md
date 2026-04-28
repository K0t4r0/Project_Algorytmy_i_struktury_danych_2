# Raport z postępów prac programistycznych – Tydzień 3

Trzeci tydzień realizacji projektu upłynął pod znakiem bardzo intensywnej współpracy zespołu. Odbyły się liczne spotkania (zarówno planowane, jak i ad hoc), podczas których omawialiśmy bieżące wyzwania, dzieliliśmy się postępami oraz wspólnie rozwiązywaliśmy pojawiające się problemy. Regularna komunikacja pozwoliła nam na szybkie reagowanie na wszelkie trudności oraz efektywne planowanie kolejnych kroków.

W tym tygodniu skoncentrowaliśmy się na implementacji szkieletów kluczowych algorytmów. W plikach `hull.py` oraz `shortest path.py` powstały kompletne szablony funkcji, które w przyszłości będą rozwijane o kolejne szczegóły i optymalizacje. Dzięki temu zespół zyskał solidną bazę do dalszych prac nad logiką algorytmiczną. Przykładowe fragmenty kodu prezentują obecny stan implementacji:

**Przykład – Otoczka wypukła (Graham scan oraz Jarvis):**
```python
import math


def run_hull_example():
    return "Hull algorithm running..."

def get_orientation(p, q, r):
    """
    0 -> Straight
    1 -> Right
    2 -> Left
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def dist_sq(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

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

**Przykład – Najkrótsza ścieżka (Dijkstra oraz Bellman-Ford-Moore):**
```python
import heapq


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
        return None
    return distances[end]
    


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
                return None

    if distances[end] == float('inf'):
        print("Bellman-Ford-Moore: no path")
        return None
    else:
        return distances[end]
```

Wstępnie przygotowano także funkcję Bellmana-Forda, która będzie rozwijana w kolejnych tygodniach.

Równolegle kontynuowano prace nad interfejsem użytkownika. Zaimplementowano szereg nowych widoków oraz poprawiono istniejące, dbając o spójność wizualną i wygodę obsługi. Interfejs staje się coraz bardziej intuicyjny, a kolejne elementy graficzne są sukcesywnie integrowane z logiką aplikacji. Wprowadzono również poprawki stylistyczne oraz usprawnienia w nawigacji pomiędzy poszczególnymi modułami.

Podsumowując, trzeci tydzień przyniósł znaczący postęp zarówno w warstwie algorytmicznej, jak i wizualnej projektu. Dzięki zaangażowaniu całego zespołu oraz sprawnej komunikacji udało się zrealizować wszystkie założone cele na ten etap. Przed nami kolejne wyzwania, ale z takim tempem pracy jesteśmy przekonani o sukcesie całego przedsięwzięcia.

---

## Najważniejsze osiągnięcia tygodnia

- Przeprowadzenie serii spotkań zespołowych i bieżąca synchronizacja postępów.
- Implementacja szkieletów algorytmów w plikach `hull.py` i `shortest path.py`.
- Dodanie przykładowych funkcji: Graham scan, Dijkstra.
- Rozwój i poprawa interfejsu użytkownika (UI).
- Usprawnienia wizualne i nawigacyjne w aplikacji.
- Utrzymanie wysokiego poziomu współpracy i motywacji w zespole.

W tym tygodniu do projektu zostały również dodane nowe funkcje umożliwiające obsługę i testowanie danych wejściowych z plików JSON (`project/json/*.json`). Pozwoliło to na łatwiejszą integrację danych testowych oraz ich wizualizację w aplikacji.


Dodatkowo, w module `project/ui/colors.py` wprowadzono dedykowaną paletę kolorów, która została wykorzystana w interfejsie użytkownika. Dzięki temu aplikacja zyskała spójny i atrakcyjny wygląd, a poszczególne elementy graficzne są teraz lepiej wyróżnione i bardziej czytelne.

```json
    BG_MAIN = "#1A1A1A"
    BG_SECONDARY = "#2A2A2A"
    BG_THIRDY = "#333333"

    PRIMARY = "#2F5EA1"
    SECONDARY = "#4D4D4D"
    PRIMARY_HOVER = "#2563EB"

    MINE_COLORS = {
        "gold": "#FFD700",
        "iron": "#828282",
        "coal": "#2B2B2B",
        "copper": "#B87333",
        "default": "#2F2F2F"
    }

    DWARF_HOME = "#B22222"
```
