"""
SkillCorner Brand Colors Configuration
"""

# SkillCorner Brand Colors
SKILLCORNER_COLORS = {
    # Primary colors
    "primary": "#00A85D",  # SkillCorner Green
    "primary_dark": "#008A4C",
    "primary_light": "#00C970",

    # Secondary colors
    "secondary": "#1A1A1A",  # Dark Gray
    "secondary_light": "#2D2D2D",

    # Accent colors
    "accent_blue": "#1D73E8",
    "accent_cyan": "#00D8B0",
    "accent_purple": "#8B5CF6",
    "accent_orange": "#FF9500",

    # Status colors
    "success": "#4CAF50",
    "warning": "#FFB300",
    "danger": "#D32F2F",
    "info": "#1D73E8",

    # Neutral colors
    "neutral": "#6E6E6E",
    "neutral_light": "#B0B0B0",
    "neutral_lighter": "#E0E0E0",

    # Background colors
    "background": "#FFFFFF",
    "background_secondary": "#F5F5F5",
    "background_dark": "#1A1A1A",

    # Text colors
    "text": "#212121",
    "text_secondary": "#6E6E6E",
    "text_light": "#FFFFFF",
}

# Chart color palette for different data series
CHART_COLORS = [
    "#00A85D",  # Primary green
    "#1D73E8",  # Blue
    "#FF9500",  # Orange
    "#8B5CF6",  # Purple
    "#00D8B0",  # Cyan
    "#FFB300",  # Yellow
    "#D32F2F",  # Red
    "#4CAF50",  # Light green
]

# Gradient definitions
GRADIENTS = {
    "primary": ["#008A4C", "#00A85D", "#00C970"],
    "performance": ["#D32F2F", "#FFB300", "#00A85D"],
    "heatmap": ["#FFFFFF", "#00D8B0", "#00A85D", "#008A4C"],
}

# Plotly theme configuration
PLOTLY_THEME = {
    "layout": {
        "plot_bgcolor": SKILLCORNER_COLORS["background"],
        "paper_bgcolor": SKILLCORNER_COLORS["background"],
        "font": {
            "family": "Arial, sans-serif",
            "size": 12,
            "color": SKILLCORNER_COLORS["text"]
        },
        "colorway": CHART_COLORS,
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": SKILLCORNER_COLORS["secondary"],
            "font": {
                "color": SKILLCORNER_COLORS["text_light"],
                "size": 12
            }
        }
    }
}
