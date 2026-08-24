import streamlit as st

# -----------------------------------------------------------------------------
# Seite & Style-Konfiguration (Modernes Design)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Modern Calculator",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS für Glassmorphism & Modernes Dark UI Design
st.markdown("""
<style>
    /* Globaler Hintergrund & Zentrierung */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }

    .block-container {
        max-width: 380px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Titel-Styling */
    h1 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        font-size: 1.6rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: 0.5px;
    }

    /* Rechner-Karten-Container (Glassmorphism) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Hilfsanzeige (ausstehende Rechnung) */
    .calc-subscreen {
        color: #94a3b8;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        text-align: right;
        min-height: 22px;
        padding-right: 8px;
        margin-bottom: 4px;
        font-weight: 500;
    }

    /* Hauptdisplay */
    .calc-screen {
        background: rgba(15, 23, 42, 0.85);
        color: #38bdf8;
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.3rem;
        font-weight: 700;
        text-align: right;
        padding: 18px 20px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
        word-wrap: break-word;
        word-break: break-all;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }

    /* Allgemeine Button-Styles */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 8px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Zahlen-Buttons */
    div.stButton > button[kind="secondary"] {
        background: rgba(51, 65, 85, 0.6) !important;
        color: #f1f5f9 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(71, 85, 105, 0.9) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }

    /* Operatoren & Aktions-Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialisierung
# -----------------------------------------------------------------------------
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'new_input' not in st.session_state:
    st.session_state.new_input = False
if 'error_state' not in st.session_state:
    st.session_state.error_state = False

# -----------------------------------------------------------------------------
# Logik-Funktionen
# -----------------------------------------------------------------------------
def reset_calc():
    st.session_state.display = '0'
    st.session_state.expression = ''
    st.session_state.new_input = False
    st.session_state.error_state = False

def press_digit(digit):
    if st.session_state.error_state:
        reset_calc()
    
    if st.session_state.new_input:
        st.session_state.display = digit if digit != '.' else '0.'
        st.session_state.new_input = False
    else:
        if st.session_state.display == '0' and digit != '.':
            st.session_state.display = digit
        elif digit == '.':
            if '.' not in st.session_state.display:
                st.session_state.display += '.'
        else:
            st.session_state.display += digit

def press_operator(op):
    if st.session_state.error_state:
        return

    disp = st.session_state.display.rstrip('.')
    
    if st.session_state.expression and not st.session_state.new_input:
        calculate_result()
        disp = st.session_state.display

    st.session_state.expression = f"{disp} {op}"
    st.session_state.new_input = True

def calculate_result():
    if st.session_state.error_state or not st.session_state.expression:
        return

    full_expr = f"{st.session_state.expression} {st.session_state.display.rstrip('.')}"
    clean_expr = full_expr.replace('×', '*').replace('÷', '/')
    
    try:
        result = eval(clean_expr, {"__builtins__": None}, {})
        
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
                
        st.session_state.display = str(result)
        st.session_state.expression = ''
        st.session_state.new_input = True

    except ZeroDivisionError:
        st.session_state.display = "Fehler: Div / 0"
        st.session_state.expression = ''
        st.session_state.error_state = True
    except Exception:
        st.session_state.display = "Fehler"
        st.session_state.expression = ''
        st.session_state.error_state = True

def press_clear():
    reset_calc()

def press_delete():
    if st.session_state.error_state or st.session_state.new_input:
        return
    
    current = st.session_state.display
    if len(current) > 1:
        st.session_state.display = current[:-1]
    else:
        st.session_state.display = '0'

def press_toggle_sign():
    if st.session_state.error_state or st.session_state.display == '0':
        return
    
    if st.session_state.display.startswith('-'):
        st.session_state.display = st.session_state.display[1:]
    else:
        st.session_state.display = '-' + st.session_state.display

def press_percent():
    if st.session_state.error_state:
        return
    try:
        val = float(st.session_state.display) / 100.0
        if val.is_integer():
            val = int(val)
        st.session_state.display = str(val)
    except ValueError:
        pass

# -----------------------------------------------------------------------------
# UI Layout
# -----------------------------------------------------------------------------
st.title("🧮 Calculator")

# Gläserne Rechner-Karte
with st.container(border=True):
    # Ausstehende Rechnung (oben rechts)
    subscreen_text = st.session_state.expression if st.session_state.expression else "&nbsp;"
    st.markdown(f'<div class="calc-subscreen">{subscreen_text}</div>', unsafe_allow_html=True)

    # Haupt-Display
    st.markdown(f'<div class="calc-screen">{st.session_state.display}</div>', unsafe_allow_html=True)

    # Reihe 1: Funktionstasten (AC | ⌫ | % | ÷)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("AC", on_click=press_clear, type="secondary")
    with col2:
        st.button("⌫", on_click=press_delete, type="secondary")
    with col3:
        st.button("%", on_click=press_percent, type="secondary")
    with col4:
        st.button("÷", on_click=press_operator, args=('÷',), type="primary")

    # Reihe 2: Zahlen 1, 2, 3 & Multiplikation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("1", on_click=press_digit, args=('1',))
    with col2:
        st.button("2", on_click=press_digit, args=('2',))
    with col3:
        st.button("3", on_click=press_digit, args=('3',))
    with col4:
        st.button("×", on_click=press_operator, args=('×',), type="primary")

    # Reihe 3: Zahlen 4, 5, 6 & Subtraktion
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("4", on_click=press_digit, args=('4',))
    with col2:
        st.button("5", on_click=press_digit, args=('5',))
    with col3:
        st.button("6", on_click=press_digit, args=('6',))
    with col4:
        st.button("-", on_click=press_operator, args=('-',), type="primary")

    # Reihe 4: Zahlen 7, 8, 9 & Addition
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("7", on_click=press_digit, args=('7',))
    with col2:
        st.button("8", on_click=press_digit, args=('8',))
    with col3:
        st.button("9", on_click=press_digit, args=('9',))
    with col4:
        st.button("+", on_click=press_operator, args=('+',), type="primary")

    # Reihe 5: Unterste Reihe (+/- | 0 | . | =)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("+/-", on_click=press_toggle_sign)
    with col2:
        st.button("0", on_click=press_digit, args=('0',))
    with col3:
        st.button(".", on_click=press_digit, args=('.',))
    with col4:
        st.button("=", on_click=calculate_result, type="primary")
