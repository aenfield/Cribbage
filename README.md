# cribbage

Reminder to me: to run the tests, from the cribbage subdirectory, I run 'python -m pytest'. Based on https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#goodpractices I think this works - it makes the import in things like test_cards.py work - because Python puts the current directory in sys.path.