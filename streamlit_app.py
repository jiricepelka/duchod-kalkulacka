import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kalkulačka důchodového spoření", layout="centered")

st.title("📈 Kalkulačka důchodového spoření")

# Uživatelské vstupy (slider + number_input vedle sebe)
col1, col2 = st.columns([2, 1])
with col1:
    rust_mzdy_slider = st.slider("Průměrný roční růst mzdy (%)", 0.0, 10.0, 3.0)
with col2:
    rust_mzdy = st.number_input("", value=rust_mzdy_slider, step=0.1, label_visibility="collapsed")

with col1:
    pocet_let_slider = st.slider("Počet let spoření", 1, 50, 30)
with col2:
    pocet_let = st.number_input("", min_value=1, value=pocet_let_slider, step=1, label_visibility="collapsed")

with col1:
    procento_sporeni_slider = st.slider("Kolik % z hrubé mzdy chceš spořit", 0.0, 100.0, 31.3)
with col2:
    procento_sporeni = st.number_input("", value=procento_sporeni_slider, step=0.1, label_visibility="collapsed")

with col1:
    inflace_slider = st.slider("Meziroční inflace (%)", 0.0, 10.0, 2.5)
with col2:
    inflace = st.number_input("", value=inflace_slider, step=0.1, label_visibility="collapsed")

with col1:
    rust_investice_slider = st.slider("Roční výnos investice (%)", 0.0, 15.0, 6.0)
with col2:
    rust_investice = st.number_input("", value=rust_investice_slider, step=0.1, label_visibility="collapsed")

hruba_mzda = st.number_input("Hrubá mzda (měsíčně, Kč)", min_value=0.0, value=40000.0, step=1000.0)

# Přepčet na desetinná čísla
rust_mzdy /= 100
procento_sporeni /= 100
inflace /= 100
rust_investice /= 100

# Inicializace proměnných
investovano = 0
zustatek_nom = 0
zustatek_real = 0

# Tabulka pro výsledky
data = []

for rok in range(1, pocet_let + 1):
    aktualni_mzda = hruba_mzda * ((1 + rust_mzdy) ** (rok - 1))
    rocni_vklad = aktualni_mzda * 12 * procento_sporeni

    investovano += rocni_vklad
    zustatek_nom = (zustatek_nom + rocni_vklad) * (1 + rust_investice)
    zustatek_real = (zustatek_real + rocni_vklad) * ((1 + rust_investice) / (1 + inflace))

    data.append({
        "Rok": rok,
        "Investovaná částka": round(investovano),
        "Nominální hodnota": round(zustatek_nom),
        "Reálná hodnota": round(zustatek_real)
    })

# DataFrame pro graf
df = pd.DataFrame(data)

# Zobrazení výsledků
st.subheader("📊 Shrnutí")
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
st.subheader("📉 Graf vývoje spoření")
zobrazeni = st.radio("Zobrazit hodnoty: ", ["Nominální", "Po inflaci"])

if zobrazeni == "Nominální":
    fig = px.bar(df, x="Rok", y=["Investovaná částka", "Nominální hodnota"],
                 barmode='group', title="Nominální hodnota vs. investice")
else:
    fig = px.bar(df, x="Rok", y=["Investovaná částka", "Reálná hodnota"],
                 barmode='group', title="Reálná hodnota (očištěná o inflaci) vs. investice")

fig.update_layout(xaxis_title="Rok", yaxis_title="Kč", legend_title="")
st.plotly_chart(fig, use_container_width=True)
