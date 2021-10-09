import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import calculations as calc


def initialize_albedo_plot(T_min, T_opt):
    # how does the growth curve of the Daisies look like?
    gw = []
    gb = []
    # amount of intervals to plot
    nt = 20

    t0 = 0
    t1 = 45
    dT = (t1 - t0) / nt
    tempv = [t0 + i * dT for i in range(nt)]

    for t in tempv:
        gw.append(calc.DaisyGrowth(t + 273.15, "w", T_min, T_opt))
        gb.append(calc.DaisyGrowth(t + 273.15, "b", T_min, T_opt))

    albedo_plot = go.Figure()
    albedo_plot.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    albedo_plot.update_xaxes(showgrid=True, zeroline=False)
    albedo_plot.update_yaxes(showgrid=True, zeroline=False)
    albedo_plot.add_trace(go.Scatter(x=tempv, y=gw, name="gw"))
    albedo_plot.add_trace(go.Scatter(x=tempv, y=gb, name="gb"))
    albedo_plot.update_layout(xaxis_title="tempv", yaxis_title="growth")

    albedo_plot.update_layout(xaxis_title="Temp [degC]", yaxis_title="Ratio")
    albedo_plot.update_xaxes(range=[0, t1])
    albedo_plot.update_yaxes(range=[0, 1])
    albedo_plot.layout.title = "Growth curve of daisies"

    return albedo_plot


def update_albedo_plot():
    pass


def constant_flux_plot(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
):
    # First experiment
    F = Fsnom * 1  # solar radiation

    # initial condition state vector
    x0 = {}
    x0["Sw"] = 0.01
    x0["Sb"] = 0.01
    x0["Su"] = 1 - x0["Sw"] - x0["Sb"]
    # note that we also need to initiate the planetary Albedo
    calc.UpdateAlbedo(x0, Albedo)
    # and the temperature
    calc.UpdateTemp(x0, F, rat, em_p, sig, ins_p, Albedo)

    # loop over generations
    ngen = 40

    xgens = []
    xgens.append(x0)
    for g in range(ngen - 1):
        xgens.append(
            calc.NextState(
                xgens[-1],
                F,
                rat,
                em_p,
                sig,
                ins_p,
                Albedo,
                death,
                minarea,
                T_min,
                T_opt,
            )
        )

    gens = [i for i in range(ngen)]

    fig = go.Figure()
    fig.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tw"] - 273.15 for x in xgens],
            name="White daisies temperature",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tb"] - 273.15 for x in xgens],
            name="Black daisies temperature",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens, y=[x["Tp"] - 273.15 for x in xgens], name="Planet temperature"
        )
    )

    fig.update_layout(xaxis_title="Generation number", yaxis_title="Temperature [degC]")
    fig.update_xaxes(range=[0, ngen])
    fig.update_yaxes(range=[0, 50])
    fig.layout.title = "Constant flux temperature with daisy generation"

    #####
    # plot temperature
    # plt.figure(1,figsize=(16,10))
    # plt.plot(gens,[x["Tw"]-273.15 for x in xgens],
    #         label="White daisies temperature")
    # plt.plot(gens,[x["Tb"]-273.15 for x in xgens],
    #         label="Black daisies temperature")
    # plt.plot(gens,[x["Tp"]-273.15 for x in xgens],
    #         label="Planets temperature")
    # plt.xlabel("generation number")
    # plt.ylabel("Degs C")
    # plt.title("Temperature with generation")
    # plt.legend()

    # #plot surface areas
    # plt.figure(2,figsize=(16,10))
    # plt.plot(gens,[x["Sw"] for x in xgens],
    #         label="White daisies area")
    # plt.plot(gens,[x["Sb"] for x in xgens],
    #         label="Black daisies area")
    # plt.plot(gens,[x["Su"] for x in xgens],
    #         label="Uninhabitated area")
    # plt.xlabel("generation number")
    # plt.ylabel("fractional area")
    # plt.title("surface area with generation")
    # plt.legend()
    return fig
