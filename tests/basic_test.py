from ..sims import data_visualizer as cat_mouse_vis
from ..sims import data_visualizer as route_choice_vis
from ..sims import data_visualizer as simple_mig_vis


@pytest.mark.skip(reason="deprecated")
def test_cat_mouse_visualizer():
    cat_mouse_vis.visualize(test=True)


@pytest.mark.skip(reason="deprecated")
def test_route_choice_visualizer():
    route_choice_vis.visualize(test=True)


@pytest.mark.skip(reason="deprecated")
def test_simple_migration_visualizer():
    simple_mig_vis.visualize(test=True)
