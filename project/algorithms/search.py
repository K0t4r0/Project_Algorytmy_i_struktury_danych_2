from collections import deque


def rabin_karp_file_search(file_path, pattern):
    m = len(pattern)
    if m == 0: return []
    
    alphabet_size = 256
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
            
            if len(window) <= m:
                current_window_hash = (alphabet_size * current_window_hash + ord(char)) % prime_modulus
            else:
                out_char = window.popleft()
                current_window_hash = (alphabet_size * (current_window_hash - ord(out_char) * h_multiplier) + ord(char)) % prime_modulus
            
            if len(window) == m:
                if current_window_hash == pattern_hash:
                    if "".join(window) == pattern:
                        occurrence_indices.append(absolute_index - m + 1)
            
            absolute_index += 1

    return occurrence_indices