"""
Phase 3: Interactive Chart Components using Plotly
SkillCorner-themed visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from ...analytics.colors import SKILLCORNER_COLORS, CHART_COLORS, PLOTLY_THEME


def create_metric_gauge(value: float, title: str, max_value: float = 100, format_string: str = '.1f') -> go.Figure:
    """
    Create a gauge chart for displaying a single metric

    Args:
        value: Current value
        title: Chart title
        max_value: Maximum value for the gauge
        format_string: Format string for the value

    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 16, 'color': SKILLCORNER_COLORS['text']}},
        number={'font': {'size': 32, 'color': SKILLCORNER_COLORS['primary']}, 'suffix': '%' if max_value == 100 else ''},
        gauge={
            'axis': {'range': [0, max_value], 'tickcolor': SKILLCORNER_COLORS['neutral']},
            'bar': {'color': SKILLCORNER_COLORS['primary']},
            'bgcolor': SKILLCORNER_COLORS['background_secondary'],
            'borderwidth': 2,
            'bordercolor': SKILLCORNER_COLORS['neutral_lighter'],
            'steps': [
                {'range': [0, max_value * 0.33], 'color': SKILLCORNER_COLORS['danger']},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': SKILLCORNER_COLORS['warning']},
                {'range': [max_value * 0.66, max_value], 'color': SKILLCORNER_COLORS['success']}
            ],
            'threshold': {
                'line': {'color': SKILLCORNER_COLORS['text'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']}
    )

    return fig


def create_bar_chart(data: Dict[str, float], title: str, orientation: str = 'v') -> go.Figure:
    """
    Create a bar chart

    Args:
        data: Dictionary of labels and values
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal

    Returns:
        Plotly figure
    """
    if orientation == 'v':
        fig = go.Figure(go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            marker_color=SKILLCORNER_COLORS['primary'],
            text=[f"{v:.1f}" for v in data.values()],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
        ))
    else:
        fig = go.Figure(go.Bar(
            y=list(data.keys()),
            x=list(data.values()),
            orientation='h',
            marker_color=SKILLCORNER_COLORS['primary'],
            text=[f"{v:.1f}" for v in data.values()],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Value: %{x:.2f}<extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor=SKILLCORNER_COLORS['background'],
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=400,
        showlegend=False,
        xaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter']},
        yaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter']}
    )

    return fig


def create_line_chart(data: pd.DataFrame, x_col: str, y_cols: List[str], title: str) -> go.Figure:
    """
    Create a line chart for time series data

    Args:
        data: DataFrame with data
        x_col: Column name for x-axis
        y_cols: List of column names for y-axis
        title: Chart title

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[col],
            mode='lines+markers',
            name=col,
            line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=3),
            marker=dict(size=8),
            hovertemplate=f'<b>{col}</b><br>Time: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor=SKILLCORNER_COLORS['background'],
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=400,
        xaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter'], 'title': x_col},
        yaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter'], 'title': 'Value'},
        legend={'bgcolor': SKILLCORNER_COLORS['background_secondary']},
        hovermode='x unified'
    )

    return fig


def create_radar_chart(categories: List[str], values: List[float], title: str, max_value: float = 100) -> go.Figure:
    """
    Create a radar chart for multi-dimensional metrics

    Args:
        categories: List of category names
        values: List of values for each category
        title: Chart title
        max_value: Maximum value for scaling

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f"rgba(0, 168, 93, 0.3)",  # SkillCorner green with transparency
        line=dict(color=SKILLCORNER_COLORS['primary'], width=3),
        marker=dict(size=8, color=SKILLCORNER_COLORS['primary']),
        hovertemplate='<b>%{theta}</b><br>Value: %{r:.2f}<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value],
                gridcolor=SKILLCORNER_COLORS['neutral_lighter'],
                tickfont={'color': SKILLCORNER_COLORS['text']}
            ),
            angularaxis=dict(
                gridcolor=SKILLCORNER_COLORS['neutral_lighter'],
                tickfont={'color': SKILLCORNER_COLORS['text'], 'size': 12}
            ),
            bgcolor=SKILLCORNER_COLORS['background']
        ),
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=500,
        showlegend=False
    )

    return fig


def create_heatmap(data: pd.DataFrame, title: str) -> go.Figure:
    """
    Create a heatmap

    Args:
        data: DataFrame with 2D data
        title: Chart title

    Returns:
        Plotly figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=[
            [0, SKILLCORNER_COLORS['background']],
            [0.5, SKILLCORNER_COLORS['accent_cyan']],
            [1, SKILLCORNER_COLORS['primary']]
        ],
        hovertemplate='Row: %{y}<br>Col: %{x}<br>Value: %{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor=SKILLCORNER_COLORS['background'],
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=500,
        xaxis={'tickangle': -45}
    )

    return fig


def create_passing_network(data: List[Dict[str, Any]], title: str = "Passing Network") -> go.Figure:
    """
    Create a passing network visualization

    Args:
        data: List of passing combinations with 'passer', 'receiver', and 'passes'
        title: Chart title

    Returns:
        Plotly figure
    """
    if not data:
        # Return empty figure
        fig = go.Figure()
        fig.update_layout(
            title=title,
            annotations=[{
                'text': 'No passing data available',
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.5,
                'y': 0.5,
                'showarrow': False,
                'font': {'size': 16, 'color': SKILLCORNER_COLORS['neutral']}
            }]
        )
        return fig

    # Create node and edge lists
    nodes = set()
    for combo in data[:10]:  # Top 10 combinations
        nodes.add(combo['passer'])
        nodes.add(combo['receiver'])

    node_list = list(nodes)

    # Create edges
    edges_x = []
    edges_y = []
    edge_text = []

    # Simple circular layout
    n = len(node_list)
    angles = [2 * np.pi * i / n for i in range(n)]
    node_x = [np.cos(angle) for angle in angles]
    node_y = [np.sin(angle) for angle in angles]

    node_positions = {node: (x, y) for node, x, y in zip(node_list, node_x, node_y)}

    for combo in data[:10]:
        passer = combo['passer']
        receiver = combo['receiver']

        if passer in node_positions and receiver in node_positions:
            x0, y0 = node_positions[passer]
            x1, y1 = node_positions[receiver]

            edges_x.extend([x0, x1, None])
            edges_y.extend([y0, y1, None])
            edge_text.append(f"{passer} → {receiver}: {combo['passes']} passes")

    # Create figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(
        x=edges_x,
        y=edges_y,
        mode='lines',
        line=dict(color=SKILLCORNER_COLORS['neutral'], width=2),
        hoverinfo='none',
        showlegend=False
    ))

    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=30,
            color=SKILLCORNER_COLORS['primary'],
            line=dict(color=SKILLCORNER_COLORS['secondary'], width=2)
        ),
        text=node_list,
        textposition='middle center',
        textfont=dict(size=10, color=SKILLCORNER_COLORS['text_light']),
        hovertemplate='<b>%{text}</b><extra></extra>',
        showlegend=False
    ))

    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor=SKILLCORNER_COLORS['background'],
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=600,
        showlegend=False,
        xaxis={'visible': False},
        yaxis={'visible': False},
        hovermode='closest'
    )

    return fig


def create_comparison_chart(categories: List[str], team_values: List[float], opponent_values: List[float], title: str) -> go.Figure:
    """
    Create a comparison chart between team and opponent

    Args:
        categories: List of category names
        team_values: List of team values
        opponent_values: List of opponent values
        title: Chart title

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Team',
        x=categories,
        y=team_values,
        marker_color=SKILLCORNER_COLORS['primary'],
        text=[f"{v:.1f}" for v in team_values],
        textposition='outside',
        hovertemplate='<b>Team</b><br>%{x}: %{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Opponent',
        x=categories,
        y=opponent_values,
        marker_color=SKILLCORNER_COLORS['danger'],
        text=[f"{v:.1f}" for v in opponent_values],
        textposition='outside',
        hovertemplate='<b>Opponent</b><br>%{x}: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': SKILLCORNER_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        barmode='group',
        plot_bgcolor=SKILLCORNER_COLORS['background'],
        paper_bgcolor=SKILLCORNER_COLORS['background'],
        font={'color': SKILLCORNER_COLORS['text']},
        height=400,
        xaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter']},
        yaxis={'gridcolor': SKILLCORNER_COLORS['neutral_lighter']},
        legend={'bgcolor': SKILLCORNER_COLORS['background_secondary']}
    )

    return fig
