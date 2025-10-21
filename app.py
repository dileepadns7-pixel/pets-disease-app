import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import base64
import time

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="Pet Disease App", page_icon="🐾", layout="wide")

# -----------------------------
# Animated DNS Logo
# -----------------------------
st.markdown("""
    <style>
    @keyframes pulseGlow {
        0% { text-shadow: 0 0 10px #ff7f50, 0 0 20px #ff1493, 0 0 30px #1e90ff; }
        50% { text-shadow: 0 0 25px #ff1493, 0 0 35px #1e90ff, 0 0 45px #ff7f50; }
        100% { text-shadow: 0 0 10px #1e90ff, 0 0 20px #ff7f50, 0 0 30px #ff1493; }
    }
    .dns-logo {
        text-align: center;
        font-size: 70px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff7f50, #ff1493, #1e90ff, #00fa9a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulseGlow 2.5s infinite alternate, float 3s ease-in-out infinite;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-top: 25px;
        letter-spacing: 3px;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>

    <div class="dns-logo">🐾 D N S 🐾</div>
""", unsafe_allow_html=True)

# -----------------------------
# Splash / Loading Screen
# -----------------------------
with st.spinner("පිටුව load වෙමින් ඇත… කරුණාකර රැඳෙන්න…"):
    time.sleep(1)
    model = joblib.load("pet_model.pkl")
    le_pet = joblib.load("le_pet.pkl")
    feature_columns = joblib.load("feature_columns.pkl")
    data = pd.read_csv("pet_disease.csv")
    symptom_columns = data.columns.drop(["Pet_Type", "Disease"])

# -----------------------------
# Disease Info Dictionary
# -----------------------------
disease_info = {
    "Parvovirus": "මෙම වෛරස රෝගය බල්ලාට ශුන්‍ය සහ වමනය සිදු කරනව. ප්‍රතිකාර: රෝහල් සැලසුම්, දියර ලබාදීම.",
    "Canine Influenza": "බල්ලාගේ පිළිස්සීමේ වෛරස රෝගය. ලක්ෂණ: උණ, හුස්ම ගැනීමේ අපහසුතාව. ප්‍රතිකාර: සහාය කේයර්, වෙන්කිරීම.",
    "Feline Flu": "බළලාන් අතර පොදු සෙසු හිස් වෛරස රෝගය. ප්‍රතිකාර: සහාය කේයර්, දියර ලබාදීම, දෙවනිකර රෝග සඳහා ඇන්ටිබයෝටික්.",
    "Feline Panleukopenia": "ඉතා ආසාදනීය වෛරස රෝගය. ප්‍රතිකාර: රෝහල් සැලසුම්, දියර, සහාය කේයර්.",
    "Foot & Mouth": "වෙක්කු මට්ටමේ සෙසු වෛරස රෝගය, පාදයේ කැපීම් සහ නොහැකි වීම. ප්‍රතිකාර: සත්ත්ව වෛද්‍ය උපදෙස්, වෙන්කිරීම.",
    "Bovine Viral Diarrhea": "ගවයන උණ සහ විශාල වියළිවීම. ප්‍රතිකාර: සහාය කේයර්, වෛද්‍ය උපදෙස්.",
    "Generic Infection": "වෙනත් සත්ත්වයන් සඳහා නොපවතින විශේෂිත ආසාදනයක්. ප්‍රතිකාර: සත්ත්ව වෛද්‍ය මග පෙන්වීම.",
    "Unknown Virus": "හැඳින්විය නොහැකි වෛරස ආසාදනයක්. ප්‍රතිකාර: සත්ත්ව වෛද්‍ය උපදෙස්."
}

# -----------------------------
# Background Function
# -----------------------------
def add_bg_from_local(image_file):
    image_path = Path(image_file)
    if image_path.exists():
        with open(image_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                url("data:image/webp;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("<style>.stApp {{background-color: #2c3e50;}}</style>", unsafe_allow_html=True)

# -----------------------------
# Emergency Contact Form
# -----------------------------
def display_contact_options(is_emergency=False, show_alert=True):
    current_pet_type = st.session_state.get('pet_type', 'නැත')
    current_selected_symptoms = st.session_state.get('selected_symptoms', [])

    if is_emergency:
        title = "📞 හදිසි වෛද්‍යවරයකු සම්බන්ධ කර ගැනීමට"
        alert_msg = "🚨 **අධික ප්‍රමුඛතාවයක් සහිතයි!** වහාම පශු වෛද්‍යවරයකු වෙත ගෙන යන්න!"
        if show_alert:
            st.error(alert_msg)
    else:
        title = "📞 වෛද්‍යවරයකු සම්බන්ධ කර ගැනීමට"
        alert_msg = "🤷‍♀️ **රෝග තත්ත්වයක් හමු නොවීය.** කරුණාකර වෙට් වෛද්‍යවරයකු අමතන්න."
        if show_alert:
            st.warning(alert_msg)

    with st.expander(title, expanded=is_emergency):
        st.markdown("📞 **දුරකථන අංකය:** [071-XXXXXXX]")
        st.markdown("🌐 [Google Maps හරහා සායන සොයන්න](https://www.google.com/maps/search/veterinary+clinic+near+me)")

# -----------------------------
# PAGE NAVIGATION SYSTEM
# -----------------------------
menu = ["මුල් පිටුව", "රෝග පරීක්ෂකය (model-based prediction)", "හදිසි පිටුව"]

if "page" not in st.session_state:
    st.session_state.page = menu[0]

# --- TOP NAV BAR ---
st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        background-color: rgba(0,0,0,0.6);
        padding: 14px;
        border-radius: 15px;
        margin: 25px auto;
        width: 85%;
    }
    div[data-testid="stButton"] > button {
        background: none;
        color: white;
        border: none;
        font-size: 17px;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 8px;
        transition: 0.3s;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #ff7f50;
        color: white;
    }
    .active-btn {
        background-color: #1e90ff !important;
        color: white !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation Buttons ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
cols = st.columns(len(menu))
for i, page in enumerate(menu):
    if page == st.session_state.page:
        with cols[i]:
            st.markdown(f'<div class="active-btn" style="text-align:center;padding:8px 16px;">{page}</div>', unsafe_allow_html=True)
    else:
        with cols[i]:
            if st.button(page, key=f"nav_{i}"):
                st.session_state.page = page
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

choice = st.session_state.page

# -----------------------------
# PAGE CONTENT
# -----------------------------
add_bg_from_local("background.JPG")

if choice == "මුල් පිටුව":
    st.markdown("<h1 style='text-align:center; color:#FFD700;'>🐾 Pet Disease App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; font-size:18px;'>සත්ත්ව රෝග අනාවැකි සහ හදිසි උපදෙස් ලබා ගැනීම සඳහා මෙය භාවිතා කරන්න.</p>", unsafe_allow_html=True)

elif choice == "රෝග පරීක්ෂකය (model-based prediction)":
    st.title("🐾 රෝග පරීක්ෂකය (Model-Based Prediction)")
    pet_type = st.selectbox(
        "සත්ත්ව වර්ගය තෝරන්න",
        options=data["Pet_Type"].unique(),
        format_func=lambda x: "🐶 බල්ලා" if x=="Dog" else ("🐱 බළලා" if x=="Cat" else ("🐮 ගවය" if x=="Cow" else "🐾 වෙනත්")),
        key="pet_type_dropdown"
    )
    st.session_state['pet_type'] = pet_type

    st.write("ඔබේ සත්ත්වයාට ඇති ලක්ෂණ තෝරන්න:")
    selected_symptoms = []
    cols = st.columns(3)
    for i, symptom in enumerate(symptom_columns):
        if cols[i % 3].checkbox(symptom, key=f"symptom_{i}"):
            selected_symptoms.append(symptom)
    st.session_state['selected_symptoms'] = selected_symptoms

    if st.button("රෝග අනාවැකි කරන්න"):
        if not selected_symptoms:
            st.warning("අවම එක ලක්ෂණයක් තෝරන්න!")
        else:
            pet_encoded = le_pet.transform([pet_type])[0]
            input_data = {col: 0 for col in feature_columns}
            for col in selected_symptoms:
                input_data[col] = 1
            input_data["Pet_Type"] = pet_encoded
            input_df = pd.DataFrame([input_data], columns=feature_columns)
            prediction = model.predict(input_df)[0]
            st.markdown(
                f"<h2 style='color:#FF4500; text-align:center;'>අනාවැකි කරන රෝගය: {prediction}</h2>"
                f"<p style='text-align:center;'>{disease_info.get(prediction, 'විස්තර නොමැත')}</p>",
                unsafe_allow_html=True
            )
            if prediction in ["Parvovirus", "Canine Influenza", "Feline Flu", "Feline Panleukopenia"]:
                display_contact_options(is_emergency=True)
            else:
                display_contact_options(is_emergency=False)

elif choice == "හදිසි පිටුව":
    st.title("🚨 හදිසි පිටුව")
    display_contact_options(is_emergency=True, show_alert=True)

# --- Improve Text Visibility on Dark Backgrounds ---
st.markdown("""
    <style>
    /* Make all text white and slightly glowing */
    label, .stMarkdown, p, span, div, h1, h2, h3, h4, h5 {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
    }

    /* Checkbox label fix */
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* Add semi-transparent dark overlay for better readability */
    .stApp {
        background-color: rgba(0,0,0,0.3);
        backdrop-filter: blur(1px);
    }
    </style>
""", unsafe_allow_html=True)
