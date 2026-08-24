# Let's create the text files and also provide a zip archive if needed, or simply output the cleanly formatted code blocks.
# The user wants code blocks for app.py, requirements.txt, and README.md.

app_py_content = '''import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Python Streamlit Taschenrechner",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for a modern calculator UI look
st.markdown("""
<style>
    /* Main container centering */
    .block-container {
        max-width: 420px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Calculator Screen Styling */
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
    
    /* Secondary expression sub-screen */
    .calc-subscreen {
        color: #a6adc8;
        font-size: 0.9rem;
        text-align: right;
        margin-bottom: -15px;
        padding-right: 5px;
        height: 20px;
    }

    /* Standardizing button sizes */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        margin-bottom: 8px;
        transition: all 0.1s ease-in-out;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialization
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
# Helper Functions for Calculator Operations
# -----------------------------------------------------------------------------
def reset_calc():
    """Resets the calculator state."""
    st.session_state.display = '0'
    st.session_state.expression = ''
    st.session_state.new_input = False
    st.session_state.error_state = False

def press_digit(digit):
    """Handles digit button clicks (0-9 and decimal point)."""
    if st.session_state.error_state:
        reset_calc()
    
    if st.session_state.new_input:
        st.session_state.display = digit if digit != '.' else '0.'
        st.session_state.new_input = False
    else:
        if st.session_state.display == '0' and digit != '.':
            st.session_state.display = digit
        elif digit == '.':
            # Prevent multiple decimal points in current number segment
            # Find current operand by splitting on operators
            current_val = st.session_state.display
            if '.' not in current_val:
                st.session_state.display += '.'
        else:
            st.session_state.display += digit

def press_operator(op):
    """Handles operator button clicks (+, -, *, /)."""
    if st.session_state.error_state:
        return

    # Prepare string for math evaluation
    disp = st.session_state.display.rstrip('.')
    
    if st.session_state.expression and not st.session_state.new_input:
        calculate_result()
        disp = st.session_state.display

    st.session_state.expression = f"{disp} {op}"
    st.session_state.new_input = True

def calculate_result():
    """Evaluates the mathematical expression."""
    if st.session_state.error_state or not st.session_state.expression:
        return

    expr = st.session_state.expression + " " + st.session_state.display.rstrip('.')
    
    # Replace visual/safe operators if needed
    clean_expr = expr.replace('×', '*').replace('÷', '/')
    
    try:
        # Evaluate safely
        result = eval(clean_expr, {"__builtins__": None}, {})
        
        # Format result (integer vs float)
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)  # prevent floating point precision issues
                
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
    """Clears display and resets memory."""
    reset_calc()

def press_delete():
    """Deletes the last typed digit."""
    if st.session_state.error_state or st.session_state.new_input:
        return
    
    current = st.session_state.display
    if len(current) > 1:
        st.session_state.display = current[:-1]
    else:
        st.session_state.display = '0'

def press_toggle_sign():
    """Toggles sign (+/-) of current entry."""
    if st.session_state.error_state or st.session_state.display == '0':
        return
    
    if st.session_state.display.startswith('-'):
        st.session_state.display = st.session_state.display[1:]
    else:
        st.session_state.display = '-' + st.session_state.display

def press_percent():
    """Converts display number to percentage."""
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
# User Interface Layout
# -----------------------------------------------------------------------------
st.title("🧮 Taschenrechner")

# Secondary Screen (shows operator in progress)
subscreen_text = st.session_state.expression if st.session_state.expression else "&nbsp;"
st.markdown(f'<div class="calc-subscreen">{subscreen_text}</div>', unsafe_allow_html=True)

# Main Screen Display
st.markdown(f'<div class="calc-screen">{st.session_state.display}</div>', unsafe_allow_html=True)

# Button Grid Layout (5 rows x 4 columns)
# Row 1: C | ⌫ | % | /
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("C", on_click=press_clear, type="secondary")
with col2:
    st.button("⌫", on_click=press_delete, type="secondary")
with col3:
    st.button("%", on_click=press_percent, type="secondary")
with col4:
    st.button("÷", on_click=press_operator, args=('/',), type="primary")

# Row 2: 7 | 8 | 9 | *
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("7", on_click=press_digit, args=('7',))
with col2:
    st.button("8", on_click=press_digit, args=('8',))
with col3:
    st.button("9", on_click=press_digit, args=('9',))
with col4:
    st.button("×", on_click=press_operator, args=('*',), type="primary")

# Row 3: 4 | 5 | 6 | -
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("4", on_click=press_digit, args=('4',))
with col2:
    st.button("5", on_click=press_digit, args=('5',))
with col3:
    st.button("6", on_click=press_digit, args=('6',))
with col4:
    st.button("-", on_click=press_operator, args=('-',), type="primary")

# Row 4: 1 | 2 | 3 | +
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("1", on_click=press_digit, args=('1',))
with col2:
    st.button("2", on_click=press_digit, args=('2',))
with col3:
    st.button("3", on_click=press_digit, args=('3',))
with col4:
    st.button("+", on_click=press_operator, args=('+',), type="primary")

# Row 5: +/- | 0 | . | =
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("+/-", on_click=press_toggle_sign)
with col2:
    st.button("0", on_click=press_digit, args=('0',))
with col3:
    st.button(".", on_click=press_digit, args=('.',))
with col4:
    st.button("=", on_click=calculate_result, type="primary")
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_py_content)

print("Created app.py successfully")
