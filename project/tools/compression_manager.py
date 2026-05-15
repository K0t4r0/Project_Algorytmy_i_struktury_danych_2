import os
from concurrent.futures import ThreadPoolExecutor
from algorithms.huffman import Huffman

class CompManager:
    MAX_WORKERS = 3

    @classmethod
    def decompress_one_file(cls, path):
        """ Structure of .kra file\n
            Offset          Value\n
            0 - 2           Magic Number\n
            3 - 6           Dict Entries\n
            7 - ...         Huffman Dictionary\n
            ...             Compressed Data\n
            last byte       Padding\n
        """
        os.makedirs("decompressed_data", exist_ok=True)
        file_size = os.path.getsize(path)

        with open(path, "rb") as f:
            if f.read(3) != b'KRA':
                raise ValueError("Not a .kra file!")

            dict_size = int.from_bytes(f.read(4), 'big')
            freqs = {}
            for _ in range(dict_size):
                char = f.read(1)[0]
                freq = int.from_bytes(f.read(4), 'big')
                freqs[char] = freq

            root = Huffman.build_tree(freqs)
            codes = Huffman.get_codes(root)

            header_end = f.tell()
            data_len = file_size - header_end - 1
            
            f.seek(file_size - 1)
            padding_len = f.read(1)[0]
            
            f.seek(header_end)

            def data_streamer(limit, chunk_size=65536):
                bytes_read = 0
                while bytes_read < limit:
                    to_read = min(chunk_size, limit - bytes_read)
                    chunk = f.read(to_read)
                    if not chunk: break
                    yield from chunk
                    bytes_read += len(chunk)

            output_filename = os.path.basename(path).replace(".kra", "").replace("_", ".", 1)
            output_path = os.path.join("decompressed_data", output_filename)

            Huffman.decompress_to_file(data_streamer(data_len), padding_len, codes, output_path)

        print(f"Finished: {output_path}")
    @classmethod
    def compress_one_file(cls, path):
        """ Structure of .kra file\n
            Offset          Value\n
            0 - 2           Magic Number\n
            3 - 6           Dict Entries\n
            7 - ...         Huffman Dictionary\n
            ...             Compressed Data\n
            last byte       Padding\n
        """
        os.makedirs("compressed_data", exist_ok=True)

        print(f"Start compressing {path}...")
        freqs = Huffman.get_file_frequencies(path)
        root = Huffman.build_tree(freqs)
        codes = Huffman.get_codes(root)

        base_name = os.path.basename(path)
        if "." in base_name:
            filename = base_name.replace(".", "_", 1) + ".kra"
        else:
            filename = base_name + ".kra"

        output_path = os.path.join("compressed_data", filename)

        with open(output_path, "wb") as f:
            f.write(b'KRA')
            f.write(len(freqs).to_bytes(4, 'big'))

            for char, freq in freqs.items():
                f.write(bytes([char]))
                f.write(freq.to_bytes(4, 'big'))

            for byte in Huffman.compress_generator(path, codes):
                f.write(byte.to_bytes(1, 'big'))

        print(f"Finished: {output_path}")

    @classmethod
    def compress_files(cls, paths):
        with ThreadPoolExecutor(max_workers=cls.MAX_WORKERS) as exec:
            results = exec.map(cls.compress_one_file, paths)
            for _ in results:
                pass
            

if __name__ == "__main__":
    # paths = ["json/test1.json", "json/test2.json", "json/test3.json"]
    # CompManager.compress_files(paths)
    CompManager.decompress_one_file("compressed_data/test1_json.kra")

        