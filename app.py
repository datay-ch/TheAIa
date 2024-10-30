import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Configuration de la page
st.set_page_config(page_title="Théâtre AI", page_icon="🎭", layout="centered")

# Initialiser la base de données
Base = declarative_base()
DATABASE_URL = "sqlite:///theatre_ai.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Définir les modèles de la base de données
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

# CSS pour le style personnalisé
st.markdown("""
    <style>
    /* Barre de titre avec dégradé rose */
    .header-bar {
        background: linear-gradient(to right, #ff5f6d, #ffc371);
        padding: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 15px;
        margin-bottom: 15px;
        position: relative;
    }
    
    /* Icône de déconnexion en haut à droite */
    .logout-icon {
        position: absolute;
        right: 10px;
        top: 10px;
        color: white;
        font-size: 20px;
        cursor: pointer;
    }
    
    /* Style général sombre */
    body, .main-content, .reportview-container, .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }

    /* Bouton stylisé type iOS vide à l'intérieur */
    .stButton>button {
        color: #ff5f6d;
        border: 2px solid #ff5f6d;
        background-color: transparent;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stButton>button:hover {
        background-color: #ff5f6d;
        color: white;
    }

    /* Style des cartes de galerie */
    .gallery-card {
        background-color: #34495e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
    }
    .gallery-title {
        font-size: 1.5em;
        color: #ffc371;
    }

    /* Lien cliquable pour inscription avec icône en haut à droite */
    .signup-link {
        position: absolute;
        top: 20px;
        right: 20px;
        color: #ff5f6d;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    .signup-link i {
        margin-right: 5px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# Barre de titre avec dégradé rose
st.markdown("<div class='header-bar'>Bienvenue au Théâtre AI</div>", unsafe_allow_html=True)

# Fonction d'affichage de l'icône de déconnexion
def afficher_icone_deconnexion():
    if st.button("Déconnexion"):
        st.session_state.authenticated_user = None
        st.session_state.page = "connexion"

# Page d'inscription
def afficher_page_inscription():
    st.markdown("<h1>Créer un Compte</h1>", unsafe_allow_html=True)
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

# Page de connexion
def afficher_page_connexion():
    st.markdown("<h1>Connexion</h1>", unsafe_allow_html=True)
    
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
    st.markdown("<h1>Créer une Nouvelle Pièce 🎭</h1>", unsafe_allow_html=True)
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



import streamlit as st

def afficher_page_galerie():
    st.markdown("<h1>Galerie de Pièces en PDF 🎭</h1>", unsafe_allow_html=True)
    st.write("Cliquez sur une pièce pour l'ouvrir dans un nouvel onglet.")

    # Liste des pièces avec le lien brut GitHub pour chaque PDF
    pieces = [
        {
            "titre": "Les Dieux Réincarnés",
            "resume": "Dans un monde en déclin, les anciens dieux se battent contre des forces modernes qui menacent leur existence.",
            "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/dieux_reincarnes.pdf"
        },
        {
            "titre": "L'Artefact du Temps",
            "resume": "Un roi grec découvre un artefact mystérieux qui manipule le temps, bouleversant les civilisations qu’il explore.",
            "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/artefact_temps.pdf"
        },
        {
            "titre": "La Prophétie des Mages",
            "resume": "Dans un royaume lointain, la prophétie d’un mage annonce des bouleversements pour le futur.",
            "lien": "https://raw.githubusercontent.com/BenJelloun-Youne/TheAIa/main/prophetie_mages.pdf"
        }
    ]

    for piece in pieces:
        st.markdown(f"### {piece['titre']}")
        st.write(piece["resume"])
        st.markdown(f"[📖 Ouvrir {piece['titre']}]({piece['lien']})", unsafe_allow_html=True)



# Page de l'historique
def afficher_page_historique():
    st.markdown("<h1>Historique des Créations</h1>", unsafe_allow_html=True)
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

# Navigation avec le menu et affichage des pages
if st.session_state.authenticated_user:
    afficher_icone_deconnexion()  # Affichage de l'icône de déconnexion
    st.sidebar.title("Menu")
    choix_page = st.sidebar.radio("Aller à", ["Créer une Pièce", "Galerie des Pièces", "Historique des Créations"])
    st.session_state.page = choix_page

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
