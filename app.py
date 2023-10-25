import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

import numpy as np

app = dash.Dash(__name__)

fig = go.Figure()

app.layout = html.Div([

    html.Div([
        html.Label("Number of Players:"),
        dcc.Input(placeholder="number of player", value=1, type="number", id="n-players"),
    ]),

    # Player Column
    html.Div([
        html.H3("Player"),
        # Player HP Bar
        html.Label("Player HP:"),
        dcc.Input(id="hp", type="number", placeholder="Enter Player HP...", value=100),
        html.Div(),
        html.Label("Player Attack Ability:"),
        dcc.Input(id="attack", type="number", placeholder="Enter Player Attack Ability Thresh...", value=80),
        html.Div(),
        html.Label("Player Defense Ability:"),
        dcc.Input(id="block", type="number", placeholder="Enter Player Defense Ability Thresh...", value=10),
        html.Div(),

        # Player Sliders
        html.Label("D4:"),
        dcc.Slider(id="player-D4", min=0, max=10, step=1, value=0),
        html.Label("D6:"),
        dcc.Slider(id="player-D6", min=0, max=10, step=1, value=0),
        html.Label("D8:"),
        dcc.Slider(id="player-D8", min=0, max=10, step=1, value=0),
        html.Label("D10:"),
        dcc.Slider(id="player-D10", min=0, max=10, step=1, value=0),
        html.Label("D12:"),
        dcc.Slider(id="player-D12", min=0, max=10, step=1, value=0),
        html.Label("D20:"),
        dcc.Slider(id="player-D20", min=0, max=10, step=1, value=0),
        html.Label("D100:"),
        dcc.Slider(id="player-D100", min=0, max=10, step=1, value=0),
    ], style={'float': 'left', 'width': '48%'},  id="player-column"),
    
    # Monster Column
    html.Div([
        html.H3("Monster"),
        
        # Monster HP Bar
        html.Label("Monster HP:"),
        dcc.Input(id="m%0%hp", type="number", placeholder="Enter Monster HP...", value=100),
        html.Div(),
        html.Label("Monster Attack Ability:"),
        dcc.Input(id="m%0%attack", type="number", placeholder="Enter Monster Attack Ability Thresh...", value=60),
        html.Div(),
        html.Label("Monster Defense Ability:"),
        dcc.Input(id="m%0%defense", type="number", placeholder="Enter Monster Defense Ability Thresh...", value=10),
        html.Div(),

        # Monster Sliders
        html.Label("D4:"),
        dcc.Slider(id="M%D4", min=0, max=10, step=1, value=0),
        html.Label("D6:"),
        dcc.Slider(id="M%D6", min=0, max=10, step=1, value=0),
        html.Label("D8:"),
        dcc.Slider(id="M%D8", min=0, max=10, step=1, value=0),
        html.Label("D10:"),
        dcc.Slider(id="M%D10", min=0, max=10, step=1, value=0),
        html.Label("D12:"),
        dcc.Slider(id="M%D12", min=0, max=10, step=1, value=0),
        html.Label("D20:"),
        dcc.Slider(id="M%D20", min=0, max=10, step=1, value=0),
        html.Label("D100:"),
        dcc.Slider(id="M%D100", min=0, max=10, step=1, value=0),
    ], style={'float': 'right', 'width': '48%'}, id="monster-column"),
    
    # Button and Stored Values
    html.Div([
        html.Button("Simulate Fight", id="sim-fight-button"),
        html.Label("        Number of Rounds: "),
        dcc.Input(id="n-rounds", type="number", value=100),
        html.Label("", id="output-rounds")
    ], style={'clear': 'both'}),
    html.Div([
        dcc.Graph(figure=fig, id="plot")  # Add the line plot to the layout
    ])
])


@app.callback(
    Output("plot", "figure"),
    Output("output-rounds", "children"),
    Input("player-column", "children"),
    Input("monster-column", "children"),
    Input("sim-fight-button", "n_clicks"),
    Input("n-rounds", "value")
)
def collect_values(players, monster, _, rounds):

    n_sim = 1

    fig = go.Figure() 
    print_val = ""

    if _ is not None:
        cPlayers = []
        for player_id in players:
            player_dict = {}

            player_children = player_id["props"]["children"]
            cPlayers.append(character_from_html(player_children))

        monster = character_from_html(monster)

        max_hp = max(c.hp for c in [*cPlayers, monster])

        histories = []
        for i in range(n_sim):
            
            for i in range(100):

                tot_dmg = 0
                for player in cPlayers:

                    dmg, result = player.roll_attack()
                    
                    if result == -1:
                        player.get_damage(dmg//2)

                    if not monster.roll_defense() and result > 0:
                        tot_dmg += dmg*result

                monster.get_damage(tot_dmg)

                dmg, result = monster.roll_attack()

                if result == -1:
                    monster.get_damage(dmg//2)

                if not cPlayers[0].roll_defense() and result > 0:
                    cPlayers[0].get_damage(dmg)
                else:
                    cPlayers[0].get_damage(0)

        idx_player = np.where(np.array(cPlayers[0].hp_history) == 0)
        idx_monster = np.where(np.array(monster.hp_history) == 0) 

        if idx_player[0].size == 0 and idx_monster[0].size == 0:
            print_val = "         Neither player nor monster reached 0 HP."
        elif idx_player[0].size == 0:
            print_val = "         Monster reached 0 HP first at Round:", idx_monster[0][0]
        elif idx_monster[0].size == 0:
            print_val = "         Player reached 0 HP first at Round:", idx_player[0][0]
        else:
        # Both player and monster reached 0 HP, compare the indices
            if idx_player[0][0] < idx_monster[0][0]:
                print_val = "         Player reached 0 HP first at Round:", idx_player[0][0]
            else:
                print_val = "         Monster reached 0 HP first at Round:", idx_monster[0][0]

        fig.add_trace(
            go.Scatter(x=list(range(len(monster.hp_history))), y=monster.hp_history, line=dict(color='blue'), name="Monster")
        )

        fig.add_trace(
            go.Scatter(x=list(range(len(cPlayers[0].hp_history))), y=cPlayers[0].hp_history, name=f"Player {0}")
        )

        fig.update_yaxes(range=[-5, max_hp+5])
        fig.update_xaxes(range=[0, rounds])

    return fig, print_val


def character_from_html(html_vals):

    char_dict = {}
    # Create a dictionary comprehension to extract values from sliders and inputs
    char_dict.update({
        part["props"]["id"].split("%")[-1]: part["props"]["value"]
        for part in html_vals
        if part["type"] in ["Slider", "Input"]
    })

    hp = char_dict["hp"]
    attack = char_dict["attack"]
    defense = char_dict["defense"]
    dice = {k: v for k, v in char_dict.items() if k not in ["hp", "attack", "defense"]}

    return Character(hp=hp, attack=attack, defense=defense, dice=dice)



def create_player_div(n, n_players):
    return html.Div([
            html.H3(f"Player {n}"),
            
            html.Label(f"Player {n} HP:"),
            dcc.Input(id=f"P%{n}%hp", type="number", placeholder="Enterf P%{n}%HP...", value=100),
            html.Div(),
            html.Label(f"Player {n} Attack Ability:"),
            dcc.Input(id=f"P%{n}%attack", type="number", placeholder="Enterf P%{n}%Attack Ability Thresh...", value=80),
            html.Div(),
            html.Label(f"Player {n} Defense Ability:"),
            dcc.Input(id=f"P%{n}%defense", type="number", placeholder="Enterf P%{n}%Defense Ability Thresh...", value=10),
            html.Div(),

            html.Label("D4:"),
            dcc.Slider(id=f"P%{n}%D4", min=0, max=10, step=1, value=0),
            html.Label("D6:"),
            dcc.Slider(id=f"P%{n}%D6", min=0, max=10, step=1, value=0),
            html.Label("D8:"),
            dcc.Slider(id=f"P%{n}%D8", min=0, max=10, step=1, value=0),
            html.Label("D10:"),
            dcc.Slider(id=f"P%{n}%D10", min=0, max=10, step=1, value=0),
            html.Label("D12:"),
            dcc.Slider(id=f"P%{n}%D12", min=0, max=10, step=1, value=0),
            html.Label("D20:"),
            dcc.Slider(id=f"P%{n}%D20", min=0, max=10, step=1, value=0),
            html.Label("D100:"),
            dcc.Slider(id=f"P%{n}%D100", min=0, max=10, step=1, value=0),
        ], style={'float': 'left', 'width':  f'{100/n_players}%'})


@app.callback(
    Output('player-column', 'children'),
    Input('n-players', 'value')
)
def update_layout(n_players):

    return [create_player_div(i, n_players) for i in range(n_players)]


class Character():

    def __init__(self, hp, attack, defense, dice):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.dice = dice
        self.hp_history = [self.hp]
        self.attack_history = []
        self.result_history = []

    def get_damage(self, damage):

        self.hp = max(0, self.hp-damage)
        self.hp_history.append(self.hp)

    def roll_defense(self):

        return self.roll_d100() < self.defense


    def roll_attack(self):

        roll = self.roll_d100()
        result = self.evaluate_roll(roll, self.attack)
        damage = self.roll_damage()

        self.attack_history.append(damage)
        self.result_history.append(result)

        return damage, result
        
    
    def roll_damage(self):
        return np.sum([np.random.randint(0, int(dice[1:]), count).sum() for dice, count in self.dice.items()])
    
    def roll_d100(self):
        return np.random.randint(1,101,1)[0]

    @staticmethod
    def evaluate_roll(roll, value, only_100=True):

        if roll < (value//10):
            return 2
        
        if only_100:

            if roll == 100:
                return -1
        else:

            if roll > (100-(100 - value)//10):
                return -1
        
        if roll >= value:
            return 0
        
        if roll < value:
            return 1



if __name__ == "__main__":
    app.run_server(debug=True)
