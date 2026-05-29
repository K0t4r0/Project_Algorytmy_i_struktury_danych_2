import json
import pytest

from data_classes.classes import Dwarf, Mine, BorderGuard
from tools.data_manager import DataManager


def test_dwarf_creation():
    dwarf = Dwarf(
        id=1,
        name="Doc",
        skills=["gold"],
        value=100,
        home_pos=(10, 20)
    )

    assert dwarf.name == "Doc"
    assert isinstance(dwarf.home_pos, tuple)
    assert len(dwarf.home_pos) == 2


def test_mine_creation():
    mine = Mine(
        id="M-01",
        mine_type="iron",
        capacity=5,
        pos=(50, 50)
    )

    assert mine.capacity > 0
    assert mine.mine_type == "iron"


def test_border_guard_creation():
    guard = BorderGuard(
        id=101,
        name="Guard_1",
        loudness=50
    )

    assert guard.id == 101
    assert guard.name == "Guard_1"
    assert guard.loudness == 50
    assert guard.position_meters == 0.0
    assert guard.edge_index == -1


def test_load_from_json_success(tmp_path):
    data = {
        "dwarves": [
            {
                "id": 1,
                "name": "Gimli",
                "skills": ["coal"],
                "value": 50,
                "home_pos": [0, 0]
            }
        ],
        "mines": [],
        "guards": [
            {
                "id": 101,
                "name": "Guard_1",
                "loudness": 10
            },
            {
                "id": 102,
                "name": "Guard_2",
                "loudness": 20
            },
            {
                "id": 103,
                "name": "Guard_3",
                "loudness": 30
            }
        ]
    }

    file = tmp_path / "test_data.json"
    file.write_text(json.dumps(data))

    manager = DataManager()
    success = manager.load_from_json(str(file))

    assert success is True
    assert len(manager.dwarves) == 1
    assert manager.dwarves[0].name == "Gimli"
    assert isinstance(manager.dwarves[0].home_pos, tuple)

    assert len(manager.guards) == 3
    assert manager.guards[0].id == 101
    assert manager.guards[0].name == "Guard_1"
    assert manager.guards[0].loudness == 10


def test_load_from_json_invalid_file():
    manager = DataManager()

    success = manager.load_from_json("non_existent_file.json")

    assert success is False


def test_data_integrity_types(tmp_path):
    data = {
        "dwarves": [
            {
                "id": 9,
                "name": "Thorin",
                "skills": [],
                "value": 200,
                "home_pos": [15, 25]
            }
        ],
        "mines": [
            {
                "id": "M-01",
                "mine_type": "gold",
                "capacity": 3,
                "pos": [50, 60]
            }
        ],
        "guards": [
            {
                "id": 101,
                "name": "Guard_1",
                "loudness": 70
            }
        ]
    }

    file = tmp_path / "integrity.json"
    file.write_text(json.dumps(data))

    manager = DataManager()
    manager.load_from_json(str(file))

    assert isinstance(manager.dwarves[0].home_pos, tuple)
    assert isinstance(manager.mines[0].pos, tuple)
    assert isinstance(manager.guards[0], BorderGuard)