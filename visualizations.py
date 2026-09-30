"""
Visualization utilities for creating charts and graphs (Clay chart theme)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import THRESHOLD

# --- Clay palette ---
CLAY_FONT = "Nunito, DM Sans, sans-serif"
CLAY_TEXT = "#332F3A"
CLAY_MUTED = "#635F69"
CLAY_GRID = "#E9E4F3"
CLAY_ACCENT = "#7C3AED"
CLAY_ACCENT_LIGHT = "#A78BFA"
CLAY_PINK = "#DB2777"
CLAY_SKY = "#0EA5E9"
CLAY_SUCCESS = "#10B981"
CLAY_WARNING = "#F59E0B"
CLAY_DANGER = "#EF4444"
CLAY_LAVENDER = "#C9C2D8"

RISK_COLORS = {"Low": CLAY_SUCCESS, "Medium": CLAY_WARNING, "High": CLAY_DANGER}
PAPER_BG = "rgba(255,255,255,0)"
PLOT_BG = "rgba(255,255,255,0.45)"


def clay_layout(title=None, height=400, show_title=True, top=60):
    """Shared claymorphism layout for every figure."""
    layout = dict(
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font={"color": CLAY_TEXT, "family": CLAY_FONT, "size": 13},
        margin=dict(l=20, r=20, t=top, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font=dict(family=CLAY_FONT, color=CLAY_TEXT, size=13),
            bordercolor=CLAY_ACCENT_LIGHT
        ),
    )
    if title:
        layout["title"] = dict(
            text=f"<b>{title}</b>" if show_title else title,
            font=dict(size=18, color=CLAY_TEXT, family=CLAY_FONT),
            x=0.02, y=0.97
        )
    return layout


def clay_axis(grid=True):
    """Common axis styling: soft rounded, lavender grid, no hard lines."""
    axis = dict(
        showgrid=grid,
        gridcolor=CLAY_GRID,
        zeroline=False,
        showline=False,
        tickfont=dict(color=CLAY_MUTED, family=CLAY_FONT, size=12),
        title_font=dict(color=CLAY_MUTED, family=CLAY_FONT, size=13),
    )
    if not grid:
        axis["showgrid"] = False
    return axis


def create_risk_distribution_chart(result_df):
    """Create interactive risk level distribution chart"""
    risk_counts = result_df['Risk_Level'].value_counts().reindex(['Low', 'Medium', 'High'], fill_value=0)

    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Level Distribution",
        color=risk_counts.index,
        color_discrete_map=RISK_COLORS,
        hole=0.55
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont={'color': '#ffffff', 'size': 14, 'family': CLAY_FONT},
        marker=dict(line=dict(color='#ffffff', width=4))
    )
    fig.update_layout(**clay_layout(height=420), showlegend=True,
                      legend=dict(font=dict(family=CLAY_FONT, color=CLAY_TEXT, size=13),
                                  bgcolor="rgba(255,255,255,0)"))
    return fig


def create_model_comparison_chart():
    """Lollipop chart comparing model accuracies, in clay colours."""
    models_data = {
        'Model': ['XGBoost', 'Decision Tree', 'Linear Regression', 'KNN'],
        'Accuracy': [80.02, 75.76, 73.70, 71.27]
    }
    model_df = pd.DataFrame(models_data).sort_values('Accuracy', ascending=True)

    fig = go.Figure()

    # Lollipop stems
    for _, row in model_df.iterrows():
        color = CLAY_ACCENT if row['Model'] == 'XGBoost' else CLAY_LAVENDER
        width = 4 if row['Model'] == 'XGBoost' else 3
        fig.add_trace(go.Scatter(
            x=[0, row['Accuracy']],
            y=[row['Model'], row['Model']],
            mode='lines',
            line=dict(color=color, width=width),
            hoverinfo='skip',
            showlegend=False
        ))

    # Lollipop heads (rounded)
    colors = [CLAY_ACCENT if m == 'XGBoost' else CLAY_LAVENDER for m in model_df['Model']]

    fig.add_trace(go.Scatter(
        x=model_df['Accuracy'],
        y=model_df['Model'],
        mode='markers+text',
        marker=dict(color=colors, size=34, line=dict(color='white', width=3), symbol='circle'),
        text=[f"{acc:.1f}" for acc in model_df['Accuracy']],
        textposition="middle center",
        textfont=dict(color='white', size=12, family=CLAY_FONT, weight='bold'),
        hoverinfo='x+y',
        name='Accuracy'
    ))

    fig.update_layout(
        **clay_layout(title="🏆 Model Accuracy Leaderboard", height=360, show_title=True),
        xaxis=dict(**clay_axis(True), range=[0, 100], title="Accuracy (%)"),
        yaxis=dict(showgrid=False, showline=False,
                   tickfont=dict(size=14, color=CLAY_TEXT, family=CLAY_FONT, weight='bold')),
        showlegend=False
    )

    xg_data = model_df[model_df['Model'] == 'XGBoost'].iloc[0]
    fig.add_annotation(
        x=xg_data['Accuracy'], y='XGBoost',
        text="★ Selected Model", showarrow=True, arrowhead=2, ax=0, ay=-48,
        font=dict(color=CLAY_ACCENT, size=12, family=CLAY_FONT, weight='bold'),
        bgcolor='rgba(255,255,255,0.92)', bordercolor=CLAY_ACCENT, borderwidth=2, borderpad=6
    )
    return fig


def create_probability_histogram(result_df):
    """Histogram of theft probabilities with clay styling."""
    prob_values = result_df['Theft_Probability_Raw'] * 100
    fig = px.histogram(
        x=prob_values,
        nbins=30,
        title="Theft Probability Distribution",
        labels={'x': 'Theft Probability (%)', 'y': 'Number of Customers'},
        color_discrete_sequence=[CLAY_ACCENT]
    )
    fig.update_traces(marker=dict(line=dict(color='white', width=1.5), cornerradius=8))
    fig.add_vline(x=THRESHOLD * 100, line_dash="dash", line_color=CLAY_DANGER, line_width=3,
                  annotation_text=f"Threshold: {THRESHOLD*100}%",
                  annotation_font_size=12, annotation_font_color=CLAY_DANGER,
                  annotation_font_family=CLAY_FONT)
    fig.update_layout(**clay_layout(height=420),
                      xaxis=dict(**clay_axis(True), title="Theft Probability (%)"),
                      yaxis=dict(**clay_axis(True), title="Number of Customers"))
    return fig


def create_feature_comparison_chart(row_data, feature_importance):
    """Bar chart showing feature importance in clay colours."""
    if not feature_importance:
        return None

    df_imp = pd.DataFrame({
        'Feature': list(feature_importance.keys()),
        'Importance (%)': list(feature_importance.values())
    }).sort_values('Importance (%)', ascending=True)

    fig = px.bar(
        df_imp,
        x='Importance (%)',
        y='Feature',
        orientation='h',
        title="Feature Contribution to Prediction",
        color='Importance (%)',
        color_continuous_scale=['#EDE9FE', CLAY_ACCENT_LIGHT, CLAY_ACCENT, CLAY_PINK],
        labels={'Importance (%)': 'Importance (%)', 'Feature': 'Feature'}
    )
    fig.update_traces(marker=dict(line=dict(color='white', width=2), cornerradius=12))
    fig.update_layout(**clay_layout(height=420), showlegend=False,
                      xaxis=dict(**clay_axis(True), title="Importance (%)"),
                      yaxis=dict(showgrid=False, tickfont=dict(family=CLAY_FONT, color=CLAY_TEXT, size=13)),
                      coloraxis_showscale=False)
    return fig


def create_risk_timeline_chart(result_df):
    """Top 20 highest-risk customers."""
    top_risky = result_df.nlargest(20, 'Risk_Score')

    fig = px.bar(
        top_risky.reset_index(),
        x='Risk_Score',
        y='CONS_NO',
        orientation='h',
        title="Top 20 Highest Risk Customers",
        color='Risk_Score',
        color_continuous_scale=['#FDE68A', CLAY_WARNING, CLAY_PINK, CLAY_DANGER],
        labels={'CONS_NO': 'Customer ID', 'Risk_Score': 'Risk Score'}
    )
    fig.update_traces(marker=dict(line=dict(color='white', width=2), cornerradius=10))
    fig.update_layout(**clay_layout(height=620),
                      yaxis=dict(categoryorder='total ascending', showgrid=False,
                                 tickfont=dict(family=CLAY_FONT, color=CLAY_TEXT, size=12)),
                      xaxis=dict(**clay_axis(True), title="Risk Score"),
                      coloraxis_showscale=False)
    return fig


def create_3d_feature_plot(result_df):
    """3D scatter plot of key features."""
    if len(result_df) < 2:
        return None

    required_cols = ['avg_consumption', 'std_consumption', 'zero_consumption_days', 'Risk_Score']
    available_cols = [col for col in required_cols if col in result_df.columns]

    if len(available_cols) < 3:
        return None

    try:
        plot_df = result_df.reset_index()
        hover_col = None
        if 'CONS_NO' in plot_df.columns:
            hover_col = 'CONS_NO'
        elif plot_df.index.name and plot_df.index.name in plot_df.columns:
            hover_col = plot_df.index.name
        elif len(plot_df) > 0:
            id_cols = [col for col in plot_df.columns if 'id' in col.lower() or 'cons' in col.lower()]
            if id_cols:
                hover_col = id_cols[0]

        fig = px.scatter_3d(
            plot_df,
            x='avg_consumption',
            y='std_consumption',
            z='zero_consumption_days',
            color='Risk_Score',
            size='Risk_Score',
            hover_name=hover_col,
            title="3D Feature Space Visualization",
            color_continuous_scale=['#6EE7B7', CLAY_WARNING, CLAY_PINK, CLAY_DANGER],
            labels={
                'avg_consumption': 'Avg Consumption',
                'std_consumption': 'Std Consumption',
                'zero_consumption_days': 'Zero Days'
            }
        )
        layout = clay_layout(height=620)
        layout['coloraxis_showscale'] = False
        layout['scene'] = dict(
            xaxis=dict(backgroundcolor='rgba(244,241,250,0.6)', gridcolor=CLAY_GRID, color=CLAY_MUTED),
            yaxis=dict(backgroundcolor='rgba(244,241,250,0.6)', gridcolor=CLAY_GRID, color=CLAY_MUTED),
            zaxis=dict(backgroundcolor='rgba(244,241,250,0.6)', gridcolor=CLAY_GRID, color=CLAY_MUTED),
            aspectmode='cube'
        )
        fig.update_layout(**layout)
        return fig
    except Exception:
        return None


def create_risk_gauge_chart(risk_score):
    """Risk score gauge in clay colours."""
    bar_color = CLAY_DANGER if risk_score > 70 else CLAY_WARNING if risk_score > 40 else CLAY_SUCCESS
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 18, 'color': CLAY_TEXT, 'family': CLAY_FONT}},
        delta={'reference': 50, 'font': {'color': CLAY_MUTED, 'family': CLAY_FONT}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': CLAY_MUTED, 'tickfont': {'color': CLAY_MUTED, 'family': CLAY_FONT}},
            'bar': {'color': bar_color},
            'bgcolor': "rgba(255,255,255,0.6)",
            'steps': [
                {'range': [0, 40], 'color': "#D1FAE5"},
                {'range': [40, 70], 'color': "#FEF3C7"},
                {'range': [70, 100], 'color': "#FEE2E2"}
            ],
            'threshold': {
                'line': {'color': CLAY_DANGER, 'width': 5},
                'thickness': 0.85,
                'value': 70
            }
        }
    ))
    fig.update_layout(**clay_layout(height=320, show_title=False, top=34))
    return fig


def create_probability_gauge_chart(prob_raw, threshold):
    """Theft probability gauge in clay colours."""
    bar_color = CLAY_DANGER if prob_raw > threshold else CLAY_SUCCESS
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_raw,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Theft Probability (%)", 'font': {'size': 18, 'color': CLAY_TEXT, 'family': CLAY_FONT}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': CLAY_MUTED, 'tickfont': {'color': CLAY_MUTED, 'family': CLAY_FONT}},
            'bar': {'color': bar_color},
            'bgcolor': "rgba(255,255,255,0.6)",
            'steps': [
                {'range': [0, 30], 'color': "#D1FAE5"},
                {'range': [30, 60], 'color': "#FEF3C7"},
                {'range': [60, 100], 'color': "#FEE2E2"}
            ],
            'threshold': {
                'line': {'color': CLAY_DANGER, 'width': 5},
                'thickness': 0.85,
                'value': threshold
            }
        }
    ))
    fig.update_layout(**clay_layout(height=320, show_title=False, top=34))
    return fig
