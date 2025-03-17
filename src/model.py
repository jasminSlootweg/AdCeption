from pathlib import Path
import numpy as np
import mesa
from mesa.examples.advanced.sugarscape_g1mt.agents import Trader
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space.property_layer import PropertyLayer

# Helper Functions
def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def geometric_mean(list_of_prices):
    return np.exp(np.log(list_of_prices).mean())

def get_trade(agent):
    if isinstance(agent, Trader):
        return agent.trade_partners
    return None

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
        seed=None,
    ):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.enable_trade = enable_trade
        self.running = True

        self.grid = OrthogonalVonNeumannGrid((self.width, self.height), torus=False, random=self.random)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "#Traders": lambda m: len(m.agents),
                "Trade Volume": lambda m: sum(len(a.trade_partners) for a in m.agents),
                "Price": lambda m: geometric_mean(flatten([a.prices for a in m.agents])),
            },
            agent_reporters={"Trade Network": get_trade},
        )

        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.spice_distribution = np.flip(self.sugar_distribution, 1)

        self.grid.add_property_layer(PropertyLayer.from_data("sugar", self.sugar_distribution))
        self.grid.add_property_layer(PropertyLayer.from_data("spice", self.spice_distribution))

        Trader.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
            sugar=self.rng.integers(endowment_min, endowment_max, (initial_population,), endpoint=True),
            spice=self.rng.integers(endowment_min, endowment_max, (initial_population,), endpoint=True),
            metabolism_sugar=self.rng.integers(metabolism_min, metabolism_max, (initial_population,), endpoint=True),
            metabolism_spice=self.rng.integers(metabolism_min, metabolism_max, (initial_population,), endpoint=True),
            vision=self.rng.integers(vision_min, vision_max, (initial_population,), endpoint=True),
        )

    def step(self):
        self.grid.sugar.data = np.minimum(self.grid.sugar.data + 1, self.sugar_distribution)
        self.grid.spice.data = np.minimum(self.grid.spice.data + 1, self.spice_distribution)

        trader_shuffle = self.agents_by_type[Trader].shuffle()
        for agent in trader_shuffle:
            agent.prices = []
            agent.trade_partners = []
            agent.move()
            agent.eat()
            agent.maybe_die()

        if not self.enable_trade:
            self.datacollector.collect(self)
            return

        trader_shuffle = self.agents_by_type[Trader].shuffle()
        for agent in trader_shuffle:
            agent.trade_with_neighbors()

        self.datacollector.collect(self)
        agent_trades = self.datacollector._agent_records[self.steps]
        agent_trades = [agent for agent in agent_trades if agent[2] is not None]
        self.datacollector._agent_records[self.steps] = agent_trades

    def run_model(self, step_count=1000):
        for _ in range(step_count):
            self.step()