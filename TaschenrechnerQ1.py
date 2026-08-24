import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BESTER TASCHENRECHNER",
    page_icon="⚡",
    layout="centered"
)

# -----------------------------------------------------------------------------
# Custom CSS for Cyber-Graffiti Neon Style matching the provided image
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Orbitron:wght@700&family=Inter:wght@700&display=swap');

    /* Global dark cyber background */
    .stApp {
        background: #09090e;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(255, 0, 128, 0.2), transparent 45%),
            radial-gradient(circle at 90% 90%, rgba(0, 240, 255, 0.2), transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(180, 0, 255, 0.15), transparent 60%);
    }

    .block-container {
        max-width: 440px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* Outer Cyber Neon Border Frame */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(13, 13, 22, 0.95) !important;
        border-radius: 28px !important;
        padding: 24px 20px !important;
        border: 2px solid transparent !important;
        background-image: linear-gradient(rgba(13, 13, 22, 0.95), rgba(13, 13, 22, 0.95)), 
                          linear-gradient(135deg, #ff007f 0%, #a000ff 50%, #00f0ff 100%) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        box-shadow: 
            0 0 25px rgba(255, 0, 127, 0.4),
            0 0 50px rgba(0, 240, 255, 0.25),
            inset 0 0 15px rgba(255, 0, 127, 0.15);
    }

    /* Header Title Style matching "BESTER TASCHENRECHNER" */
    .graffiti-title {
        text-align: center;
        font-family: 'Permanent Marker', cursive, sans-serif;
        line-height: 1.0;
        margin-bottom: 20px;
    }
    
    .title-sub {
        font-size: 1.8rem;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255,255,255,0.8), 2px 2px 0px #000;
        letter-spacing: 2px;
        display: block;
    }
    
    .title-main {
        font-size: 2.6rem;
        background: linear-gradient(180deg, #ffea00 0%, #ff007f 60%, #a000ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(3px 3px 0px #000) drop-shadow(0 0 15px rgba(255, 0, 127, 0.8));
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Subscreen expression display */
    .calc-subscreen {
        color: #ff77bc;
        font-size: 0.95rem;
        font-family: 'Orbitron', monospace;
        text-align: right;
        min-height: 22px;
        padding-right: 12px;
        margin-bottom: 4px;
        font-weight: 700;
    }

    /* LCD Screen Display - 7 Segment LCD Look */
    .calc-screen {
        background: #090a0f;
        color: #ffffff;
        font-family: 'Orbitron', monospace, sans-serif;
        font-size: 3rem;
        font-weight: bold;
        text-align: right;
        padding: 12px 20px;
        border-radius: 18px;
        margin-bottom: 20px;
        border: 2px solid #00f0ff;
        box-shadow: 
            0 0 18px rgba(0, 240, 255, 0.5),
            inset 0 0 15px rgba(0, 0, 0, 0.9);
        word-wrap: break-word;
        word-break: break-all;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        letter-spacing: 2px;
    }

    /* Base Button Styling */
    div.stButton > button {
        width: 100% !important;
        height: 64px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        margin-bottom: 10px !important;
        color: #ffffff !important;
        transition: transform 0.1s ease, filter 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.4);
    }
    
    div.stButton > button:hover {
        transform: scale(1.04) !important;
        filter: brightness(1.2) !important;
    }

    /* Color Palette matching exact image buttons */
    
    /* Top Row Function Keys (AC, +/-, %) */
    .fn-btn div.stButton > button {
        background: linear-gradient(180deg, #32353e 0%, #1c1e24 100%) !important;
        color: #ffffff !important;
    }

    /* Pink Operator Column (÷, ×, -, +, =) */
    .op-btn div.stButton > button {
        background: linear-gradient(180deg, #ff3b93 0%, #e60067 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.5) !important;
    }

    /* Row 7, 8, 9 (Red -> Orange -> Yellow) */
    .btn-7 div.stButton > button { background: linear-gradient(180deg, #ff4b4b 0%, #d62828 100%) !important; }
    .btn-8 div.stButton > button { background: linear-gradient(180deg, #ff8c00 0%, #e65100 100%) !important; }
    .btn-9 div.stButton > button { background: linear-gradient(180deg, #ffcc00 0%, #f57f17 100%) !important; }

    /* Row 4, 5, 6 (Yellow-Green -> Lime -> Green) */
    .btn-4 div.stButton > button { background: linear-gradient(180deg, #d4e157 0%, #9e9d24 100%) !important; }
    .btn-5 div.stButton > button { background: linear-gradient(180deg, #aeea00 0%, #64dd17 100%) !important; }
    .btn-6 div.stButton > button { background: linear-gradient(180deg, #26a69a 0%, #00695c 100%) !important; }

    /* Row 1, 2, 3 (Teal -> Cyan -> Blue) */
    .btn-1 div.stButton > button { background: linear-gradient(180deg, #00bcd4 0%, #00838f 100%) !important; }
    .btn-2 div.stButton > button { background: linear-gradient(180deg, #03a9f4 0%, #0277bd 100%) !important; }
    .btn-3 div.stButton > button { background: linear-gradient(180deg, #2979ff 0%, #1565c0 100%) !important; }

    /* Row 0 and , (Purple / Violet) */
    .btn-0 div.stButton > button { background: linear-gradient(180deg, #651fff 0%, #4527a0 100%) !important; }
    .btn-comma div.stButton > button { background: linear-gradient(180deg, #aa00ff 0%, #6a1b9a 100%) !important; }

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
# Logic Functions
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
        st.session_state.display = "FEHLER"
        st.session_state.expression = ''
        st.session_state.error_state = True
    except Exception:
        st.session_state.display = "FEHLER"
        st.session_state.expression = ''
        st.session_state.error_state = True

def press_clear():
    reset_calc()

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
# Main Calculator Container (UI Layout matching the image)
# -----------------------------------------------------------------------------
with st.container(border=True):
    # Header Title
    st.markdown('''
    <div class="graffiti-title">
        <span class="title-sub">BESTER</span>
        <span class="title-main">TASCHENRECHNER</span>
    </div>
    ''', unsafe_allow_html=True)

    # Subscreen
    subscreen_text = st.session_state.expression if st.session_state.expression else "&nbsp;"
    st.markdown(f'<div class="calc-subscreen">{subscreen_text}</div>', unsafe_allow_html=True)

    # LCD Screen Display
    display_show = st.session_state.display.replace('.', ',')
    st.markdown(f'<div class="calc-screen">{display_show}</div>', unsafe_allow_html=True)

    # Row 1: AC | +/- | % | ÷
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="fn-btn">', unsafe_allow_html=True)
        st.button("AC", on_click=press_clear)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="fn-btn">', unsafe_allow_html=True)
        st.button("+/-", on_click=press_toggle_sign)
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="fn-btn">', unsafe_allow_html=True)
        st.button("%", on_click=press_percent)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="op-btn">', unsafe_allow_html=True)
        st.button("÷", on_click=press_operator, args=('÷',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 2: 7 | 8 | 9 | ×
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="btn-7">', unsafe_allow_html=True)
        st.button("7", on_click=press_digit, args=('7',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-8">', unsafe_allow_html=True)
        st.button("8", on_click=press_digit, args=('8',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-9">', unsafe_allow_html=True)
        st.button("9", on_click=press_digit, args=('9',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="op-btn">', unsafe_allow_html=True)
        st.button("×", on_click=press_operator, args=('×',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 3: 4 | 5 | 6 | -
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="btn-4">', unsafe_allow_html=True)
        st.button("4", on_click=press_digit, args=('4',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-5">', unsafe_allow_html=True)
        st.button("5", on_click=press_digit, args=('5',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-6">', unsafe_allow_html=True)
        st.button("6", on_click=press_digit, args=('6',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="op-btn">', unsafe_allow_html=True)
        st.button("-", on_click=press_operator, args=('-',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 4: 1 | 2 | 3 | +
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="btn-1">', unsafe_allow_html=True)
        st.button("1", on_click=press_digit, args=('1',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-2">', unsafe_allow_html=True)
        st.button("2", on_click=press_digit, args=('2',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-3">', unsafe_allow_html=True)
        st.button("3", on_click=press_digit, args=('3',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="op-btn">', unsafe_allow_html=True)
        st.button("+", on_click=press_operator, args=('+',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 5: 0 (breit / 2 Spalten) | , | =
    c1_wide, c3, c4 = st.columns([2, 1, 1])
    with c1_wide:
        st.markdown('<div class="btn-0">', unsafe_allow_html=True)
        st.button("0", on_click=press_digit, args=('0',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-comma">', unsafe_allow_html=True)
        st.button(",", on_click=press_digit, args=('.',))
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="op-btn">', unsafe_allow_html=True)
        st.button("=", on_click=calculate_result)
        st.markdown('</div>', unsafe_allow_html=True)
