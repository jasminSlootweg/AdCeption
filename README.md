# Sugarscape Simulation - Implementation Overview

### §A. Overview of the Current Implementation State

The **Sugarscape simulation** has been adapted to model an **AI recommendation system** where:

- **Traders** represent **AI recommendation systems** that facilitate interactions between **users** and **advertisements**.
- **Sugar** represents **users**, and each user is assigned a **content type preference**.
- **Spice** represents **advertisements**, each with a specific **content type**.
- **Behavior**: Traders (AI recommendation systems) will only facilitate trades (recommendations) between **users (sugar)** and **advertisements (spice)** if their **content types match**. This ensures that users only receive advertisements that are relevant to their preferences, mimicking real-world recommendation systems.
- **Grid Environment**: The simulation takes place on a grid, where traders (AI systems) move and interact with users and advertisements. 
- **Metrics**: The model tracks **trader population**, **price**, and **trader preferences** (athough trader preferences is not yet visualized, simulating how AI recommendation systems match users with advertisements based on content relevance.

This simulation provides an environment to observe how recommendation systems function by ensuring users only engage with content that aligns with their preferences.

### §B. How to run the simulation

In order to run the simulation, open up the project in VSCode. In VSCode, open a terminal, and run the following commands
- **Create a Virtual Environment (Optional)**
- ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
  
- Install the Required Python Packages
- ```bash
  pip install altair solara networkx fuzzytm matplotlib requests clyent defusedxml urllib3 mesa conda-repo-cli
  
- Run the simulation
- ```bash
  solara run src/app.py

### §C. Limitations and Planned Improvements for the Next Phase

**Development Challenges:**
The initial setup of the Sugarscape agent-based simulation posed significant challenges. Extracting the source code from the MESA website required careful adjustments to ensure proper functionality. Our team encountered numerous errors when attempting to run the server, requiring the installation of several additional packages like **Solara**, **Mesa**, **NetworkX**, **FuzzyTM**, **Matplotlib**, **DefusedXML**, **Clyent**, **Altair**, **Conda-repo-cli**, and **Requests**. Once these packages were installed, we were able to successfully run the simulation on the Solara platform.

Modifying the base simulation code also proved difficult, as even small changes led to numerous errors without clear indications of their sources. After much troubleshooting, we shifted focus from interface modifications to refining agent behaviors. We implemented preference-based trade logic, ensuring that traders (AI systems) only engaged with resources matching their personal preferences.

**Planned Improvements:**
Future iterations will enhance the simulation by visually distinguishing traders based on their content preferences, showcasing the emergent "bubbles" of interaction. Additionally, we plan to introduce different recommendation strategies (e.g., aggressive targeting or balanced recommendations) to model various AI behaviors and improve the robustness of the simulation.




