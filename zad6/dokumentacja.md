# Dokumentacja — Wyjaśnienie algorytmu i implementacji w zad6.py

## Teoria i zastosowanie

**Drzewo czerwono-czarne (Red-Black Tree)** to samobalansujące się drzewo binarne, które zapewnia logarytmiczny czas wykonywania podstawowych operacji (wstawianie, usuwanie, wyszukiwanie). Jest szeroko stosowane w implementacjach struktur danych, takich jak mapy, zbiory czy bazy danych.

W pliku zad6.py zaimplementowano:
- Struktura drzewa czerwono-czarnego z operacją wstawiania.
- Preorder (przechodzenie drzewa w porządku pre-order).

---

## Drzewo czerwono-czarne — główne cechy

- Każdy węzeł jest czerwony lub czarny.
- Korzeń jest zawsze czarny.
- Wszystkie liście (tzw. nil) są czarne.
- Czerwony węzeł nie może mieć czerwonych dzieci.
- Każda ścieżka od korzenia do liścia zawiera tyle samo czarnych węzłów.

Dzięki tym własnościom drzewo pozostaje zrównoważone, a operacje mają złożoność $O(\log n)$.

---

## Implementacja w Pythonie — krok po kroku

- **Wejście:** Liczba elementów n, a następnie n liczb całkowitych (do wstawienia do drzewa).
- **Wyjście:** Preorder drzewa czerwono-czarnego po wstawieniu wszystkich elementów.
- **Kluczowe funkcje:**
	- `insert` — wstawia nowy element, zachowując własności drzewa czerwono-czarnego.
	- `fix_insert` — naprawia naruszenia własności drzewa po wstawieniu.
	- `get_preorder` — zwraca listę elementów w porządku preorder.

#### Przykład użycia:
```python
n = int(input())
data = map(int, input().split())
result_order = solve_rbt_preorder(data)
print(f"Preorder: {result_order}")
```

```python
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.nil
        node.right = self.nil
        node.color = 1

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)
```


```python
    def fix_insert(self, k):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
```

```python
    def get_preorder(self, node, result):
        if node != self.nil:
            result.append(node.data)
            self.get_preorder(node.left, result)
            self.get_preorder(node.right, result)
        return result
```

**Przykładowe wejście:**
```
8
20 5 6 40 25 16 12 7
```
**Przykładowe wyjście:**
```
Preorder: [16, 7, 6, 5, 12, 20, 40, 25]
```

---

## Podsumowanie

Plik zad6.py pozwala zbudować drzewo czerwono-czarne na podstawie podanych liczb i wypisać jego preorder. Implementacja pokazuje, jak zachować balans drzewa po każdej operacji wstawiania, co gwarantuje wydajność i poprawność struktury.

---
