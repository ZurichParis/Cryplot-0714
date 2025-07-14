import pandas as pd
import plotly.graph_objects as go

def plotter(df: pd.DataFrame, x: str, y: list[str], title: str):
    fig = go.Figure()

    # Define colors and styles for different traces
    colors = ['#F7931A', '#667eea', '#FF6B6B', '#4ECDC4']  # Bitcoin orange, blue, red, teal
    line_styles = [
        dict(width=3, dash='solid'),      # Main data
        dict(width=2, dash='dot'),        # Prediction
        dict(width=1, dash='dash'),       # Plus bias
        dict(width=1, dash='dash')        # Minus bias
    ]
    
    for i, y_col in enumerate(y):
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y_col],
            mode='lines',
            name=y_col,
            hoverinfo='none', 
            line=dict(width=line_styles[i % len(line_styles)]['width'], 
                     color=colors[i % len(colors)],
                     dash=line_styles[i % len(line_styles)]['dash'])
        ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Segoe UI, Arial, sans-serif", color='#495057'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        hovermode='x unified',
        template='plotly_white',
        xaxis=dict(
            tickformat='%Y-%m-%d',
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            title=dict(text="Date", font=dict(color='#495057'))
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            title=dict(text="Price (USD)", font=dict(color='#495057'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Segoe UI, Arial, sans-serif", color='#495057')
    )

    fig.update_yaxes(
        showspikes=True, 
        spikemode='across', 
        spikesnap='cursor', 
        spikethickness=1,
        spikecolor='rgba(247,147,26,0.6)'
    )
    fig.update_xaxes(
        showspikes=True, 
        spikemode='across', 
        spikesnap='cursor', 
        spikethickness=1,
        spikecolor='rgba(247,147,26,0.6)'
    )

    return fig
