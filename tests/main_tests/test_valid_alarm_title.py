import main
from main import valid_alarm_title


def test_1():
    main.alarms = []
    test_alarm_name = "test"
    expected_output = True
    assert valid_alarm_title(test_alarm_name) == expected_output

def test_2():
    main.alarms = [{"title": "test", "content": ""}]
    test_alarm_name = "test"
    expected_output = False
    assert valid_alarm_title(test_alarm_name) == expected_output

def test_3():
    main.alarms = [{"title": "test2", "content": ""}]
    test_alarm_name = "test"
    expected_output = True
    assert valid_alarm_title(test_alarm_name) == expected_output
