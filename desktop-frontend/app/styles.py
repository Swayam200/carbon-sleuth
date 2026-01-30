"""
Centralized stylesheet definitions for the Desktop App.
All QSS (Qt Style Sheets) strings are defined here for maintainability.

Color Palette (Industrial Dark Theme):
- Background: #0b0c10 (Dark Navy)
- Card BG: rgba(31, 40, 51, 0.6) (Metallic)
- Primary Text: #66fcf1 (Neon Cyan)
- Secondary Text: #c5c6c7 (Silver)
- Muted Text: #8b949e (Gray)
- Accent: #45a29e (Teal)
- Success: #20fc8f (Neon Green)
- Danger: #fc2044 (Neon Red)
- Warning: #e0a800 (Amber)
"""

# --- Main Window & Layout ---
MAIN_WINDOW_STYLE = """
    background-color: #0b0c10;
    color: #c5c6c7;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
"""

SIDEBAR_STYLE = """
    QWidget {
        background-color: #0b0c10;
        border-right: 1px solid #1f2833;
    }
    QListWidget {
        border: none;
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    QListWidget::item {
        padding: 10px;
        border-bottom: 1px solid #1f2833;
    }
    QListWidget::item:selected {
        background-color: #1f2833;
        color: #66fcf1;
        border-left: 3px solid #66fcf1;
    }
    QListWidget::item:hover {
        background-color: #1f2833;
    }
"""

# --- Buttons ---
BUTTON_PRIMARY = """
    QPushButton {
        background-color: rgba(69, 162, 158, 0.1);
        color: #66fcf1;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 2px;
        border: 1px solid #45a29e;
        font-family: monospace;
    }
    QPushButton:hover {
        background-color: #45a29e;
        color: #0b0c10;
    }
"""

BUTTON_SUCCESS = """
    QPushButton {
        background-color: rgba(32, 252, 143, 0.1);
        color: #20fc8f;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 2px;
        border: 1px solid #20fc8f;
        font-family: monospace;
    }
    QPushButton:hover {
        background-color: #20fc8f;
        color: #0b0c10;
    }
    QPushButton:disabled {
        background-color: #1f2833;
        color: #45a29e;
        border: 1px solid #1f2833;
    }
"""

BUTTON_DANGER = """
    QPushButton {
        background-color: transparent;
        color: #fc2044;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 2px;
        border: 1px solid #fc2044;
        font-family: monospace;
    }
    QPushButton:hover {
        background-color: #fc2044;
        color: #0b0c10;
    }
"""

BUTTON_SAVE = """
    QPushButton {
        background-color: #45a29e;
        color: #0b0c10;
        padding: 8px 16px;
        border-radius: 2px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #66fcf1; }
    QPushButton:disabled { background-color: #1f2833; color: #8b949e; }
"""

BUTTON_RESET = """
    QPushButton {
        background-color: transparent;
        color: #8b949e;
        padding: 8px 16px;
        border: 1px solid #1f2833;
        border-radius: 2px;
    }
    QPushButton:hover { background-color: #1f2833; color: #c5c6c7; }
    QPushButton:disabled { color: #45a29e; }
"""

# --- Stats Cards ---
STAT_CARD_STYLE = """
    background-color: rgba(31, 40, 51, 0.6);
    border: 1px solid #1f2833;
    border-radius: 2px;
    color: #66fcf1;
    padding: 15px;
    font-size: 12px;
    font-weight: bold;
    font-family: monospace;
"""

# --- Tables ---
TABLE_STYLE = """
    QTableWidget {
        background-color: #0b0c10;
        color: #c5c6c7;
        gridline-color: #1f2833;
        border: 1px solid #1f2833;
        font-family: monospace;
    }
    QHeaderView::section {
        background-color: #1f2833;
        color: #66fcf1;
        padding: 4px;
        border: 1px solid #0b0c10;
        font-weight: bold;
    }
    QTableCornerButton::section {
        background-color: #1f2833;
    }
"""

# --- Group Boxes ---
OUTLIER_GROUP_STYLE = """
    QGroupBox {
        background-color: rgba(252, 32, 68, 0.05);
        border: 1px solid #fc2044;
        border-radius: 2px;
        margin-top: 10px;
        padding-top: 15px;
        font-weight: bold;
        color: #fc2044;
        font-family: monospace;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
"""

ADVANCED_GROUP_STYLE = """
    QGroupBox {
        background-color: rgba(31, 40, 51, 0.4);
        border: 1px solid #45a29e;
        border-radius: 2px;
        margin-top: 10px;
        padding-top: 15px;
        font-weight: bold;
        color: #45a29e;
        font-family: monospace;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
"""

THRESHOLD_GROUP_STYLE = """
    QGroupBox {
        background-color: rgba(69, 162, 158, 0.05);
        border: 1px solid #45a29e;
        border-radius: 2px;
        margin-top: 10px;
        padding-top: 15px;
        font-weight: bold;
        color: #45a29e;
        font-family: monospace;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
"""

# --- Scroll Area ---
SCROLL_AREA_STYLE = "QScrollArea { border: none; background-color: #0b0c10; }"

# --- Navigation Toolbar (Matplotlib) ---
NAV_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #1f2833;
        border: 1px solid #45a29e;
        border-radius: 4px;
        padding: 4px;
        spacing: 4px;
    }
    QToolButton {
        background-color: #e8e8e8;
        border: 1px solid #45a29e;
        border-radius: 3px;
        padding: 6px;
        margin: 2px;
        min-width: 28px;
        min-height: 28px;
    }
    QToolButton:hover {
        background-color: #66fcf1;
        border-color: #66fcf1;
    }
    QToolButton:pressed, QToolButton:checked {
        background-color: #45a29e;
    }
"""

# --- Sliders ---
WARNING_SLIDER_STYLE = """
    QSlider::groove:horizontal { background: #1f2833; height: 8px; border-radius: 4px; }
    QSlider::handle:horizontal { background: #e0a800; width: 16px; margin: -4px 0; border-radius: 8px; }
    QSlider::sub-page:horizontal { background: #e0a800; border-radius: 4px; }
"""

IQR_SLIDER_STYLE = """
    QSlider::groove:horizontal { background: #1f2833; height: 8px; border-radius: 4px; }
    QSlider::handle:horizontal { background: #fc2044; width: 16px; margin: -4px 0; border-radius: 8px; }
    QSlider::sub-page:horizontal { background: #fc2044; border-radius: 4px; }
"""

# --- Login Dialog ---
def get_login_dialog_style(img_path: str) -> str:
    """Returns the login dialog stylesheet with the background image path."""
    return f"""
        QDialog {{
            background-image: url('{img_path}');
            background-position: center;
            background-repeat: no-repeat;
            border: 2px solid #45a29e;
        }}
    """

LOGIN_CONTAINER_STYLE = """
    QWidget {
        background-color: rgba(11, 12, 16, 0.85);
        border: 1px solid rgba(102, 252, 241, 0.3);
        border-radius: 4px;
    }
"""

LOGIN_HEADER_STYLE = """
    color: #66fcf1;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 2px;
    background: transparent;
    border: none;
    margin-bottom: 5px;
"""

LOGIN_SUBHEADER_STYLE = """
    color: #45a29e;
    font-family: monospace;
    font-size: 14px;
    background: transparent;
    border: none;
    margin-bottom: 20px;
"""

LOGIN_INPUT_STYLE = """
    QLineEdit {
        background-color: #0d1117;
        border: 1px solid #1f2833;
        color: #66fcf1;
        padding: 10px;
        font-family: monospace;
        border-radius: 0px;
    }
    QLineEdit:focus {
        border: 1px solid #66fcf1;
        background-color: #000;
    }
"""

LOGIN_ACTION_BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(69, 162, 158, 0.1);
        color: #66fcf1;
        padding: 12px;
        font-weight: bold;
        border: 1px solid #45a29e;
        border-radius: 2px;
        font-family: monospace;
        letter-spacing: 1px;
    }
    QPushButton:hover {
        background-color: #45a29e;
        color: #0b0c10;
    }
"""

LOGIN_TOGGLE_BUTTON_STYLE = """
    QPushButton {
        background: none;
        border: none;
        color: #8b949e;
        font-family: monospace;
        font-size: 12px;
    }
    QPushButton:hover {
        color: #66fcf1;
    }
"""

LOGIN_EXIT_BUTTON_STYLE = """
    QPushButton {
        background: none;
        border: none;
        color: #fc2044;
        font-family: monospace;
        font-size: 11px;
        margin-top: 10px;
    }
    QPushButton:hover {
        text-decoration: underline;
    }
"""
