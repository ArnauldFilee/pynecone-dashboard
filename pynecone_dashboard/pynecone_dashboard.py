"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

import pandas as pd
import plotly.graph_objects as go
import pynecone as pc

from pcconfig import config

"""DATAS TO TEST"""
class Data(pc.Base):
    name : str
    value : list[int]


DATA_BAR_1 =[
    Data(name="Revenue Service", value=[0,100]),
    Data(name="Revenue License", value=[100,120]),
    Data(name="Costs Azure", value=[70, 120]),
    Data(name="Costs human", value=[30, 70]),
    Data(name="Current Margin", value=[0, 30]),
]
DATA_BAR_2 =[
    Data(name="Revenue Service", value=[0,100]),
    Data(name="Revenue License", value=[100,120]),
]
DATA_CORR = {
    "Solution definition": [0, 3],
    "Market maturity": [2, 3],
    "Outside in view": [1, 3],
}

_ACCORDION_PARAMS_ORIGIN = [
    {"title": "Project 1", "step": "1", "country": "Belgium", "owner": "John Doe", "created": "2021-01-01", "datas": DATA_BAR_1},
    {"title": "Project 2", "step": "3", "country": "France", "owner": "Delaware", "created": "2022-01-01", "datas": DATA_BAR_2},
    {"title": "Project 3", "step": "2", "country": "Germany", "owner": "BNP", "created": "2023-01-01", "datas": DATA_BAR_1},
    {"title": "Project 4", "step": "2", "country": "Belgium", "owner": "John Doe", "created": "2021-01-01", "datas": DATA_BAR_2},
    {"title": "Project 5", "step": "1", "country": "France", "owner": "Delaware", "created": "2022-01-01", "datas": DATA_BAR_1},
    {"title": "Project 6", "step": "3", "country": "Germany", "owner": "BNP", "created": "2023-01-01", "datas": DATA_BAR_2},
]

"""SETUP OPTIONS SELECT"""
OPTIONS_PHASES = list(set(["Phase "+invest["step"] for invest in _ACCORDION_PARAMS_ORIGIN]))
OPTIONS_PHASES.sort()
OPTIONS_COUNTRIES = list(set([invest["country"] for invest in _ACCORDION_PARAMS_ORIGIN]))
OPTIONS_COUNTRIES.sort()

"""SETUP CUSTOM VAR"""

class Item(pc.Base):
    title : str
    step : str
    country : str
    owner : str
    created : str
    datas : list[Data]


"""STATE SETUP"""
class State(pc.State):
    """The app state."""
    pass

class FilterState(State):
    option_phase : str = "all"
    option_country : str = "all"
    value_mrl : list = [0, 5]
    value_trl : list = [0, 5]
    item : Item = Item(**_ACCORDION_PARAMS_ORIGIN[0])
    @pc.var
    def get_items(self) -> list[Item]:
        if self.option_phase in OPTIONS_PHASES:
            items = [Item(**invest) for invest in _ACCORDION_PARAMS_ORIGIN if invest["step"] == self.option_phase.split(" ")[-1]]
        else:
            items = [Item(**invest) for invest in _ACCORDION_PARAMS_ORIGIN]
        
        if self.option_country in OPTIONS_COUNTRIES:
            items = [item for item in items if item.country == self.option_country]
        
        return items
    
    """
    Get_only the first item of the list to display the bar chart
    Because not yet possible to adapt the chart to the number of items.
    -> for the 3 functions below
    """
    @pc.var
    def get_bar_fig(self) -> go.Figure:
        fig = go.Figure()
        if self.get_items:
            datas = self.get_items[0].datas
            for data in datas:
                fig.add_trace(go.Bar(x=[data.name], y=[data.value[1]-data.value[0]],base=data.value[0]))
        return fig
    
    @pc.var
    def get_correlation_fig(self) -> go.Figure:
        fig = go.Figure()
        datas = DATA_CORR
        df = pd.DataFrame(datas)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df.iloc[0],
            theta=df.columns,
            fill='toself',
            name='Project 1'
        ))
        fig.add_trace(go.Scatterpolar(
            r=df.iloc[1],
            theta=df.columns,
            fill='toself',
            name='Project 2'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[self.value_mrl[0], self.value_mrl[1]]
                )),
            showlegend=True
        )
        return fig
    
    @pc.var
    def get_correlation_fig2(self) -> go.Figure:
        fig = go.Figure()
        datas = DATA_CORR
        df = pd.DataFrame(datas)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df.iloc[0],
            theta=df.columns,
            fill='toself',
            name='Project 1'
        ))
        fig.add_trace(go.Scatterpolar(
            r=df.iloc[1],
            theta=df.columns,
            fill='toself',
            name='Project 2'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[self.value_trl[0], self.value_trl[1]]
                )),
            width=10,
            showlegend=True
        )
        return fig
    
    """SETTER FOR ITEM (set following the click on the accordion)"""
    def setter_item(self, item : Item):
        self.item = item

    """Test to get the bar chart displaying following the item selected in the accordion"""
    # @pc.var
    # def get_bar_fig(self)-> go.Figure:
    #     if self.item :
    #         fig = go.Figure()
    #         datas = self.item.datas
    #         for key in datas:
    #                 fig.add_trace(go.Bar(x=[key], y=[datas[key][1]-datas[key][0]],base=datas[key][0]))
    #         return fig
        



        
"""SETUP FILTERS"""
def header() -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.image(src="/bulb.png", height="50px"),
                pc.flex(
                    pc.heading("ip hub", size="md"),
                    pc.heading("By Delaware", size="sm"),
                    direction="column"
                ),
                align_items="center",
            ),
            pc.heading("ip investment dashboard", size="lg"),
            pc.heading(""),
            justify="space-between",
            padding = "10px",
        ),
        pc.hstack(
            pc.hstack(
                pc.image(src="/filter.png", width="auto", height="30px"),
                pc.select(OPTIONS_PHASES, placeholder="Phases (all)", on_change= FilterState.set_option_phase),
            ),
            pc.hstack(
                pc.text("MRL"),
                pc.vstack(
                    pc.text(FilterState.value_mrl[0] + " - " + FilterState.value_mrl[1]),
                    pc.range_slider(on_change=FilterState.set_value_mrl, width="500px", min_=0, max_=5, step=1, value=FilterState.value_mrl),
                ), 
            ),
            pc.hstack(
                pc.text("TRL"),
                pc.vstack(
                    pc.text(FilterState.value_trl[0] + " - " + FilterState.value_trl[1]),
                    pc.range_slider(on_change=FilterState.set_value_trl, width="500px", min_=0, max_=5, step=1, value=FilterState.value_trl),
                ),
            ),
            pc.hstack(
                pc.select(OPTIONS_COUNTRIES, placeholder="Countries (all)", on_change= FilterState.set_option_country),
            ),
            justify="space-between",
            padding = "10px",
        ),
        width="100%",
        bg = "WhiteSmoke"
    )
    
""" SET UP ACCORDION ITEMS"""
def accordion_item(item : Item) -> pc.Component:
    return pc.accordion_item(
        pc.accordion_button(
            pc.center(
                pc.image(src="/icon_box.png", width="auto", height="40px"), 
                pc.heading(item.title, padding="0 0 0 20px"),
            ),
            pc.spacer(),
            pc.image(src='/steps/step_' + item.step + '.png', width="auto", height="40px", padding_right="20px"),
            pc.image(src = "countries/"+item.country+".svg", height="40px"),
            pc.accordion_icon(),
        ),
        pc.accordion_panel(
            pc.flex(
                pc.center(pc.text("Owner: ", as_="strong"), pc.text(item.owner, padding="0 10px 0 10px"), pc.icon(tag="email")),
                pc.spacer(),
                pc.center(pc.text("Created: " + item.created)),
            ),
            pc.hstack(
                pc.vstack(
                    pc.plotly(data = FilterState.get_bar_fig, width="auto"),
                    pc.text(FilterState.item.title),
                    # width="33%",
                ),
                pc.vstack(
                    pc.plotly(data = FilterState.get_correlation_fig, width="auto"),
                    pc.text("MRL"),
                    # width="33%",
                ),
                pc.vstack(
                    pc.plotly(data = FilterState.get_correlation_fig2, width="auto"),
                    pc.text("TRL"),
                    # width="33%",
                ),
            ),
        ),
        on_focus = FilterState.setter_item(item),      
    )

"""SET UP ACCORDION"""
def accordion() -> pc.Component:
    return pc.accordion(
        pc.foreach(FilterState.get_items, accordion_item),
        width="100%",
    )

"""SET UP PAGE"""
def index() -> pc.Component:
    return pc.vstack(
        header(),
        accordion(),
        pc.text(FilterState.item.title),
    )


# Add state and page to the app.
app = pc.App(state = State)
app.add_page(index)
app.compile()
