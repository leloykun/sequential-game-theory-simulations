from ..sims.migration import migration

def test_migration():
    assert migration.Mouse.colour == 'gray'
    assert migration.CasualCell.wall == False