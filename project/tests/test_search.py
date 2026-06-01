from algorithms.search import rabin_karp_file_search


def test_rabin_karp_file_search(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("abc abc abc", encoding="utf-8")

    result = rabin_karp_file_search(file_path, "abc")

    assert result == [0, 4, 8]
