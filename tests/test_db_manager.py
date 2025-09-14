import pytest

import db_manager as dbm
from config import DATABASE_PATH

@pytest.fixture
def db_manager():
    return dbm.DBManager(DATABASE_PATH)

def test_script_data(db_manager):
    manager = db_manager
    assert "Script1" == manager.get_script_data(1)


def test_script_name(db_manager):
    manager = db_manager
    assert "Name1" == manager.get_script_name(1)


def test_script_description(db_manager):
    manager = db_manager
    assert "Description1" == manager.get_script_description(1)


def test_script_creator(db_manager):
    manager = db_manager
    assert "User1" == manager.get_script_author(1)


def test_script_likes(db_manager):
    manager = db_manager
    assert 1 == manager.get_script_likes(1)


def test_script_views(db_manager):
    manager = db_manager
    assert 10 == manager.get_script_views(1)


def test_users_rating(db_manager):
    manager = db_manager
    assert ["BlockMaster777", "User2", "User1"] == manager.get_users_rating()


def test_scripts_rating(db_manager):
    manager = db_manager
    assert [("Name3", 3, "BlockMaster777", 3, 30), ("Name2", 2, "User2", 2, 20), ("Name1", 1, "User1", 1, 10)] == manager.get_scripts_rating()


def test_user_id(db_manager):
    manager = db_manager
    assert 1 == manager.get_user_id("User1")


def test_search_scripts_by_name(db_manager):
    manager = db_manager
    assert ["Name3", "Name2", "Name1"] == manager.search_scripts_by_name("Name")