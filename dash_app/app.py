import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Load the DataFrame
df = pd.read_csv("./assets/merged_df.csv")

# Ensure that the FinBERT_Aggregated_Score is numeric, converting if necessary
df['FinBERT_Aggregated_Score'] = pd.to_numeric(df['FinBERT_Aggregated_Score'], errors='coerce')

# Now you can calculate the mean safely, grouping by sentiment
finbert_scores = df.groupby('FinBERT_Overall_Sentiment')['FinBERT_Aggregated_Score'].mean().reset_index()
finbert_scores.columns = ['Sentiment', 'Score']

# Ensure 'Date' is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Include Font Awesome and Bootstrap in external stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
]

# Create the Dash app instance
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Navbar Component
PROJECT_LOGO = "./assets/logo.png"

navbar = dbc.Navbar(
    dbc.Nav(
        [
            dbc.NavLink(
                html.Img(src=PROJECT_LOGO, style={"width": "100%", "maxHeight": "10vh", "marginTop": "10px"}),
                active="exact",
                style={"backgroundColor": "transparent", "border": "none"}
            ),
            html.Br(),
            dbc.Stack(
                dbc.NavLink(
                    html.Img(src="./assets/home.png", style={"width": "50%", "maxHeight": "10vh"}),
                    href="/",
                    active="exact",
                    style={"backgroundColor": "transparent", "border": "none"}
                ),
            ),
            dbc.NavLink(
                html.Img(src="./assets/user.png", style={"width": "100%", "maxHeight": "10vh", "marginBottom": "10px"}),
                href="/aboutme",
                active="exact",
                style={"backgroundColor": "transparent", "border": "none"}
            ),
        ],
        vertical="md",
        style={
            "textAlign": "center",
            "display": "flex",
            "flexDirection": "column",
            "height": "100%",
            "justifyContent": "space-between",
        },
    ),
    color="dark",
    dark=True,
    style={
        "height": "100vh",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "zIndex": "1000",
        "backgroundColor": "#343a40",
        "padding": "0",
    },
)

# Define the available options
options = [
    {"label": "Article Selection by Date", "value": "article_selection"},
    {"label": "Sentiment Score over Time", "value": "sentiment_score"},
    {"label": "Emotion Scores Distribution", "value": "emotion_distribution"},
    {"label": "Article Count by Month", "value": "article_count"},
    # Add all other options similarly...
]

def create_card(card_number):
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(f"Interactive Feature {card_number}")),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id=f"dropdown-{card_number}",
                        options=options,
                        value=options[0]["value"],  # Default value
                        clearable=False,
                    ),
                    html.Div(id=f"output-{card_number}"),  # Placeholder for the plot
                ]
            ),
        ],
        className="mb-4",
    )

# App layout
app.layout = html.Div(
    style={"display": "flex", "height": "100vh"},
    children=[
        dbc.Col(
            navbar,
            width=2,
            style={"padding": 0},
        ),
        dbc.Col(
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            id="cards-container",
                            children=[create_card(1)],  # Initial card
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                [
                                    html.I(className="fas fa-plus", style={"fontSize": "30px"}),
                                ],
                                id="add-card-icon",
                                className="text-center",
                                style={"cursor": "pointer", "marginTop": "20px"},
                            ),
                            width={"size": 2, "offset": 5},
                        ),
                    ),
                ],
                style={"marginTop": "20px"},
            ),
            width=10,
            style={"marginLeft": "0"},
        ),
    ]
)

# Callback to dynamically add up to 5 cards and hide plus icon after 5 cards
@app.callback(
    [Output("cards-container", "children"),
     Output("add-card-icon", "style")],
    Input("add-card-icon", "n_clicks"),
    State("cards-container", "children"),
)
def add_card(n_clicks, existing_cards):
    if n_clicks is None:
        return existing_cards, {"display": "block"}
    
    num_cards = len(existing_cards) + 1
    if num_cards <= 5:  # Limit to 5 cards
        existing_cards.append(create_card(num_cards))
    
    # Hide the plus icon if 5 or more cards
    plus_icon_style = {"display": "block"} if num_cards < 5 else {"display": "none"}
    
    return existing_cards, plus_icon_style

# Placeholder for dynamic callbacks for each plot based on selected functionality
@app.callback(
    Output("output-1", "children"),
    Input("dropdown-1", "value"),
)
def update_output(value):
    if value == "article_selection":
        return generate_date_selection()
    elif value == "sentiment_score":
        return generate_sentiment_score_plot()
    elif value == "emotion_distribution":
        return generate_emotion_distribution_plot()
    elif value == "article_count":
        return generate_article_count_plot()
    return "Select a feature to see the plot."

# Date selection and article display
def generate_date_selection():
    return html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['Date'].min(),
            end_date=df['Date'].max(),
            display_format='YYYY-MM-DD',
        ),
        html.Button("Submit", id="date-submit", n_clicks=0),
        dcc.Dropdown(id='article-dropdown', placeholder="Select an article", clearable=True),
        html.Div(id='bart-summary-container', style={'marginTop': '20px'}),
        dcc.Dropdown(id='plot-options', options=[
            {'label': 'FinBERT Scores', 'value': 'finbert_scores'},
            # Add more options later...
        ], placeholder="Select a plot option", clearable=True),
        html.Div(id='plot-output', style={'marginTop': '20px'}),
    ])

# Callback for updating article dropdown based on selected date range
@app.callback(
    Output('article-dropdown', 'options'),
    Input('date-submit', 'n_clicks'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
)
def update_article_dropdown(n_clicks, start_date, end_date):
    if n_clicks > 0:
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        return [{'label': title, 'value': index} for index, title in enumerate(filtered_df['Title'])]
    return []

# Callback to display BART summary when an article title is selected
@app.callback(
    Output('bart-summary-container', 'children'),
    Input('article-dropdown', 'value'),
)
def display_bart_summary(selected_index):
    if selected_index is not None:
        bart_summary = df.iloc[selected_index]['Bart_Summary']
        return html.Div([
            html.H5("BART Summary"),
            html.P(bart_summary),
        ])
    return "Select an article to see the BART summary."

# Callback to plot FinBERT scores when an option is selected
@app.callback(
    Output('plot-output', 'children'),
    Input('plot-options', 'value'),
    Input('article-dropdown', 'value'),
)
def update_plot(selected_option, selected_index):
    if selected_option == 'finbert_scores':
        return generate_emotions_plot_for_article(selected_index)
    
    return "Select an option to see the plot."


# def generate_finbert_plot():
#     # Data processing for FinBERT scores
#     print(df.iloc[])
#     finbert_scores = df.groupby('FinBERT_Overall_Sentiment')['FinBERT_Aggregated_Score'].mean().reset_index()
#     finbert_scores.columns = ['Sentiment', 'Score']

#     # Generate bar plot using Plotly Express
#     fig = px.bar(finbert_scores, x='Sentiment', y='Score', title='Average FinBERT Scores by Sentiment')
#     return dcc.Graph(figure=fig)

# Example plot functions (unchanged)

emotions_sum_cols = ["Emotion_Agg_Sum_Anger",
                    "Emotion_Agg_Sum_Disgust",
                    "Emotion_Agg_Sum_Fear",
                    "Emotion_Agg_Sum_Negative",
                    "Emotion_Agg_Sum_Sadness",
                    "Emotion_Agg_Sum_Surprise",
                    "Emotion_Agg_Sum_Positive",
                    "Emotion_Agg_Sum_Anticipation",
                    "Emotion_Agg_Sum_Joy",
                    "Emotion_Agg_Sum_Trust"]

def generate_emotions_plot_for_article(selected_index):
    if selected_index is None:
        return "Select an article to see the plot."

    # Extract the emotion scores for the selected article
    article_emotions_sum = df.iloc[selected_index][emotions_sum_cols]

    # Prepare data for the bar plot
    emotions_data = {
        "Emotion": emotions_sum_cols,
        "Score": article_emotions_sum.values  # Get the scores as a list
    }
    emotions_df = pd.DataFrame(emotions_data)

    # Generate bar plot using Plotly Express
    fig = px.bar(emotions_df,
                 x='Emotion',
                 y='Score',
                 title='Sum of Emotions in Selected Article (Scores Given for Each Sentence Separately)')
    
    return dcc.Graph(figure=fig)


def generate_sentiment_score_plot():    
    # Sample data processing (adjust as needed)
    avg_sentiment = df.groupby(df['Date'].dt.month)['Vader_Compound'].mean().reset_index(name='average_sentiment')

    # Generate a bar plot using Plotly Express
    fig = px.bar(avg_sentiment, x='Date', y='average_sentiment', title='Average Sentiment Score by Month')
    return dcc.Graph(figure=fig)

def generate_emotion_distribution_plot():
    # Sample data processing (adjust as needed)
    emotion_columns = ['Emotion_Agg_Sum_Anger', 'Emotion_Agg_Sum_Sadness', 'Emotion_Agg_Sum_Joy']  # Adjust as necessary
    emotion_data = df[emotion_columns].sum().reset_index(name='Total').rename(columns={'index': 'Emotion'})

    # Generate a pie chart using Plotly Express
    fig = px.pie(emotion_data, values='Total', names='Emotion', title='Emotion Distribution')
    return dcc.Graph(figure=fig)

def generate_article_count_plot():
    # Sample data processing (adjust as needed)
    articles_per_month = df['Date'].dt.to_period('M').value_counts().sort_index().reset_index()
    articles_per_month.columns = ['Month', 'Count']

    # Generate a bar plot using Plotly Express
    fig = px.bar(articles_per_month, x='Month', y='Count', title='Number of Articles per Month')
    return dcc.Graph(figure=fig)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
