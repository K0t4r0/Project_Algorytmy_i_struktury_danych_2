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
    def build_tree(cls, frequencies):
        queue = [cls._Node(char, f) for char, f in frequencies.items()]
        heapq.heapify(queue)
        while len(queue) > 1:
            l, r = heapq.heappop(queue), heapq.heappop(queue)
            merged = cls._Node(None, l.freq + r.freq)
            merged.left, merged.right = l, r
            heapq.heappush(queue, merged)
        return queue[0] if queue else None

    @classmethod
    def get_codes(cls, node, current_code="", codes=None):
        if codes is None: codes = {}
        if node:
            if node.char is not None:
                codes[node.char] = current_code
            cls.get_codes(node.left, current_code + "0", codes)
            cls.get_codes(node.right, current_code + "1", codes)
        return codes

    @staticmethod
    def get_file_frequencies(file_path, chunk_size=65536):
        counter = Counter()
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                counter.update(chunk)
        return counter

    @classmethod
    def compress_generator(cls, file_path, codes, chunk_size=65536):
        current_byte = 0
        bits_filled = 0

        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                for byte in chunk:
                    symbol_code = codes[byte]
                    for bit in symbol_code:
                        current_byte = (current_byte << 1) | int(bit)
                        bits_filled += 1
                        
                        if bits_filled == 8:
                            yield current_byte
                            current_byte = 0
                            bits_filled = 0
            
            if bits_filled > 0:
                padding_len = 8 - bits_filled
                current_byte <<= padding_len
                yield current_byte
                yield padding_len
            else:
                yield 0

    @staticmethod
    def decompress_to_file(compressed_data_stream, padding_len, huffman_codes, output_path):
        reverse_codes = {v: k for k, v in huffman_codes.items()}
        current_code = ""
        
        write_buffer = bytearray()
        BUFFER_SIZE = 65536

        with open(output_path, 'wb') as f:
            it = iter(compressed_data_stream)
            
            try:
                byte = next(it)
            except StopIteration:
                return

            while True:
                try:
                    next_byte = next(it)
                    
                    for i in range(7, -1, -1):
                        bit = (byte >> i) & 1
                        current_code += str(bit)
                        if current_code in reverse_codes:
                            write_buffer.append(reverse_codes[current_code])
                            current_code = ""
                    
                    byte = next_byte

                    if len(write_buffer) >= BUFFER_SIZE:
                        f.write(write_buffer)
                        write_buffer.clear()

                except StopIteration:
                    bits_to_read = 8 - padding_len
                    for i in range(7, 7 - bits_to_read, -1):
                        bit = (byte >> i) & 1
                        current_code += str(bit)
                        if current_code in reverse_codes:
                            write_buffer.append(reverse_codes[current_code])
                            current_code = ""
                    break
            
            if write_buffer:
                f.write(write_buffer)