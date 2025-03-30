from pathlib import Path
import numpy as np
import mesa
from mesa.examples.advanced.sugarscape_g1mt.agents import Trader
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space.property_layer import PropertyLayer

class SugarscapeG1mt(mesa.Model):
    def __init__(
        self,
        width=50,
        height=50,
        initial_population=200,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
        enable_trade=True,
        preference_switch_threshold=3,  # Default threshold for switching
        seed=None,
    ):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.enable_trade = enable_trade
        self.preference_switch_threshold = preference_switch_threshold  # Store threshold
        self.running = True

        self.grid = OrthogonalVonNeumannGrid((self.width, self.height), torus=False, random=self.random)
        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.spice_distribution = np.flip(self.sugar_distribution, 1)

        self.grid.add_property_layer(PropertyLayer.from_data("sugar", self.sugar_distribution))
        self.grid.add_property_layer(PropertyLayer.from_data("spice", self.spice_distribution))

        Trader.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
        )

    def step(self):
        """Advances the model by one step."""
        self.grid.sugar.data = np.minimum(self.grid.sugar.data + 1, self.sugar_distribution)
        self.grid.spice.data = np.minimum(self.grid.spice.data + 1, self.spice_distribution)

        for agent in self.agents_by_type[Trader].shuffle():
            agent.prices = []
            agent.trade_partners = []
            agent.move()
            agent.eat()
            agent.maybe_die()

        if self.enable_trade:
            for agent in self.agents_by_type[Trader].shuffle():
                agent.trade_with_neighbors()
