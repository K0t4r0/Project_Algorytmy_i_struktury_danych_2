# Raport z postępów prac programistycznych – Tydzień 5

Piąty tydzień realizacji projektu przyniósł kolejne, zauważalne postępy zarówno w zakresie implementacji nowych algorytmów, jak i stopniowej rozbudowy całej aplikacji. Był to etap, w którym zespół zaczął coraz wyraźniej przechodzić od prac koncepcyjnych i przygotowawczych do bardziej konkretnej realizacji poszczególnych komponentów. W związku z tym duża część działań skupiała się nie tylko na samym pisaniu kodu, ale również na analizie przyjętych rozwiązań, sprawdzaniu ich poprawności oraz dopasowywaniu ich do wcześniej ustalonej architektury projektu.

W trakcie tego tygodnia zespół kontynuował regularne spotkania robocze, podczas których omawiano bieżące problemy, wzajemnie konsultowano wyniki pracy oraz planowano kolejne kroki. Taka organizacja pozwoliła utrzymać spójny kierunek działań i sprawiła, że poszczególne elementy projektu były rozwijane w sposób uporządkowany. Dzięki stałej komunikacji możliwe było również szybkie reagowanie na trudności techniczne, dzielenie się pomysłami i wspólne wypracowywanie rozwiązań, które najlepiej odpowiadały wymaganiom projektu.

## Rozwój algorytmów

W tym tygodniu główny nacisk położono na implementację oraz integrację nowych modułów algorytmicznych, które stanowią istotną część całego systemu. Zespół pracował nad rozwiązaniami odpowiadającymi za wyszukiwanie wzorców w plikach tekstowych, a także nad algorytmami kompresji i dekompresji danych. Oba te obszary są ważne nie tylko z punktu widzenia samej funkcjonalności aplikacji, ale również jako elementy pokazujące praktyczne zastosowanie opracowywanych przez nas narzędzi.

W przypadku algorytmu wyszukiwania szczególną uwagę zwrócono na wydajność oraz czytelność implementacji. Zastosowanie metody Rabina-Karpa pozwoliło na efektywne przetwarzanie dużych plików tekstowych i odnajdywanie wszystkich wystąpień zadanego wzorca. Praca nad tym modułem obejmowała zarówno samo napisanie funkcji, jak i przemyślenie sposobu obsługi danych wejściowych, wykrywania dopasowań oraz zwracania wyników w sposób umożliwiający dalsze wykorzystanie w aplikacji.

* **Algorytmy wyszukiwania** – w pliku `search.py` zaimplementowano algorytm wyszukiwania wzorca w pliku tekstowym z wykorzystaniem metody Rabina-Karpa. Funkcja umożliwia efektywne odnajdywanie wszystkich wystąpień zadanego wzorca w dużych plikach tekstowych, co stanowi istotny element dla przyszłych modułów analizy danych.

Przykładowy fragment kodu – **Rabin-Karp**:

```python
from collections import deque

def rabin_karp_file_search(file_path, pattern):
    m = len(pattern)
    if m == 0: return []
    alphabet_size = 128
    prime_modulus = 1000000007
    pattern_hash = 0
    current_window_hash = 0
    h_multiplier = pow(alphabet_size, m - 1, prime_modulus)
    for char in pattern:
        pattern_hash = (alphabet_size * pattern_hash + ord(char)) % prime_modulus
    occurrence_indices = []
    window = deque()
    with open(file_path, 'r', encoding='utf-8') as f:
        absolute_index = 0
        while True:
            char = f.read(1)
            if not char: break
            window.append(char)
            current_window_hash = (alphabet_size * current_window_hash + ord(char)) % prime_modulus
            if len(window) > m:
                out_char = window.popleft()
                current_window_hash = (alphabet_size * (current_window_hash - ord(out_char) * h_multiplier) + 0) % prime_modulus
            if len(window) == m:
                if current_window_hash == pattern_hash:
                    if "".join(window) == pattern:
                        occurrence_indices.append(absolute_index - m + 1)
            absolute_index += 1
    return occurrence_indices
```

* **Algorytmy kompresji i dekompresji** – w pliku `huffman.py` zaimplementowano pełny algorytm kompresji i dekompresji danych oparty na kodowaniu Huffmana. Moduł umożliwia generowanie drzewa kodowego, kompresję plików oraz ich dekompresję do oryginalnej postaci. Zaimplementowano również generatory pozwalające na etapową wizualizację procesu kompresji.

Przykładowy fragment kodu – **Huffman**:

```python
class Huffman:
    class _Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
        def __lt__(self, other):
            return self.freq < other.freq
    @classmethod
    def build_tree(cls, frequencies):
        queue = [cls._Node(char, f) for char, f in frequencies.items()]
        heapq.heapify(queue)
        while len(queue) > 1:
            l, r = heapq.heappop(queue), heapq.heappop(queue)
            merged = cls._Node(None, l.freq + r.freq)
            merged.left, merged.right = l, r
            heapq.heappush(queue, merged)
        return queue[0] if queue else None
    @classmethod
    def get_codes(cls, node, current_code="", codes=None):
        if codes is None: codes = {}
        if node:
            if node.char is not None:
                codes[node.char] = current_code
            cls.get_codes(node.left, current_code + "0", codes)
            cls.get_codes(node.right, current_code + "1", codes)
        return codes
```

Dodatkowo opracowano funkcje odpowiedzialne za kompresję i dekompresję plików oraz przygotowano generatory umożliwiające etapową wizualizację procesu kodowania. Takie rozwiązanie będzie szczególnie przydatne podczas dalszych prac nad interfejsem użytkownika, ponieważ pozwoli lepiej pokazać przebieg działania algorytmu oraz zwiększy przejrzystość całego procesu dla użytkownika końcowego.

## Rozwój interfejsu użytkownika

W tym tygodniu rozpoczęto również intensywniejsze prace nad integracją nowych algorytmów z interfejsem użytkownika. Po wcześniejszym przygotowaniu podstawowej struktury aplikacji nadszedł czas na rozbudowę widoków oraz dopasowanie ich do nowych funkcjonalności. W tym celu utworzono wstępne szkielety ekranów dla modułów wyszukiwania i kompresji, które w kolejnych etapach zostaną uzupełnione o pełną logikę działania, dodatkowe elementy obsługi oraz animacje wspierające wizualizację procesów.

Zespół zwrócił szczególną uwagę na spójność interfejsu, prostotę obsługi oraz zachowanie jednolitego stylu w całej aplikacji. Dzięki temu użytkownik końcowy będzie mógł poruszać się po systemie w sposób intuicyjny, a kolejne moduły będą wyglądały i działały w podobny, uporządkowany sposób. Prace nad GUI obejmowały nie tylko rozmieszczenie elementów na ekranie, lecz także przygotowanie odpowiednich miejsc na komunikaty zwrotne, przyciski sterujące oraz przyszłe komponenty wizualizacyjne.

## Testy jednostkowe

Ważną częścią prac w piątym tygodniu było również przygotowanie testów jednostkowych dla nowych modułów. Zespół zadbał o to, aby implementowane funkcje były sprawdzane pod kątem poprawności działania już na możliwie wczesnym etapie rozwoju. Testy obejmują zarówno standardowe przypadki użycia, jak i sytuacje brzegowe, które mogą ujawnić potencjalne błędy w logice algorytmów.

Szczególną uwagę poświęcono weryfikacji poprawności wyników po dekompresji, sprawdzeniu skuteczności wyszukiwania wzorców oraz ocenie działania funkcji w przypadku nietypowych lub pustych danych wejściowych. Dzięki temu możliwe jest szybsze wykrywanie problemów i ich naprawa jeszcze przed pełną integracją z resztą aplikacji. Tego rodzaju podejście znacząco zwiększa stabilność projektu oraz ułatwia dalszy rozwój kodu.

## Współpraca zespołowa

Piąty tydzień pokazał również, jak dużą rolę w powodzeniu projektu odgrywa dobra organizacja pracy zespołowej. Każdy z członków grupy miał przypisane konkretne zadania, ale jednocześnie wszyscy pozostawali w stałym kontakcie i na bieżąco konsultowali swoje postępy. Takie podejście pozwoliło zachować równowagę pomiędzy samodzielną pracą a wspólnym podejmowaniem decyzji technicznych.

Wspólne omawianie trudniejszych fragmentów kodu, wymiana sugestii oraz wzajemna pomoc przy rozwiązywaniu problemów technicznych sprawiły, że prace postępowały sprawnie i bez większych przestojów. Regularne spotkania umożliwiły także lepszą kontrolę nad harmonogramem oraz wyłapywanie ewentualnych opóźnień na wczesnym etapie. Dzięki temu zespół mógł elastycznie dostosowywać plan działania do bieżących potrzeb projektu.

## Podsumowanie

Piąty tydzień zakończył się bardzo pozytywnie i można uznać go za jeden z bardziej produktywnych etapów dotychczasowej realizacji projektu. Udało się zaimplementować i przetestować kluczowe algorytmy wyszukiwania oraz kompresji, co znacząco poszerzyło funkcjonalność systemu i przybliżyło nas do stworzenia kompletnej aplikacji. Jednocześnie rozpoczęto dalszą rozbudowę interfejsu użytkownika oraz przygotowywanie elementów potrzebnych do integracji nowych funkcji z resztą projektu.

W kolejnych tygodniach planowana jest dalsza integracja opracowanych rozwiązań z GUI, rozwój modułów odpowiedzialnych za wizualizację działania algorytmów oraz stopniowa optymalizacja wydajności kodu. Zespół zamierza również kontynuować rozbudowę testów, aby zapewnić wysoką jakość i stabilność implementowanych funkcji.

Na obecnym etapie projektu można zauważyć, że większość kluczowych fundamentów aplikacji została już przygotowana, a kolejne prace koncentrują się głównie na dopracowywaniu szczegółów, integracji poszczególnych komponentów oraz finalnej optymalizacji. Dzięki systematycznej pracy i dobrej organizacji zespół stopniowo zbliża się do ukończenia projektu oraz osiągnięcia wszystkich założonych celów.
