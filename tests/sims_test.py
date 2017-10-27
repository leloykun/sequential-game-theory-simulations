from ..src.sims import cat_mouse
from ..src.sims import cat_mouse_cheese
from ..src.sims import route_choice
from ..src.sims import simple_migration
from ..src.sims import migration


def test_cat_mouse():
    cat_mouse.run("1 2 1", test=True, to_save=False)


def test_cat_mouse_cheese():
    cat_mouse_cheese.run((1, 100, 100), test=True, to_save=False)


def test_route_choice():
    route_choice.run(["1", "100", "10", "1", "2", "3", "4"], test=True)


def test_simple_migration():
    simple_migration.run([1, 100, 2], test=True)


def test_migration():
    migration.run((1, 100, 3), test=True)
