import main
from main import valid_alarm_title


def test_valid_alarm():
    main.alarms = []
    test_alarm_name = "test"
    expected_output = True
    assert valid_alarm_title(test_alarm_name) == expected_output

def test_invalid_alarm():
    main.alarms = [{"title": "test", "content": ""}]
    test_alarm_name = "test"
    expected_output = False
    assert valid_alarm_title(test_alarm_name) == expected_output

def test_another_valid_alarm():
    main.alarms = [{"title": "test2", "content": ""}]
    test_alarm_name = "test"
    expected_output = True
    assert valid_alarm_title(test_alarm_name) == expected_output
