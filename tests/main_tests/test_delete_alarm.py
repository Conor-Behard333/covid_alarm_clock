import main
from main import delete_alarm


def test_deleting_from_empty_list():
    main.alarms = []
    delete_alarm("test")
    assert len(main.alarms) == 0


def test_deleting_alarm_from_list():
    main.alarms = [{"title": "test", "content": ""}]
    delete_alarm("test")
    assert len(main.alarms) == 0


def test_deleting_one_alarm_from_list():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_alarm("test")
    assert len(main.alarms) == 1


def test_deleting_different_alarm_from_list():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test2", "content": ""}]
    delete_alarm("test")
    assert main.alarms == expected

def test_deleting_non_existent_alarm():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_alarm("test3")
    assert main.alarms == expected
