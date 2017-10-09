from ..sims.migration import migration

def test_migration():
    assert migration.Mouse.colour == 'gray'
    assert migration.CasualCell.wall == False
    assert migration.process("1 13 11") == [1, 13, 11]
    assert migration.process(("1", "13", "11")) == [1, 13, 11]
    assert migration.process([1, 13, 11]) == [1, 13, 11]
    migration.run((1, 100, 3))
