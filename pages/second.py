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
                html.H1("Влияние показателей здоровья на качество сна", style={"font-weight": "bold", "color": "#211B5F", "font-size": "2.5rem", "margin-top": "0rem", "margin-left": "0rem", "margin-bottom": "-1rem"})
         ])
    ]),

    html.Br(),

    # Элементы управления фильтрацией данных
    dbc.Row ([
        # Выпадающий список для выбора категории ИМТ
        dbc.Col([
            dbc.Label("Индекс массы тела:"),
            dcc.Dropdown(
                id="bmi-dropdown_2",
                options=[
                    {"label": "Нормальный вес", "value": "Normal Weight"},
                    {"label": "Избыточный вес", "value": "Obese"},
                    {"label": "Ожирение", "value": "Overweight"}
                ],
                multi=True,
                style={"color": "#211B5F", "background-color": "#E3E1F4", "border-radius": "13px"}
            ), 
        ], className="dash-bootstrap", width=6),

        # Выпадающий список для выбора профессии
        dbc.Col([
            dbc.Label("Профессия:"),
            dcc.Dropdown(
                id="profession-dropdown",
                options=[
                    {"label": "Бухгалтер", "value": "Accountant"},
                    {"label": "Врач", "value": "Doctor"},
                    {"label": "Инженер", "value": "Engineer"},
                    {"label": "Адвокат", "value": "Lawyer"},
                    {"label": "Менеджер", "value": "Manager"},
                    {"label": "Медсестра", "value": "Nurse"},
                    {"label": "Торговый представитель", "value": "Sales Representative"},
                    {"label": "Продавец", "value": "Salesperson"},
                    {"label": "Учёный", "value": "Scientist"},
                    {"label": "Программист", "value": "Software Engineer"},
                    {"label": "Учитель", "value": "Teacher"},
                ],
                multi=True,
                style={"color": "#211B5F", "background-color": "#E3E1F4", "border-radius": "13px"}
            ), 
        ], className="dash-bootstrap", width=6)
    ]),

    html.Br(),

    # Графики в первом ряду
    dbc.Row ([
        # График качества сна по полу и возрасту
        dbc.Col([
            html.H4("Зависимость качества сна от пола и возраста", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id='age-gender-chart', style={'border-radius': '50px', 'overflow': 'hidden'})   
        ],width=6),

        # Индикатор уровня стресса
        dbc.Col([
            dcc.Graph(id='stress-indicator', style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=3),

        # Индикатор качества сна
        dbc.Col([
            dcc.Graph(id='sleep-quality-indicator', style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=3)
    ]),

    html.Br(),

    # Графики во втором ряду
    dbc.Row ([
        # Линейный график зависимости давления и продолжительности сна
        dbc.Col([
            html.H4("Взаимосвязь давления и продолжительности сна", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id='line-chart_2', style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=8),

        # Круговая диаграмма распределения нарушений сна
        dbc.Col([
            html.H4("Распределение нарушений сна", style={"text-align": "center", "color": "#211B5F"}),
            dcc.Graph(id='pie-chart_2', style={'border-radius': '50px', 'overflow': 'hidden'})
        ],width=4)
    ])
])

# Функция обратного вызова для обновления графиков
@callback(
    [Output('line-chart_2', 'figure'),
     Output('pie-chart_2', 'figure'),
     Output('stress-indicator', 'figure'),
     Output('sleep-quality-indicator', 'figure'),
     Output('age-gender-chart', 'figure')],
    [Input('bmi-dropdown_2', 'value'),
     Input('profession-dropdown', 'value')]
)
def update_graphs(bmi_categories, occupations):
    # Фильтрация данных на основе выбранных значений
    filtered_df = df.copy()
    
    if bmi_categories:
        filtered_df = filtered_df[filtered_df['BMI Category'].isin(bmi_categories)]
    
    if occupations:
        filtered_df = filtered_df[filtered_df['Occupation'].isin(occupations)]
    
    # Создание линейного графика
    line_fig = px.line(filtered_df.groupby('Blood Pressure')['Sleep Duration'].mean().reset_index(), 
                       x='Blood Pressure', y='Sleep Duration',
                       labels={"Blood Pressure": "Давление", "Sleep Duration": "Продолжительность сна"})
    line_fig.update_traces(line_color='#826DBA')
    line_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#E3E1F4', height=335)
    
    # Создание круговой диаграммы
    sleep_disorder_translation = {
        "Insomnia": "Бессонница",
        "Sleep Apnea": "Апноэ",
        "No": "Отсутствует"
    }

    pie_data = filtered_df['Sleep Disorder'].value_counts().reset_index()
    pie_data['Sleep Disorder'] = pie_data['Sleep Disorder'].map(sleep_disorder_translation)
    pie_fig = go.Figure(data=[go.Pie(
        labels=pie_data['Sleep Disorder'],
        values=pie_data['count'],
        marker=dict(colors=px.colors.sequential.YlOrBr[:len(pie_data)]),
        texttemplate="%{percent:.1%}",
        textposition="inside",
        hovertemplate="<b>%{label}</b><br>Количество: %{value}<extra></extra>",
    )])
    pie_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#E3E1F4', height=335, margin=dict(t=10, b=0, l=20, r=15), legend_title_text="Нарушения сна", legend=dict(y=0.5))
    
    # Создание индикатора уровня стресса
    stress_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=filtered_df['Stress Level'].mean(),
        title={'text': "Уровень стресса", "font": {"color": "#211B5F"}},
         gauge={'axis': {'range': [0, 10], 'tickfont': {"size": 15, "color": "#211B5F"}}, 'bar': {'color': "#F4D66F"}}
    ))
    stress_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#ADA6E4', height=378, margin=dict(t=0, b=0, l=17, r=27))
    
    # Создание индикатора качества сна
    sleep_quality_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=filtered_df['Quality of Sleep'].mean(),
        title={'text': "Качество сна", "font": {"color": "#211B5F"}},
        gauge={'axis': {'range': [0, 10], 'tickfont': {"size": 15, "color": "#211B5F"}}, 'bar': {'color': "#211B5F"}}
    ))
    sleep_quality_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#ADA6E4', height=378, margin=dict(t=0, b=0, l=17, r=27))
    
    # Создание графика качества сна по полу и возрасту
    age_gender_df = filtered_df.groupby(['Age', 'Gender'])['Quality of Sleep'].mean().reset_index()
    age_gender_df['Gender'] = age_gender_df['Gender'].map({"Male": "Мужчины", "Female": "Женщины"})
    age_gender_fig = px.bar(age_gender_df, x="Quality of Sleep", y="Age", orientation="h", color="Gender",
                            labels={"Quality of Sleep": "Качество сна", "Age": "Возраст", "Gender": "Пол"},
                            color_discrete_map={"Мужчины": "#826DBA", "Женщины": "#E8B93F"})
    # Инвертирование значений для мужчин для создания симметричного графика
    for trace in age_gender_fig.data:
        if trace.name == 'Мужчины':
            trace.x = [-x for x in trace.x]
    age_gender_fig.update_layout(plot_bgcolor='#E3E1F4', paper_bgcolor='#E3E1F4', height=378, legend=dict(y=0.5))
    
    return line_fig, pie_fig, stress_fig, sleep_quality_fig, age_gender_fig