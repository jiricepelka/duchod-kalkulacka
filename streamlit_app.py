import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Kalkulačka důchodového spoření", layout="centered")

st.title("📈 Kalkulačka důchodového spoření")

hruba_mzda = st.number_input("Hrubá mzda (měsíčně, Kč)", min_value=0.0, value=40000.0, step=1000.0)

def synced_slider(label, min_val, max_val, default, step):
    col1, col2 = st.columns([4, 1], gap="small")
    with col1:
        slider_val = st.slider(label, min_val, max_val, default, step=step, key=label+"_slider")
    with col2:
        st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
        num_val = st.number_input(" ", min_value=min_val, max_value=max_val, value=slider_val, step=step,
                                 label_visibility="collapsed", key=label+"_input")

    # Synchronizace slideru a inputu
    if num_val != slider_val:
        slider_val = num_val
    return slider_val

rust_mzdy = synced_slider("Průměrný roční růst mzdy (%)", 0.0, 100.0, 3.0, 0.1)
pocet_let = int(synced_slider("Počet let spoření", 1, 100, 30, 1))
procento_sporeni = synced_slider("Kolik % z hrubé mzdy chceš spořit", 0.0, 100.0, 31.3, 0.1)
inflace = synced_slider("Meziroční inflace (%)", 0.0, 100.0, 2.5, 0.1)
rust_investice = synced_slider("Roční výnos investice (%)", 0.0, 100.0, 6.0, 0.1)

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
