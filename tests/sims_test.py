from ..sims.cat_mouse import cat_mouse
from ..sims.cat_mouse_cheese import cat_mouse_cheese
from ..sims.route_choice import route_choice
from ..sims.simple_migration import simple_migration
from ..sims.migration import migration


def test_cat_mouse():
    assert cat_mouse.sim_name == 'cat_mouse'
    assert cat_mouse.output_dir == 'sims/cat_mouse/data/'
    assert cat_mouse.max_visual_depth == 4
    cat_mouse.run("1 2 1", test=True)


def test_route_choice():
    assert route_choice.sim_name == 'route_choice'


def test_migration():
    assert migration.Mouse.colour == 'gray'
    assert migration.CasualCell.wall == False
    assert migration.process("1 13 11") == [1, 13, 11]
    assert migration.process(("1", "13", "11")) == [1, 13, 11]
    assert migration.process([1, 13, 11]) == [1, 13, 11]
    migration.run((1, 100, 3))
    assert migration.__name__ == 'socialsims.sims.migration.migration'
