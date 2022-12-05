import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging
from plotly.subplots import make_subplots
import plotly.express as px
import dash_table
import pickle
import matplotlib.pyplot as plt
from PIL import Image

# Importamos los modelos
model_goles_importado = pickle.load(open("modelo_goles", 'rb'))
model_asistencias_importado = pickle.load(open("modelo_asistencias", 'rb'))
    
# Importamos los datos
players_fifa23 = pd.read_excel("fifa23.xlsx")
datos_modelo_importados = pd.read_excel("datos_modelo.xlsx")
datos_unidos = pd.read_excel("datos_unidos.xlsx")


teams23 = ['Manchester United', 'Manchester City', 'Tottenham Hotspur',
       'Chelsea', 'Liverpool', 'Leicester City', 'Arsenal', 'Everton',
       'Wolverhampton Wanderers', 'Crystal Palace', 'Aston Villa',
       'Leeds United', 'West Ham United', 'Fulham', 'Southampton',
       'Brighton & Hove Albion', 'Newcastle United', 'AFC Bournemouth',
       'Nottingham Forest', 'Brentford']

players_fifa23 =  players_fifa23[players_fifa23['Club'].isin(teams23)]

players = players_fifa23['FullName'].unique()
players.sort()

options_dropdown_players = []
for player in players:
    options_dropdown_players.append({'label': player, 'value': player})
    
    
clubs = players_fifa23['Club'].unique()
clubs.sort()
    
options_dropdown_teams = []
for club in clubs:
    options_dropdown_teams.append({'label': club, 'value': club})
    

posiciones = players_fifa23['ClubPosition'].unique()
posiciones.sort()
    
options_dropdown_posiciones = []
for posicion in posiciones:
    options_dropdown_posiciones.append({'label': posicion, 'value': posicion})    
    

nacionalidades = players_fifa23['Nationality'].unique()
nacionalidades.sort()
    
options_dropdown_nacionalidades = []
for nacionalidad in nacionalidades:
    options_dropdown_nacionalidades.append({'label': nacionalidad, 'value': nacionalidad}) 
    
    
df = players_fifa23[['FullName','Age','Nationality','Overall','Club','ValueEUR','ReleaseClause','WageEUR']]

df_2 = players_fifa23[['FullName','Age','Nationality','Overall','Club','ValueEUR','ReleaseClause','WageEUR','ClubPosition']]

valor_maximo = df_2['ValueEUR'].max()
salario_maximo = df_2['WageEUR'].max()

#variables campo

posiciones_campo = pd.DataFrame()
posiciones_campo['Pos']= ['GK','DF','MF','FW']
posiciones_campo['x']= [None,None,None,None]
posiciones_campo['y']= [None,None,None,None]


app = dash.Dash()

app.layout = html.Div(
    children = [
        html.Div(
            children = [
                html.H1(
                    children = "Prediccion Goles y Asistencias",
                    id = "titulo",
                    style = {
                        "text-align": "centre",
                        "color": "white",
                        "width": "500px", 
                        "display": "inline-block"
                        }
                    ),
                html.P(
                    children = "Por Pablo Ríos y Pedro González",
                    id = "autores",
                    style = {
                        "text-align": "right",
                        "color": "white",
                        "display":"inline-block",
                        "margin-left": "200px"
                        }),
                ],
            style = {
                    "background-image": "url(https://thumbs.dreamstime.com/z/d-illustration-above-view-green-grass-football-play-ground-field-pattern-textured-concept-183620911.jpg)"
                }
            ),
        dcc.Tabs(
            id = "tabs",
            children = [
                dcc.Tab(
                    id = "primer-tab",
                    value = "Descriptivo",
                    label = "Descriptivo"
                    ),
                dcc.Tab(
                    id = "segundo-tab",
                    value = "Jugadores",
                    label = "Jugadores"
                ),
                dcc.Tab(
                    id = "tercer-tab",
                    value = "Predicción",
                    label = "Predicción"
                )   
            ],
        ),
        html.Div(
        id = "resultado-tabulacion"
        )
    ],
    style = {
        }
) 

@app.callback(
    [
        Output("resultado-tabulacion", "children"),
        Input("tabs", "value")
    ]
)
def layout_tabulacion(tab):

    if tab == "Jugadores":
        return [html.Div(
            children = [
                dcc.Dropdown(
                    options = [5,10,20,50],
                    placeholder = "Seleccione el número de jugadores que desea mostrar",
                    id = "Dropdown_Tamaño_tabla",
                    value = 15,
                    style = {
                        "width":"400px"
                        }
                    ),
                dash_table.DataTable(
                    id = "Tabla_general_jugadores",
                    columns = [
                        {'name': 'Nombre', 'id':'FullName','type':'text'},
                        {'name': 'Edad', 'id':'Age','type':'numeric'},
                        {'name': 'Nacionalidad', 'id':'Nationality','type':'text'},
                        {'name': 'Media', 'id':'Overall','type':'numeric'},
                        {'name': 'Equipo', 'id':'Club','type':'text'},
                        {'name': 'Valor del jugador (€)', 'id':'ValueEUR','type':'numeric'},
                        {'name': 'Clausula de recisión', 'id':'ReleaseClause','type':'numeric'},
                        {'name': 'Salario semanal', 'id':'WageEUR','type':'numeric'},
                        {'name': 'Posición', 'id':'ClubPosition','type':'numeric'}
                        ],
                        data=df_2.to_dict('records'),
                        page_size=15,
                        style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    }
                    ),
                dcc.Dropdown(
                    options = options_dropdown_teams,
                    placeholder = "Seleccione uno o varios equipos",
                    id = "Dropdown_Equipos",
                    multi=True,
                    style = {
                        "width":"300px",
                        "display": "inline-block"
                        }
                    ),
                 dcc.Dropdown(
                     options = options_dropdown_posiciones,
                     placeholder = "Seleccione una o varias posiciones",
                     id = "Dropdown_Posiciones",
                     multi=True,
                     style = {
                         "width":"300px",
                         "display": "inline-block"
                         }
                     ),
                 dcc.Dropdown(
                     options = options_dropdown_nacionalidades,
                     placeholder = "Seleccione una o varias nacionalidades",
                     id = "Dropdown_Nacionalidades",
                     multi=True,
                     style = {
                         "width":"300px",
                         "display": "inline-block"
                         }
                     ),
                html.H3(
                    children = "Seleccione un rango para la media",
                    id = 'titulo_media'
                    ),
                dcc.RangeSlider(0,100,1,
                           value = [0,100],
                           id = 'slider_overall'
                           ),
                html.H4(
                    children = "Seleccione rango para el valor del jugador",
                    id = 'titulo_valor_jugador'
                    ),
                dcc.RangeSlider(0,valor_maximo,5000000,
                           value = [0,valor_maximo],
                           id = 'slider_valor'
                           ),
                html.H4(
                    children = "Seleccione un rango de salario semanal",
                    id = 'titulo_salario'
                    ),
                dcc.RangeSlider(0,salario_maximo,10000,
                           value = [0,salario_maximo],
                           id = 'slider_salario'
                           )
                ]
            )]
    elif tab == "Predicción":
       
        return [html.Div(
                children=[
                    html.Div(
                        children = [
                            html.H4(
                                children = "Jugadores"
                                ),
                            html.Div(
                                children = [
                                    dcc.Dropdown(
                                        options = options_dropdown_players,
                                        placeholder = "Seleccione un jugador",
                                        id = "Dropdown_Jugadores",
                                        value = "Kevin De Bruyne")
                                    ]),
                            dcc.Graph(
                                id = "estadisticas_jugador",
                                style = {
                                    "display":"none",
                                    "width": "375px",
                                    "height":"375px"}
                                )
                            ],
                        id = "bloque_izq",
                        style = {
                            }
                        ),
                    html.Div(
                        children = [
                            html.Div(
                                html.H3(
                                    children = "Información del jugador")
                                ),
                            html.Div(
                                children = [
                                    dash_table.DataTable(
                                        id = "tabla_info_extra_jugador",
                                        columns = [
                                            {'name': 'Nombre', 'id':'FullName','type':'text'},
                                            {'name': 'Edad', 'id':'Age','type':'numeric'},
                                            {'name': 'Nacionalidad', 'id':'Nationality','type':'text'},
                                            {'name': 'Media', 'id':'Overall','type':'numeric'},
                                            {'name': 'Equipo', 'id':'Club','type':'text'},
                                            {'name': 'Valor del jugador (€)', 'id':'ValueEUR','type':'numeric'},
                                            {'name': 'Clausula de recisión', 'id':'ReleaseClause','type':'numeric'},
                                            {'name': 'Salario semanal', 'id':'WageEUR','type':'numeric'}
                                            ],
                                        data=df.to_dict('records'),
                                        page_size=1,
                                        style_header={
                                            'backgroundColor': 'rgb(30, 30, 30)',
                                            'color': 'white'
                                            },
                                        style_data={
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white',
                                            "margin-right": "25px"
                                            }),
                                    html.H3(
                                        children = "Predicción"
                                        ),
                                    dash_table.DataTable(
                                        id = "tabla_predicciones",
                                        columns = [
                                            {"name":"Goles","id":"Goles","type":"numeric"},
                                            {"name":"Asistencias","id":"Asistencias","type":"numeric"}
                                            ],
                                        data = 'null',
                                        page_size = 1,
                                        style_header={
                                            'backgroundColor': 'rgb(30, 30, 30)',
                                            'color': 'white'
                                            },
                                        style_data={
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white',
                                            "margin-right": "25px"
                                            })
                                    ])
                            ],
                        id = "bloque_dcha",
                        style = {
                            }
                        )
                    ]
                )]
    
    elif tab == "Descriptivo":
        return [html.Div(
            children = [
                html.Div(
                    children = [
                        html.H4(
                            children = "Selecciona las posiciones de los futbolistas",
                            style = {
                            "font-family":"verdana",
                            "font-size":"150%",
                            }
                            ),
                        
                        dcc.Checklist(
                            options = [    
                                {'label': 'Portero  ', 'value': 'GK'},
                                {'label': 'Defensa  ', 'value': 'DF'},
                                {'label': 'Centrocampista  ', 'value': 'MF'},
                                {'label': 'Delantero  ', 'value': 'FW'},
                            ],value=['FW'],
                            id = "Checklist_posiciones_goles",
                            style = {
                            "font-family":"verdana",
                            }
                            ),
                        
                        html.Div(
                    children = [
                        dcc.Graph(
                            id = "media_posiciones"
                            )
                        ],
                    style = {
                        #"border-radius": "5px",
                        "display":"block",
                        "margin-top": "25px",
                        "margin-right": "25px"
                        })
                        
                     ],              
                    style = {
                        "display":"inline-block",
                        "width":"40%",
                        "vertical-align": "top",
                        "margin-left": "25px"
                        }),
                
                
                 html.Div(
                    children = [
                        dcc.Graph(
                            id = "campo",
                            style = {
                                "display":"block",
                                }
                            ),
                        ],
                    style = {
                        #"border":"2px black solid",
                        "display":"inline-block",
                        "width":"40%",
                        "vertical-align": "bottom",
                        }),                               
                html.Div(
                    children = [
                        dcc.Graph(
                            id = "graf_goles_por_pos",
                            style = {
                                "display":"block"
                                }
                            ),
                        ],
                    style = {
                        "border":"2px black solid",
                        "display":"inline-block",
                        "width":"40%"
                        }),
                
                html.Div(
                    children = [
                        dcc.Graph(
                            id = "graf_asistencias_por_pos",
                            style = {
                                "display":"block"
                                }
                            ),
                        ],
                    style = {
                        "border":"2px black solid",
                        "display":"inline-block",
                        "width":"40%",
                        "margin-left":"50px"
                        }),
                
                html.Div(
                    children = [
                        dcc.Graph(
                            id = "goleadores_por_pos",
                            style = {
                                "display":"block"
                                }
                            ),
                        ],
                    style = {
                        "border":"2px black solid",
                        "display":"inline-block",
                        "width":"40%",
                        "margin-left":"50px"
                        }),
                
                html.Div(
                    children = [
                        dcc.Graph(
                            id = "asistentes_por_pos",
                            style = {
                                "display":"block"
                                }
                            ),
                        ],
                    style = {
                        "border":"2px black solid",
                        "display":"inline-block",
                        "width":"40%",
                        "margin-left":"50px"
                        }),
                ]
            )]
    else:
        return [html.Div(
            children = [
                html.H2(
                    children = "¡Bienvenidos al dashboard interactivo de la Premier League!",
                    style = {
                        "text-align":"center",
                        "margin-top":"50px"
                        }
                    )
                ]
            )]




@app.callback(
    Output("estadisticas_jugador","figure"),
    Output("estadisticas_jugador","style"),
    Input("Dropdown_Jugadores","value")
    )

def estadisticas_jugador(Dropdown_Jugadores_value):
    jugador = players_fifa23[players_fifa23.FullName == Dropdown_Jugadores_value]
    jugador_estadisticas = pd.DataFrame(dict(
        estadisticas=[jugador['PaceTotal'].mean(), jugador['ShootingTotal'].mean(), jugador['PassingTotal'].mean(),\
                      jugador['DribblingTotal'].mean(), jugador['DefendingTotal'].mean(), jugador['PhysicalityTotal'].mean()], 
        nombres=['pace','shooting','passing',
               'dribbling', 'defending', 'physic']))
    fig = px.line_polar(jugador_estadisticas, r='estadisticas', theta='nombres', line_close=True, title = f"Atributos de {Dropdown_Jugadores_value}",markers=True)
    fig.update_traces(fill='toself')
    fig.show()
    
    return(fig,{"display":"block"})

@app.callback(
    Output("tabla_info_extra_jugador","data"),
    Input("Dropdown_Jugadores","value")
    )

def display_stats(Dropdown_Jugadores_value):
    dff = df.copy() 
    
    if Dropdown_Jugadores_value:
        dff = dff[dff['FullName'] == Dropdown_Jugadores_value]
        
    return dff.to_dict('records')

@app.callback(
    Output("tabla_predicciones","data"),
    Input("Dropdown_Jugadores","value")
    )

def predicciones_modelos(jugador):
    fifa23_jugador = datos_modelo_importados[datos_modelo_importados['FullName']==jugador]
    fifa23_jugador = fifa23_jugador.iloc[:,1:] 

    fifa23_jugador.columns = ['overall','pace','shooting','passing','dribbling','defending','physic','attacking_crossing','attacking_finishing','attacking_heading_accuracy','attacking_short_passing','attacking_volleys','skill_dribbling','skill_curve','skill_fk_accuracy','skill_long_passing','skill_ball_control','power_shot_power','power_jumping','power_long_shots','mentality_positioning','mentality_vision','mentality_aggression','mentality_penalties']
    goles = np.round(model_goles_importado.predict(fifa23_jugador))
    asistencias = np.round(model_asistencias_importado.predict(fifa23_jugador))
    
    predicciones_finales_jugador = pd.DataFrame(data=goles, columns=['Goles'])
    asistencias_df = pd.DataFrame(data=asistencias, columns=['Asistencias'])

    predicciones_finales_jugador['Asistencias'] = asistencias_df['Asistencias']
    
    return predicciones_finales_jugador.to_dict('records')

@app.callback(
    Output("Tabla_general_jugadores","data"),
    Output("Tabla_general_jugadores","page_size"),
    Input("Dropdown_Tamaño_tabla","value"),
    Input("Dropdown_Equipos","value"),
    Input("slider_overall","value"),
    Input("slider_valor","value"),
    Input("slider_salario","value"),
    Input("Dropdown_Posiciones","value"),
    Input("Dropdown_Nacionalidades","value")
    )

def tabla_jugadores(tamaño_tabla_value, equipos_value, overall_value, valor_value, salario_value, posicion_value, nacionalidad_value):
    dff_2 = df_2.copy()
    print(tamaño_tabla_value)
    
    if equipos_value:
        dff_2 = dff_2[dff_2['Club'].isin(equipos_value)]
    
    if posicion_value:
        dff_2 = dff_2[dff_2['ClubPosition'].isin(posicion_value)]
        
    if nacionalidad_value:
        dff_2 = dff_2[dff_2['Nationality'].isin(nacionalidad_value)]
        
    dff_2 = dff_2[(dff_2['Overall']>=overall_value[0])&(dff_2['Overall']<=overall_value[1])]
    dff_2 = dff_2[(dff_2['ValueEUR']>=valor_value[0])&(dff_2['ValueEUR']<=valor_value[1])]
    dff_2 = dff_2[(dff_2['WageEUR']>=salario_value[0])&(dff_2['WageEUR']<=salario_value[1])]

    
    return dff_2.to_dict('records'), tamaño_tabla_value

@app.callback(
    Output("graf_goles_por_pos","figure"),
    Output("graf_goles_por_pos","style"),
    Input("Checklist_posiciones_goles","value")
    )

def grafica_goles(posicion):
    datos = datos_unidos[datos_unidos['Pos_corta'].isin(posicion)]
    print(datos)
    fig = px.histogram(datos, x="Gls",labels = {"reading score": "Goles"}, title='Distribución de goles por posición',
                       color = 'Pos_corta',nbins = 30) # Si agregamos histnorm='probability density' normalizamos el resultado

    #Agregar espacios entre barras
    fig.update_layout(bargap = 0.1)
    
    return(fig,{"display":"block"})

@app.callback(
    Output("graf_asistencias_por_pos","figure"),
    Output("graf_asistencias_por_pos","style"),
    Input("Checklist_posiciones_goles","value")
    )

def grafica_asistencias(posicion):
    datos = datos_unidos[datos_unidos['Pos_corta'].isin(posicion)]
    print(datos)
    fig = px.histogram(datos, x="Ast",labels = {"reading score": "Asistencias"}, title='Distribución de asistencias por posición',
                       color = 'Pos_corta',nbins = 30) # Si agregamos histnorm='probability density' normalizamos el resultado

    #Agregar espacios entre barras
    fig.update_layout(bargap = 0.1)
    
    return(fig,{"display":"block"})

## PABLO

@app.callback(
    Output("goleadores_por_pos","figure"),
    Output("goleadores_por_pos","style"),
    Input("Checklist_posiciones_goles","value")
    )

def grafica_maximos_goleadores(posicion):
    datos = datos_unidos[datos_unidos['Pos_corta'].isin(posicion)]
    #max_goleadores = datos.loc[datos['Gls'] > 7]
    max_goleadores = datos.sort_values(by=['Gls'],ascending=True)
    max_goleadores = max_goleadores.tail(15)
    
     
    fig = px.bar(max_goleadores, x="Gls", y="Player", orientation='h',labels = {"Gls": "Goles"}, title='Máximos goleadores según la posición',color='Pos_corta')
    
    fig.update_layout(yaxis_categoryorder = 'total ascending')

    fig.update_layout(bargap = 0.1)
    
    return(fig,{"display":"block"})
    
    
    
@app.callback(
    Output("asistentes_por_pos","figure"),
    Output("asistentes_por_pos","style"),
    Input("Checklist_posiciones_goles","value")
    )

def grafica_maximos_asistentes(posicion):
    datos = datos_unidos[datos_unidos['Pos_corta'].isin(posicion)]
    #max_asistentes = datos.loc[datos['Gls'] > 7]
    max_asistentes = datos.sort_values(by=['Ast'],ascending=True)
    max_asistentes = max_asistentes.tail(15)
    
     
    fig = px.bar(max_asistentes, x="Ast", y="Player", orientation='h',labels = {"Ast": "Asistencias"}, title='Máximos asistentes según la posición',color='Pos_corta')
    
    fig.update_layout(yaxis_categoryorder = 'total ascending')

    fig.update_layout(bargap = 0.1)
    
    return(fig,{"display":"block"})




@app.callback(
    Output("campo","figure"),
    Output("campo","style"),
    Input("Checklist_posiciones_goles","value")
    )

def grafica_campo(posicion):
    
    global x_p, y_p
    
    if 'GK' in posicion :
        posiciones_campo.loc[0,"x"] = 8
        posiciones_campo.loc[0,"y"]  = 47.5
        
    else:
        posiciones_campo.loc[0,"x"] = None
        posiciones_campo.loc[0,"y"] = None    
    
    if 'DF' in posicion :
        posiciones_campo.loc[1,"x"] = 30
        posiciones_campo.loc[1,"y"]= 47.5
        
    else:
        posiciones_campo.loc[1,"x"] = None
        posiciones_campo.loc[1,"y"] = None 
        
    if 'MF' in posicion :
        posiciones_campo.loc[2,"x"]  = 67
        posiciones_campo.loc[2,"y"] = 47.5
        
    else:
        posiciones_campo.loc[2,"x"] = None
        posiciones_campo.loc[2,"y"] = None 
        
    if 'FW' in posicion :
        posiciones_campo.loc[3,"x"] = 120
        posiciones_campo.loc[3,"y"] = 47.5
        
    else:
        posiciones_campo.loc[3,"x"] = None
        posiciones_campo.loc[3,"y"] = None 

     
    img = Image.open('./campo.png')
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=posiciones_campo['x'],
                   y=posiciones_campo['y'],
                    mode='markers',
                    marker=dict(size=20,
                    color='red'),
    ))

    # axis hide、yaxis reversed
    fig.update_layout(
        autosize=False,
        width=600,
        height=400,
        xaxis=dict(visible=False,range=[-20, 150]),
        yaxis=dict(visible=False,range=[105, -10])
    )

    # background image add
    fig.add_layout_image(
        dict(source=img,
             xref='x',
             yref='y',
             x=0,
             y=0,
             sizex=135,
             sizey=95,
             sizing='stretch',
             opacity=0.9,
             layer='below')
    )

    layout = go.Layout(
      margin=go.layout.Margin(
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=0  #top margin
            )
        )

    # Set templates
    fig.update_layout(layout)  
    
    print(posicion)
    print(posiciones_campo['x'])
    print(posiciones_campo['y'])
        
    
    return(fig,{"display":"block"})


@app.callback(
    Output("media_posiciones","figure"),
    Output("media_posiciones","style"),
    Input("Checklist_posiciones_goles","value")
    )

def media_por_pos(checklist):
    defensas = datos_unidos[datos_unidos.Pos == 'DF']
    centrocampistas = datos_unidos[datos_unidos.Pos == 'MF']
    delanteros = datos_unidos[datos_unidos.Pos == 'FW']

    nombres=['pace','shooting','passing','dribbling', 'defending', 'physic']


    medias_def=[defensas['pace'].mean(), defensas['shooting'].mean(),\
                 defensas['passing'].mean(), defensas['dribbling'].mean(),\
                 defensas['defending'].mean(), defensas['physic'].mean()]

    medias_cen=[centrocampistas['pace'].mean(), centrocampistas['shooting'].mean(),\
                 centrocampistas['passing'].mean(), centrocampistas['dribbling'].mean(),\
                 centrocampistas['defending'].mean(), centrocampistas['physic'].mean()]

    medias_del=[delanteros['pace'].mean(), delanteros['shooting'].mean(),\
                 delanteros['passing'].mean(), delanteros['dribbling'].mean(),\
                 delanteros['defending'].mean(), delanteros['physic'].mean()]


    fig = go.Figure()
    
    if 'DF' in checklist:
        fig.add_trace(
            go.Scatterpolar(
            r=medias_def,
            theta=nombres,
            fill='toself',
            name="Defensas"
        ))

    if 'MF' in checklist:
        fig.add_trace(
            go.Scatterpolar(
            r=medias_cen,
            theta=nombres,
            fill='toself',
            name="Mediocentros"
        ))

    if 'FW' in checklist:
        fig.add_trace(
            go.Scatterpolar(
            r=medias_del,
            theta=nombres,
            fill='toself',
            name="Delanteros"
        ))
        

    return (fig,{"display":"block"})




if __name__ == '__main__':
    app.run_server()