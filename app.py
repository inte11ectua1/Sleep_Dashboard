from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from pages import main, first, second

# Настройка внешних стилей для приложения
external_stylesheets = [dbc.themes.MORPH, 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap', 'https://use.fontawesome.com/releases/v5.15.4/css/all.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# Определение цветовой схемы
DARK = "#211B5F"
LIGHT = "#ADA6E4"
ACCENT = "#E8B93F"

# Стили для боковой панели
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": DARK,
    "color": "#E3E1F4",
    "box-shadow": "2px 0 5px rgba(0,0,0,0.1)",
}

# Стили для основного содержимого
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": "#ADA6E4",
    "color": DARK
}

# Стили для кнопок
BUTTON_STYLE = {
    "width": "100%",
    "text-align": "left",
    "margin-bottom": "10px",
    "color": LIGHT,
    "background-color": "#2B2476",
    "border": "none",
    "transition": "all 0.3s",
    "box-shadow": "0 2px 4px #141135",
    "text-shadow": "0 2px 10px #141135"
}

# Стили для активных кнопок
BUTTON_STYLE_ACTIVE = {
    "background-color": ACCENT,
    "color": "#FFEEB3",
    "box-shadow": "0 4px 8px #141135",
    "text-shadow": "0 2px 12px #A67A09"
}

# Создание боковой панели
sidebar = html.Div(
    [
        html.H2("Страницы", className="display-6", style={"font-weight": "bold", "color": LIGHT, "font-size": "2.6rem", "margin-top": "0rem", "margin-left": "0.7rem", "text-shadow": "0 2px 10px #141135"}),
        html.Div([
            dbc.Button([html.Img(src="/assets/star1.png", style={"width": "24px", "height": "24px", "marginLeft": "0px"}, id="img-home"), " Главная"], href="/", style=BUTTON_STYLE, id="btn-home"),
            dbc.Button([html.Img(src="/assets/sleep1.png", style={"width": "24px", "height": "24px", "marginLeft": "0px"}, id="img-page-1"), " Образ жизни"], href="/page-1", style=BUTTON_STYLE, id="btn-page-1"),
            dbc.Button([html.Img(src="/assets/hp1.png", style={"width": "24px", "height": "24px", "marginLeft": "0px"}, id="img-page-2"), " Здоровье"], href="/page-2", style=BUTTON_STYLE, id="btn-page-2"),
        ],style={"margin-top": "2rem"}),
    ],
    style=SIDEBAR_STYLE,
)

# Создание контейнера для основного содержимого
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Определение макета приложения
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
], style={"font-family": "Roboto, sans-serif", "background-color": LIGHT})

# Callback для обновления стилей кнопок и изображений в зависимости от текущей страницы
@app.callback(
    [Output("btn-home", "style"),
     Output("btn-page-1", "style"),
     Output("btn-page-2", "style"),
     Output("img-home", "src"),
     Output("img-page-1", "src"),
     Output("img-page-2", "src")],
    [Input("url", "pathname")]
)
def update_active_button(pathname):
    btn_styles = [BUTTON_STYLE.copy(), BUTTON_STYLE.copy(), BUTTON_STYLE.copy()]
    img_srcs = ["/assets/star1.png", "/assets/sleep1.png", "/assets/hp1.png"]
    
    if pathname == "/":
        btn_styles[0].update(BUTTON_STYLE_ACTIVE)
        img_srcs[0] = "/assets/star2.png"
    elif pathname == "/page-1":
        btn_styles[1].update(BUTTON_STYLE_ACTIVE)
        img_srcs[1] = "/assets/sleep2.png"
    elif pathname == "/page-2":
        btn_styles[2].update(BUTTON_STYLE_ACTIVE)
        img_srcs[2] = "/assets/hp2.png"
    
    return btn_styles + img_srcs

# Callback для отображения содержимого страницы в зависимости от URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return main.layout
    elif pathname == "/page-1":
        return first.layout
    elif pathname == "/page-2":
        return second.layout
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...", className="lead"),
        ],
        className="p-5 bg-light rounded-3 text-center",
    )

# Запуск сервера приложения
if __name__ == '__main__':
        app.run_server(debug=True)