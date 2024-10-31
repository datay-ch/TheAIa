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

    @keyframes dynamic-gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Style sans bordure pour les boutons */
    .stButton>button {{
        color: #ff5f6d;
        background-color: transparent;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .stButton>button:hover {{
        background-color: #ff5f6d;
        color: white;
    }}

    /* Pied de page */
    .footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        color: #888;
    }}

    /* Responsivité pour mobile */
    @media (max-width: 768px) {{
        .gradient-title {{
            font-size: 1.5em;
        }}
        .footer {{
            font-size: 12px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Fonction pour afficher un titre avec logo après le texte
def afficher_titre_avec_logo(titre):
    st.markdown("<div class='animated-bar'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <h1 class='gradient-title'>
            {titre} <img src='data:image/jpg;base64,{logo_base64}' alt='logo' class='title-logo'/>
        </h1>
    """, unsafe_allow_html=True)

# Définition des modèles de la base de données
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

# Initialisation de l'état de l'application
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None
if "page" not in st.session_state:
    st.session_state.page = "connexion"

# Fonctions d'inscription et d'authentification
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
    afficher_titre_avec_logo("Créer un Compte")
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

# Page de connexion avec un disclaimer
def afficher_page_connexion():
    afficher_titre_avec_logo("Bienvenue sur Théâtre AI")

    # Disclaimer
    st.write("### Bienvenue au Théâtre AI 🎭")
    st.write("Découvrez une nouvelle manière de créer, de partager et de découvrir des pièces de théâtre avec Théâtre AI. "
             "Inscrivez-vous pour accéder à toutes les fonctionnalités de création et de gestion de vos œuvres théâtrales.")

    # Champs de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    # Bouton de connexion
    if st.button("Se connecter"):
        user = authenticate(username, password)
        if user:
            st.session_state.authenticated_user = user
            st.session_state.page = "Créer une Pièce"
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

    # Bouton "Créer un compte" sous le bouton de connexion
    if st.button("Créer un compte"):
        st.session_state.page = "inscription"

# Page de création de pièce
def afficher_page_creation():
    afficher_titre_avec_logo("Créer une Nouvelle Pièce")
    user_id = st.session_state.authenticated_user.id
    with st.form(key="creation_form"):
        theme = st.text_input("Thème de la pièce")
        era = st.text_input("Époque souhaitée")
        description = st.text_area("Description de la pièce")
        submit_button = st.form_submit_button(label="Générer la pièce")
    if submit_button:
        new_creation = Creation(theme=theme, era=era, description=description, user_id=user_id)
        session.add(new_creation)
        session.commit()
        st.success("Votre création a été enregistrée dans la base de données !")

# Page de la galerie
def afficher_page_galerie():
    afficher_titre_avec_logo("Galerie de Pièces en PDF")
    st.write("Cliquez sur une pièce pour l'ouvrir dans un nouvel onglet.")
    pieces = [
        {"titre": "Les Dieux Réincarnés", "resume": "Dans un monde en déclin, les anciens dieux se battent contre des forces modernes qui menacent leur existence.", "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/dieux_reincarnes.pdf"},
        {"titre": "L'Artefact du Temps", "resume": "Un roi grec découvre un artefact mystérieux qui manipule le temps, bouleversant les civilisations qu’il explore.", "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/artefact_temps.pdf"},
        {"titre": "La Prophétie des Mages", "resume": "Dans un royaume lointain, la prophétie d’un mage annonce des bouleversements pour le futur.", "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/prophetie_mages.pdf"}
    ]
    for piece in pieces:
        st.markdown(f"### {piece['titre']}")
        st.write(piece["resume"])
        st.markdown(f"[📖 Ouvrir {piece['titre']}]({piece['lien']})", unsafe_allow_html=True)

# Page de l'historique
def afficher_page_historique():
    afficher_titre_avec_logo("Historique des Créations")
    user_id = st.session_state.authenticated_user.id
    creations = session.query(Creation).filter_by(user_id=user_id).all()
    if creations:
        for idx, creation in enumerate(creations):
            st.markdown(f"#### Création {idx + 1}")
            st.write(f"**Thème**: {creation.theme}")
            st.write(f"**Époque**: {creation.era}")
            st.write(f"**Description**: {creation.description}")
            st.write("---")
    else:
        st.write("Aucune création dans l'historique.")

# Navigation avec le menu latéral
if st.session_state.authenticated_user:
    st.sidebar.title("Menu")
    choix_page = st.sidebar.radio("Aller à", ["Créer une Pièce", "Galerie des Pièces", "Historique des Créations"])
    st.session_state.page = choix_page

    # Bouton Déconnexion en bas de la barre latérale
    st.sidebar.markdown("<div class='logout-button'>", unsafe_allow_html=True)
    st.sidebar.button("Déconnexion", key="logout", on_click=lambda: st.session_state.update(authenticated_user=None, page="connexion"))
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.page == "Créer une Pièce":
        afficher_page_creation()
    elif st.session_state.page == "Galerie des Pièces":
        afficher_page_galerie()
    elif st.session_state.page == "Historique des Créations":
        afficher_page_historique()
else:
    if st.session_state.page == "inscription":
        afficher_page_inscription()
    else:
        afficher_page_connexion()

# Afficher le pied de page en bas de la page
st.markdown("<div class='footer'>Tous droits réservés et créé par Aya Rochdi</div>", unsafe_allow_html=True)
