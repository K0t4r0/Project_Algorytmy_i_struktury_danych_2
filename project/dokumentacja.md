# Dokumentacja Projektu
## Algorytmy i Struktury Danych II — 2026

---

## 1. Skład zespołu i role

| Imię i nazwisko | Rola |
|-----------------|------|
| *Artemiusz Rzewucki* | Implementacja algorytmów: Graham Scan, Jarvis; Team Leader projektu – koordynacja prac zespołu, organizacja i prowadzenie regularnych spotkań projektowych, planowanie harmonogramu realizacji kolejnych etapów, monitorowanie postępów prac, przydzielanie zadań między członkami zespołu, zarządzanie repozytorium Git, wsparcie procesu integracji modułów oraz przygotowanie i nadzór nad dokumentacją projektu |
| *Oleksander Piletskyi* | Implementacja algorytmów: Min-Cost Max-Flow oraz Bellman-Ford; projektowanie i rozwój modułów pomocniczych odpowiedzialnych za zarządzanie danymi wejściowymi i wyjściowymi, przygotowanie generatora danych testowych, integracja warstwy danych z pozostałymi komponentami aplikacji oraz wsparcie techniczne podczas łączenia poszczególnych modułów projektu |
| *Denys Pshenychykov* | Implementacja algorytmów: Sparse Table oraz Segment Tree (RMQ); rozwój i utrzymanie modułów interfejsu użytkownika związanych z wizualizacją algorytmów, integracja komponentów aplikacji, optymalizacja wydajności przetwarzania danych oraz udział w testowaniu poprawności działania zaimplementowanych rozwiązań |
| *Anastasiia Hodun* | Implementacja algorytmu Rabina-Karpa; projektowanie oraz rozwój interfejsu użytkownika (GUI), przygotowanie i rozbudowa stron aplikacji, dbanie o spójność wizualną projektu, poprawę ergonomii obsługi oraz integrację nowych funkcjonalności z warstwą prezentacji systemu |
| *Illia Merzhyevskyi* | Implementacja algorytmu Huffmana odpowiedzialnego za kompresję i dekompresję danych; przygotowanie i rozwój testów jednostkowych oraz integracyjnych, walidacja poprawności działania poszczególnych modułów, analiza wyników testów oraz kontrola jakości i stabilności całej aplikacji |

---

## 2. Tytuł projektu

**Królestwo Królewny Śnieżki — system zarządzania krasnoludkami**

System rozwiązuje cztery powiązane ze sobą problemy algorytmiczne osadzone w fabule bajki o Królewnie Śnieżce i krasnoludkach. Aplikacja łączy grafowy algorytm przepływu, geometrię obliczeniową, struktury danych do zapytań przedziałowych oraz kompresję danych — wszystkie zintegrowane w graficznym interfejsie użytkownika z wizualizacją krok po kroku.

---

## 3. Specyfikacja problemu

### Problem 1 — Przydział krasnoludków do kopalń

Królewna Śnieżka zarządza królestwem krasnoludków. Każdy krasnoludek posiada określone umiejętności (rodzaje minerałów, które potrafi wydobywać) oraz miejsce zamieszkania. Każda kopalnia ma określony typ (złoto, żelazo, węgiel, miedź) oraz pojemność (maksymalna liczba pracowników). Wartość produkcji zależy wyłącznie od tego, czy krasnoludek pracuje zgodnie ze swoimi umiejętnościami.

**Cel:** Przydzielić krasnoludki do kopalń zgodnych z ich umiejętnościami tak, aby **całkowita odległość** pokonywana codziennie przez wszystkich krasnoludków była **minimalna**, przy zachowaniu maksymalnej wartości produkcji.

**Formalizacja:** Minimalny koszt — maksymalny przepływ (Min-Cost Max-Flow) w grafie dwudzielnym.

### Problem 2 — Trasa patrolu granicznego

Książę codziennie musi okrążyć teren obejmujący wszystkie **aktualnie używane** kopalnie, aby egzekwować zakaz spożywania jabłek.

**Cel:** Wyznaczyć **minimalną trasę** zamkniętą obejmującą wszystkie aktywne kopalnie.

**Formalizacja:** Otoczka wypukła (Convex Hull) zbioru punktów — kopalń.

### Problem 3 — Najgłośniejszy dekametrówiec na odcinku granicy

Wzdłuż wyznaczonej granicy rozmieszczeni są dekametrówcy (krasnoludki-łucznicy) co N metrów. Przy ataku jabłkami na dany odcinek granicy należy szybko znaleźć najgłośniejszego spośród dekametrówców na tym odcinku — to on wydaje rozkaz do salwy.

**Cel:** Efektywnie odpowiadać na zapytania o **maksimum na przedziale** (Range Maximum Query).

**Formalizacja:** Sparse Table (O(1) zapytanie) lub Segment Tree (O(log n) zapytanie z obsługą aktualizacji).

### Problem 4 — Przechowywanie i wyszukiwanie wiedzy

Królewna chce przechowywać wyniki obliczeń w sposób oszczędny i umożliwić szybkie wyszukiwanie informacji.

**Cel:** **Kompresja** danych wynikowych oraz **wyszukiwanie wzorców** w skompresowanych/nieskompresowanych danych.

**Formalizacja:** Kodowanie Huffmana (kompresja) + algorytm Rabina-Karpa (wyszukiwanie wzorca).

---

## 4. Podział problemu na podproblemy i osoby odpowiedzialne

| Podproblem | Moduł | Odpowiedzialny |
|------------|--------|----------------|
| Min-Cost Max-Flow | `algorithms/min_cost_max_flow.py` | Oleksander Piletskyi |
| Bellman-Ford (najkrótsza ścieżka) | `algorithms/shortest_path.py` | Oleksander Piletskyi |
| Generator danych testowych | `tools/generator.py` | Oleksander Piletskyi |
| Zarządzanie danymi wejściowymi i wyjściowymi | `tools/data_manager.py` | Oleksander Piletskyi |
| Sparse Table + Segment Tree (RMQ) | `algorithms/segment.py` | Denys Pshenychykov |
| GUI — FlowPage | `ui/flow_page.py` | Denys Pshenychykov |
| GUI — HullPage | `ui/hull_page.py` | Denys Pshenychykov |
| Integracja modułów i optymalizacja wydajności | cały projekt | Denys Pshenychykov |
| Graham Scan + Jarvis (otoczka wypukła) | `algorithms/hull.py` | Artemiusz Rzewucki |
| Dokumentacja techniczna projektu | `/stages` | Artemiusz Rzewucki |
| Koordynacja zespołu i harmonogram prac | organizacja projektu | Artemiusz Rzewucki |
| Zarządzanie repozytorium Git | cały projekt | Artemiusz Rzewucki |
| Huffman (kompresja/dekompresja) | `algorithms/huffman.py` | Illia Merzhyevskyi |
| Testy algorytmów | `tests/test_huffman.py`, `tests/test_search.py`, `tests/test_hull.py` | Illia Merzhyevskyi |
| Testy integracyjne aplikacji | `tests/` | Illia Merzhyevskyi |
| Walidacja poprawności działania modułów | cały projekt | Illia Merzhyevskyi |
| Rabin-Karp (wyszukiwanie wzorca) | `algorithms/search.py` | Anastasiia Hodun |
| GUI — SegmentPage | `ui/segment_page.py` | Anastasiia Hodun |
| GUI — CompressionPage | `ui/compression_page.py` | Anastasiia Hodun |
| Projekt wizualny i ergonomia interfejsu | wszystkie moduły GUI | Anastasiia Hodun |

---

## 5. Harmonogram realizacji projektu

```
Tydzień →        1    2    3    4    5    6    7
─────────────────────────────────────────────────────
Struktura proj.  ████
Organizacja zesp.     ████
Algorytmy (szkic)          ████
MCMF + Hull GUI                 ████
Huffman + Search                     ████
Integracja GUI                            ████
Testy końcowe                                  ████
Dokumentacja     ██████████████████████████████████
─────────────────────────────────────────────────────
```

**Kamienie milowe:**
- **Tydzień 4:** Działający MCMF z animacją + GUI dla otoczki wypukłej
- **Tydzień 5:** Działający Huffman + Rabin-Karp
- **Tydzień 6:** Pełna integracja wszystkich modułów
- **Tydzień 7:** Testy końcowe + dokumentacja + wersja finalna

---

## 6. Ogólny opis przebiegu prac

### Tydzień 1 — Fundament projektu
Pierwszy tydzień został poświęcony na przygotowanie podstaw projektu oraz opracowanie jego architektury. Utworzono strukturę katalogów (`algorithms/`, `data_classes/`, `tools/`, `ui/`, `tests/`, `json/`, `stages/`) oraz przygotowano podstawowe pliki aplikacji. W module `data_classes/classes.py` zdefiniowano klasy danych `Dwarf` i `Mine`, natomiast w katalogu `algorithms/` utworzono szkielety modułów `compression.py`, `flow.py`, `hull.py` oraz `segment.py`. Rozpoczęto również implementację narzędzia do obsługi danych w pliku `tools/data_manager.py`, skonfigurowano główne pliki aplikacji (`app.py`, `main.py`) oraz przygotowano pierwsze strony interfejsu użytkownika, takie jak `ui/main_menu.py` i `ui/compression_page.py`. Dodatkowo utworzono pierwsze testy jednostkowe w katalogu `tests/`.

### Tydzień 2 — Organizacja zespołu
Drugi tydzień koncentrował się głównie na organizacji pracy zespołowej oraz przygotowaniu planu realizacji projektu. Ustalono role wszystkich członków zespołu, określono zakres odpowiedzialności za poszczególne moduły oraz opracowano szczegółowy harmonogram prac podzielony na kolejne etapy realizacji. Wdrożono pracę z wykorzystaniem systemu kontroli wersji Git i oddzielnych gałęzi rozwojowych, co umożliwiło równoległe rozwijanie różnych części projektu. Równocześnie kontynuowano rozwój interfejsu użytkownika oraz przygotowywano podstawy pod dalszą implementację modułów algorytmicznych i narzędzi pomocniczych.

### Tydzień 3 — Pierwsze implementacje
W trzecim tygodniu rozpoczęto właściwe prace programistyczne nad kluczowymi algorytmami. W plikach `algorithms/hull.py` oraz `algorithms/shortest_path.py` zaimplementowano algorytmy Graham Scan, Jarvis, Dijkstra oraz Bellman-Ford-Moore. Równolegle rozbudowano moduł `tools/data_manager.py`, dodając obsługę danych wejściowych zapisanych w plikach JSON. W warstwie wizualnej projektu przygotowano dedykowaną paletę kolorów w pliku `ui/colors.py`, która została wykorzystana przez kolejne elementy interfejsu użytkownika.
### Tydzień 4 — Główne algorytmy i GUI
Czwarty tydzień przyniósł rozwój najbardziej rozbudowanych modułów projektu. Ukończono implementację algorytmu Min Cost Max Flow w pliku `algorithms/min_cost_max_flow.py`, wyposażając go w generator kroków umożliwiający późniejszą animację działania. Powstał również moduł `algorithms/royal_border_patrol.py`, wykorzystujący algorytmy Graham Scan i Jarvis do analizy danych wejściowych. Rozbudowano interfejs użytkownika poprzez stworzenie stron `ui/flow_page.py` oraz `ui/hull_page.py`, a także przygotowano generator danych testowych w pliku `tools/generator.py` oraz zestaw testów jednostkowych dla nowych modułów.

### Tydzień 5 — Kompresja i wyszukiwanie
Piąty tydzień był poświęcony implementacji kolejnych kluczowych algorytmów. W pliku `algorithms/search.py` zaimplementowano algorytm Rabina-Karpa umożliwiający wyszukiwanie wzorców w plikach tekstowych, natomiast w module `algorithms/huffman.py` zrealizowano pełny mechanizm kompresji i dekompresji danych oparty na kodowaniu Huffmana. Rozpoczęto również integrację nowych funkcjonalności z warstwą wizualną aplikacji poprzez rozwój stron `ui/compression_page.py` oraz przygotowanie interfejsów dla nowych modułów.

### Tydzień 6 — Finalizacja i integracja
Szósty tydzień stanowił etap finalizacji projektu i integracji wszystkich wcześniej przygotowanych komponentów. Dopracowano moduły `algorithms/hull.py`, `algorithms/segment.py`, `data_classes/classes.py`, `tools/data_manager.py`, `tools/generator.py` oraz `tools/draw.py`. Zintegrowano także wszystkie strony interfejsu użytkownika: `ui/flow_page.py`, `ui/hull_page.py`, `ui/segment_page.py`, `ui/compression_page.py`, `ui/generate_page.py` i `ui/main_menu.py`. Projekt otrzymał również finalną identyfikację wizualną poprzez dodanie pliku `Icon.png`, a całość została poddana kompleksowym testom funkcjonalnym.

### Tydzień 7 — Poprawki końcowe i testy
Ostatni tydzień został przeznaczony na usunięcie pozostałych błędów oraz przeprowadzenie końcowej weryfikacji działania aplikacji. Poprawki wprowadzono między innymi w plikach `algorithms/min_cost_max_flow.py`, `algorithms/shortest_path.py`, `ui/compression_page.py`, `ui/flow_page.py`, `ui/hull_page.py` oraz `ui/segment_page.py`. Następnie uruchomiono pełny zestaw testów jednostkowych i integracyjnych obejmujący moduły znajdujące się w katalogu `tests/`, w tym `test_huffman.py`, `test_search.py`, `test_hull.py`, `test_min_cost_max_flow.py`, `test_segment.py` oraz `test_shortest_path.py`. Po pomyślnym zakończeniu testów projekt został uznany za gotowy do oddania.

---

## 7. Zastosowane algorytmy i złożoność obliczeniowa

### Problem 1 — Min-Cost Max-Flow (MCMF)

Sieć przepływowa złożona z czterech warstw: źródło S → krasnoludki → kopalnie → ujście T.

- Krawędź S → krasnoludek: pojemność 1, koszt 0
- Krawędź krasnoludek → kopalnia: pojemność 1, koszt = odległość euklidesowa² (tylko gdy umiejętności pasują)
- Krawędź kopalnia → T: pojemność = capacity kopalni, koszt 0

Algorytm augmentacji oparty na **Bellman-Ford** dla wyznaczania najkrótszych ścieżek w grafie z ujemnymi wagami (wagi krawędzi powrotnych są ujemne).

Optymalizacja: wczesne zakończenie Bellmana-Forda gdy brak aktualizacji (`updated = False`).

| Operacja | Złożoność |
|---|---|
| Budowa sieci | O(N · M) |
| Bellman-Ford (jedna iteracja) | O(V · E) = O((N+M) · N·M) |
| Cały MCMF (F augmentacji) | O(F · V · E) |
| Całkowita | O(N · (N+M) · N·M) |

gdzie N = liczba krasnoludków, M = liczba kopalń, F ≤ N.

### Problem 2 — Otoczka wypukła (Convex Hull)

Zaimplementowano dwa algorytmy:

**Graham Scan**
1. Wybierz punkt startowy (najniższy, skrajnie lewy)
2. Posortuj pozostałe punkty po kącie polarnym względem startowego
3. Przetwarzaj punkty utrzymując stos — wyrzucaj punkty tworzące skręt w prawo

| Operacja | Złożoność |
|---|---|
| Sortowanie | O(n log n) |
| Budowa otoczki | O(n) |
| **Łącznie** | **O(n log n)** |

**Jarvis March (Gift Wrapping)**
Na każdym kroku szukaj punktu tworzącego najbardziej lewoskrętny kąt względem aktualnego.

| Operacja | Złożoność |
|---|---|
| Jeden krok | O(n) |
| **Łącznie** | **O(n · h)** gdzie h = liczba wierzchołków otoczki |

Graham Scan jest szybszy dla gęstych zbiorów. Jarvis jest lepszy gdy h << n.

### Problem 3 — Range Maximum Query (RMQ)

#### Sparse Table (podstawowa implementacja)

Tablica dwuwymiarowa `st[k][i]` = indeks maksimum na przedziale `[i, i + 2^k - 1]`.

Zapytanie: dwa nakładające się okna długości `2^k` pokrywają cały przedział `[l, r]`.

| Operacja | Złożoność |
|---|---|
| Budowa | O(n log n) |
| Zapytanie query(l, r) | **O(1)** |
| Aktualizacja | ❌ nie wspierana |
| Pamięć | O(n log n) |

#### Segment Tree (alternatywna implementacja)

Drzewo binarne gdzie każdy węzeł przechowuje indeks maksimum w swoim zakresie.

| Operacja | Złożoność |
|---|---|
| Budowa | O(n) |
| Zapytanie query(l, r) | O(log n) |
| Aktualizacja update(i, val) | **O(log n)** |
| Pamięć | O(n) |

**Wybór implementacji:** Sparse Table — gdy dane statyczne (gwardia stoi na stałe), Segment Tree — gdy możliwe zmiany głośności strażnika.

### Problem 4 — Kompresja i wyszukiwanie

**Kodowanie Huffmana**

Buduje optymalne drzewo kodowe na podstawie częstotliwości bajtów w pliku. Bajty częstsze → krótsze kody bitowe.

| Operacja | Złożoność |
|---|---|
| Zliczanie częstotliwości | O(n) |
| Budowa drzewa (min-heap) | O(k log k), k = liczba unikalnych bajtów ≤ 256 |
| Kompresja pliku | O(n) |
| Dekompresja | O(n) |
| **Łącznie** | **O(n)** praktycznie |

**Algorytm Rabina-Karpa**

Wyszukiwanie wzorca metodą haszowania kroczącegorolling hash). Okno długości m przesuwa się po tekście; hash okna aktualizowany w O(1).

| Operacja | Złożoność |
|---|---|
| Obliczenie hasha wzorca | O(m) |
| Przetwarzanie pliku | O(n) |
| Weryfikacja dopasowania | O(m) przy kolizji |
| **Łącznie (średnio)** | **O(n + m)** |

---

## 8. Poprawność rozwiązania i wyniki testowania

### Pokrycie testami

Testy jednostkowe w folderze `tests/` obejmują wszystkie moduły:

| Plik testowy | Liczba testów | Zakres |
|---|---|---|
| `test_min_cost_max_flow.py` | 13 | Budowa sieci, augmentacja, pojemność, brak umiejętności |
| `test_hull.py` | ~10 | Trójkąt, kwadrat, punkty współliniowe, punkt wewnętrzny |
| `test_huffman.py` | ~8 | Kompresja/dekompresja, puste pliki, jeden symbol |
| `test_segment.py` | ~8 | RMQ na różnych przedziałach, przypadki brzegowe |
| `test_shortest_path.py` | ~6 | Ścieżki, brak ścieżki, cykl ujemny |
| `test_generator.py` | ~6 | Generowanie danych, walidacja struktury |
| `test_royal_border_patrol.py` | ~5 | Graham vs Jarvis, zgodność wyników |
| `test_compression_manager.py` | ~5 | Kompresja → dekompresja → identyczność |
| `test_classes_and_data.py` | ~4 | Tworzenie obiektów, ładowanie JSON |
| `test_search.py` | ~4 | Znalezienie wzorca, brak wzorca, wzorzec pusty |

### Kluczowe przypadki testowe MCMF

```python
# krasnoludek bez pasujących umiejętności → brak przydziału
def test_solve_generator_does_not_assign_dwarf_without_matching_skill():
    # wynik: steps == []  ✓

# pojemność kopalni = 1 → max jeden krasnoludek
def test_solve_generator_respects_mine_capacity():
    # wynik: len(dwarf_to_mine_paths) == 1  ✓

# pojemność = 2 → dwóch krasnoludków, koszt sumaryczny poprawny
def test_solve_generator_can_assign_two_dwarves_when_capacity_allows():
    # wynik: total_cost_so_far == 300.0  ✓
```

### Wyniki testów końcowych

Wszystkie testy zaliczone pomyślnie. Aplikacja przeszła testy integracyjne na przykładach `Example 1.json`, `Example 2.json`, `Example 3.json` oraz danych generowanych losowo przez `DwarfDataGenerator`.

---

## 9. Technologia i języki programowania

### Język programowania

**Python 3.11+** — wybrany ze względu na czytelność kodu, dostępność bibliotek matematycznych i graficznych oraz łatwość implementacji generatorów do animacji krok po kroku.

### Biblioteki zewnętrzne

| Biblioteka | Zastosowanie |
|---|---|
| `customtkinter` | Nowoczesny interfejs graficzny (GUI) |
| `matplotlib` | Wizualizacja grafów, otoczek wypukłych, granicy |
| `heapq` | Kolejka priorytetowa w Huffmanie i Dijkstrze |
| `bisect` | Binarny search przy rozmieszczaniu dekametrówców |
| `pytest` | Framework do testów jednostkowych |
| `json` | Obsługa plików danych wejściowych i wynikowych |
| `threading` | Wątek tła do zapisu wyników bez blokowania GUI |
| `glob`, `os` | Zarządzanie plikami, automatyczne numerowanie przykładów |

### Struktura projektu

```
project/
├── algorithms/
│   ├── min_cost_max_flow.py   # Problem 1: MCMF
│   ├── shortest_path.py       # Bellman-Ford, Dijkstra
│   ├── hull.py                # Problem 2: Graham Scan, Jarvis
│   ├── segment.py             # Problem 3: Sparse Table, Segment Tree
│   ├── huffman.py             # Problem 4: kompresja Huffmana
│   ├── search.py              # Problem 4: Rabin-Karp
│   └── royal_border_patrol.py # wrapper otoczki wypukłej
├── data_classes/
│   └── classes.py             # Dwarf, Mine, BorderGuard
├── tools/
│   ├── data_manager.py        # ładowanie/zapis danych
│   ├── generator.py           # generator danych testowych
│   ├── draw.py                # funkcje rysowania matplotlib
│   ├── compression_manager.py # zarządzanie plikami .kra
│   └── names.json             # lista imion krasnoludków
├── ui/
│   ├── main_menu.py
│   ├── flow_page.py           # wizualizacja MCMF
│   ├── hull_page.py           # wizualizacja otoczki
│   ├── segment_page.py        # wizualizacja RMQ
│   ├── compression_page.py    # wizualizacja Huffmana
│   ├── generator_page.py      # generator danych w GUI
│   └── colors.py              # paleta kolorów
├── tests/                     # testy jednostkowe
├── json/                      # przykładowe dane wejściowe
├── compressed_data/           # pliki .kra (wyniki skompresowane)
├── decompressed_data/         # pliki tymczasowe
├── app.py                     # konfiguracja okna, routing
└── main.py                    # punkt wejścia
```

### System kontroli wersji

**Git** — praca na oddzielnych gałęziach dla każdego modułu, merge do gałęzi głównej po przeglądzie kodu.

### Format danych

Pliki wejściowe w formacie **JSON**:

```json
{
  "dwarves": [
    { "id": 1, "name": "Gimli", "skills": ["gold"], "value": 100, "home_pos": [10, 20] }
  ],
  "mines": [
    { "id": "M-01", "mine_type": "gold", "capacity": 2, "pos": [45, 55] }
  ],
  "guards": [
    { "id": 101, "name": "Bofur", "loudness": 85 }
  ]
}
```

Pliki wynikowe kompresowane algorytmem Huffmana do formatu `.kra`.

---

## 10. Informacje dodatkowe

### Wizualizacja krok po kroku

Kluczową cechą aplikacji jest możliwość obserwowania działania algorytmów w czasie rzeczywistym. Każdy algorytm posiada generator (`solve_generator`, `graham_generator`, `jarvis_generator`, `compress_generator`) pozwalający na:
- wykonywanie kroków ręcznie (przód/tył)
- automatyczną animację z regulowaną prędkością
- resetowanie do stanu początkowego

### Wątek tła (threading)

Wyniki działania algorytmów zapisywane są asynchronicznie w osobnym wątku, aby nie blokować animacji w głównym wątku GUI. Użyto blokady (`threading.Lock`) dla bezpiecznego dostępu do plików przy równoległych zapisach.

### Generator danych testowych

Klasa `DwarfDataGenerator` generuje losowe, ale spójne dane testowe z konfigurowalnymi parametrami (liczba krasnoludków, kopalń, strażników, rozmiar siatki, typy kopalń itp.). Automatycznie nadaje nazwy plikom (`Example N.json`) i obsługuje walidację zakresu parametrów przez GUI.

### Paleta kolorów

```python
BG_MAIN      = "#1A1A1A"   # tło główne
BG_SECONDARY = "#2A2A2A"   # tło paneli
BG_THIRDY    = "#333333"   # tło wykresów
PRIMARY      = "#2F5EA1"   # przyciski główne
MINE_COLORS  = {
    "gold":   "#FFD700",
    "iron":   "#828282",
    "coal":   "#2B2B2B",
    "copper": "#B87333"
}
```
