import math
import random
from mesa.experimental.cell_space import CellAgent

# Helper function
def get_distance(cell_1, cell_2):
    """
    Calculate the Euclidean distance between two positions
    used in trade.move()
    """
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class Trader(CellAgent):
    """
    Trader:
    - Has a metabolism of sugar and spice
    - Harvests and trades sugar and spice to survive
    - Prefers to trade based on assigned ad/user preferences (1 or 2)
    """

    def __init__(self, model, cell, sugar=0, spice=0, metabolism_sugar=0, metabolism_spice=0, vision=0):
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.spice = spice
        self.metabolism_sugar = metabolism_sugar
        self.metabolism_spice = metabolism_spice
        self.vision = vision
        self.prices = []
        self.trade_partners = []

        # Each trader prefers either type 1 or 2 resources (ad categories)
        self.preference = random.choice([1, 2])

    def get_trader(self, cell):
        """Helper function used in self.trade_with_neighbors()"""
        for agent in cell.agents:
            if isinstance(agent, Trader):
                return agent

    def trade_with_neighbors(self):
        """
        Traders will only trade sugar and spice that match their preference.
        """
        for neighbor in self.cell.get_neighborhood(radius=self.vision).agents:
            sugar_type = self.model.grid.sugar_type[neighbor.cell.coordinate]
            spice_type = self.model.grid.spice_type[neighbor.cell.coordinate]

            # Skip trade if the resource type does not match trader's preference
            if sugar_type != self.preference or spice_type != self.preference:
                continue  

            self.trade(neighbor)

    def harvest_sugar(self):
        sugar_available = self.cell.sugar
        sugar_type = self.model.grid.sugar_type[self.cell.coordinate]  # Get sugar type

        # Only harvest if it matches preference
        if sugar_type == self.preference:
            self.sugar += sugar_available

        self.cell.sugar = 0

    def harvest_spice(self):
        spice_available = self.cell.spice
        spice_type = self.model.grid.spice_type[self.cell.coordinate]  # Get spice type

        # Only harvest if it matches preference
        if spice_type == self.preference:
            self.spice += spice_available

        self.cell.spice = 0

    def move(self):
        """
        Function for trader agent to identify optimal move
        Traders prefer locations with their preferred resource type.
        """

        # Identify all possible moves
        neighboring_cells = [
            cell
            for cell in self.cell.get_neighborhood(self.vision, include_center=True)
            if cell.is_empty
        ]

        # Determine which move maximizes welfare while matching preference
        welfares = []
        for cell in neighboring_cells:
            sugar_type = self.model.grid.sugar_type[cell.coordinate]
            spice_type = self.model.grid.spice_type[cell.coordinate]

            # Only consider cells that match the trader's preference
            if sugar_type == self.preference or spice_type == self.preference:
                welfares.append(self.calculate_welfare(self.sugar + cell.sugar, self.spice + cell.spice))
            else:
                welfares.append(-1)  # Low priority if it doesn't match preference

        if not welfares:
            return  # No valid move

        # Find highest welfare move
        max_welfare = max(welfares)
        candidate_indices = [i for i, w in enumerate(welfares) if math.isclose(w, max_welfare)]
        candidates = [neighboring_cells[i] for i in candidate_indices]

        # Choose the closest best option
        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [
            cell for cell in candidates if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
        ]

        # Move to selected cell
        self.cell = self.random.choice(final_candidates)

    def eat(self):
        """Traders only consume resources that match their preference."""
        sugar_type = self.model.grid.sugar_type[self.cell.coordinate]
        spice_type = self.model.grid.spice_type[self.cell.coordinate]

        if sugar_type == self.preference:
            self.sugar += self.cell.sugar
            self.cell.sugar = 0
        self.sugar -= self.metabolism_sugar

        if spice_type == self.preference:
            self.spice += self.cell.spice
            self.cell.spice = 0
        self.spice -= self.metabolism_spice

    def maybe_die(self):
        """Function to remove Traders who have consumed all their preferred sugar or spice."""
        if self.is_starved():
            self.remove()
