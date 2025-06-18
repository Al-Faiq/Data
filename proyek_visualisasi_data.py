import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Styling
st.set_page_config(page_title="Visualisasi Kecanduan Sosial Media", layout="wide")
sns.set_style("whitegrid")

# Tambahan CSS untuk mengubah warna sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #F0F2F6;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Contoh DataFrame buatan untuk simulasi
np.random.seed(42)
data = {
    'Gender': np.random.choice(['Laki-laki', 'Perempuan'], 200),
    'Most_Used_Platform': np.random.choice(['Instagram', 'TikTok', 'YouTube', 'Facebook', 'Twitter'], 200),
    'Avg_Daily_Usage_Hours': np.random.uniform(1, 8, 200).round(1),
    'Sleep_Hours_Per_Night': np.random.uniform(4, 9, 200).round(1),
    'Mental_Health_Score': np.random.randint(1, 11, 200),
    'Addicted_Score': np.random.randint(1, 11, 200),
    'Affects_Academic_Performance': np.random.choice(['Ya', 'Tidak'], 200)
}
df = pd.DataFrame(data)

# Sidebar - Filter Data
st.sidebar.title("🎛️ Filter Data")
selected_gender = st.sidebar.selectbox("Pilih Jenis Kelamin:", options=["Semua"] + list(df['Gender'].unique()))
selected_platform = st.sidebar.multiselect("Pilih Platform:", options=df['Most_Used_Platform'].unique(), default=df['Most_Used_Platform'].unique())

# Terapkan filter
if selected_gender != "Semua":
    df = df[df['Gender'] == selected_gender]
df = df[df['Most_Used_Platform'].isin(selected_platform)]

# Judul umum
st.title("📱 Visualisasi Data Kecanduan Media Sosial di Kalangan Pelajar")
st.markdown("""
Proyek ini bertujuan untuk memvisualisasikan pola penggunaan media sosial oleh pelajar dan dampaknya terhadap kesehatan mental, waktu tidur, serta performa akademik.
Visualisasi ini membantu orang tua, guru, dan pelajar memahami risiko dari penggunaan media sosial secara berlebihan.
""")

# Semua visualisasi langsung ditampilkan tanpa kondisi logika
st.header("📊 Bar Chart: Platform & Tingkat Adiksi")
st.markdown("""
Visualisasi ini menunjukkan dua aspek penting: platform media sosial yang paling sering digunakan serta rata-rata tingkat kecanduan berdasarkan jenis kelamin. Hal ini membantu memahami preferensi penggunaan dan potensi risiko kecanduan pada masing-masing kelompok.
""")
platform_counts = df['Most_Used_Platform'].value_counts().reset_index()
platform_counts.columns = ['Platform', 'Jumlah Pengguna']
fig = px.bar(platform_counts, x='Platform', y='Jumlah Pengguna', color='Platform', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig, use_container_width=True)

gender_addiction = df.groupby("Gender")["Addicted_Score"].mean().reset_index()
fig = px.bar(gender_addiction, x="Gender", y="Addicted_Score", color="Gender", color_discrete_map={"Laki-laki": "#1f77b4", "Perempuan": "#e377c2"})
st.plotly_chart(fig, use_container_width=True)

st.header("📉 Scatter Plot: Hubungan Durasi dan Tidur")
st.markdown("""
Scatter plot ini mengilustrasikan hubungan antara durasi penggunaan media sosial dengan jumlah waktu tidur per malam. Visualisasi ini membantu mengidentifikasi apakah kebiasaan penggunaan yang tinggi berdampak pada kualitas tidur siswa.
""")
fig = px.scatter(df, x="Avg_Daily_Usage_Hours", y="Sleep_Hours_Per_Night", color="Gender", color_discrete_map={"Laki-laki": "#1f77b4", "Perempuan": "#e377c2"}, opacity=0.6)
st.plotly_chart(fig, use_container_width=True)

st.header("🌡️ Heatmap: Korelasi antar Variabel")
st.markdown("""
Heatmap berikut menggambarkan kekuatan hubungan antar variabel numerik seperti durasi penggunaan, waktu tidur, skor kesehatan mental, dan tingkat kecanduan. Ini memberikan gambaran apakah ada keterkaitan signifikan antara satu faktor dengan faktor lainnya.
""")
correlation_data = df[["Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score", "Addicted_Score"]].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.header("📈 Line & Area Chart: Tren Kesehatan Mental")
st.markdown("""
Line chart menunjukkan tren rata-rata skor kesehatan mental berdasarkan durasi harian penggunaan media sosial. Grafik area memperkuat pemahaman terhadap tren tersebut secara visual dan memperlihatkan fluktuasi data lebih halus.
""")
df_line = df.groupby("Avg_Daily_Usage_Hours")["Mental_Health_Score"].mean().reset_index()
fig = px.line(df_line, x="Avg_Daily_Usage_Hours", y="Mental_Health_Score", markers=True, color_discrete_sequence=["#636EFA"])
st.plotly_chart(fig, use_container_width=True)
st.area_chart(df_line.set_index("Avg_Daily_Usage_Hours"))

st.header("🥧 Pie Chart: Distribusi Responden")
st.markdown("""
Dua pie chart berikut menampilkan proporsi jenis kelamin responden serta pandangan mereka terhadap dampak media sosial terhadap akademik. Ini memberikan konteks distribusi demografis dan persepsi siswa terhadap pengaruh media sosial.
""")
fig1 = px.pie(df, names="Gender", title="Persentase Responden", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(df, names="Affects_Academic_Performance", title="Apakah Media Sosial Mempengaruhi Akademik?", color_discrete_sequence=px.colors.sequential.Tealgrn)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Proyek ini dikembangkan oleh Muhammad Nizar Al-Faiq & Sabrina Marliani untuk mata kuliah Visualisasi Data.")
