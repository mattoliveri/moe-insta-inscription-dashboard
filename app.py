import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="MOE - Inscriptions × Instagram",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Système d'authentification
def check_login():
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get('authenticated', False)

def login_page():
    """Affiche la page de connexion"""
    st.title("🔐 Connexion MOE Dashboard")
    st.markdown("---")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.subheader("Accès sécurisé")
            
            with st.form("login_form"):
                username = st.text_input("Nom d'utilisateur", placeholder="admin")
                password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
                submit_button = st.form_submit_button("Se connecter", use_container_width=True)
                
                if submit_button:
                    # Récupération des identifiants depuis secrets.toml à la racine ou valeurs par défaut
                    try:
                        import toml
                        secrets = toml.load("secrets.toml")
                        admin_user = secrets.get("auth", {}).get("username", "admin")
                        admin_pass = secrets.get("auth", {}).get("password", "AdminMOE13")
                    except (FileNotFoundError, ImportError):
                        # Valeurs par défaut si le fichier secrets.toml n'existe pas
                        admin_user = "admin"
                        admin_pass = "AdminMOE13"
                    
                    if username == admin_user and password == admin_pass:
                        st.session_state['authenticated'] = True
                        st.success("Connexion réussie ! Redirection en cours...")
                        st.rerun()
                    else:
                        st.error("Nom d'utilisateur ou mot de passe incorrect")
            
            st.markdown("---")
            st.caption("Dashboard MOE - Accès administrateur requis")

def logout():
    """Déconnecte l'utilisateur"""
    st.session_state['authenticated'] = False
    st.rerun()

# Vérification de l'authentification
if not check_login():
    login_page()
    st.stop()

# Configuration locale
TIMEZONE = pytz.timezone('Europe/Paris')

# Chemins des fichiers (à la racine du projet)
INSTAGRAM_CSV = "insta_data.csv"
REG_CSV = "data_registration_moe.csv"

# Fonctions utilitaires
def format_number(n):
    """Formate les nombres avec séparateur de milliers"""
    return f"{int(n):,}".replace(",", " ")

def format_percent(n):
    """Formate les pourcentages"""
    return f"{n:.1f}%"

def mask_email(email):
    """Masque les emails pour la protection des données"""
    if pd.isna(email):
        return email
    parts = email.split('@')
    if len(parts) != 2:
        return email
    username, domain = parts
    masked_username = username[:3] + '•' * (len(username) - 3)
    return f"{masked_username}@{domain}"

def mask_phone(phone):
    """Masque les numéros de téléphone pour la protection des données"""
    if pd.isna(phone):
        return phone
    phone = str(phone).replace(' ', '')
    if len(phone) < 4:
        return phone
    return phone[:2] + '•' * (len(phone) - 4) + phone[-2:]

# Chargement des données
@st.cache_data
def load_data():
    try:
        # Lecture des données Instagram
        df_insta = pd.read_csv(INSTAGRAM_CSV, sep=';')
        
        # Conversion des dates Instagram
        df_insta['date'] = pd.to_datetime(df_insta['Date']).dt.date
        df_insta['timestamp'] = pd.to_datetime(df_insta['Date'] + ' ' + df_insta['Heure'].fillna('12:00'))
        
        # Lecture des données d'inscription
        df_reg = pd.read_csv(REG_CSV, sep=';')
        
        # Conversion des dates d'inscription
        df_reg['date'] = pd.to_datetime(df_reg['DATE INSCRIPTION']).dt.date
        df_reg['timestamp'] = pd.to_datetime(df_reg['DATE INSCRIPTION'])
        
        # Extraction du parcours (5, 12 ou 21)
        df_reg['parcours'] = df_reg['PARCOURS'].str.extract(r'(\d+)').astype(float)
        
        # Flags
        df_reg['is_paid'] = df_reg['PAIEMENT'].str.upper().isin(['PAYE', 'OK', 'VALIDÉ', 'OUI', '1', 'TRUE'])
        df_reg['has_licence'] = df_reg['FEDERATION'].notna() | df_reg['Numéro de licence'].notna()
        df_reg['is_handisport'] = df_reg['HANDISPORT'].str.upper().isin(['OUI', '1', 'TRUE'])
        
        return df_insta, df_reg
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        return None, None

# Chargement des données
df_insta, df_reg = load_data()

if df_insta is None or df_reg is None:
    st.error("Impossible de charger les données. Vérifiez que les fichiers CSV sont présents à la racine du projet.")
    st.stop()

# Filtres globaux (sidebar)
with st.sidebar:
    # Bouton de déconnexion
    st.markdown("---")
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout()
    st.markdown("---")
    
    st.header("Filtres")
    
    # Période d'inscription
    st.subheader("Période d'inscription")
    min_date = df_reg['date'].min()
    max_date = df_reg['date'].max()
    date_range = st.date_input(
        "Plage de dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_reg = df_reg[
            (df_reg['date'] >= start_date) &
            (df_reg['date'] <= end_date)
        ]
    
    # Parcours
    st.subheader("Course")
    parcours_values = sorted(df_reg['parcours'].unique())
    parcours_options = ['Tous'] + [f"{int(x)}K" for x in parcours_values]
    parcours_selected = st.selectbox("Parcours", parcours_options)
    if parcours_selected != 'Tous':
        parcours_km = float(parcours_selected.replace('K', ''))
        df_reg = df_reg[df_reg['parcours'] == parcours_km]
    
    # Statut
    st.subheader("Statut")
    
    # Paiement
    paiement_status = st.radio(
        "Paiement",
        ["Tous", "Payé", "Non payé"],
        horizontal=True
    )
    if paiement_status == "Payé":
        df_reg = df_reg[df_reg['is_paid']]
    elif paiement_status == "Non payé":
        df_reg = df_reg[~df_reg['is_paid']]
    
    # Licence
    licence_status = st.radio(
        "Licence",
        ["Tous", "Avec licence", "Sans licence"],
        horizontal=True
    )
    if licence_status == "Avec licence":
        df_reg = df_reg[df_reg['has_licence']]
    elif licence_status == "Sans licence":
        df_reg = df_reg[~df_reg['has_licence']]
    
    # Handisport
    handisport_status = st.radio(
        "Handisport",
        ["Tous", "Oui", "Non"],
        horizontal=True
    )
    if handisport_status == "Oui":
        df_reg = df_reg[df_reg['is_handisport']]
    elif handisport_status == "Non":
        df_reg = df_reg[~df_reg['is_handisport']]
    
    # Filtres Instagram (pour onglets Impact & Charts)
    st.subheader("Filtres Instagram")
    
    # Dates posts
    min_date_post = df_insta['date'].min()
    max_date_post = df_insta['date'].max()
    date_range_post = st.date_input(
        "Plage de dates posts",
        value=(min_date_post, max_date_post),
        min_value=min_date_post,
        max_value=max_date_post,
        key="date_range_post"
    )
    if len(date_range_post) == 2:
        start_date_post, end_date_post = date_range_post
        df_insta = df_insta[
            (df_insta['date'] >= start_date_post) &
            (df_insta['date'] <= end_date_post)
        ]
    
    # Type de post
    type_options = ['Tous'] + sorted(df_insta['Type'].unique().tolist())
    type_selected = st.selectbox("Type de post", type_options)
    if type_selected != 'Tous':
        df_insta = df_insta[df_insta['Type'] == type_selected]

# Interface utilisateur
st.title("MOE - Inscriptions × Instagram")
st.caption("Panel d'analyse des inscriptions et de l'impact de la communication Instagram")

# Création des onglets
tab_overview, tab_inscriptions, tab_impact, tab_charts, tab_explorer = st.tabs([
    "Overview",
    "Inscriptions",
    "Impact Com × Inscriptions",
    "Charts",
    "Explorer"
])

# Onglet Overview
with tab_overview:
    st.header("Vue d'ensemble")
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_inscr = len(df_reg)
        total_paid = df_reg['is_paid'].sum()
        st.metric(
            "Total inscriptions",
            format_number(total_inscr),
            format_percent(total_paid / total_inscr * 100) if total_inscr > 0 else "0%"
        )
    
    with col2:
        inscr_5k = len(df_reg[df_reg['parcours'] == 5])
        st.metric(
            "5K",
            format_number(inscr_5k),
            format_percent(inscr_5k / total_inscr * 100) if total_inscr > 0 else "0%"
        )
    
    with col3:
        inscr_12k = len(df_reg[df_reg['parcours'] == 12])
        st.metric(
            "12K",
            format_number(inscr_12k),
            format_percent(inscr_12k / total_inscr * 100) if total_inscr > 0 else "0%"
        )
    
    with col4:
        inscr_21k = len(df_reg[df_reg['parcours'] == 21])
        st.metric(
            "21K",
            format_number(inscr_21k),
            format_percent(inscr_21k / total_inscr * 100) if total_inscr > 0 else "0%"
        )
    
    with col5:
        licencies = df_reg['has_licence'].sum()
        st.metric(
            "Licenciés",
            format_number(licencies),
            format_percent(licencies / total_inscr * 100) if total_inscr > 0 else "0%"
        )
    
    # Évolution temporelle
    st.subheader("Évolution temporelle")
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        # Sélection de la métrique Instagram
        insta_metrics = {
            'Vues': 'Vues',
            'Likes': 'Likes',
            'Commentaires': 'Commentaires',
            'Partage': 'Partages',
            'Clics sur le lien': 'Clics liens',
            'Enregistrements': 'Enregistrements'
        }
        available_metrics = [m for m in insta_metrics.keys() if m in df_insta.columns]
        if not available_metrics:
            st.error("Aucune métrique Instagram disponible dans les données")
            st.stop()
        
        selected_metric = st.selectbox(
            "Métrique Instagram",
            options=available_metrics
        )
    
    with col2:
        # Type d'agrégation
        agg_type = st.radio(
            "Type d'agrégation",
            options=["Somme", "Moyenne mobile 7j"],
            horizontal=True
        )
    
    # Préparation des données
    daily_reg = df_reg.groupby('date').size().reset_index(name='inscriptions')
    
    # Conversion des valeurs Instagram en nombres (gestion des virgules)
    try:
        # Vérifier que les colonnes existent
        if selected_metric not in df_insta.columns:
            st.error(f"La colonne '{selected_metric}' n'existe pas dans les données Instagram")
            st.write("Colonnes disponibles:", list(df_insta.columns))
            st.stop()
        
        # Nettoyer et convertir les données
        df_insta_clean = df_insta.copy()
        
        # Debug: afficher quelques valeurs pour diagnostiquer
        st.write(f"Échantillon de données pour {selected_metric}:")
        st.write(df_insta_clean[selected_metric].head())
        
        df_insta_clean[selected_metric] = pd.to_numeric(
            df_insta_clean[selected_metric].astype(str).str.replace(',', '.').str.replace(' ', ''),
            errors='coerce'
        ).fillna(0)
        
        daily_insta = df_insta_clean.groupby('date')[selected_metric].sum().reset_index()
        
        # Vérifier que nous avons des données après traitement
        if daily_insta.empty or daily_insta[selected_metric].sum() == 0:
            st.warning(f"Aucune donnée valide trouvée pour {selected_metric}")
            st.stop()
            
    except Exception as e:
        st.error(f"Erreur lors du traitement des données Instagram : {str(e)}")
        st.write("Colonnes dans df_insta:", list(df_insta.columns))
        st.stop()
    
    # Tri par date
    daily_reg = daily_reg.sort_values('date')
    daily_insta = daily_insta.sort_values('date')
    
    # Application de l'agrégation choisie
    if agg_type == "Moyenne mobile 7j":
        daily_reg['inscriptions'] = daily_reg['inscriptions'].rolling(window=7, min_periods=1).mean()
        daily_insta[selected_metric] = daily_insta[selected_metric].rolling(window=7, min_periods=1).mean()
    
    # Création du graphique
    try:
        fig = go.Figure()
        
        # Vérifier que les données ne sont pas vides
        if daily_reg.empty or daily_insta.empty:
            st.warning("Pas de données disponibles pour créer le graphique")
            st.stop()
        
        # Courbe des inscriptions
        fig.add_trace(
            go.Scatter(
                x=daily_reg['date'],
                y=daily_reg['inscriptions'],
                name="Inscriptions",
                line=dict(color='#FF4B4B', width=3),
                mode='lines',
                yaxis='y',
                hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Inscriptions: %{y:.0f}<extra></extra>"
            )
        )
        
        # Courbe de la métrique Instagram
        fig.add_trace(
            go.Scatter(
                x=daily_insta['date'],
                y=daily_insta[selected_metric],
                name=selected_metric,
                line=dict(color='#636EFA', width=3),
                mode='lines',
                yaxis='y2',
                hovertemplate=f"<b>%{{x|%d/%m/%Y}}</b><br>{selected_metric}: %{{y:.0f}}<extra></extra>"
            )
        )
        # Mise en page
        fig.update_layout(
            title=dict(
                text=f"Évolution des inscriptions et {selected_metric.lower()} ({agg_type.lower()})",
                font=dict(size=20)
            ),
            xaxis=dict(
                title="Date",
                tickformat='%d/%m/%Y',
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            yaxis=dict(
                title="Nombre d'inscriptions",
                titlefont=dict(color='#FF4B4B'),
                tickfont=dict(color='#FF4B4B'),
                showgrid=True,
                gridcolor='rgba(255, 75, 75, 0.1)'
            ),
            yaxis2=dict(
                title=selected_metric,
                titlefont=dict(color='#636EFA'),
                tickfont=dict(color='#636EFA'),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template="plotly_white",
            height=500,
            hovermode='x unified',
            # Ajout des boutons de téléchargement
            modebar=dict(
                bgcolor='rgba(0,0,0,0)',
                color='#636EFA',
                activecolor='#FF4B4B',
                add=['downloadImage']
            )
        )
        
        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique : {str(e)}")
        st.warning("Problème avec les données. Vérifiez le format des colonnes dans les fichiers CSV.")
        st.stop()


# Onglet Inscriptions
with tab_inscriptions:
    st.header("Analyse des inscriptions")
    
    # Répartitions principales
    st.subheader("Répartition des inscriptions")
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par parcours
        parcours_data = df_reg['parcours'].value_counts().reset_index()
        parcours_data.columns = ['parcours', 'count']
        parcours_data['parcours'] = parcours_data['parcours'].astype(str) + 'K'
        
        fig_parcours = px.pie(
            parcours_data,
            values='count',
            names='parcours',
            title="Répartition par parcours",
            hole=0.4,
            template="plotly_white"
        )
        
        # Configuration de la barre d'outils
        fig_parcours.update_layout(
            modebar=dict(
                bgcolor='rgba(0,0,0,0)',
                color='#636EFA',
                activecolor='#FF4B4B',
                add=['downloadImage']
            )
        )
        
        st.plotly_chart(fig_parcours, use_container_width=True)
        
        # Export données
        st.download_button(
            "💾 Télécharger données parcours",
            parcours_data.to_csv(index=False).encode('utf-8'),
            "repartition_parcours.csv",
            "text/csv"
        )
    
    with col2:
        # Répartition par statut de paiement
        payment_data = df_reg.groupby('is_paid').size().reset_index()
        payment_data.columns = ['status', 'count']
        payment_data['status'] = payment_data['status'].map({True: 'Payé', False: 'Non payé'})
        
        fig_payment = px.pie(
            payment_data,
            values='count',
            names='status',
            title="Statut des paiements",
            hole=0.4,
            template="plotly_white"
        )
        st.plotly_chart(fig_payment, use_container_width=True)
        
        # Export données
        st.download_button(
            "💾 Télécharger données paiement",
            payment_data.to_csv(index=False).encode('utf-8'),
            "statut_paiement.csv",
            "text/csv"
        )
    
    # Évolution temporelle par parcours
    st.subheader("Évolution des inscriptions")
    
    # Sélecteur de granularité
    time_granularity = st.radio(
        "Granularité temporelle",
        ["Jour", "Semaine", "Mois"],
        horizontal=True
    )
    
    # Préparation des données selon la granularité
    if time_granularity == "Jour":
        time_group = df_reg['date']
    elif time_granularity == "Semaine":
        time_group = df_reg['timestamp'].dt.isocalendar().week
    else:  # Mois
        time_group = df_reg['timestamp'].dt.month
    
    evolution_data = df_reg.groupby([time_group, 'parcours']).size().reset_index()
    evolution_data.columns = ['periode', 'parcours', 'inscriptions']
    evolution_data['parcours'] = evolution_data['parcours'].astype(str) + 'K'
    
    fig_evolution = px.line(
        evolution_data,
        x='periode',
        y='inscriptions',
        color='parcours',
        title=f"Évolution des inscriptions par {time_granularity.lower()}",
        template="plotly_dark"
    )
    
    fig_evolution.update_layout(
        xaxis_title=time_granularity,
        yaxis_title="Nombre d'inscriptions",
        height=400,
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
            color='#636EFA',
            activecolor='#FF4B4B',
            add=['downloadImage']
        )
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Export données
    st.download_button(
        "💾 Télécharger données évolution",
        evolution_data.to_csv(index=False).encode('utf-8'),
        f"evolution_inscriptions_{time_granularity.lower()}.csv",
        "text/csv"
    )
    
    # Analyse des paiements par parcours
    st.subheader("Analyse des paiements")
    
    payment_by_course = df_reg.groupby('parcours').agg({
        'is_paid': ['count', 'sum']
    }).reset_index()
    
    payment_by_course.columns = ['parcours', 'total', 'payes']
    payment_by_course['taux_paiement'] = (payment_by_course['payes'] / payment_by_course['total'] * 100)
    payment_by_course['parcours'] = payment_by_course['parcours'].astype(str) + 'K'
    
    fig_payment_course = px.bar(
        payment_by_course,
        x='parcours',
        y='taux_paiement',
        title="Taux de paiement par parcours",
        text=payment_by_course['taux_paiement'].apply(lambda x: f"{x:.1f}%"),
        template="plotly_dark"
    )
    
    fig_payment_course.update_layout(
        xaxis_title="Parcours",
        yaxis_title="Taux de paiement (%)",
        height=400,
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
            color='#636EFA',
            activecolor='#FF4B4B',
            add=['downloadImage']
        )
    )
    
    st.plotly_chart(fig_payment_course, use_container_width=True)
    
    # Export données
    st.download_button(
        "💾 Télécharger données paiement par parcours",
        payment_by_course.to_csv(index=False).encode('utf-8'),
        "paiement_par_parcours.csv",
        "text/csv"
    )

# Onglet Impact Com × Inscriptions
with tab_impact:
    st.header("Impact de la communication Instagram")
    
    # Sélection de la fenêtre d'analyse
    st.subheader("Fenêtre d'analyse")
    window_hours = st.selectbox(
        "Période d'analyse après chaque post",
        ["0-24h", "24-48h", "48-72h"],
        index=0
    )
    
    # Conversion de la sélection en heures
    if window_hours == "0-24h":
        start_hours, end_hours = 0, 24
    elif window_hours == "24-48h":
        start_hours, end_hours = 24, 48
    else:
        start_hours, end_hours = 48, 72
    
    # Analyse de l'impact pour chaque post
    impact_data = []
    for _, post in df_insta.iterrows():
        post_time = post['timestamp']
        window_start = post_time + pd.Timedelta(hours=start_hours)
        window_end = post_time + pd.Timedelta(hours=end_hours)
        
        # Inscriptions dans la fenêtre
        inscr_window = df_reg[
            (df_reg['timestamp'] >= window_start) &
            (df_reg['timestamp'] < window_end)
        ]
        
        # Baseline : même jour de la semaine sur ±4 semaines (hors fenêtre d'impact)
        day_of_week = post_time.day_name()
        baseline_period_start = post_time - pd.Timedelta(weeks=4)
        baseline_period_end = post_time + pd.Timedelta(weeks=4)
        
        baseline_inscr = df_reg[
            (df_reg['timestamp'] >= baseline_period_start) &
            (df_reg['timestamp'] <= baseline_period_end) &
            (df_reg['timestamp'].dt.day_name() == day_of_week) &
            ~(
                (df_reg['timestamp'] >= (post_time - pd.Timedelta(hours=72))) &
                (df_reg['timestamp'] <= (post_time + pd.Timedelta(hours=72)))
            )
        ]
        
        baseline_daily_avg = len(baseline_inscr) / 8  # 8 semaines de référence
        
        impact_data.append({
            'date_post': post_time.date(),
            'type': post['Type'],
            'titre': post['Titre'],
            'vues': post['Vues'],
            'likes': post['Likes'],
            'inscriptions_window': len(inscr_window),
            'baseline': baseline_daily_avg,
            'delta': len(inscr_window) - baseline_daily_avg,
            'delta_pct': ((len(inscr_window) - baseline_daily_avg) / baseline_daily_avg * 100) if baseline_daily_avg > 0 else 0
        })
    
    df_impact = pd.DataFrame(impact_data)
    
    # Affichage des top posts par impact
    st.subheader(f"Top posts par impact ({window_hours})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 posts positifs
        st.write("Meilleurs posts")
        top_posts = df_impact.nlargest(5, 'delta')[
            ['date_post', 'type', 'titre', 'vues', 'inscriptions_window', 'baseline', 'delta', 'delta_pct']
        ]
        
        fig_top = px.bar(
            top_posts,
            x='date_post',
            y='delta',
            text=top_posts['delta'].apply(lambda x: f"+{x:.0f}"),
            title="Top 5 posts à impact positif",
            template="plotly_white"
        )
        
        fig_top.update_layout(
                    xaxis_title="Date du post",
        yaxis_title="Delta inscriptions",
        height=400,
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
            color='#636EFA',
            activecolor='#FF4B4B',
            add=['downloadImage']
        )
        )
        
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Détails des top posts
        st.write("Détails des meilleurs posts :")
        for _, post in top_posts.iterrows():
            with st.expander(f"{post['date_post']} - {post['type']}"):
                st.write(f"Titre : {post['titre']}")
                st.write(f"Vues : {format_number(post['vues'])}")
                st.write(f"Inscriptions : {format_number(post['inscriptions_window'])} (baseline : {post['baseline']:.1f})")
                st.write(f"Impact : +{format_number(post['delta'])} (+{post['delta_pct']:.1f}%)")
    
    with col2:
        # Impact moyen par type de post
        st.write("Impact moyen par type de post")
        impact_by_type = df_impact.groupby('type').agg({
            'delta': 'mean',
            'delta_pct': 'mean'
        }).reset_index()
        
        fig_type = px.bar(
            impact_by_type,
            x='type',
            y='delta',
            text=impact_by_type['delta'].apply(lambda x: f"{x:+.1f}"),
            title="Impact moyen par type de post",
            template="plotly_white"
        )
        
        fig_type.update_layout(
                    xaxis_title="Type de post",
        yaxis_title="Delta moyen inscriptions",
        height=400,
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
            color='#636EFA',
            activecolor='#FF4B4B',
            add=['downloadImage']
        )
        )
        
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Export des données
    st.subheader("Export des données")
    
    st.download_button(
        "💾 Télécharger analyse impact par post",
        df_impact.to_csv(index=False).encode('utf-8'),
        "impact_posts.csv",
        "text/csv"
    )
    
    # Avertissement
    st.caption("Note : Cette analyse est purement descriptive et ne permet pas d'établir de liens de causalité.")

# Onglet Charts
with tab_charts:
    st.header("Graphiques personnalisables")
    
    # Sélection du dataset
    dataset = st.radio(
        "Sélectionner le dataset",
        ["Inscriptions", "Instagram"],
        horizontal=True
    )
    
    if dataset == "Inscriptions":
        # Ajout d'une colonne pour le comptage
        df = df_reg.copy()
        df['nombre'] = 1
        
        # Configuration des métriques disponibles
        metrics = {
            'nombre': 'Nombre d\'inscriptions',
            'is_paid': 'Taux de paiement',
            'has_licence': 'Taux de licence',
            'is_handisport': 'Taux handisport'
        }
        
        # Configuration des dimensions disponibles
        dimensions = {
            'parcours': 'Parcours',
            'date': 'Date',
            'jour_semaine': 'Jour de la semaine',
            'is_paid': 'Statut paiement',
            'has_licence': 'Statut licence',
            'is_handisport': 'Statut handisport'
        }
        
    else:  # Instagram
        # Configuration des métriques disponibles
        metrics = {
            'Vues': 'Vues',
            'Likes': 'Likes',
            'Commentaires': 'Commentaires',
            'Partage': 'Partages'
        }
        
        # Configuration des dimensions disponibles
        dimensions = {
            'Type': 'Type de post',
            'date': 'Date',
            'jour_semaine': 'Jour de la semaine'
        }
        
        df = df_insta
    
    # Configuration du graphique
    st.subheader("Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Sélection de la métrique
        selected_metric = st.selectbox(
            "Métrique à analyser",
            list(metrics.keys()),
            format_func=lambda x: metrics[x]
        )
        
        # Type d'agrégation
        agg_func = st.radio(
            "Type d'agrégation",
            ['sum', 'mean'],
            format_func=lambda x: 'Somme' if x == 'sum' else 'Moyenne',
            horizontal=True
        )
    
    with col2:
        # Sélection de la dimension
        selected_dimension = st.selectbox(
            "Dimension",
            list(dimensions.keys()),
            format_func=lambda x: dimensions[x]
        )
    
    with col3:
        # Type de graphique
        chart_type = st.radio(
            "Type de graphique",
            ['bar', 'line', 'pie'],
            format_func=lambda x: {
                'bar': 'Barres',
                'line': 'Lignes',
                'pie': 'Camembert'
            }[x],
            horizontal=True
        )
    
    # Préparation des données
    if dataset == "Inscriptions" and selected_metric in ['is_paid', 'has_licence', 'is_handisport']:
        # Pour les métriques booléennes, calculer le pourcentage
        if selected_dimension == 'date':
            agg_data = df.groupby('date').agg({
                selected_metric: ['count', 'sum']
            }).reset_index()
            agg_data['taux'] = (agg_data[(selected_metric, 'sum')] / agg_data[(selected_metric, 'count')] * 100)
            agg_data = agg_data[['date', 'taux']].rename(columns={'taux': selected_metric})
        else:
            agg_data = df.groupby(selected_dimension).agg({
                selected_metric: ['count', 'sum']
            }).reset_index()
            agg_data['taux'] = (agg_data[(selected_metric, 'sum')] / agg_data[(selected_metric, 'count')] * 100)
            agg_data = agg_data[[selected_dimension, 'taux']].rename(columns={'taux': selected_metric})
    else:
        # Pour les autres métriques, agrégation simple
        if selected_dimension == 'date':
            agg_data = df.groupby('date')[selected_metric].agg(agg_func).reset_index()
        else:
            agg_data = df.groupby(selected_dimension)[selected_metric].agg(agg_func).reset_index()
    
    # Création du graphique
    if chart_type == 'bar':
        fig = px.bar(
            agg_data,
            x=selected_dimension,
            y=selected_metric,
            title=f"{metrics[selected_metric]} par {dimensions[selected_dimension].lower()}",
            template="plotly_white"
        )
    elif chart_type == 'line':
        fig = px.line(
            agg_data,
            x=selected_dimension,
            y=selected_metric,
            title=f"Évolution {metrics[selected_metric].lower()}",
            template="plotly_white"
        )
    else:  # pie
        fig = px.pie(
            agg_data,
            values=selected_metric,
            names=selected_dimension,
            title=f"Répartition {metrics[selected_metric].lower()}",
            template="plotly_white"
        )
    
    # Mise en page
    fig.update_layout(
        xaxis_title=dimensions[selected_dimension],
        yaxis_title=metrics[selected_metric],
        height=500,
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
            color='#636EFA',
            activecolor='#FF4B4B',
            add=['downloadImage']
        )
    )
    
    # Affichage du graphique
    st.plotly_chart(fig, use_container_width=True)
    
    # Export des données
    st.subheader("Export des données")
    
    st.download_button(
        "💾 Télécharger les données",
        agg_data.to_csv(index=False).encode('utf-8'),
        f"analyse_{dataset.lower()}_{selected_metric}_{selected_dimension}.csv",
        "text/csv"
    )

# Onglet Explorer
with tab_explorer:
    st.header("Explorateur de données")
    
    # Sélection du dataset
    dataset_tabs = st.tabs(["Inscriptions", "Posts Instagram"])
    
    # Onglet Inscriptions
    with dataset_tabs[0]:
        st.subheader("Données d'inscription")
        
        # Préparation des données avec masquage PII
        df_display = df_reg.copy()
        
        # Masquage des données personnelles
        if 'NOM' in df_reg.columns:
            df_display['nom_masked'] = df_reg['NOM'].apply(lambda x: x[:1] + '•' * (len(str(x)) - 1) if pd.notna(x) else x)
        if 'PRENOM' in df_reg.columns:
            df_display['prenom_masked'] = df_reg['PRENOM'].apply(lambda x: x[:1] + '•' * (len(str(x)) - 1) if pd.notna(x) else x)
        if 'EMAIL' in df_reg.columns:
            df_display['email_masked'] = df_reg['EMAIL'].apply(mask_email)
        if 'TELEPHONE' in df_reg.columns:
            df_display['telephone_masked'] = df_reg['TELEPHONE'].apply(mask_phone)
        
        # Colonnes de base toujours présentes
        base_columns = ['parcours', 'is_paid', 'has_licence', 'is_handisport']
        
        # Colonnes optionnelles avec mapping
        optional_columns = {
            'DATE INSCRIPTION': 'DATE INSCRIPTION',
            'CIVILITE': 'CIVILITE',
            'nom_masked': 'nom_masked',
            'prenom_masked': 'prenom_masked',
            'email_masked': 'email_masked',
            'telephone_masked': 'telephone_masked',
            'VILLE': 'VILLE',
            'departement_nom': 'departement_nom',
            'CLUB': 'CLUB',
            'PAIEMENT': 'PAIEMENT',
            'CODE PROMO': 'CODE PROMO'
        }
        
        # Construction de la liste finale des colonnes
        display_columns = base_columns + [col for col, orig in optional_columns.items() 
                                        if orig in df_display.columns]
        
        # Filtres de recherche
        st.write("Filtres de recherche")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            parcours_filter = st.multiselect(
                "Parcours",
                options=sorted(df_reg['parcours'].unique()),
                format_func=lambda x: f"{int(x)}K"
            )
        
        with col2:
            civilite_filter = st.multiselect(
                "Civilité",
                options=sorted(df_reg['CIVILITE'].unique()) if 'CIVILITE' in df_reg.columns else []
            )
        
        with col3:
            dept_filter = st.multiselect(
                "Département",
                options=sorted(df_reg['departement_nom'].unique()) if 'departement_nom' in df_reg.columns else []
            )
        
        # Application des filtres
        df_filtered = df_display.copy()
        if parcours_filter:
            df_filtered = df_filtered[df_filtered['parcours'].isin(parcours_filter)]
        if civilite_filter and 'CIVILITE' in df_reg.columns:
            df_filtered = df_filtered[df_filtered['CIVILITE'].isin(civilite_filter)]
        if dept_filter and 'departement_nom' in df_reg.columns:
            df_filtered = df_filtered[df_filtered['departement_nom'].isin(dept_filter)]
        
        # Configuration des colonnes pour l'affichage
        column_config = {
            'parcours': st.column_config.NumberColumn(
                "Parcours",
                format="%dK"
            ),
            'is_paid': st.column_config.CheckboxColumn("Payé"),
            'has_licence': st.column_config.CheckboxColumn("Licence"),
            'is_handisport': st.column_config.CheckboxColumn("Handisport")
        }
        
        if 'DATE INSCRIPTION' in df_filtered.columns:
            column_config['DATE INSCRIPTION'] = st.column_config.DatetimeColumn(
                "Date d'inscription",
                format="DD/MM/YYYY HH:mm"
            )
        
        # Affichage du tableau
        st.dataframe(
            df_filtered[display_columns],
            hide_index=True,
            column_config=column_config
        )
        
        # Export CSV
        st.download_button(
            "💾 Télécharger les données filtrées",
            df_filtered[display_columns].to_csv(index=False).encode('utf-8'),
            "inscriptions_filtrees.csv",
            "text/csv"
        )
    
    # Onglet Posts Instagram
    with dataset_tabs[1]:
        st.subheader("Posts Instagram")
        
        # Vérification des colonnes disponibles
        insta_columns = [col for col in [
            'date',
            'Type',
            'Titre',
            'Contenue',
            'Periode',
            'Vues',
            'Likes',
            'Commentaires',
            'Partage',
            'hashtags'
        ] if col in df_insta.columns]
        
        # Filtres de recherche
        st.write("Filtres de recherche")
        col1, col2 = st.columns(2)
        
        with col1:
            type_filter = st.multiselect(
                "Type de post",
                options=sorted(df_insta['Type'].unique()) if 'Type' in df_insta.columns else []
            )
        
        with col2:
            periode_filter = st.multiselect(
                "Période",
                options=sorted(df_insta['Periode'].unique()) if 'Periode' in df_insta.columns else []
            )
        
        # Application des filtres
        df_insta_filtered = df_insta.copy()
        if type_filter and 'Type' in df_insta.columns:
            df_insta_filtered = df_insta_filtered[df_insta_filtered['Type'].isin(type_filter)]
        if periode_filter and 'Periode' in df_insta.columns:
            df_insta_filtered = df_insta_filtered[df_insta_filtered['Periode'].isin(periode_filter)]
        
        # Configuration des colonnes numériques
        numeric_config = {
            col: st.column_config.NumberColumn(col, format="%d")
            for col in ['Vues', 'Likes', 'Commentaires', 'Partage']
            if col in insta_columns
        }
        
        # Configuration de la colonne date
        if 'date' in insta_columns:
            numeric_config['date'] = st.column_config.DatetimeColumn(
                "Date",
                format="DD/MM/YYYY"
            )
        
        # Affichage du tableau
        st.dataframe(
            df_insta_filtered[insta_columns],
            hide_index=True,
            column_config=numeric_config
        )
        
        # Export CSV
        st.download_button(
            "💾 Télécharger les données filtrées",
            df_insta_filtered[insta_columns].to_csv(index=False).encode('utf-8'),
            "posts_instagram_filtres.csv",
            "text/csv"
        )
