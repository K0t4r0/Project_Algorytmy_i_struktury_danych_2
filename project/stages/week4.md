# Raport z postępów prac programistycznych – Tydzień 4

Czwarty tydzień realizacji projektu przyniósł kolejne istotne postępy zarówno w warstwie algorytmicznej, jak i w rozwoju interfejsu użytkownika. Zespół kontynuował regularne spotkania, podczas których omawiano bieżące wyzwania, dzielono się postępami oraz planowano dalsze działania. Sprawna komunikacja i dobra współpraca ponownie okazały się kluczowe dla efektywnej realizacji zadań.

## Rozwój algorytmów

W tym tygodniu główny nacisk położono na implementację oraz integrację bardziej zaawansowanych algorytmów grafowych i struktur danych. Szczególną uwagę poświęcono następującym modułom:

* **Min Cost Max Flow** – w pliku `min_cost_max_flow.py` zaimplementowano klasę `MCMF`, umożliwiającą wyznaczanie przepływu o minimalnym koszcie. Algorytm został zintegrowany z interfejsem graficznym oraz wyposażony w generator kroków, dzięki czemu możliwa stała się wizualizacja kolejnych etapów działania.
* **Royal Border Patrol** – powstał moduł `royal_border_patrol.py`, w którym zaimplementowano logikę wyznaczania otoczki wypukłej dla zbioru punktów (kopalń) z możliwością wyboru algorytmu: Graham scan lub Jarvis. Dodano również funkcje umożliwiające porównanie wyników obu metod.
* **Compression & Segment Tree** – przygotowano szkielety implementacji oraz dedykowane strony w interfejsie użytkownika dla algorytmów kompresji (Union-Find) i drzewa przedziałowego, co stanowi podstawę do dalszej rozbudowy aplikacji.

Przykładowy fragment kodu – **Min Cost Max Flow**:

```python
class MCMF:
	def __init__(self, dwarves, mines):
		...
	def add_edge(self, u, v, cap, cost):
		...
	def build_network(self):
		...
	def solve_generator(self):
		...
```

## Rozwój interfejsu użytkownika

Wprowadzono nowe widoki oraz rozbudowano istniejące elementy aplikacji:

* **FlowPage** – umożliwia wybór przykładu, wizualizację przepływu oraz animację kroków algorytmu Min Cost Max Flow.
* **HullPage** – pozwala na porównanie działania algorytmów otoczki wypukłej (Graham, Jarvis) na tych samych danych wejściowych.
* **CompressionPage** i **SegmentPage** – przygotowano szablony stron, które w kolejnych tygodniach zostaną uzupełnione o pełną logikę i animacje.
* **MainMenu** – zaktualizowano menu główne, dodając nowe sekcje i usprawniając nawigację.

Wszystkie strony zachowują spójność wizualną dzięki wykorzystaniu dedykowanej palety kolorów z pliku `colors.py`.

## Wizualizacja przepływu i animacja krok po kroku

### Implementacja strony wizualizacji przepływu (`project/ui/flow_page.py`)

Została stworzona kompletna strona do wizualizacji algorytmu Min Cost Max Flow. Interfejs umożliwia wybór przykładu, uruchamianie animacji krok po kroku, regulację prędkości oraz powrót do poprzednich stanów. Do rysowania grafu i ścieżek wykorzystano bibliotekę `matplotlib`.

**Kluczowe elementy interfejsu:**

* lista przykładów w formacie JSON do szybkiego ładowania danych,
* przyciski sterujące animacją: start/stop, krok w przód/w tył, reset,
* suwak do regulacji prędkości animacji,
* panel informacyjny z opisem aktualnego stanu.

**Przykład kodu (metody sterowania animacją):**

```python
def toggle_animation_button(self):
	if self.toggle_btn.cget("text") == "Reset":
		self.reset_logic()
		ax = self.canvas.figure.axes[0]
		ax.clear()
		draw_world(self.canvas)
	elif not self.is_animating:
		self.start_animation()
	else:
		self.stop_animation()

def start_animation(self):
	self.is_animating = True
	self.toggle_btn.configure(text="Stop Animation")
	self.run_animation_loop()

def stop_animation(self):
	self.is_animating = False
	self.toggle_btn.configure(text="Start Animation")
```

### Dodatkowe funkcje animacji w Min Cost Max Flow (`project/algorithms/min_cost_max_flow.py`)

W module Min Cost Max Flow zaimplementowano generator kroków, który umożliwia etapową wizualizację działania algorytmu. Dzięki temu użytkownik może obserwować, jak budowany jest przepływ, które krawędzie są wykorzystywane oraz w jaki sposób zmieniają się ścieżki w kolejnych iteracjach.

**Przykład kodu (generator kroków):**

```python
def solve_generator(self):
	while True:
		result = bellman_ford(self.graph, self.nodes_count, self.S, self.T)
		if result is None or result[0][self.T] == float('inf'):
			break
                
		dist, parent, edge_from = result
		curr = self.T
		while curr != self.S:
			idx = edge_from[curr]
			rev_idx = self.graph[idx][4]
			self.graph[idx][2] -= 1
			self.graph[rev_idx][2] += 1
			curr = parent[curr]
                
		self.update_store_paths()
		current_step_paths = list(data_store.flow_paths)
		yield current_step_paths
```

Rozwiązanie to umożliwia płynną animację i przejrzystą analizę działania algorytmu krok po kroku.

## Otoczka wypukła – szablon GUI i generatory kroków

### Ukończony szablon GUI dla otoczki wypukłej (`project/ui/hull_page.py`)

Stworzono i dopracowano szablon strony służącej do wizualizacji algorytmów budowy otoczki wypukłej (Convex Hull). Interfejs wspiera:

* wybór przykładu z pliku JSON,
* jednoczesne porównanie dwóch algorytmów: Graham i Jarvis,
* animację budowy otoczki z możliwością sterowania prędkością i wykonywania kroków.

**Kluczowe elementy:**

* dwa wykresy do równoległego wyświetlania postępu obu algorytmów,
* przyciski sterujące animacją i krokami,
* panel informacyjny.

### Dodane funkcje wspierające animację otoczki wypukłej (`project/algorithms/hull.py`)

W module `hull` zaimplementowano generatory kroków dla obu algorytmów (Graham i Jarvis), co pozwala wizualizować każdy etap budowy otoczki.

**Przykład kodu (`graham_generator`):**

```python
def graham_generator(points):
	if len(points) < 3:
		yield (points, None)
		return

	start_point = min(points, key=lambda p: (p[1], p[0]))
	points_without_start = [p for p in points if p != start_point]
	sorted_points = sorted(
		points_without_start,
		key=lambda p: (math.atan2(p[1] - start_point[1], p[0] - start_point[0]), dist_sq(start_point, p))
	)

	hull = [start_point]
	for p in sorted_points:
		yield (list(hull), p)
		while len(hull) >= 2 and get_orientation(hull[-2], hull[-1], p) != 2:
			hull.pop()
			yield (list(hull), p)
		hull.append(p)
		yield (list(hull), None)
	yield (hull + [hull[0]], None)
```

Analogicznie działa `jarvis_generator`.

## Generator danych testowych

### Dodane narzędzie do generowania danych (`project/tools/generator.py`, `project/tools/names.json`)

Stworzono rozbudowany generator danych testowych dla algorytmów. Narzędzie pozwala elastycznie definiować parametry, takie jak liczba krasnoludów, kopalń, strażników, rozmiar siatki czy typy kopalń, a także korzystać z osobnej listy imion zapisanej w pliku `names.json`.

**Przykład kodu (generowanie i zapis):**

```python
def generate_and_save(self, output_file="json/generator_test.json"):
	data = self.generate()
	with open(output_file, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)
	print(f"The data has been successfully generated and saved in '{output_file}'")
	return data
```

Plik `names.json` zawiera dużą listę unikalnych imion wykorzystywanych przy generowaniu krasnoludów.

## Testy jednostkowe

### Dodane testy dla generatora danych, hull i min_cost_max_flow (`project/tests/`)

Dla wszystkich nowych i zmienionych modułów przygotowano szczegółowe testy:

* **test_generator.py** — sprawdza poprawność generowania danych, obsługę błędów oraz strukturę danych wyjściowych.
* **test_hull.py** — testuje kluczowe funkcje i generatory kroków dla otoczki wypukłej.
* **test_min_cost_max_flow.py** — sprawdza poprawność tworzenia grafu, obliczania odległości, dodawania krawędzi oraz działania generatora kroków.

**Przykład testu dla hull:**

```python
def test_graham_scan_square_with_inner_point():
	points = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]
	hull = graham_scan(points)
	assert set(hull) == {(0, 0), (0, 2), (2, 0), (2, 2)}
```

## Podsumowanie

W trakcie czwartego tygodnia zrealizowano szeroki zakres prac: od nowych widoków interfejsu i generatorów kroków do animacji, po rozbudowane narzędzia do generowania danych testowych oraz pełne pokrycie testami najważniejszych modułów. Dzięki temu projekt stał się nie tylko bardziej funkcjonalny, ale także wygodniejszy w testowaniu, rozwijaniu i wizualnej analizie działania algorytmów.

---

Czwarty tydzień zakończył się realizacją wszystkich zaplanowanych celów oraz przygotowaniem solidnej bazy pod dalszy rozwój projektu. Kolejne etapy będą skupiać się na optymalizacji istniejących rozwiązań oraz wdrażaniu nowych funkcjonalności.
