import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# ---------- GLOBAL STYLE ----------
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.figsize": (5, 3),
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# -----------------------------
# PIE TYPE PROSPECT
# -----------------------------
def pie_prospect(kpis: dict):
    values = kpis["type_prospect_dist"]["values"]
    labels = kpis["type_prospect_dist"]["labels"]

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct='%1.0f%%',
        startangle=90,
        wedgeprops=dict(width=0.65),  # donut look
    )

    ax.axis('equal')
    plt.tight_layout()

    st.pyplot(fig)


# -----------------------------
# HISTO ADHERENTS
# -----------------------------
def histo_adhérents(kpis: dict):
    values = kpis["adherents_distribution"]

    fig, ax = plt.subplots()

    sns.barplot(x=list(range(len(values))), y=values, ax=ax)

    ax.set_title("Répartition adhérents")
    ax.set_xlabel("Tranches")
    ax.set_ylabel("Nombre")

    plt.tight_layout()

    st.pyplot(fig)


# -----------------------------
# HISTO FOLLOWERS
# -----------------------------
def histo_followers(kpis: dict):
    values = kpis["followers_distribution"]

    fig, ax = plt.subplots()

    sns.barplot(x=list(range(len(values))), y=values, ax=ax)

    ax.set_title("Répartition followers")
    ax.set_xlabel("Tranches")
    ax.set_ylabel("Nombre")

    plt.tight_layout()

    st.pyplot(fig)


# -----------------------------
# MAP PROSPECTS
# -----------------------------
def map_prospects(data):
    if data.empty:
        st.warning("Aucun prospect à afficher")
        return

    if "lat" not in data.columns or "lon" not in data.columns:
        st.error("Colonnes lat/lon absentes")
        return

    df = data.dropna(subset=["lat", "lon"])

    if df.empty:
        st.warning("Aucune coordonnée valide")
        return

    # center automatically
    center = [df["lat"].mean(), df["lon"].mean()]

    m = folium.Map(location=center, zoom_start=6)

    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        popup = f"""
        <b>{row.get('nom_structure','')}</b><br>
        {row.get('region','')}<br>
        {row.get('type_prospect','')}
        """

        folium.Marker(
            [row["lat"], row["lon"]],
            popup=popup
        ).add_to(cluster)

    st_folium(m, use_container_width=True, height=600)


# -----------------------------
# TREEMAP
# -----------------------------
def treemap_followers(kpis: dict):
    networks = kpis["followers_by_network"]

    pairs = [
        ("Facebook", networks["facebook"], "#1877F2"),
        ("Twitter", networks["twitter"], "#1DA1F2"),
        ("Instagram", networks["instagram"], "#E1306C"),
        ("YouTube", networks["youtube"], "#FF0000"),
        ("TikTok", networks["tiktok"], "#111111"),
    ]

    pairs = [(l, s, c) for l, s, c in pairs if s > 0]

    if not pairs:
        st.info("Aucun follower disponible")
        return

    pairs.sort(key=lambda x: x[1], reverse=True)

    labels = [f"{l}\n{s:,}" for l, s, _ in pairs]
    sizes = [s for _, s, _ in pairs]
    colors = [c for _, _, c in pairs]

    fig, ax = plt.subplots(figsize=(6, 4))

    squarify.plot(
        sizes=sizes,
        label=labels,
        color=colors,
        alpha=0.9,
        text_kwargs={"fontsize": 11, "color": "white", "weight": "bold"},
        ax=ax
    )

    ax.axis("off")
    plt.tight_layout()

    st.pyplot(fig)


# -----------------------------
# BAR STATUTS
# -----------------------------
def bar_statuts(kpis: dict):
    values = kpis["statut_dist"]["values"]
    labels = kpis["statut_dist"]["labels"]

    fig, ax = plt.subplots()

    sns.barplot(x=labels, y=values, palette="Blues_d", ax=ax)

    ax.set_ylabel("Nombre")

    plt.xticks(rotation=25)
    plt.tight_layout()

    st.pyplot(fig)


# -----------------------------
# WEBSITE PIE
# -----------------------------
def website_pie_chart(kpis: dict):
    with_web = kpis["website_with"]
    without_web = kpis["website_without"]

    fig, ax = plt.subplots()

    ax.pie(
        [with_web, without_web],
        labels=['Avec', 'Sans'],
        autopct='%1.0f%%',
        startangle=90,
        wedgeprops=dict(width=0.65),
    )

    ax.axis('equal')



    st.pyplot(fig)


# -----------------------------
# GAUGES
# -----------------------------
def gauge_accepte_com(kpis: dict):
    st.progress(kpis["acceptance_percentage"])


def gauge_non_contactés(kpis: dict):
    st.progress(kpis["non_contactes_percentage"])


def gauge_tel_manquants(kpis: dict):
    st.progress(kpis["tel_manquants_percentage"])


def gauge_mail_manquants(kpis: dict):
    st.progress(kpis["mail_manquants_percentage"])