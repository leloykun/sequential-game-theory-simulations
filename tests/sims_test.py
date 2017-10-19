from ..sims.cat_mouse import cat_mouse
from ..sims.cat_mouse_cheese import cat_mouse_cheese
from ..sims.route_choice import route_choice
from ..sims.simple_migration import simple_migration
from ..sims.migration import migration


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
    # assert migration.__name__ == 'socialsims.sims.migration.migration'
