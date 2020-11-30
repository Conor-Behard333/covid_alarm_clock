import main
from main import delete_alarm


def test_1():
    main.alarms = []
    delete_alarm("test")
    assert len(main.alarms) == 0


def test_2():
    main.alarms = [{"title": "test", "content": ""}]
    delete_alarm("test")
    assert len(main.alarms) == 0


def test_3():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_alarm("test")
    assert len(main.alarms) == 1


def test_4():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test2", "content": ""}]
    delete_alarm("test")
    assert main.alarms == expected

def test_5():
    main.alarms = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_alarm("test3")
    assert main.alarms == expected
