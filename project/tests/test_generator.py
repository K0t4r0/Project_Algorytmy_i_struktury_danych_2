import json
import pytest

from tools.generator import DwarfDataGenerator


def test_generator_creation_with_list_names_file(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli", "Balin", "Dwalin"]))

    generator = DwarfDataGenerator(names_file=str(names_file))

    assert generator.names == ["Gimli", "Balin", "Dwalin"]
    assert generator.config["min_dwarves"] == 10
    assert generator.config["max_dwarves"] == 50


def test_generator_creation_with_dwarf_names_key(tmp_path):
    data = {
        "dwarf_names": ["Gimli", "Balin", "Thorin"]
    }

    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(data))

    generator = DwarfDataGenerator(names_file=str(names_file))

    assert generator.names == ["Gimli", "Balin", "Thorin"]


def test_generator_file_not_found():
    with pytest.raises(FileNotFoundError):
        DwarfDataGenerator(names_file="not_existing_names_file.json")


def test_generator_unknown_json_structure(tmp_path):
    data = {
        "wrong_key": ["Gimli", "Balin"]
    }

    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(data))

    with pytest.raises(ValueError):
        DwarfDataGenerator(names_file=str(names_file))


def test_custom_config_overrides_default_values(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli", "Balin"]))

    custom_config = {
        "min_dwarves": 2,
        "max_dwarves": 2,
        "grid_size": 20
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    assert generator.config["min_dwarves"] == 2
    assert generator.config["max_dwarves"] == 2
    assert generator.config["grid_size"] == 20


def test_random_pos_is_inside_grid(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli"]))

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config={"grid_size": 10}
    )

    pos = generator._random_pos()

    assert isinstance(pos, list)
    assert len(pos) == 2
    assert 0 <= pos[0] <= 10
    assert 0 <= pos[1] <= 10


def test_get_valid_pos_returns_position_not_too_close(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli"]))

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config={
            "grid_size": 100,
            "min_distance": 5
        }
    )

    occupied_positions = [[0, 0]]
    pos = generator._get_valid_pos(occupied_positions)

    assert isinstance(pos, list)
    assert len(pos) == 2

    distance = ((pos[0] - 0) ** 2 + (pos[1] - 0) ** 2) ** 0.5
    assert distance >= 5


def test_generate_returns_main_sections(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli", "Balin", "Dwalin"]))

    custom_config = {
        "min_dwarves": 2,
        "max_dwarves": 2,
        "min_mines": 1,
        "max_mines": 1,
        "min_guards": 3,
        "max_guards": 3
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    data = generator.generate()

    assert "dwarves" in data
    assert "mines" in data
    assert "guards" in data

    assert len(data["dwarves"]) == 2
    assert len(data["mines"]) == 1
    assert len(data["guards"]) == 3


def test_generate_dwarf_structure(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli", "Balin"]))

    custom_config = {
        "min_dwarves": 1,
        "max_dwarves": 1,
        "min_mines": 0,
        "max_mines": 0,
        "min_guards": 0,
        "max_guards": 0,
        "mine_types": ["gold", "iron"],
        "min_skills": 1,
        "max_skills": 2,
        "min_value": 50,
        "max_value": 100,
        "grid_size": 20
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    data = generator.generate()
    dwarf = data["dwarves"][0]

    assert dwarf["id"] == 1
    assert dwarf["name"] in ["Gimli", "Balin"]
    assert isinstance(dwarf["skills"], list)
    assert len(dwarf["skills"]) >= 1
    assert all(skill in ["gold", "iron"] for skill in dwarf["skills"])
    assert 50 <= dwarf["value"] <= 100
    assert isinstance(dwarf["home_pos"], list)
    assert len(dwarf["home_pos"]) == 2


def test_generate_mine_structure(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli"]))

    custom_config = {
        "min_dwarves": 0,
        "max_dwarves": 0,
        "min_mines": 1,
        "max_mines": 1,
        "min_guards": 0,
        "max_guards": 0,
        "mine_types": ["gold"],
        "min_capacity": 2,
        "max_capacity": 5,
        "grid_size": 20
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    data = generator.generate()
    mine = data["mines"][0]

    assert mine["id"] == "M-01"
    assert mine["mine_type"] == "gold"
    assert 2 <= mine["capacity"] <= 5
    assert isinstance(mine["pos"], list)
    assert len(mine["pos"]) == 2


def test_generate_guards_values_are_inside_range(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli"]))

    custom_config = {
        "min_dwarves": 0,
        "max_dwarves": 0,
        "min_mines": 0,
        "max_mines": 0,
        "min_guards": 5,
        "max_guards": 5,
        "min_loudness": 10,
        "max_loudness": 20
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    data = generator.generate()

    assert len(data["guards"]) == 5

    for guard in data["guards"]:
        assert "id" in guard
        assert "name" in guard
        assert "loudness" in guard

        assert isinstance(guard["id"], int)
        assert isinstance(guard["name"], str)
        assert 10 <= guard["loudness"] <= 20


def test_generate_uses_default_dwarf_name_when_names_are_missing(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps([]))

    custom_config = {
        "min_dwarves": 2,
        "max_dwarves": 2,
        "min_mines": 0,
        "max_mines": 0,
        "min_guards": 0,
        "max_guards": 0
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    data = generator.generate()

    assert data["dwarves"][0]["name"] == "Dwarf_1"
    assert data["dwarves"][1]["name"] == "Dwarf_2"


def test_generate_and_save_creates_json_file(tmp_path):
    names_file = tmp_path / "names.json"
    names_file.write_text(json.dumps(["Gimli", "Balin"]))

    output_file = tmp_path / "generated_data.json"

    custom_config = {
        "min_dwarves": 1,
        "max_dwarves": 1,
        "min_mines": 1,
        "max_mines": 1,
        "min_guards": 1,
        "max_guards": 1
    }

    generator = DwarfDataGenerator(
        names_file=str(names_file),
        custom_config=custom_config
    )

    saved_path, data = generator.generate_and_save(output_file=str(output_file))

    assert output_file.exists()
    assert saved_path == str(output_file)

    saved_data = json.loads(output_file.read_text())

    assert saved_data == data
    assert "dwarves" in saved_data
    assert "mines" in saved_data
    assert "guards" in saved_data