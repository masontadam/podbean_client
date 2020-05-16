from podbean_client import hello_world

def test_helloworld_no_params():
    assert say_hello() == "Hello, World!"

def test_helloworld_with_param():
    assert say_hello("Everyone") == "Hello, Everyone!"
