import streamlit as st
import random
import time

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Geometry Dance Challenge", page_icon="📐")

# --- CSS: Animation සහ පෙනුම ---
st.markdown("""
<style>
    @keyframes dance {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(15deg) scale(1.1); }
        50% { transform: rotate(-15deg) scale(1.1); }
        75% { transform: rotate(10deg) scale(1.1); }
        100% { transform: rotate(0deg) scale(1); }
    }
    .dance-shape { animation: dance 0.8s infinite; display: inline-block; }
    .shape-container {
        text-align: center; padding: 40px; background: #ffffff;
        border-radius: 20px; border: 4px solid #3b82f6; margin-bottom: 20px;
    }
    .stButton>button { border-radius: 15px; font-size: 18px; font-weight: bold; height: 3em; }
</style>
""", unsafe_allow_html=True)

# --- Game Logic ---
if 'q_no' not in st.session_state:
    st.session_state.q_no = 1
    st.session_state.score = 0

def generate_question():
    shape_type = random.choice(["Square", "Rectangle", "Triangle"])
    w = random.randint(3, 10) # පළල/ආධාරකය
    h = random.randint(3, 10) # උස/දිග
    
    pixel_scale = 25 # රූපය පෙන්වන විශාලත්වය
    
    if shape_type == "Square":
        area = w * w
        label = "සමචතුරස්‍රයේ වර්ගඵලය සොයන්න"
        # SVG for Square with Text
        draw = f'''
        <svg width="{w*pixel_scale + 100}" height="{w*pixel_scale + 60}" style="margin:auto; display:block;">
            <rect x="50" y="10" width="{w*pixel_scale}" height="{w*pixel_scale}" fill="#ef4444" stroke="black" stroke-width="3"/>
            <text x="{50 + (w*pixel_scale)/2}" y="{w*pixel_scale + 40}" text-anchor="middle" font-size="20" font-weight="bold">{w}cm</text>
            <text x="20" y="{10 + (w*pixel_scale)/2}" text-anchor="middle" font-size="20" font-weight="bold" transform="rotate(-90, 20, {10 + (w*pixel_scale)/2})">{w}cm</text>
        </svg>'''
        
    elif shape_type == "Rectangle":
        area = w * h
        label = "සෘජුකෝණාස්‍රයේ වර්ගඵලය සොයන්න"
        draw = f'''
        <svg width="{w*pixel_scale + 100}" height="{h*pixel_scale + 60}" style="margin:auto; display:block;">
            <rect x="50" y="10" width="{w*pixel_scale}" height="{h*pixel_scale}" fill="#3b82f6" stroke="black" stroke-width="3"/>
            <text x="{50 + (w*pixel_scale)/2}" y="{h*pixel_scale + 40}" text-anchor="middle" font-size="20" font-weight="bold">{w}cm (දිග)</text>
            <text x="20" y="{10 + (h*pixel_scale)/2}" text-anchor="middle" font-size="20" font-weight="bold" transform="rotate(-90, 20, {10 + (h*pixel_scale)/2})">{h}cm (පළල)</text>
        </svg>'''
        
    else: # Triangle
        area = (w * h) / 2
        label = "ත්‍රිකෝණයේ වර්ගඵලය සොයන්න"
        draw = f'''
        <svg width="{w*pixel_scale + 100}" height="{h*pixel_scale + 60}" style="margin:auto; display:block;">
            <polygon points="50,{h*pixel_scale + 10} {w*pixel_scale + 50},{h*pixel_scale + 10} {50 + (w*pixel_scale)/2},10" fill="#22c55e" stroke="black" stroke-width="3"/>
            <line x1="50" y1="{h*pixel_scale + 10}" x2="{w*pixel_scale + 50}" y2="{h*pixel_scale + 10}" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
            <text x="{50 + (w*pixel_scale)/2}" y="{h*pixel_scale + 40}" text-anchor="middle" font-size="20" font-weight="bold">{w}cm (ආධාරකය)</text>
            <text x="30" y="{10 + (h*pixel_scale)/2}" text-anchor="middle" font-size="18" font-weight="bold">{h}cm (උස)</text>
        </svg>'''
        
    options = random.sample(list(set([area, area + 5, area + 10, area - 3, area * 2, area / 2])), 4)
    if area not in options: options[0] = area
    random.shuffle(options)
    
    return label, area, options, draw

# --- GAME INTERFACE ---
if st.session_state.q_no <= 50:
    if 'current_q' not in st.session_state:
        st.session_state.current_q = generate_question()

    label, correct_area, opts, svg = st.session_state.current_q

    st.markdown(f"<h2 style='text-align:center; color:#1e293b;'>ප්‍රශ්නය {st.session_state.q_no} / 50</h2>", unsafe_allow_html=True)
    
    # Progress Bar
    st.progress(st.session_state.q_no / 50)
    
    st.info(label)

    # ප්‍රදර්ශනය කරන කොටස
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f'<div class="shape-container">{svg}</div>', unsafe_allow_html=True)

    st.write("### නිවැරදි වර්ගඵලය තෝරන්න:")
    cols = st.columns(2)
    
    for i, opt in enumerate(opts):
        with cols[i % 2]:
            if st.button(f"{opt} cm²", key=f"ans_{i}"):
                if opt == correct_area:
                    placeholder.markdown(f'<div class="shape-container"><div class="dance-shape">{svg}</div><br><h2 style="color:#16a34a;">නිවැරදියි! ඉතා විශිෂ්ටයි! 🕺🎉</h2></div>', unsafe_allow_html=True)
                    st.balloons()
                    st.markdown('<audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                    st.session_state.score += 1
                    time.sleep(2.5)
                else:
                    st.error(f"අයියෝ වැරදුනා! නිවැරදි පිළිතුර: {correct_area} cm²")
                    time.sleep(2)
                
                st.session_state.q_no += 1
                del st.session_state.current_q
                st.rerun()

else:
    st.balloons()
    st.success("සියලුම ප්‍රශ්න අවසන්!")
    st.header(f"ඔබේ අවසන් ලකුණු සංඛ්‍යාව: {st.session_state.score} / 50")
    if st.button("නැවත සෙල්ලම් කරන්න"):
        st.session_state.q_no = 1
        st.session_state.score = 0
        st.rerun()
