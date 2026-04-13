# Raport z postępów prac programistycznych – Tydzień 1

Pierwszy tydzień pracy nad projektem był kluczowy dla wyznaczenia kierunku dalszego rozwoju oraz zbudowania solidnych fundamentów pod kolejne etapy implementacji. Zespół skupił się przede wszystkim na dokładnym omówieniu założeń projektu, wymianie pomysłów oraz analizie możliwych rozwiązań architektonicznych. Szczególny nacisk położono na spójność koncepcji oraz skalowalność systemu, tak aby w przyszłości możliwe było łatwe rozszerzanie funkcjonalności. Równolegle rozpoczęto tworzenie wstępnej struktury aplikacji, co pozwoliło uporządkować pracę i nadać jej bardziej systematyczny charakter.

W trakcie licznych dyskusji zespołowych doprecyzowano główne cele projektu oraz określono podział na kluczowe moduły. Już na tym etapie podjęto decyzję o rozpoczęciu prac od warstwy interfejsu użytkownika, co umożliwia szybszą wizualizację postępów oraz lepsze zrozumienie przyszłych interakcji użytkownika z systemem. Jednocześnie rozpoczęto przygotowywanie podstawowych komponentów logicznych oraz klas danych, które będą stanowiły fundament dla dalszej implementacji algorytmów i narzędzi.

---

## 1. Struktura projektu

Projekt został podzielony na logiczne moduły i foldery:
- `algorithms/` – algorytmy (kompresja, przepływ, otoczka wypukła, segmentacja)
- `data_classes/` – klasy danych
- `tools/` – narzędzia do zarządzania danymi
- `ui/` – interfejs użytkownika
- `tests/` – testy jednostkowe
- `json/` – pliki testowe
- `stages/` – dokumentacja etapów

Już na tym etapie zadbano o przejrzystość i łatwość rozwoju projektu.

---

## 2. Klasy danych

W pliku `data_classes/classes.py` zdefiniowano podstawowe klasy danych, które będą wykorzystywane w całym projekcie. Przykład:

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Dwarf:
	id: int
	name: str
	skills: List[str]
	value: int
	home_pos: Tuple[int, int]

@dataclass
class Mine:
	id: str
	mine_type: str
	capacity: int
	pos: Tuple[int, int]
```

---

## 3. Moduły algorytmiczne

W folderze `algorithms/` utworzono pliki odpowiadające za implementację kluczowych algorytmów. Każdy plik zawiera funkcję przykładową, która będzie rozwijana w kolejnych tygodniach. Przykłady:

**comperession.py**
```python
def run_compression_example(x):
	return f"Compression algorithm running (example {x})..."
```

**flow.py**
```python
def run_flow_example():
	return "Flow algorithm running..."
```

**hull.py**
```python
def run_hull_example():
	return "Hull algorithm running..."
```

**segment.py**
```python
def run_segment_example():
	return "Segment algorithm running..."
```

---

## 4. Narzędzia do zarządzania danymi

W pliku `tools/data_manager.py` rozpoczęto implementację klasy do zarządzania danymi wejściowymi/wyjściowymi. Przykład:

```python
import json
from data_classes.classes import Dwarf, Mine

class DataManager:
	def __init__(self):
		self.dwarves = []
		self.mines = []
		self.guards = []

	def load_from_json(self, file_path : str) -> bool:
		try:
			with open(file_path, "r", encoding="utf-8") as file:
				data = json.load(file)

			self.dwarves = [Dwarf(d["id"], d["name"], d["skills"], d["value"], tuple(d["home_pos"])) for d in data["dwarves"]]
			self.mines = [Mine(m["id"], m["type"], m["capacity"], tuple(m["pos"])) for m in data["mines"]]
			self.guards = data.get('guards', [])
			return True
		except Exception as e:
			print("Loading error:", e)
			return False
```

---

## 5. Interfejs użytkownika (UI)

W folderze `ui/` powstały pliki odpowiadające za poszczególne strony aplikacji. Przykład fragmentu z `main_menu.py`:

```python
import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		ctk.CTkLabel(
			self,
			text="Main Menu",
			font=("Arial", 42, "bold")
		).pack(pady=(40, 10))
		# ...
```

W pliku `compression_page.py` przygotowano dynamiczne generowanie przycisków do uruchamiania przykładów algorytmu kompresji:

```python
for i in range(1, 31):
	ctk.CTkButton(scroll, 
				text=f"Example {i}",
				font=("Arial", 15),  
				height=30, 
				fg_color=SECONDARY,
				command=lambda i=i: self.run_example(i)).pack(pady=5, padx=10, fill="x")
```

---

## 6. Pliki startowe

W pliku `main.py` znajduje się punkt wejścia do aplikacji:

```python
from app import App

if __name__ == "__main__":
	app = App()
	app.mainloop()
```

W `app.py` skonfigurowano główne okno oraz routing pomiędzy stronami:

```python
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Algorytmy Projekt")
		# ...
		for F in (MainMenu, FlowPage, HullPage, SegmentPage, CompressionPage):
			frame = F(container, self)
			self.frames[F.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame("MainMenu")
```

---

## 7. Testy jednostkowe

W folderze `tests/` powstały pierwsze testy jednostkowe, np. test tworzenia obiektu Dwarf:

```python
def test_dwarf_creation():
	dwarf = Dwarf(
		id=1, 
		name="Doc", 
		skills=["gold"], 
		value=100, 
		home_pos=(10, 20)
	)
	assert dwarf.name == "Doc"
	assert isinstance(dwarf.home_pos, tuple)
	assert len(dwarf.home_pos) == 2
```

---

## 8. Współpraca zespołowa

W pierwszym tygodniu pracy szczególną rolę odegrała współpraca zespołowa oraz regularna komunikacja pomiędzy członkami grupy. Pomimo że dwie osoby były bezpośrednio zaangażowane w implementację kodu, pozostali uczestnicy aktywnie brali udział w spotkaniach, burzach mózgów oraz dyskusjach dotyczących koncepcji i architektury systemu. Dzięki temu udało się wypracować wspólne podejście do projektu oraz lepiej zrozumieć wymagania i potencjalne wyzwania.

Istotnym elementem organizacji pracy było również wstępne określenie ról w zespole, obejmujących takie obszary jak wizualizacja, rozwój narzędzi (skryptów wspierających inne programy), implementacja algorytmów, testowanie oraz zarządzanie projektem przez lidera zespołu. Podział ten pozwolił uporządkować odpowiedzialności i stworzyć podstawy do bardziej efektywnej pracy w kolejnych etapach.

Dodatkowo zdecydowano się na pracę w oparciu o system kontroli wersji z wykorzystaniem oddzielnych gałęzi, co umożliwiło równoległe rozwijanie różnych części projektu bez ryzyka konfliktów. Takie podejście sprzyja nie tylko lepszej organizacji kodu, ale również ułatwia jego integrację oraz późniejsze przeglądy zmian. Regularna wymiana informacji oraz stopniowe synchronizowanie postępów pozwoliły utrzymać spójność projektu i zapewnić jego stabilny rozwój.

---

## 9. Podsumowanie i plany

W ciągu pierwszego tygodnia:
- Ustalono strukturę katalogów i podział na moduły.
- Przygotowano szablony plików dla kluczowych komponentów.
- Rozpoczęto implementację klas danych, algorytmów oraz interfejsu użytkownika.
- Utworzono podstawowe testy jednostkowe.
- Prace były prowadzone równolegle przez dwie osoby.

W kolejnych tygodniach planowane jest rozwijanie poszczególnych modułów, implementacja algorytmów oraz rozbudowa interfejsu użytkownika.
