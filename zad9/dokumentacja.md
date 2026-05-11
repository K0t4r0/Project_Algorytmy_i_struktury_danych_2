# Dokumentacja — Wyjaśnienie algorytmów i implementacji w zad9.py

## Teoria i zastosowanie

W pliku **zad9.py** zaimplementowano dwa klasyczne algorytmy wyszukiwania wzorca w tekście:

- **Algorytm Rabina-Karpa** — oparty na funkcji haszującej, pozwala szybko wyszukiwać wzorzec w tekście, szczególnie efektywny przy wielu wzorcach.
- **Algorytm Knutha-Morrisa-Pratta (KMP)** — wykorzystuje tzw. tablicę prefiksów, umożliwiając wyszukiwanie wzorca w czasie liniowym względem długości tekstu.

Algorytmy te są szeroko stosowane w przetwarzaniu tekstu, edytorach, narzędziach do wyszukiwania oraz analizie danych.

---

## Algorytm Rabina-Karpa — główne cechy

- Wykorzystuje funkcję haszującą do porównywania fragmentów tekstu z wzorcem.
- Pozwala na szybkie odrzucenie niepasujących fragmentów bez porównywania znak po znaku.
- W najgorszym przypadku złożoność czasowa $O(nm)$, w praktyce często bliska $O(n + m)$.

## Algorytm Knutha-Morrisa-Pratta (KMP) — główne cechy

- Buduje tablicę prefiksów (tzw. prefix table), która pozwala unikać powtarzających się porównań.
- Gwarantuje złożoność czasową $O(n + m)$ niezależnie od danych wejściowych.

---

## Implementacja w Pythonie — krok po kroku

- **Wejście:**
	- Tekst (ciąg znaków), w którym szukamy wzorca.
	- Wzorzec (ciąg znaków), który chcemy znaleźć.
- **Wyjście:**
	- Lista indeksów, na których wzorzec występuje w tekście (dla obu algorytmów).
- **Kluczowe funkcje:**
	- `rabin_karp_search(text, pattern)` — zwraca listę indeksów wystąpień wzorca w tekście za pomocą algorytmu Rabina-Karpa.
	- `kmp_search(text, pattern)` — zwraca listę indeksów wystąpień wzorca w tekście za pomocą algorytmu KMP.


## Algorytm Rabina-Karpa(kod)

```python
def rabin_karp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    alphabet_size = 128
    prime_modulus = 1000000007
    if m > n:
        return []

    pattern_hash = 0
    current_window_hash = 0
    h_multiplier = pow(alphabet_size, m - 1, prime_modulus)

    for i in range(m):
        pattern_hash = (alphabet_size * pattern_hash + ord(pattern[i])) % prime_modulus
        current_window_hash = (alphabet_size * current_window_hash + ord(text[i])) % prime_modulus

    occurrence_indices = []

    for i in range(n - m + 1):
        if pattern_hash == current_window_hash:
            if text[i:i + m] == pattern:
                occurrence_indices.append(i)

        if i < n - m:
            current_window_hash = (alphabet_size * (current_window_hash - ord(text[i]) * h_multiplier) + ord(text[i + m])) % prime_modulus
            
            if current_window_hash < 0:
                current_window_hash += prime_modulus

    return occurrence_indices
```

## KMP(kod)
Pytanie: 
dlaczego potrzebujemy `compute_prefix_table(pattern)`?

Ta funkcja buduje tablicę prefiksów potrzebną do działania algorytmu KMP.

#### Parametr:
- `pattern` — wzorzec.

#### Zwracana wartość:
- tablica prefiksów.

#### Działanie:
1. Dla kolejnych fragmentów wzorca sprawdza zgodność prefiksu i sufiksu.
2. Zapamiętuje długość najlepszego dopasowania.
3. Umożliwia późniejsze szybkie cofanie się w trakcie wyszukiwania.

```python
def compute_prefix_table(pattern):
    m = len(pattern)
    prefix_table = [0] * (m + 1)
    t = 0
    
    for j in range(2, m + 1):
        while t > 0 and pattern[t] != pattern[j - 1]:
            t = prefix_table[t]
        if pattern[t] == pattern[j - 1]:
            t += 1
        prefix_table[j] = t
    return prefix_table

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0: return []
    
    prefix_table = compute_prefix_table(pattern)
    occurrence_indices = []
    
    i = 1 
    j = 0
    
    while i <= n - m + 1:
        j = prefix_table[j]
        while j < m and pattern[j] == text[i + j - 1]:
            j += 1
            
        if j == m:
            occurrence_indices.append(i - 1) 
            
        i = i + max(1, j - prefix_table[j])
        
    return occurrence_indices
```

#### Przykład użycia:
```python
text = input()
pattern = input()
print(f"rabin_karp_search: {rabin_karp_search(text, pattern)}")
print(f"kmp_search: {kmp_search(text, pattern)}")
```

**Przykładowe wejście:**
```
ABACABADABACABA_ABACABA
ABACABA
```
**Przykładowe wyjście:**
```
rabin_karp_search: [0, 8, 15]
kmp_search: [0, 8, 15]
```

---

## Podsumowanie

Plik **zad9.py** prezentuje dwie wydajne metody wyszukiwania wzorca w tekście. Algorytm Rabina-Karpa jest szczególnie przydatny przy wielu wzorcach lub bardzo długich tekstach, natomiast KMP gwarantuje liniową złożoność niezależnie od danych. Oba algorytmy są fundamentem nowoczesnych narzędzi do przetwarzania tekstu.

---
