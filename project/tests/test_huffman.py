from algorithms.huffman import Huffman


def test_get_file_frequencies_counts_bytes(tmp_path):
    file_path = tmp_path / "sample.bin"
    file_path.write_bytes(b"abbccc")

    frequencies = Huffman.get_file_frequencies(file_path)

    assert frequencies[ord("a")] == 1
    assert frequencies[ord("b")] == 2
    assert frequencies[ord("c")] == 3


def test_build_tree_and_get_codes_contains_all_symbols():
    frequencies = {ord("a"): 5, ord("b"): 2, ord("c"): 1}

    root = Huffman.build_tree(frequencies)
    codes = Huffman.get_codes(root)

    assert set(codes.keys()) == set(frequencies.keys())
    assert all(isinstance(code, str) for code in codes.values())
    assert all(code != "" for code in codes.values())


def test_compress_and_decompress_round_trip(tmp_path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"
    input_path.write_bytes(b"ala ma kota ala ma psa")

    frequencies = Huffman.get_file_frequencies(input_path)
    root = Huffman.build_tree(frequencies)
    codes = Huffman.get_codes(root)

    compressed = list(Huffman.compress_generator(input_path, codes))
    padding_len = compressed[-1]
    compressed_data = compressed[:-1]

    Huffman.decompress_to_file(compressed_data, padding_len, codes, output_path)

    assert output_path.read_bytes() == input_path.read_bytes()
