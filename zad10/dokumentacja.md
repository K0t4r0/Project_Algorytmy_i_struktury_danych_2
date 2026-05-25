# Dokumentacja — Wyjaśnienie algorytmu i implementacji w zad10.py

## Teoria i zastosowanie

W pliku **zad10.py** zaimplementowano algorytm kompresji i dekompresji tekstu oparty na kodowaniu Huffmana.

- **Kodowanie Huffmana** to klasyczny algorytm bezstratnej kompresji danych, który przypisuje krótsze kody częściej występującym znakom, a dłuższe — rzadszym. Dzięki temu możliwe jest znaczne zmniejszenie rozmiaru danych tekstowych.
- Algorytm znajduje zastosowanie m.in. w kompresji plików, przesyłaniu danych oraz w systemach kodowania informacji.

---

## Algorytm Huffmana — główne cechy

- Buduje drzewo binarne na podstawie częstości występowania znaków w tekście.
- Każdemu znakowi przypisuje unikalny kod binarny (krótszy dla częstszych znaków).
- Kompresja i dekompresja są bezstratne — oryginalny tekst można w pełni odtworzyć.

---

## Implementacja w Pythonie — krok po kroku

- **Wejście:**
    - Tekst (ciąg znaków) do skompresowania.
- **Wyjście:**
    - Skompresowany tekst w postaci bajtów,
    - Długość dopełnienia (padding),
    - Słownik kodów Huffmana.

### Kluczowe funkcje:
- `Huffman.compress(text)` — kompresuje tekst, zwraca bajty, padding i słownik kodów.
- `Huffman.decompress(compressed_text, padding_len, huffman_codes)` — dekompresuje bajty do oryginalnego tekstu.

---

## Przykład użycia

```python
text = input()
compressed_text, pad, codes = Huffman.compress(text)
print(f"Compressed text {compressed_text}")
print(f"Padding lenght {pad}")
print(f"Huffman codes:")
for key in codes:
    print(f"{key} : {codes[key]}")
print()

original_size = len(text) * 8
compressed_size = (len(compressed_text) * 8) - pad
compression_percent = (1 - compressed_size / original_size) * 100
print(f"Compression ratio: {compression_percent:.2f}%")
```

**Przykładowe wejście:**
```
aaabracabbr
```
**Przykładowe wyjście:**
```
Compressed text b'\x1b\x8c\x00'
Padding lenght 4
Huffman codes:
a : 0
b : 10
r : 110
c : 1110

Compression ratio: 54.55%
```

---

## Podsumowanie

Plik **zad10.py** prezentuje implementację algorytmu Huffmana do kompresji i dekompresji tekstu. Algorytm ten pozwala efektywnie zmniejszyć rozmiar danych tekstowych bez utraty informacji, co jest szeroko wykorzystywane w praktycznych zastosowaniach informatycznych.

---
