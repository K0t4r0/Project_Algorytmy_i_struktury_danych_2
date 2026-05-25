# Dokumentacja — Wyjaśnienie algorytmu i implementacji w zad11.py

## Teoria i zastosowanie

W pliku **zad11.py** zaimplementowano algorytm wyszukiwania wzorca w tekście oparty na metodzie Boyera-Moore'a.

- **Algorytm Boyera-Moore'a** to jeden z najszybszych algorytmów wyszukiwania wzorca w tekście, szczególnie efektywny dla długich tekstów i krótkich wzorców.
- Wykorzystuje dwie główne heurystyki: zły znak (bad character) oraz dobra sufiks (good suffix), co pozwala na pomijanie wielu niepotrzebnych porównań.
- Algorytm znajduje zastosowanie w edytorach tekstu, narzędziach do przeszukiwania plików oraz analizie danych.

---

## Algorytm Boyera-Moore'a — główne cechy

- Przeszukuje tekst od końca wzorca, co pozwala na duże skoki w przypadku niezgodności.
- W najgorszym przypadku złożoność czasowa wynosi $O(nm)$, ale w praktyce często jest znacznie szybszy.
- Wykorzystuje tablice pomocnicze: ostatnie wystąpienie znaku (last table) oraz tablicę dobrego sufiksu (bmnext table).

---

## Implementacja w Pythonie — krok po kroku

- **Wejście:**
    - Tekst (ciąg znaków), w którym szukamy wzorca.
    - Wzorzec (ciąg znaków), który chcemy znaleźć.
- **Wyjście:**
    - Lista indeksów, na których wzorzec występuje w tekście.

### Kluczowe funkcje:
- `BoyerMoore.search(text, pattern)` — zwraca listę indeksów wystąpień wzorca w tekście.

---

## Przykład użycia

```python
print("Enter the text:")
text = input()
print("Enter the pattern to search for:")
pattern = input()

matches = BoyerMoore.search(text, pattern)

print(f"\nText: {text}")
print(f"Pattern: {pattern}")
print("Results:")
if matches:
    print(f"Pattern found at indices : {matches}")
    print(f"Total occurrences        : {len(matches)}")
else:
    print("Pattern not found in the text.")
print()
```

**Przykładowe wejście:**
```
ABCDBABCABBCDABCAB
ABCAB
```
**Przykładowe wyjście:**
```
Text: ABCDBABCABBCDABCAB
Pattern: ABCAB
Results:
Pattern found at indices : [4, 12]
Total occurrences        : 2
```

---

## Podsumowanie

Plik **zad11.py** prezentuje implementację algorytmu Boyera-Moore'a do szybkiego wyszukiwania wzorca w tekście. Dzięki zastosowaniu heurystyk algorytm ten jest bardzo wydajny i szeroko wykorzystywany w praktycznych zastosowaniach informatycznych.

---
