import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Prédiction du taux de croissance économique du Maroc", layout="centered")


# TITRE ET DESCRIPTION
st.markdown("<h1 style='text-align: center; color: #D62828;'>Prédiction du taux de croissance économique du Maroc(2000–2030)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-size:16px;'>Données historiques (2000–2023) et prévisions ajustables (2024–2030)</h4>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size:15px;'>"
    "Ce tableau de bord interactif permet de visualiser les prévisions de croissance du PIB marocain "
    "jusqu’en 2030. Vous pouvez ajuster les principaux facteurs économiques (taux de chômage, taux d’intérêt, IDE) "
    "grâce aux curseurs à gauche. Les courbes du graphique s’actualisent automatiquement pour refléter vos ajustements."
    "</p>",
    unsafe_allow_html=True
)



# 1. DONNÉES RÉELLES
df_real = pd.read_excel("croissance_maroc.xlsx", engine='openpyxl')
df_real['Année'] = pd.to_datetime(df_real['Année'], format='%Y')
df_real.set_index('Année', inplace=True)
real_pib = df_real['PIB']


# 2. PRÉVISIONS ARIMA (2024–2030)
future_years = pd.date_range(start='2024', periods=7, freq='YS')
pib_pred = [3.11, 4.15, 3.42, 3.93, 3.58, 3.67, 3.81]
pib_forecast = pd.Series(pib_pred, index=future_years)


# 3. COEFFICIENTS DE RÉGRESSION (facteurs)
coefficients = {
    "Taux de chômage": -1.0364,
    "Taux d'intérêt": 1.1448,
    "IDE": 0.9445
}


# 4. SIDEBAR INTERACTIVE
st.sidebar.markdown("<h3 style='color:#D62828;'>Ajuster les facteurs économiques</h3>", unsafe_allow_html=True)
user_inputs = {
    factor: st.sidebar.slider(f"Variation de {factor}", -5.0, 5.0, 0.0, 0.1)
    for factor in coefficients
}


# 5. CALCUL DE LA PRÉVISION AJUSTÉE
adjusted_forecast = pib_forecast.copy()
for factor, coef in coefficients.items():
    adjusted_forecast += user_inputs[factor] * coef


# 6. AFFICHAGE DU GRAPHIQUE
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(real_pib.index, real_pib, label="📈 PIB Réel (2000–2023)", color='#444444', linewidth=2)
ax.plot(pib_forecast.index, pib_forecast, label="🔵 Prévision Initiale", linestyle='--', color='#1f77b4', linewidth=2)
ax.plot(adjusted_forecast.index, adjusted_forecast, label="🔴 Prévision Ajustée", linestyle='-', color='#d62728', linewidth=2)
ax.set_title("Évolution du PIB Marocain", fontsize=18, weight='bold')
ax.set_xlabel("Année", fontsize=12)
ax.set_ylabel("PIB (%)", fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.markdown("---")
st.pyplot(fig)
st.markdown("---")


# 7. TABLEAU DES PRÉVISIONS AJUSTÉES
st.subheader("Valeurs Prévisionnelles du PIB Ajustées selon les Facteurs Économiques")
# Formater l'index en année et l'ajouter comme colonne "Année"
df_affichage = adjusted_forecast.round(2).rename("PIB (%)").reset_index()
df_affichage['Année'] = df_affichage['index'].dt.year
df_affichage.drop(columns='index', inplace=True)
df_affichage.set_index('Année', inplace=True)
st.dataframe(df_affichage)


# 8. TÉLÉCHARGEMENT CSV
adjusted_df = pd.DataFrame({
    "Année": adjusted_forecast.index.year,
    "Croissance PIB ajustée (%)": adjusted_forecast.values
})
csv = adjusted_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Télécharger les prévisions ajustées (.csv)",
    data=csv,
    file_name="prevision_pib_ajustee.csv",
    mime='text/csv'
)
