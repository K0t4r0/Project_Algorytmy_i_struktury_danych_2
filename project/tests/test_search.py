from algorithms.search import compute_prefix_table, kmp_file_search, rabin_karp_file_search


def test_compute_prefix_table_for_repeated_pattern():
    assert compute_prefix_table("ababaca") == [0, 0, 1, 2, 3, 0, 1]


def test_kmp_file_search_finds_all_occurrences(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("ababa ababa", encoding="utf-8")

    result = kmp_file_search(file_path, "aba")

    assert result == [0, 2, 6, 8]


def test_rabin_karp_file_search_finds_first_occurrence(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("abc abc abc", encoding="utf-8")

    result = rabin_karp_file_search(file_path, "abc")

    assert result == [0]


def test_search_returns_empty_list_for_empty_pattern(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("abc", encoding="utf-8")

    assert kmp_file_search(file_path, "") == []
    assert rabin_karp_file_search(file_path, "") == []


def test_search_returns_empty_list_when_pattern_not_found(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("abcdef", encoding="utf-8")

    assert kmp_file_search(file_path, "xyz") == []
    assert rabin_karp_file_search(file_path, "xyz") == []
