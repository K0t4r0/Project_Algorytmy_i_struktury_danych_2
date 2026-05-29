import os

import pytest

from tools.compression_manager import CompManager


def test_compress_one_file_creates_kra_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "sample.txt"
    source.write_bytes(b"simple text for compression")

    CompManager.compress_one_file(source)

    output = tmp_path / "compressed_data" / "sample_txt.kra"
    assert output.exists()
    assert output.read_bytes().startswith(b"KRA")


def test_compress_and_decompress_one_file_round_trip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "sample.txt"
    source.write_bytes(b"ababababccccddddeeee")

    CompManager.compress_one_file(source)
    compressed = tmp_path / "compressed_data" / "sample_txt.kra"
    CompManager.decompress_one_file(compressed)

    decompressed = tmp_path / "decompressed_data" / "sample.txt"
    assert decompressed.exists()
    assert decompressed.read_bytes() == source.read_bytes()


def test_decompress_one_file_rejects_file_without_kra_magic_number(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    bad_file = tmp_path / "bad.kra"
    bad_file.write_bytes(b"BAD")

    with pytest.raises(ValueError, match="Not a .kra file"):
        CompManager.decompress_one_file(bad_file)
