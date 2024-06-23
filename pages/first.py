from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from data import df
import plotly.graph_objects as go

# Определение макета дашборда
layout = dbc.Container([
    # Заголовок дашборда
    dbc.Row([
         html.Div([
                html.H1("Влияние образа жизни на качество сна", style={"font-weight": "bold", "color": "#211B5F", "font-size": "2.5rem", "margin-top": "0rem", "margin-left": "0rem", "margin-bottom": "-1rem"})
         ])
    ]),

    html.Br(),

    # Элементы управления фильтрацией данных
    dbc.Row ([
        # Чекбокс для выбора пола
        dbc.Col([
            dbc.Label("Пол:"),
            dbc.Checklist(
                options=[
                {"label": "М", "value": "Male"},
                {"label": "Ж", "value": "Female"},
            ],
            value=[],
            id="gender-checklist",
            inline=True,
            style={"color": "#211B5F", "background-color": "#ADA6E4"}
            ),
        ],width=8),

        # Выпадающий список для выбора категории ИМТ
        dbc.Col([
            dbc.Label("Индекс массы тела:"),
            dcc.Dropdown(
                id="bmi-dropdown",
                options=[
                    {"label": "Нормальный вес", "value": "Normal Weight"},
                    {"label": "Избыточный вес", "value": "Obese"},
                    {"label": "Ожирение", "value": "Overweight"}
                ],
                multi=True,
            style={"color": "#211B5F", "background-color": "#E3E1F4", "border-radius": "13px"}
            ), 
        ], className="dash-bootstrap", width=4)
    ]),

    html.Br(),

    # Графики
    dbc.Row ([
        # График рассеяния
        dbc.Col([
            html.H4("Влияние стресса и продолжительности сна на качество сна", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id="scatter-plot", style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=8),

        # Круговая диаграмма
        dbc.Col([
            html.H4("Зависимость сна от активности", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id="pie-chart", style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=4)
    ]),

    html.Br(),

    # Линейный график
    dbc.Row ([
        dbc.Col([
            html.H4("Зависимость качества сна от его продолжительности", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id="line-chart", style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=12)
    ])
])

# Функция обратного вызова для обновления графиков
@callback(
    [Output("scatter-plot", "figure"),
     Output("pie-chart", "figure"),
     Output("line-chart", "figure")],
    [Input("gender-checklist", "value"),
     Input("bmi-dropdown", "value")]
)
def update_graphs(selected_genders, selected_bmis):
    # Фильтрация данных на основе выбранных значений
    filtered_df = df.copy()
    
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    
    if selected_bmis:
        filtered_df = filtered_df[filtered_df['BMI Category'].isin(selected_bmis)]
    
    # Создание графика рассеяния
    profession_translation = {
        "Teacher": "Учитель",
        "Engineer": "Инженер",
        "Lawyer": "Адвокат",
        "Nurse": "Медсестра",
        "Doctor": "Врач",
        "Manager": "Менеджер",
        "Salesperson": "Продавец",
        "Accountant": "Бухгалтер",
        "Sales Representative": "Торговый представитель",
        "Software Engineer": "Программист",
        "Scientist": "Учёный"
    }

    color_palette = [
        '#AA2E62', '#F4A76F', '#FFF3C9', '#3B2FAD', '#C1BAFA',
        '#C699C3', '#F4776F', '#250F37', '#F4D66F', '#B96FF4', '#9B9FFF'
    ]

    color_map = {profession: color for profession, color in zip(filtered_df['Occupation'].unique(), color_palette)}

    grouped_df = filtered_df.groupby(['Occupation', 'Sleep Duration', 'Stress Level'])['Quality of Sleep'].mean().reset_index().round(2)
    grouped_df['Occupation'] = grouped_df['Occupation'].map(profession_translation)
    
    scatter_fig = px.scatter(
        filtered_df.groupby(['Occupation', 'Sleep Duration', 'Stress Level'])['Quality of Sleep'].mean().reset_index().round(2),
        x="Sleep Duration", 
        y="Stress Level", 
        color="Occupation", 
        size="Quality of Sleep",
        color_discrete_map=color_map,
        labels={"Sleep Duration": "Продолжительность сна", "Stress Level": "Уровень стресса", "Occupation": "Профессия", "Quality of Sleep": "Качество сна"},
        category_orders={"Occupation": list(profession_translation.keys())}
    ).update_traces(marker=dict(sizeref=0.30, sizemode='diameter'))

    scatter_fig.for_each_trace(lambda t: t.update(name=profession_translation[t.name]))

    scatter_fig.update_traces(
    hovertemplate="<br>".join([
        "Профессия: %{customdata[0]}",
        "Продолжительность сна: %{x}",
        "Уровень стресса: %{y}",
        "Качество сна: %{marker.size:.2f}"
    ])
    )

    scatter_fig.update_traces(customdata=grouped_df[['Occupation']])

    scatter_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#E3E1F4', height=378)

    # Создание круговой диаграммы
    pie_data = filtered_df.groupby('Quality of Sleep')['Daily Steps'].mean().reset_index().sort_values('Quality of Sleep')

    colors = px.colors.sequential.Purp[:len(pie_data)]

    pie_fig = go.Figure(data=[go.Pie(
        labels=pie_data['Quality of Sleep'],
        values=pie_data['Daily Steps'],
        hole=.3,
        marker=dict(colors=colors),
        texttemplate="%{value:.0f}",
        textposition="inside",
        hovertemplate="<b>%{label}</b><br>Шаги: %{value:.0f}<extra></extra>",
        pull=[0.05] * len(pie_data),
    )])

    pie_fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale=colors,
            showscale=True,
            cmin=pie_data['Quality of Sleep'].min(),
            cmax=pie_data['Quality of Sleep'].max(),
            colorbar=dict( 
                titleside='top',
                thickness=30,
                len=1,
                x=1.1 
            )
        ),
        hoverinfo='none',
        showlegend=False
    ))
    
    pie_fig.update_layout(
    showlegend=False,
    plot_bgcolor='#E3E1F4',
    paper_bgcolor='#E3E1F4',
    height=378,
    margin=dict(r=120, l=50),
    annotations=[dict(
        x=1.36,
        y=1.1,
        xref='paper',
        yref='paper',
        text='Качество сна',
        showarrow=False
    )]
    )

    pie_fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    pie_fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    
    # Создание линейного графика
    line_fig = px.line(
        filtered_df.groupby('Sleep Duration')['Quality of Sleep'].mean().reset_index(), 
        x='Sleep Duration', 
        y='Quality of Sleep',
        labels={"Sleep Duration": "Продолжительность сна", "Quality of Sleep": "Качество сна"}
    )

    line_fig.update_traces(line_color='#826DBA')
    
    line_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#E3E1F4', height=335)

    return scatter_fig, pie_fig, line_fig