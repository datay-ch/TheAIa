import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import base64

# Configuration de la page
st.set_page_config(page_title="Théâtre AI", page_icon="🎭", layout="centered")

# Initialiser la base de données
Base = declarative_base()
DATABASE_URL = "sqlite:///theatre_ai.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Charger l'image en base64
def get_base64_image():
    logo_path = "logosaas.jpg"  # Assurez-vous que le logo est dans le même dossier que le script
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

logo_base64 = get_base64_image()

# Initialiser l'état des notifications
if "show_notifications" not in st.session_state:
    st.session_state.show_notifications = False

# Fonction pour basculer l'état des notifications
def toggle_notifications():
    st.session_state.show_notifications = not st.session_state.show_notifications

# CSS pour le style personnalisé
st.markdown(f"""
    <style>
    /* Barre de titre avec dégradé rose animé */
    .animated-bar {{
        width: 100%;
        height: 10px;
        background: linear-gradient(90deg, #ff5f6d, #ffc371);
        background-size: 200% 200%;
        animation: gradient-animation 3s ease infinite;
        border-radius: 15px;
        margin-bottom: 20px;
    }}

    @keyframes gradient-animation {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Style pour le titre avec dégradé animé dynamique */
    .gradient-title {{
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(270deg, #ff5f6d, #ffc371, #ff5f6d);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: dynamic-gradient 6s ease infinite;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .title-logo {{
        width: 30px;
        height: auto;
        margin-left: 10px;
    }}

    /* Cloche de notification stylisée */
    .notification {{
        position: relative;
        display: inline-block;
        cursor: pointer;
        font-size: 1.1em;
        margin-left: 15px;
        color: #ff5f6d;
    }}

    /* Badge de notification */
    .notification .badge {{
        position: absolute;
        top: -5px;
        right: -5px;
        padding: 5px;
        border-radius: 50%;
        background-color: #ff5f6d;
        color: white;
        font-size: 0.7em;
        font-weight: bold;
    }}

    /* Popup de notification */
    .popup {{
        position: absolute;
        top: 35px;
        right: -10px;
        width: 300px;
        padding: 15px;
        background-color: rgba(0, 0, 0, 0.9); /* Fond semi-transparent */
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        color: white;
        font-size: 0.9em;
        z-index: 10;
    }}
    .popup p {{
        font-weight: bold;
        margin-top: 0;
        color: #ff5f6d;
    }}
    .popup ul {{
        list-style: none;
        padding: 0;
        color: #fff;
    }}
    .popup ul li {{
        padding: 8px 0;
        border-bottom: 1px solid #666;
    }}
    .popup ul li:last-child {{
        border-bottom: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# Fonction pour afficher un titre avec logo et icône de notification
def afficher_titre_avec_logo(titre, username):
    st.markdown("<div class='animated-bar'></div>", unsafe_allow_html=True)
    # Afficher la cloche de notification et le bouton de toggle
    st.markdown(f"""
        <h1 class='gradient-title'>
            {titre} <img src='data:image/jpg;base64,{logo_base64}' alt='logo' class='title-logo'/>
            <div class="notification" title="Notifications" onclick="document.getElementById('notif-button').click();">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-bell-fill" viewBox="0 0 16 16">
                    <path d="M8 16a2 2 0 0 0 1.985-1.75H6.016A2 2 0 0 0 8 16zm.104-1.793a2.5 2.5 0 0 1-1.208-2.89A6.002 6.002 0 0 1 2 9V6.5a5.5 5.5 0 1 1 11 0V9c0 1.538-.747 2.926-1.9 3.617a2.5 2.5 0 0 1-1.208 2.89h-1.888z"/>
                </svg>
                <span class="badge">3</span>
            </div>
        </h1>
    """, unsafe_allow_html=True)

    # Bouton caché pour déclencher le changement d'état des notifications
    if st.button("Afficher/Masquer Notifications", key="notif-button", on_click=toggle_notifications):
        pass

    # Afficher les notifications si l'état est activé
    if st.session_state.show_notifications:
        st.markdown("""
            <div class="popup">
                <p>Bonjour {username}</p>
                <ul>
                    <li>🎉 Nouvelle mise à jour : explorez nos dernières fonctionnalités !</li>
                    <li>🕒 Votre création est en cours de traitement et sera prête sous peu.</li>
                    <li>🌟 N'oubliez pas de visiter la galerie pour voir les nouvelles pièces.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Le reste du code est inchangé...

# Définition des modèles de la base de données (inchangée)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    creations = relationship("Creation", back_populates="user")

class Creation(Base):
    __tablename__ = 'creations'
    id = Column(Integer, primary_key=True)
    theme = Column(String, nullable=False)
    era = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="creations")

Base.metadata.create_all(engine)

# Initialisation de l'état de l'application (inchangée)
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None
if "page" not in st.session_state:
    st.session_state.page = "connexion"

# Fonctions d'inscription et d'authentification (inchangées)
def authenticate(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user

def signup(username, password, email, first_name, last_name, phone):
    if session.query(User).filter_by(username=username).first():
        st.error("Ce nom d'utilisateur est déjà pris.")
        return False
    if session.query(User).filter_by(email=email).first():
        st.error("Cet email est déjà utilisé.")
        return False
    
    new_user = User(username=username, password=password, email=email,
                    first_name=first_name, last_name=last_name, phone=phone)
    session.add(new_user)
    session.commit()
    return True

# Page d'inscription
def afficher_page_inscription():
    afficher_titre_avec_logo("Créer un Compte", "")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    email = st.text_input("Adresse e-mail")
    first_name = st.text_input("Prénom")
    last_name = st.text_input("Nom")
    phone = st.text_input("Numéro de téléphone")
    if st.button("S'inscrire"):
        if signup(username, password, email, first_name, last_name, phone):
            st.success("Compte créé avec succès. Veuillez vous connecter.")
            st.session_state.page = "connexion"
        else:
            st.error("Erreur lors de la création du compte. Veuillez vérifier les informations saisies.")

# Le reste du code inchangé
