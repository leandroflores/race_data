from project_1 import main

def test_max_value():
    assert main.max_value([]) == None
    assert main.max_value([-3]) == -3
    assert main.max_value([0, -5]) == 0