# FightSimulator

The **FightSimulator** is a Python-based application that allows users to simulate fights between a player and a monster. The application is built using the Dash framework and provides a user-friendly interface to input various parameters and visualize the results.

## Features

1. **Interactive Dashboard**: The application provides an interactive dashboard where users can input various parameters related to the player and the monster, such as health points (HP), attack ability, defense ability, and more.

2. **Customizable Parameters**: Users can customize the number of players, HP, attack and defense abilities, and even the type of dice used for determining attack outcomes.

3. **Simulate Fights**: By clicking the "Simulate Fight" button, users can simulate a fight between the player and the monster for a specified number of rounds. The results are visualized in a graph, showing the HP history of both the player and the monster.

4. **Dynamic Player Creation**: The application supports the creation of multiple players, allowing users to simulate fights with multiple players against a single monster.

5. **Character Class**: The application includes a `Character` class that defines the properties and methods related to a character (player or monster). This class handles the logic for rolling dice, evaluating attack outcomes, and updating HP.

6. **Responsive Layout**: The layout of the application is responsive, adjusting based on the number of players and ensuring a user-friendly experience.

## How to Use

1. Input the number of players you want to simulate.
2. For each player, set the desired HP, attack ability, defense ability, and select the type and number of dice.
3. Set the parameters for the monster in a similar manner.
4. Specify the number of rounds for the simulation.
5. Click the "Simulate Fight" button to start the simulation.
6. View the results in the graph below, showing the HP history of the player(s) and the monster.

## Code Structure

- **app.py**: This is the main file that contains the logic for the application. It defines the layout of the dashboard, the callback functions to update the layout and simulate fights, and the `Character` class for handling character-related operations. You can view the code [here](https://github.com/SimonBon/FightSimulator/blob/main/app.py).

## Running the Application

To run the application, execute the `app.py` file. Ensure you have the required libraries installed, including Dash and Plotly.

```bash
python app.py
