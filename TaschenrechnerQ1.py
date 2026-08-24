import streamlit as st

# -----------------------------------------------------------------------------
# Seite & Style-Konfiguration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Taschenrechner App",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS für echtes Taschenrechner-Design
st.markdown("""
<style>
    /* Haupt-Container zentrieren und schmaler halten */
    .block-container {
        max-width: 400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hauptdisplay Styling */
    .calc-screen {
        background-color: #1e1e2e;
        color: #a6e3a1;
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: right;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
        word-wrap: break-word;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    
    /* Hilfsanzeige für die aktuelle Rechnung oben rechts */
    .calc-subscreen {
        color: #a6adc8;
        font-size: 0.95rem;
        font-family: monospace;
        text-align: right;
        margin-bottom: 4px;
        padding-right: 5px;
        height: 20px;
    }

    /* Buttons vereinheitlichen */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        margin-bottom: 6px;
        transition: all 0.1s ease-in-out;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Zustandsverwaltung (Session State)
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
    """Setzt den gesamten Taschenrechner zurück."""
    st.session_state.display = '0'
    st.session_state.expression = ''
    st.session_state.new_input = False
    st.session_state.error_state = False

def press_digit(digit):
    """Verarbeitet die Eingabe von Ziffern und dem Dezimalpunkt."""
    if st.session_state.error_state:
        reset_calc()
    
    if st.session_state.new_input:
        st.session_state.display = digit if digit != '.' else '0.'
        st.session_state.new_input = False
    else:
        if st.session_state.display == '0' and digit != '.':
            st.session_state.display = digit
        elif digit == '.':
            # Verhindert mehrfache Punkte in einer Zahl
            if '.' not in st.session_state.display:
                st.session_state.display += '.'
        else:
            st.session_state.display += digit

def press_operator(op):
    """Verarbeitet Operatoren (+, -, *, /)."""
    if st.session_state.error_state:
        return

    disp = st.session_state.display.rstrip('.')
    
    # Falls bereits eine Operation aussteht, berechne Zwischenergebnis
    if st.session_state.expression and not st.session_state.new_input:
        calculate_result()
        disp = st.session_state.display

    st.session_state.expression = f"{disp} {op}"
    st.session_state.new_input = True

def calculate_result():
    """Führt die mathematische Berechnung aus."""
    if st.session_state.error_state or not st.session_state.expression:
        return

    full_expr = f"{st.session_state.expression} {st.session_state.display.rstrip('.')}"
    
    # Umwandlung für Python-Auswertung
    clean_expr = full_expr.replace('×', '*').replace('÷', '/')
    
    try:
        # Sichere Auswertung des Ausdrucks
        result = eval(clean_expr, {"__builtins__": None}, {})
        
        # Formatierung: Ganze Zahlen ohne Nachkommastellen anzeigen
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)  # Rundung gegen Floating-Point-Ungenauigkeiten
                
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
    """C: Alles zurücksetzen."""
    reset_calc()

def press_delete():
    """DEL: Letztes Zeichen löschen."""
    if st.session_state.error_state or st.session_state.new_input:
        return
    
    current = st.session_state.display
    if len(current) > 1:
        st.session_state.display = current[:-1]
    else:
        st.session_state.display = '0'

def press_toggle_sign():
    """+/-: Vorzeichen wechseln."""
    if st.session_state.error_state or st.session_state.display == '0':
        return
    
    if st.session_state.display.startswith('-'):
        st.session_state.display = st.session_state.display[1:]
    else:
        st.session_state.display = '-' + st.session_state.display

def press_percent():
    """%: In Prozent umrechnen."""
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
# Benutzeroberfläche (Grid Layout)
# -----------------------------------------------------------------------------
st.title("🧮 Taschenrechner")

# Neben-Display für laufende Rechnung
subscreen_text = st.session_state.expression if st.session_state.expression else "&nbsp;"
st.markdown(f'<div class="calc-subscreen">{subscreen_text}</div>', unsafe_allow_html=True)

# Haupt-Display
st.markdown(f'<div class="calc-screen">{st.session_state.display}</div>', unsafe_allow_html=True)

# Reihe 1: C | ⌫ | % | ÷
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("C", on_click=press_clear, type="secondary")
with col2:
    st.button("⌫", on_click=press_delete, type="secondary")
with col3:
    st.button("%", on_click=press_percent, type="secondary")
with col4:
    st.button("÷", on_click=press_operator, args=('÷',), type="primary")

# Reihe 2: 7 | 8 | 9 | ×
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("7", on_click=press_digit, args=('7',))
with col2:
    st.button("8", on_click=press_digit, args=('8',))
with col3:
    st.button("9", on_click=press_digit, args=('9',))
with col4:
    st.button("×", on_click=press_operator, args=('×',), type="primary")

# Reihe 3: 4 | 5 | 6 | -
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("4", on_click=press_digit, args=('4',))
with col2:
    st.button("5", on_click=press_digit, args=('5',))
with col3:
    st.button("6", on_click=press_digit, args=('6',))
with col4:
    st.button("-", on_click=press_operator, args=('-',), type="primary")

# Reihe 4: 1 | 2 | 3 | +
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("1", on_click=press_digit, args=('1',))
with col2:
    st.button("2", on_click=press_digit, args=('2',))
with col3:
    st.button("3", on_click=press_digit, args=('3',))
with col4:
    st.button("+", on_click=press_operator, args=('+',), type="primary")

# Reihe 5: +/- | 0 | . | =
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("+/-", on_click=press_toggle_sign)
with col2:
    st.button("0", on_click=press_digit, args=('0',))
with col3:
    st.button(".", on_click=press_digit, args=('.',))
with col4:
    st.button("=", on_click=calculate_result, type="primary")
