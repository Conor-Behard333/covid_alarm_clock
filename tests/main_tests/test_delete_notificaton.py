import main
from main import delete_notification


def test_1():
    main.notifications = []
    delete_notification("test")
    assert len(main.notifications) == 0


def test_2():
    main.notifications = [{"title": "test", "content": ""}]
    delete_notification("test")
    assert len(main.notifications) == 0


def test_3():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_notification("test")
    assert len(main.notifications) == 1


def test_4():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test2", "content": ""}]
    delete_notification("test")
    assert main.notifications == expected

def test_5():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_notification("test3")
    assert main.notifications == expected
