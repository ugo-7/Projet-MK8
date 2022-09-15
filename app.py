import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np

df = pd.read_excel('Courses_mk8.xlsx')

df = df.fillna(0)

# Mise en place des classement en version plus facile à interpreter
for column in df.iloc[:, 4:]:
        df[column] = df[column].apply(lambda x : (str(column)+" ")*int(x))
df["Places"] = df[1]+df[2]+df[3]+df[4]+df[5]+df[6]+df[7]+df[8]+df[9]+df[10]+df[11]+df[12]
df["Places"] = df["Places"].apply(lambda x : [i for i in x.split(' ')[:-1]])

df = df[['Course', 'Tiers', 'Extension', 'Coupe', 'Places']]

df.loc[:, 'mean']  = df['Places'].apply(lambda row: np.mean(list(map(int, row))) if len(row)>0 else None)
df.loc[:, 'std']   = df['Places'].apply(lambda row: np.std(list(map(int, row))) if len(row)>0 else None)
df.loc[:, 'count'] = df['Places'].apply(lambda row: len(row))

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Courses Mario Kart 8 Deluxe",),
        html.P(children="Analyse des classements sur les courses du jeu MK8DX",),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["Course"],
                        "y": df["mean"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Classement en fonction de la course"},
            },
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
