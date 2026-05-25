class BoyerMoore:
    @classmethod
    def _build_last_table(cls, pattern):
        m = len(pattern)
        p_1 = " " + pattern
        last_table = {}
        
        for i in range(1, m + 1):
            last_table[p_1[i]] = i
            
        return last_table

    @classmethod
    def _build_bmnext_table(cls, pattern):
        m = len(pattern)
        p_1 = " " + pattern
        bmnext = [0] * (m + 2)
        pi = [0] * (m + 3)


        i = m + 1
        b = m + 2
        pi[i] = b

        while i > 1:
            while b <= m + 1 and p_1[i - 1] != p_1[b - 1]:
                if bmnext[b] == 0:
                    bmnext[b] = b - i
                b = pi[b]
            b -= 1
            i -= 1
            pi[i] = b

        
        b = pi[1]
        for i in range(1, m + 2):
            if bmnext[i] == 0:
                bmnext[i] = b - 1
            if i == b:
                b = pi[b]

        return bmnext

    @classmethod
    def search(cls, text, pattern):
        if text is None:
            raise ValueError("The parameter 'text' is None. Cannot search in a None text!")
        if pattern is None:
            raise ValueError("The parameter 'pattern' is None. Cannot search for a None pattern!")

        n = len(text)
        m = len(pattern)

        if m == 0 or n == 0 or m > n:
            return []

        # Pad strings with a blank space to exactly match the 1-based indexing 
        # used in the academic pseudo-code
        t_1 = " " + text
        p_1 = " " + pattern

        last_table = cls._build_last_table(pattern)
        bmnext_table = cls._build_bmnext_table(pattern)

        matches = []
        i = 1

        while i <= n - m:
            j = m
            while j > 0 and p_1[j] == t_1[i + j - 1]:
                j -= 1

            if j > 0:
                shift_good_suffix = bmnext_table[j + 1]
                shift_bad_char = j - last_table.get(t_1[i + j - 1], 0)
                i += max(shift_good_suffix, shift_bad_char)
            else:
                # Match found. Convert the 1-based index 'i' back to a 0-based index
                matches.append(i - 1)
                i += bmnext_table[1]

        return matches

# Example
# ============================================================
# Text: ABCDBABCABBCDABCAB
# Pattern: ABCAB
# ============================================================

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