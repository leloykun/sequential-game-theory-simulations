from ..sims.cat_mouse import data_analyzer as cat_mouse_ana

from ..sims.cat_mouse import data_visualizer as cat_mouse_vis
from ..sims.route_choice import data_visualizer as route_choice_vis
from ..sims.simple_migration import data_visualizer as simple_mig_vis

def test_data_analyzers():
    cat_mouse_ana.analyze()

def test_data_visualizers():
    cat_mouse_vis.visualize()
    route_choice_vis.visualize()
    simple_mig_vis.visualize()
