from ..sims.migration import migration
from ..sims.route_choice import route_choice


def test_migration():
    assert migration.Mouse.colour == 'gray'
    assert migration.CasualCell.wall == False
    assert migration.process("1 13 11") == [1, 13, 11]
    assert migration.process(("1", "13", "11")) == [1, 13, 11]
    assert migration.process([1, 13, 11]) == [1, 13, 11]
    migration.run((1, 100, 3))
    assert migration.__name__ == 'socialsims.sims.migration.migration'


def test_route_choice():
    assert route_choice.sim_name == 'route_choice'
