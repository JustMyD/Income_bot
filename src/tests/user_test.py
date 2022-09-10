from src.services.user import new_user

def test_new_user():
    assert new_user("1823068761") == False