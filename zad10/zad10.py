import heapq
from collections import Counter

class Huffman:
    class _Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    @classmethod
    def _create_tree(cls, text):
        freq = Counter(text)
        queue = [cls._Node(char, f) for char, f in freq.items()]
        heapq.heapify(queue)

        while len(queue) > 1:
            left = heapq.heappop(queue)
            right = heapq.heappop(queue)
            
            merged = cls._Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(queue, merged)

        return queue[0]

    @classmethod
    def _generate_codes(cls, huffman_codes, node, current_code=""):
        if node is None:
            return
        
        if node.char is not None:
            huffman_codes[node.char] = current_code
            
        cls._generate_codes(huffman_codes, node.left, current_code + "0")
        cls._generate_codes(huffman_codes, node.right, current_code + "1")

    @classmethod
    def compress(cls, text):
        if text is None:
            raise ValueError("The parameter 'text' is None. The text cannot be compressed!")

        root = cls._create_tree(text)
        huffman_codes = {}
        cls._generate_codes(huffman_codes, root)

        encoded_str = "".join(huffman_codes[char] for char in text)
        padding_len = 8 - (len(encoded_str) % 8) % 8
        encoded_str = encoded_str + ("0" * padding_len)

        byte_array = bytearray()
        for i in range(0, len(encoded_str), 8):
            byte = encoded_str[i:i+8]
            byte_array.append(int(byte, 2))
        
        return bytes(byte_array), padding_len, huffman_codes

    @staticmethod
    def decompress(compressed_text, padding_len, huffman_codes):
        if compressed_text is None:
            raise ValueError("Compressed text is None!")
        if padding_len is None:
            raise ValueError("Padding lenght is None!")
        if huffman_codes is None:
            raise ValueError("Huffman codes is None!")

        byte_array = bytearray(compressed_text)
        reverse_codes = {v: k for k, v in huffman_codes.items()}
        text = ""

        encoded_str = "".join(f"{b:08b}" for b in byte_array)

        if padding_len > 0:
            encoded_str = encoded_str[:-padding_len]

        current_code = ""
        for bit in encoded_str:
            current_code += bit
            char = reverse_codes.get(current_code)
            if char is not None:
                text += char
                current_code = ""

        return text
    
# Example
# ============================================================
# aaabracabbr
# ============================================================

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
