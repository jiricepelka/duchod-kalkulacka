import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kalkulačka důchodového spoření", layout="centered")

st.title("\U0001F4C8 Kalkulačka důchodového spoření")

# Úzivatelské vstupy
hruba_mzda = st.number_input("Hrubá mzda (měsíčně, Kč)", min_value=0.0, value=40000.0, step=1000.0)
rust_mzdy = st.slider("Průměrný roční růst mzdy (%)", 0.0, 10.0, 3.0)
pocet_let = st.slider("Počet let spoření", 1, 50, 30)
procento_sporeni = st.slider("Kolik % z hrubé mzdy chceš spořit", 0.0, 100.0, 31.3)
inflace = st.slider("Meziroční inflace (%)", 0.0, 10.0, 2.5)
rust_investice = st.slider("Roční výnos investice (%)", 0.0, 15.0, 6.0)

# Přepočet na desetinná čísla
rust_mzdy /= 100
procento_sporeni /= 100
inflace /= 100
rust_investice /= 100

# Výpočet spoření
data = []
celkove_uspory = 0
celkem_investovano = 0
realna_uspora = 0

for rok in range(1, pocet_let + 1):
    aktualni_mzda = hruba_mzda * ((1 + rust_mzdy) ** (rok - 1))
    rocni_vklad = aktualni_mzda * 12 * procento_sporeni
    doba_investice = pocet_let - (rok - 1)

    # Nominální budoucí hodnota
    bud_hodnota_nom = rocni_vklad * ((1 + rust_investice) ** doba_investice)

    # Reálná budoucí hodnota
    bud_hodnota_real = bud_hodnota_nom / ((1 + inflace) ** doba_investice)

    celkem_investovano += rocni_vklad
    celkove_uspory += bud_hodnota_nom
    realna_uspora += bud_hodnota_real

    data.append({
        "Rok": rok,
        "Investovaná částka": round(celkem_investovano),
        "Nominální hodnota": round(celkove_uspory),
        "Reálná hodnota": round(realna_uspora)
    })

# DataFrame pro graf
df = pd.DataFrame(data)

# Zobrazení výsledků
st.subheader("\U0001F4CA Shrnutí")
st.markdown(f"### Celková naspořená částka: **{df['Nominální hodnota'].iloc[-1]:,.0f} Kč**")
st.markdown(f"### Očištěná o inflaci: **{df['Reálná hodnota'].iloc[-1]:,.0f} Kč**")
st.markdown(f"<small>Investovaná částka: {df['Investovaná částka'].iloc[-1]:,.0f} Kč</small>", unsafe_allow_html=True)

# Tlačítko pro zobrazení renty
if st.button("Spočítat bezpečnou roční rentu"):
    realny_vynos = rust_investice - inflace
    renta = df['Reálná hodnota'].iloc[-1] * realny_vynos
    st.markdown(f"### Bezpečná roční renta: **{renta:,.0f} Kč/rok**")
    st.caption("Vypočteno jako naspořená částka × (výnos - inflace). Předpoklad: částku nevyčerpáš a necháš ji investovanou.")

# Interaktivní graf
st.subheader("\U0001F4C9 Graf vývoje spoření")
zobrazeni = st.radio("Zobrazit hodnoty: ", ["Nominální", "Po inflaci"])

if zobrazeni == "Nominální":
    fig = px.bar(df, x="Rok", y=["Investovaná částka", "Nominální hodnota"],
                 barmode='group', title="Nominální hodnota vs. investice")
else:
    fig = px.bar(df, x="Rok", y=["Investovaná částka", "Reálná hodnota"],
                 barmode='group', title="Reálná hodnota (očištěná o inflaci) vs. investice")

fig.update_layout(xaxis_title="Rok", yaxis_title="Kč", legend_title="")
st.plotly_chart(fig, use_container_width=True)
