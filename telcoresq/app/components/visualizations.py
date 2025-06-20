import plotly.express as px
import pandas as pd
import re

def create_sentiment_pie_chart(df, sentiment_col='sentiment_label'):
    """
    Creates a pie chart of sentiment distribution.
    """
    if sentiment_col not in df.columns:
        return None
    
    sentiment_counts = df[sentiment_col].value_counts()
    fig = px.pie(
        values=sentiment_counts.values, 
        names=sentiment_counts.index, 
        title='Sentiment Distribution',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    return fig 

def parse_themes_to_df(themes_text):
    """
    Parses the raw text output of theme extraction into a DataFrame.
    Assumes themes are listed line by line, potentially with descriptions.
    e.g., "Theme 1: Description" or "- Theme 1"
    """
    if not themes_text:
        return pd.DataFrame(columns=['theme', 'count'])

    # A simple regex to capture theme names, trying to be flexible
    theme_lines = re.findall(r'^(?:-|\*|\d+\.)\s*(.*?)(?::|$)', themes_text, re.MULTILINE)
    
    if not theme_lines:
        # Fallback for simple line splits
        theme_lines = themes_text.strip().split('\n')

    # For this visualization, we assume each mention is a "frequency" of 1
    # A more advanced implementation would count actual occurrences
    theme_counts = pd.Series(theme_lines).value_counts().reset_index()
    theme_counts.columns = ['theme', 'count']
    return theme_counts


def create_theme_frequency_bar_chart(themes_df):
    """
    Creates a bar chart of theme frequencies.
    """
    if themes_df.empty:
        return None
    
    fig = px.bar(
        themes_df, 
        x='count', 
        y='theme', 
        orientation='h',
        title='Theme Frequency',
        labels={'count': 'Frequency', 'theme': 'Theme'}
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig 