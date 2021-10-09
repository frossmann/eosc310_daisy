# file app.py

# bastardizing this model for now at https://github.com/strawpants/daisyworld

import dash
from dash import dcc
from dash import html
from dash.development.base_component import Component
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import plotting as plot

es = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=es)

# initial parameter values
sig = 5.670373e-8  # Stefan Boltzmann constant [W m^-2 K^-4]
ins_p = 0.2  # Insulation factor (0...1)
em_p = 1  # Emmissivity of the Planet (optional)
rat = 1 / 4  # ratio of cross section versus surface area of the Planet
Albedo = {
    "none": 0.5,
    "w": 0.75,
    "b": 0.25,
}  # Albedo vector [uninhabitated Planet , White daisies, Black daisies]

## growth optimum Temp of the white daisies
T_opt = {"w": 22.5 + 273.15}  # in Kelvin
T_min = {"w": 273.15 + 5}  # no growth below this temperature
death = {"w": 0.3}  # death rate of White daisies (fraction)

# assume the same growth curve for Black daisies (change if needed)
T_opt["b"] = T_opt["w"]
T_min["b"] = T_min["w"]
death["b"] = death["w"]
minarea = 0.01  # minimum area as a fraction occupied by each species
Fsnom = 3668  # nominal Flux in W/m^2

##############################
albedo_plot = plot.initialize_albedo_plot(T_min, T_opt)
constant_flux_plot = plot.constant_flux_plot(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
)


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    """
            ### EOSC 310: Daisyworld
            
            Explore daisyworld! 
            ----------
            """
                ),
            ],
            style={
                "width": "100%",
                "display": "inline-block",
                "padding": "0 20",
                "vertical-align": "middle",
                "margin-bottom": 30,
                "margin-right": 50,
                "margin-left": 20,
            },
        ),
        html.Div(
            [
                dcc.Graph(figure=albedo_plot),
            ],
            style={"width": "100%", "display": "inline-block"},
        ),
        ###
        html.Div(
            [
                dcc.Markdown(
                    """
                ----------
                Adjust the sliders below to change the albedo of white and black daisies,
                and also the albedo of the planetary surface. 
                """
                ),
            ],
            style={
                "width": "100%",
                "display": "inline-block",
                "padding": "0 20",
                "vertical-align": "middle",
                "margin-bottom": 30,
                "margin-right": 50,
                "margin-left": 20,
            },
        ),
        ###
        html.Div(
            [
                dcc.Markdown(""" White daisy albedo:"""),
                dcc.Slider(
                    id="Aw",
                    min=0.5,
                    max=1,
                    step=0.05,
                    value=Albedo["w"],
                    marks={0.5: "0.5", 1: "1"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
            ],
            style={
                "width": "37%",
                "display": "inline-block",
                "vertical-align": "top",
            },
        ),
        html.Div(
            [
                dcc.Markdown(""" Black daisy albedo: """),
                dcc.Slider(
                    id="Ab",
                    min=0,
                    max=0.5,
                    step=0.05,
                    value=Albedo["b"],
                    marks={0: "0", 0.5: "0.5"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
            ],
            style={"width": "37%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Markdown(""" Background albedo:"""),
                dcc.Slider(
                    id="Ap",
                    min=0,
                    max=1,
                    step=0.05,
                    value=Albedo["none"],
                    marks={0: "0", 1: "1"},
                    tooltip={"always_visible": True, "placement": "topRight"},
                ),
            ],
            style={
                "width": "37%",
                "display": "inline-block",
                "vertical-align": "top",
            },
        ),
        html.Div(
            [
                dcc.Graph(id="constant_flux_plot"),
            ],
            style={"width": "100%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                #### Sources
                
                1. Jacked from [DaisyWorld Jupyter Notebook](https://github.com/strawpants/daisyworld)
                ----------
                """
                ),
            ],
            style={
                "width": "100%",
                "display": "inline-block",
                "padding": "0 20",
                "vertical-align": "middle",
                "margin-bottom": 30,
                "margin-right": 50,
                "margin-left": 20,
            },
        ),
    ],
    style={"width": "1000px"},
)
#################
@app.callback(
    Output(component_id="constant_flux_plot", component_property="figure"),
    Input(component_id="Aw", component_property="value"),
    Input(component_id="Ab", component_property="value"),
    Input(component_id="Ap", component_property="value"),
)
def update_constant_flux_plot(Aw, Ab, Ap):
    Albedo["w"] = Aw
    Albedo["b"] = Ab
    Albedo["none"] = Ap
    return plot.constant_flux_plot(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
    )


if __name__ == "__main__":
    app.run_server(debug=True)