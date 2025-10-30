# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 Visualizzatore di segnali accelerometrici")

# Upload CSV
uploaded_file = st.file_uploader("Trascina qui il file CSV", type="csv")

if uploaded_file:
    # Dimensione del file
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.write(f"📦 Dimensione del file: {file_size_mb:.2f} MB")

    # Lettura header
    header_line = uploaded_file.readline().decode('utf-8').strip()
    column_names = header_line.split(';')
    timestamp_col = column_names[0]
    signal_columns = column_names[1:]

    # Reset file pointer e lettura completa
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, sep=';', engine='python')

    # Informazioni generali
    st.write(f"📄 Numero di righe totali: {df.shape[0]}")
    st.write(f"📊 Numero di colonne: {df.shape[1]}")
    st.write(f"📈 Numero di segnali: {len(signal_columns)}")

    # Frequenza di campionamento
    try:
        timestamps = pd.to_datetime(df.iloc[:1000, 0], format='%Y/%m/%d %H:%M:%S:%f')
        time_deltas = timestamps.diff().dropna().dt.total_seconds()
        sampling_interval = time_deltas.mode()[0]
        sampling_frequency_hz = round(1 / sampling_interval)
        st.write(f"⏱️ Frequenza di campionamento stimata: {sampling_frequency_hz} Hz")
    except:
        st.warning("⚠️ Impossibile calcolare la frequenza di campionamento.")

    # Selezione multipla dei segnali
    selected_signals = st.multiselect("📌 Seleziona uno o più segnali da visualizzare", signal_columns)

    # Plot interattivo
    if selected_signals:
        st.subheader("📊 Grafico interattivo")
        fig = px.line(df, x=timestamp_col, y=selected_signals, title="Segnali accelerometrici")
        fig.update_layout(xaxis_tickangle=-45)

        st.plotly_chart(fig, use_container_width=True)
