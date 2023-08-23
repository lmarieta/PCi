import dash
from dash import dcc
from dash.dependencies import Input, Output
from dash import html
from dash import dash_table
import pandas as pd

# Sample data as a list of dictionaries
data = [
    {'Quoi': 'Pause vendredi matin: où et comment', 'Responsable': '', 'Délai': ''},
    {'Quoi': 'Traitement des déchets à Ballens', 'Responsable': '', 'Délai': ''},
    {'Quoi': '', 'Responsable': '', 'Délai': ''}
] + [{'Quoi': '', 'Responsable': '', 'Délai': ''}] * 20
df = pd.DataFrame(data)


# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of your dashboard
app.layout = html.Div([
    html.H1('Avancée des travaux'),
    dcc.Slider(id='slider', min=0, max=100, step=10, value=50),
    html.Div(id='slider-output'),
    html.H1('Prochain rapport'),
    dcc.Input(id='time-input', type='text', value='12:45'),  # Input component
    html.H1(children='Points en suspens'),
    dash_table.DataTable(
        id='table1',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'border': '1px solid black'},  # Add border for gridlines
        editable=True  # Allow cell editing
    )
])


# Define callback to update the output based on slider value
@app.callback(Output('slider-output', 'children'), [Input('slider', 'value')])
def update_output(value):
    return f"Slider value: {value}%"


# Define callback to update the edited cell
@app.callback(
    dash.dependencies.Output('table1', 'data'),
    [dash.dependencies.Input('table1', 'data_previous')],
    [dash.dependencies.State('table1', 'data')]
)
def update_edited_cell(previous_data, current_data):
    try:
        if previous_data is None:
            raise dash.exceptions.PreventUpdate

        edited_item = next((item for item in current_data if item not in previous_data), None)

        if edited_item is None:
            raise dash.exceptions.PreventUpdate

        changed_columns = [col for col in current_data[0] if edited_item[col] != previous_data[0][col]]

        if not changed_columns:
            raise dash.exceptions.PreventUpdate

        updated_data = current_data.copy()

        # Apply your update logic here based on changed_columns and edited_item

        return updated_data
    except Exception as e:
        print(f"Error in update_edited_cell callback: {e}")
        raise dash.exceptions.PreventUpdate


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
