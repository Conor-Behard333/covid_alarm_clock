import main
from main import delete_notification


def test_deleting_from_empty_list():
    main.notifications = []
    delete_notification("test")
    assert len(main.notifications) == 0


def test_deleting_notification_from_list():
    main.notifications = [{"title": "test", "content": ""}]
    delete_notification("test")
    assert len(main.notifications) == 0


def test_deleting_one_notification_from_list():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_notification("test")
    assert len(main.notifications) == 1


def test_deleting_different_notification_from_list():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test2", "content": ""}]
    delete_notification("test")
    assert main.notifications == expected


def test_deleting_non_existent_notification():
    main.notifications = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    expected = [{"title": "test", "content": ""}, {"title": "test2", "content": ""}]
    delete_notification("test3")
    assert main.notifications == expected
