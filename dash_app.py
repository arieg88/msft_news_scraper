import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# Load your DataFrame
df = pd.read_csv('final_df.csv')  # Replace with your DataFrame source

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Navbar
navbar = dbc.NavbarSimple(
    brand="Your Project Name",
    brand_href="#",
    color="primary",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Word Cloud", href="/wordcloud")),
        dbc.NavItem(dbc.NavLink("VADER", href="/vader")),
        dbc.NavItem(dbc.NavLink("FinBERT", href="/finbert")),
        dbc.NavItem(dbc.NavLink("Emotions", href="/emotions")),
    ],
)

# Layout for the app
app.layout = dbc.Container(
    [
        navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ],
    fluid=True,
)

# Home Page
def home_page():
    return html.Div([
        html.H1("Welcome to Your Project"),
        html.P("This app allows you to visualize data using various techniques."),
        html.P("Navigate using the navbar to explore different analyses.")
    ])

# Word Cloud Page
def wordcloud_page():
    months = df['original_Month'].unique()
    return html.Div([
        html.H1("Word Cloud Analysis"),
        html.P("Select a month and an article to generate a word cloud."),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in months],
            placeholder="Select a month"
        ),
        dcc.Dropdown(
            id='title-dropdown',
            placeholder="Select an article title"
        ),
        html.Button("Generate Word Cloud", id='wordcloud-button'),
        html.Div(id='wordcloud-output')
    ])

@app.callback(
    Output('title-dropdown', 'options'),
    Input('month-dropdown', 'value')
)
def update_title_dropdown(selected_month):
    if selected_month:
        filtered_df = df[df['original_Month'] == selected_month]
        return [{'label': title, 'value': title} for title in filtered_df['original_Title']]
    return []

@app.callback(
    Output('wordcloud-output', 'children'),
    Input('wordcloud-button', 'n_clicks'),
    Input('title-dropdown', 'value'),
    prevent_initial_call=True
)
def generate_wordcloud(n_clicks, selected_title):
    if selected_title:
        content = df[df['original_Title'] == selected_title]['original_clean_content_no_stopwords'].values[0]
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(content)
        
        # Save the word cloud to a BytesIO object
        img = io.BytesIO()
        wordcloud.to_image().save(img, format='PNG')
        img.seek(0)
        img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
        
        return html.Img(src=f"data:image/png;base64,{img_b64}")

# VADER Page
def vader_page():
    return html.Div([
        html.H1("VADER Sentiment Analysis"),
        html.P("Select a month to see the VADER analysis."),
        dcc.Dropdown(
            id='vader-month-dropdown',
            options=[{'label': month, 'value': month} for month in df['original_Month'].unique()],
            placeholder="Select a month"
        ),
        dcc.Graph(id='vader-graph'),
    ])

@app.callback(
    Output('vader-graph', 'figure'),
    Input('vader-month-dropdown', 'value')
)
def update_vader_graph(selected_month):
    if selected_month:
        filtered_df = df[df['original_Month'] == selected_month]
        # Calculate means of VADER features
        means = filtered_df[['vader_neg', 'vader_neu', 'vader_pos', 'vader_compound']].mean()
        figure = {
            'data': [{'x': means.index, 'y': means.values, 'type': 'bar', 'name': 'VADER'}],
            'layout': {'title': 'Mean VADER Sentiment Scores'}
        }
        return figure
    return {}

# FinBERT Page (similar to VADER)
def finbert_page():
    return html.Div([
        html.H1("FinBERT Sentiment Analysis"),
        html.P("Select a month to see the FinBERT analysis."),
        dcc.Dropdown(
            id='finbert-month-dropdown',
            options=[{'label': month, 'value': month} for month in df['original_Month'].unique()],
            placeholder="Select a month"
        ),
        dcc.Graph(id='finbert-graph'),
    ])

@app.callback(
    Output('finbert-graph', 'figure'),
    Input('finbert-month-dropdown', 'value')
)
def update_finbert_graph(selected_month):
    if selected_month:
        filtered_df = df[df['original_Month'] == selected_month]
        # Calculate means of FinBERT features
        means = filtered_df[['finbert_Negative', 'finbert_Neutral', 'finbert_Positive']].mean()
        figure = {
            'data': [{'x': means.index, 'y': means.values, 'type': 'bar', 'name': 'FinBERT'}],
            'layout': {'title': 'Mean FinBERT Sentiment Scores'}
        }
        return figure
    return {}

# Emotions Page (updated to use a scatter plot)
def emotions_page():
    return html.Div([
        html.H1("Emotions Analysis"),
        html.P("Select a month to see the emotions analysis."),
        dcc.Dropdown(
            id='emotions-month-dropdown',
            options=[{'label': month, 'value': month} for month in df['original_Month'].unique()],
            placeholder="Select a month"
        ),
        dcc.Graph(id='emotions-graph'),
    ])


@app.callback(
    Output('emotions-graph', 'figure'),
    Input('emotions-month-dropdown', 'value')
)
def update_emotions_graph(selected_month):
    if selected_month:
        filtered_df = df[df['original_Month'] == selected_month]
        # Calculate means of emotion features
        means = filtered_df[['emotions_sadness', 'emotions_negative', 'emotions_positive', 
                             'emotions_trust', 'emotions_fear', 'emotions_anticipation', 
                             'emotions_disgust', 'emotions_joy', 'emotions_surprise', 
                             'emotions_anger']].mean()
        
        # Sort the means for better visualization
        means = means.sort_values(ascending=False)
        
        # Define color mapping for each emotion
        color_map = {
            'emotions_sadness': 'blue',
            'emotions_negative': 'grey',
            'emotions_positive': 'green',
            'emotions_trust': 'teal',
            'emotions_fear': 'purple',
            'emotions_anticipation': 'orange',
            'emotions_disgust': 'brown',
            'emotions_joy': 'yellow',
            'emotions_surprise': 'pink',
            'emotions_anger': 'red'
        }

        # Create scatter plot
        figure = {
            'data': [{
                'x': means.index,
                'y': [0] * len(means),  # All points on the same y-axis (horizontal alignment)
                'mode': 'markers',
                'marker': {
                    'size': means.values * 30,  # Adjust size based on value (smaller dots)
                    'color': [color_map[emotion] for emotion in means.index],
                    'sizemode': 'diameter',
                    'line': {'width': 2, 'color': 'black'}
                },
                'text': [f"{emotion}: {value:.2f}" for emotion, value in means.items()],
                'hoverinfo': 'text',
            }],
            'layout': {
                'title': 'Emotion Scores (Scaled by Value)',
                'xaxis': {'title': 'Emotions'},
                'yaxis': {'visible': False},  # Hide the y-axis since we're only using it for alignment
                'height': 500,
                'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
                'plot_bgcolor': 'white'
            }
        }
        return figure
    return {}


# Page Content Routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return home_page()
    elif pathname == '/wordcloud':
        return wordcloud_page()
    elif pathname == '/vader':
        return vader_page()
    elif pathname == '/finbert':
        return finbert_page()
    elif pathname == '/emotions':
        return emotions_page()
    return home_page()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
