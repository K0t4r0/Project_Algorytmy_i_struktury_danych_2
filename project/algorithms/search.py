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

def compute_prefix_table(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k-1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi

def kmp_file_search(file_path, pattern):
    m = len(pattern)
    if m == 0: return []
    
    pi = compute_prefix_table(pattern)
    occurrence_indices = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        q = 0
        absolute_index = 0
        
        while True:
            char = f.read(1)
            if not char: break
            
            while q > 0 and pattern[q] != char:
                q = pi[q-1]
            if pattern[q] == char:
                q += 1
            
            if q == m:
                occurrence_indices.append(absolute_index - m + 1)
                q = pi[q-1]
                
            absolute_index += 1
            
    return occurrence_indices