# Konfiguracja Projektu

Ten dokument zawiera szczegółowe instrukcje dotyczące przygotowania środowiska lokalnego do uruchomienia projektu. Jeśli wykonasz wszystkie kroki po kolei, projekt powinien działać poprawnie na Twoim komputerze.

---

## 👥 Zespół projektowy

Projekt jest rozwijany przez zespół:

* Artemiusz Rzewucki
* Oleksander Piletskyi
* Denys Pshenychnykov
* Illia Merzhyevskyi
* Anastasiia Hodun

---

## 1. Tworzenie środowiska wirtualnego `(venv)`

Na początku należy utworzyć wirtualne środowisko. Pozwala ono odizolować zależności projektu od innych projektów oraz od globalnej instalacji Pythona, co zapobiega konfliktom wersji bibliotek.

Dzięki temu każdy projekt może mieć własne, niezależne środowisko.

**Windows 🪟:**

```bash
python -m venv venv
```

**Linux / macOS 🐧🍎:**

```bash
python3 -m venv venv
```

Po wykonaniu tej komendy w katalogu projektu pojawi się folder `venv`, który zawiera wszystkie pliki środowiska.

---

## 2. Aktywacja środowiska wirtualnego

Przed instalacją pakietów należy aktywować utworzone środowisko. Jest to ważne, ponieważ instalowane biblioteki trafią wtedy do lokalnego środowiska, a nie do globalnej instalacji Pythona.

Po aktywacji powinieneś zobaczyć `(venv)` na początku linii w terminalu.

**Windows 🪟:**

```bash
venv\Scripts\activate
```

**Linux / macOS 🐧🍎:**

```bash
source venv/bin/activate
```

Aby dezaktywować środowisko w dowolnym momencie, użyj:

```bash
deactivate
```

---

## 3. Instalacja wymaganych pakietów

Gdy środowisko wirtualne jest aktywne, można przejść do instalacji wymaganych bibliotek.

Lista zależności znajduje się w pliku `requirements.txt`, który zawiera wszystkie potrzebne pakiety wraz z ich wersjami.

```bash
pip install -r requirements.txt
```

Proces ten może potrwać chwilę — zależnie od liczby i rozmiaru pakietów.

---

## 4. Sprawdzenie poprawności instalacji (opcjonalnie)

Aby upewnić się, że wszystkie pakiety zostały poprawnie zainstalowane, możesz wyświetlić listę zainstalowanych bibliotek:

```bash
pip list
```

Możesz także sprawdzić wersję Pythona:

```bash
python --version
```

---

## 5. Uruchomienie projektu

Po poprawnej konfiguracji środowiska możesz uruchomić projekt zgodnie z jego przeznaczeniem, np.:

```bash
python main.py
```

> ℹ️ Uwaga: jeśli plik startowy projektu ma inną nazwę, dostosuj powyższą komendę odpowiednio.

---
