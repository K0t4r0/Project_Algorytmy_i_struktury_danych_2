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

# Example
# ====================================================================
# ABACABADABACABA_ABACABA

# ABACABA
# ====================================================================

text = input()
pattern = input()
print(f"rabin_karp_search: {rabin_karp_search(text, pattern)}")
print(f"kmp_search: {kmp_search(text, pattern)}")