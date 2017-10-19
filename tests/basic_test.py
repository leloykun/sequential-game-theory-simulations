from ..sims.cat_mouse import data_visualizer as cat_mouse_vis
from ..sims.route_choice import data_visualizer as route_choice_vis
from ..sims.simple_migration import data_visualizer as simple_mig_vis


def test_cat_mouse_visualizer():
    cat_mouse_vis.visualize(test=True)


def test_route_choice_visualizer():
    route_choice_vis.visualize(test=True)


def test_simple_migration_visualizer():
    simple_mig_vis.visualize(test=True)
