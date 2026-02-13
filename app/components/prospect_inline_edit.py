from typing import Any, Dict, Optional
import streamlit as st

from services.prospects_api import update_prospect
from utils.validators import is_valid_email, is_valid_phone
from utils.constants import (
    TYPE_PROSPECT_OPTIONS,
    REGION_FRANCE_OPTIONS,
    DEPARTEMENT_OPTIONS,
    PAYS_OPTIONS,
    METHODE_CONTACT_OPTIONS,
)


def render_prospect_inline_edit(
    prospect: Dict[str, Any],
    *,
    key: str = "inline_edit",
) -> Optional[str]:
    """
    Formulaire d'édition inline d'un prospect.
    - Ne change pas de page.
    - Valide email/téléphone côté UI.
    - Gère le cas doublon (409) : stocke le conflit en session_state.
    """

    pid = prospect.get("prospect_id")
    if not pid:
        st.error("Prospect invalide : pas de prospect_id.")
        return None

    st.subheader("Modifier le prospect")

    # State doublon pour ce composant
    conflict_key = f"{key}_pending_conflict"
    payload_key = f"{key}_pending_payload"
    if conflict_key not in st.session_state:
        st.session_state[conflict_key] = None
    if payload_key not in st.session_state:
        st.session_state[payload_key] = None

    # Valeurs initiales
    init_nom_structure = prospect.get("nom_structure") or ""
    init_nom_contact = prospect.get("nom_contact") or ""
    init_type = prospect.get("type_prospect")
    init_ville = prospect.get("ville") or ""
    init_email = prospect.get("email") or ""
    init_tel = prospect.get("telephone") or ""
    init_site = prospect.get("sit_web") or ""

    init_region = prospect.get("region") or ""
    init_departement = prospect.get("departement") or ""
    init_pays = prospect.get("pays") or ""
    init_adresse = prospect.get("adresse") or ""

    init_accepte = bool(prospect.get("accepte_contact"))
    init_methode = prospect.get("methode_contact") or ""
    init_commentaires = prospect.get("commentaires") or ""

    init_fb = prospect.get("facebook") or ""
    init_fb_f = prospect.get("facebook_followers")
    init_x = prospect.get("x") or ""
    init_x_f = prospect.get("x_followers")
    init_ig = prospect.get("instagram") or ""
    init_ig_f = prospect.get("instagram_followers")
    init_tt = prospect.get("tictok") or ""
    init_tt_f = prospect.get("tictok_followers")
    init_yt = prospect.get("youtube") or ""
    init_yt_f = prospect.get("youtube_followers")

    # Index selectbox
    try:
        init_type_index = TYPE_PROSPECT_OPTIONS.index(init_type) if init_type else None
    except ValueError:
        init_type_index = None
    try:
        region_index = REGION_FRANCE_OPTIONS.index(init_region) if init_region else None
    except ValueError:
        region_index = None
    try:
        departement_index = DEPARTEMENT_OPTIONS.index(init_departement) if init_departement else None
    except ValueError:
        departement_index = None
    try:
        pays_index = PAYS_OPTIONS.index(init_pays) if init_pays else PAYS_OPTIONS.index("France")
    except ValueError:
        pays_index = PAYS_OPTIONS.index("France")

    with st.form(f"{key}_form"):
        st.write("#### Identité")
        nom_structure = st.text_input("Nom de la structure", value=init_nom_structure)
        nom_contact = st.text_input("Nom du contact", value=init_nom_contact)
        type_prospect = st.selectbox(
            "Type",
            TYPE_PROSPECT_OPTIONS,
            index=init_type_index,
            placeholder="Choisir un type",
        )

        st.write("#### Contact")
        email = st.text_input("Email", value=init_email)
        telephone = st.text_input("Téléphone", value=init_tel)
        sit_web = st.text_input("Site web", value=init_site)

        st.write("#### Localisation")
        ville = st.text_input("Ville", value=init_ville)
        region = st.selectbox(
            "Région",
            REGION_FRANCE_OPTIONS,
            index=region_index,
        )
        departement = st.selectbox(
            "Département",
            DEPARTEMENT_OPTIONS,
            index=departement_index,
        )
        pays = st.selectbox(
            "Pays",
            PAYS_OPTIONS,
            index=pays_index,
        )
        adresse = st.text_input("Adresse", value=init_adresse)

        st.write("#### Réseaux sociaux")
        c1, c2 = st.columns(2)
        with c1:
            facebook = st.text_input("Facebook (lien)", value=init_fb)
            facebook_followers = st.number_input(
                "Facebook followers",
                min_value=0,
                value=int(init_fb_f) if isinstance(init_fb_f, int) else 0,
            )
            x_link = st.text_input("X (lien)", value=init_x)
            x_followers = st.number_input(
                "X followers",
                min_value=0,
                value=int(init_x_f) if isinstance(init_x_f, int) else 0,
            )
            instagram = st.text_input("Instagram (lien)", value=init_ig)
            instagram_followers = st.number_input(
                "Instagram followers",
                min_value=0,
                value=int(init_ig_f) if isinstance(init_ig_f, int) else 0,
            )
        with c2:
            tictok = st.text_input("TikTok (lien)", value=init_tt)
            tictok_followers = st.number_input(
                "TikTok followers",
                min_value=0,
                value=int(init_tt_f) if isinstance(init_tt_f, int) else 0,
            )
            youtube = st.text_input("YouTube (lien)", value=init_yt)
            youtube_followers = st.number_input(
                "YouTube followers",
                min_value=0,
                value=int(init_yt_f) if isinstance(init_yt_f, int) else 0,
            )

        st.write("#### Statut")
        try:
            methode_index = METHODE_CONTACT_OPTIONS.index(init_methode) if init_methode else None
        except ValueError:
            methode_index = None
        accepte_contact = st.checkbox("Accepte d’être contacté", value=init_accepte)
        methode_contact = st.selectbox(
            "Méthode de contact",
            METHODE_CONTACT_OPTIONS,
            index=methode_index,
        )
        commentaires = st.text_area("Commentaires", value=init_commentaires)

        col_a, col_b = st.columns(2)
        save = col_a.form_submit_button("Enregistrer")
        cancel = col_b.form_submit_button("Annuler")

    if cancel:
        st.session_state[conflict_key] = None
        st.session_state[payload_key] = None
        return "cancel"

    if not save:
        # Si on n'a pas soumis, on affiche éventuellement la zone de résolution de conflit plus bas
        pass
    else:
        # -------------------------
        # Validation UI
        # -------------------------
        errors = []

        # On garde la règle -> au moins email OU téléphone
        if not email and not telephone:
            errors.append("Renseigne au moins un email ou un téléphone.")

        if email and not is_valid_email(email):
            errors.append("Format email invalide.")
        if telephone and not is_valid_phone(telephone):
            errors.append("Format téléphone invalide.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            # Payload PATCH : on envoie ce qu'on veut mettre à jour.
            payload = {
                "nom_structure": nom_structure or None,
                "nom_contact": nom_contact or None,
                "type_prospect": type_prospect or None,
                "ville": ville or None,
                "region": region or None,
                "departement": departement or None,
                "pays": pays or None,
                "adresse": adresse or None,
                "email": email or None,
                "telephone": telephone or None,
                "sit_web": sit_web or None,
                "accepte_contact": accepte_contact,
                "methode_contact": methode_contact or None,
                "commentaires": commentaires or None,
                "facebook": facebook or None,
                "facebook_followers": int(facebook_followers),
                "x": x_link or None,
                "x_followers": int(x_followers),
                "instagram": instagram or None,
                "instagram_followers": int(instagram_followers),
                "tictok": tictok or None,
                "tictok_followers": int(tictok_followers),
                "youtube": youtube or None,
                "youtube_followers": int(youtube_followers),
            }

            updated, err = update_prospect(pid, payload, force=False)

            if err:
                if err.get("type") == "conflict":
                    st.session_state[payload_key] = payload
                    st.session_state[conflict_key] = err.get("detail")
                    st.warning("Doublon détecté.")
                    return "conflict"

                st.error(err.get("message", "Erreur lors de la mise à jour."))
            else:
                st.success("Prospect mis à jour")
                st.session_state[conflict_key] = None
                st.session_state[payload_key] = None
                return "saved"

    # ------------------------------------------------------------
    # Résolution conflit (forcer / annuler) sans changer de page
    # ------------------------------------------------------------
    if st.session_state[conflict_key]:
        st.divider()
        st.warning("Conflit : un prospect similaire existe déjà.")
        st.json(st.session_state[conflict_key])

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Annuler le conflit", key=f"{key}_conflict_cancel"):
                st.session_state[conflict_key] = None
                st.session_state[payload_key] = None
                return None

        with c2:
            if st.button("Forcer la mise à jour", key=f"{key}_conflict_force"):
                force_payload = st.session_state[payload_key]
                updated2, err2 = update_prospect(pid, force_payload, force=True)

                if err2:
                    st.error(err2.get("message", "Impossible de forcer la mise à jour."))
                else:
                    st.success("Mise à jour forcée")
                    st.session_state[conflict_key] = None
                    st.session_state[payload_key] = None
                    return "saved"

    return None
