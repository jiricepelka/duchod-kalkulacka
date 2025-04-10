import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kalkulačka důchodového spoření", layout="centered")

st.title("📈 Kalkulačka důchodového spoření")

# Uživatelské vstupy
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
nominální_rocni_zustatek = []
realna_rocni_zustatek = []
celkove_uspory = 0

for rok in range(1, pocet_let + 1):
    aktualni_mzda = hruba_mzda * ((1 + rust_mzdy) ** (rok - 1))
    rocni_vklad = aktualni_mzda * 12 * procento_sporeni
    doba_investice = pocet_let - (rok - 1)
    bud_hodnota = rocni_vklad * ((1 + rust_investice) ** doba_investice)
    celkove_uspory += bud_hodnota

    nominální_rocni_zustatek.append(celkove_uspory)
    realna_rocni_zustatek.append(celkove_uspory / ((1 + inflace) ** rok))

# Výstup
st.subheader("📊 Výsledky")
st.write(f"**Celková naspořená částka (nominálně):** {nominální_rocni_zustatek[-1]:,.0f} Kč")
st.write(f"**Očištěno o inflaci (reálná hodnota dnes):** {realna_rocni_zustatek[-1]:,.0f} Kč")

# Graf
fig, ax = plt.subplots()
roky = list(range(1, pocet_let + 1))
ax.plot(roky, nominální_rocni_zustatek, label="Nominální hodnota")
ax.plot(roky, realna_rocni_zustatek, label="Reálná hodnota (po inflaci)", linestyle="--")
ax.set_xlabel("Rok")
ax.set_ylabel("Naspořená částka (Kč)")
ax.set_title("Vývoj důchodového spoření")
ax.legend()
ax.grid(True)

st.pyplot(fig)
