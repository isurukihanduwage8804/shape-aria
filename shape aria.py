import streamlit as st
import random
import time

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Geometry Dance Challenge", page_icon="📐")

# --- CSS: පෙනුම සහ Animation ---
st.markdown("""
<style>
    @keyframes dance {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(10deg) scale(1.05); }
        50% { transform: rotate(-10deg) scale(1.05); }
        75% { transform: rotate(5deg) scale(1.05); }
        100% { transform: rotate(0deg) scale(1); }
    }
    .dance-shape { animation: dance 0.8s infinite; display: inline-block; }
    .shape-container {
        text-align: center; 
        padding: 50px; 
        background: #ffffff;
        border-radius: 20px; 
        border: 4px solid #3b82f6; 
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 450px;
    }
    .stButton>button { border-radius: 15px; font-size: 18px; font-weight: bold; height: 3em; }
</style>
""", unsafe_allow_html=True)

# --- Sound Function ---
def play_win_sound():
    # නිවැරදි පිළිතුරට ජයග්‍රාහී ශබ්දයක්
    sound_html = """
    <audio autoplay>
        <source src="https://cdn.pixabay.com/audio/2021/08/04/audio_0625c1539c.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# --- Game Logic ---
if 'q_no' not in st.session_state:
    st.session_state.q_no = 1
    st.session_state.score = 0
    st.session_state.asked_questions = []

def generate_unique_question():
    while True:
        shape_type = random.choice(["Square", "Rectangle", "Triangle"])
        w = random.randint(2, 20)
        h = random.randint(2, 20)
        q_id = f"{shape_type}_{w}_{h}"
        if q_id not in st.session_state.asked_questions:
            st.session_state.asked_questions.append(q_id)
            break

    max_val = max(w, h)
    scale = 300 / max_val if max_val > 10 else 30
    canvas_w, canvas_h = 500, 450
    
    if shape_type == "Square":
        area = w * w
        label = "සමචතුරස්‍රයේ වර්ගඵලය සොයන්න"
        draw = f'''<svg width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}">
            <rect x="100" y="50" width="{w*scale}" height="{w*scale}" fill="#ef4444" stroke="black" stroke-width="3"/>
            <text x="{100 + (w*scale)/2}" y="{w*scale + 90}" text-anchor="middle" font-size="24" font-weight="bold" fill="black">{w}cm</text>
            <text x="70" y="{50 + (w*scale)/2}" text-anchor="middle" font-size="24" font-weight="bold" fill="black" transform="rotate(-90, 70, {50 + (w*scale)/2})">{w}cm</text>
        </svg>'''
    elif shape_type == "Rectangle":
        area = w * h
        label = "සෘජුකෝණාස්‍රයේ වර්ගඵලය සොයන්න"
        draw = f'''<svg width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}">
            <rect x="100" y="50" width="{w*scale}" height="{h*scale}" fill="#3b82f6" stroke="black" stroke-width="3"/>
            <text x="{100 + (w*scale)/2}" y="{h*scale + 90}" text-anchor="middle" font-size="24" font-weight="bold" fill="black">{w}cm (දිග)</text>
            <text x="70" y="{50 + (h*scale)/2}" text-anchor="middle" font-size="24" font-weight="bold" fill="black" transform="rotate(-90, 70, {50 + (h*scale)/2})">{h}cm (පළල)</text>
        </svg>'''
    else: # Triangle
        area = (w * h) / 2
        label = "ත්‍රිකෝණයේ වර්ගඵලය සොයන්න"
        draw = f'''<svg width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}">
            <polygon points="100,{h*scale + 50} {w*scale + 100},{h*scale + 50} {100 + (w*scale)/2},50" fill="#22c55e" stroke="black" stroke-width="3"/>
            <text x="{100 + (w*scale)/2}" y="{h*scale + 90}" text-anchor="middle" font-size="24" font-weight="bold" fill="black">{w}cm (ආධාරකය)</text>
            <text x="60" y="{50 + (h*scale)/2}" text-anchor="middle" font-size="24" font-weight="bold" fill="black">{h}cm (උස)</text>
        </svg>'''
    
    opts = list(set([area, area + 5, area + 10, area - 2, area * 2, area + random.randint(1,20)]))
    random.shuffle(opts)
    final_opts = opts[:3] + [area] if area not in opts[:3] else opts[:4]
    random.shuffle(final_opts)
    return label, area, final_opts, draw

# --- UI ---
if st.session_state.q_no <= 50:
    if 'current_q' not in st.session_state:
        st.session_state.current_q = generate_unique_question()

    label, correct_area, opts, svg = st.session_state.current_q
    st.markdown(f"<h2 style='text-align:center;'>ප්‍රශ්නය {st.session_state.q_no} / 50</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.q_no / 50)
    st.info(label)

    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f'<div class="shape-container"><div>{svg}</div></div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, opt in enumerate(opts):
        with cols[i % 2]:
            if st.button(f"{opt} cm²", key=f"ans_{i}"):
                if opt == correct_area:
                    placeholder.markdown(f'<div class="shape-container"><div class="dance-shape">{svg}</div></div><h2 style="text-align:center;color:green;">නිවැරදියි! 🕺</h2>', unsafe_allow_html=True)
                    st.balloons()
                    play_win_sound() # ශබ්දය ක්‍රියාත්මක කිරීම
                    st.session_state.score += 1
                    time.sleep(2.5)
                else:
                    st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_area} cm²")
                    time.sleep(1.5)
                
                st.session_state.q_no += 1
                del st.session_state.current_q
                st.rerun()
else:
    st.success("ක්‍රීඩාව අවසන්!")
    st.header(f"ලකුණු: {st.session_state.score} / 50")
    if st.button("නැවත ආරම්භ කරන්න"):
        st.session_state.q_no = 1
        st.session_state.score = 0
        st.session_state.asked_questions = []
        st.rerun()
