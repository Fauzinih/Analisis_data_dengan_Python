# Import Semua Packages/Library yang Digunakan
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
from babel.numbers import format_currency 

# Set style Seaborn
sns.set(style='darkgrid')


hour_data = pd.read_csv('hour.csv')
day_data = pd.read_csv('day.csv')

# Cleaning Data
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
day_data['dteday'] = pd.to_datetime(day_data['dteday'])


st.title("CAPITAL BIKESHARE")
st.write("Analisis data penyewaan sepeda di Capital Bikeshare.")

if 'date_selected' not in st.session_state:
    st.session_state.date_selected = False

# Sebuah informasi tambahan
with st.expander("Informasi Tambahan"):
    st.write("""
    Capital Bikeshare (CaBi) adalah sistem berbagi sepeda. Capital Bikeshare diluncurkan pada September 2010. Ini adalah salah satu program berbagi sepeda pertama di Amerika Serikat yang memanfaatkan teknologi modern untuk memudahkan pengguna dalam menyewa dan mengembalikan sepeda. Sistem ini telah berkembang pesat sejak peluncurannya, dengan penambahan stasiun dan sepeda dari waktu ke waktu. Hingga Januari 2023, sistem ini memiliki lebih dari 700 stasiun dan lebih dari 5.400 sepeda.
    Hingga Januari 2023, Capital Bikeshare memiliki lebih dari 700 stasiun dan lebih dari 5.400 sepeda. Stasiun-stasiun ini tersebar di seluruh Washington, D.C., serta di beberapa kota terdekat seperti Arlington, Virginia, dan Montgomery County, Maryland.
    """)

# Memilih tampilan visualisasi
visualization_type = st.radio(
    "Pilih tipe visualisasi yang ingin ditampilkan:",
    ("Per Jam", "Per Hari")
)

# Menyiapkan data yang digunakan untuk visualisasi
if visualization_type == "Per Jam":
    data = hour_data
else:
    data = day_data

# Menambahkan logo
st.sidebar.image("sepeda.png", use_column_width=True)

# Mengatur filter rentang waktu
st.sidebar.title("Periode Waktu")
min_date = data['dteday'].min()
max_date = data['dteday'].max()

# Mengatur input rentang tanggal dan memberikan nilai default
start_date = st.sidebar.date_input(
    label='Pilih Tanggal Awal',
    min_value=min_date,
    max_value=max_date,
    value=min_date  # Nilai default untuk tanggal awal
)

end_date = st.sidebar.date_input(
    label='Pilih Tanggal Akhir',
    min_value=start_date,  # Tanggal akhir tidak boleh kurang dari tanggal awal
    max_value=max_date,
    value=max_date  # Nilai default untuk tanggal akhir
)

# Mengatur pesan sebelum dan sudah dipilih tanggal
if st.sidebar.button("Terapkan"):
    st.session_state.date_selected = True  
if not st.session_state.date_selected:
    st.info("Silahkan pilih tanggal untuk melihat analisis.")
else:
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]
    
    # Visualisasi pertama: Jumlah penyewaan sepeda berdasarkan musim
    st.header('Jumlah Penyewaan Sepeda berdasarkan Musim')
    season_names = ['Spring', 'Summer', 'Fall', 'Winter']
    filtered_data['season'] = filtered_data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    rentals_by_season = filtered_data.groupby('season')['cnt'].sum().reindex(season_names)

    fig, ax = plt.subplots(figsize=(10, 6))
    rentals_by_season.plot(kind='bar', color=['green', 'blue', 'orange', 'red'], ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Rentals')
    ax.set_title('Total Count of Rentals by Season')
    st.pyplot(fig)

    # Visualisasi kedua: Jumlah penyewaan sepeda berdasarkan hari
    st.header('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu')
    day_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    filtered_data['weekday'] = filtered_data['weekday'].map({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                                                            4: 'Thursday', 5: 'Friday', 6: 'Saturday'})
    rentals_by_day = filtered_data.groupby('weekday')['cnt'].sum().reindex(day_of_week)

    fig, ax = plt.subplots(figsize=(10, 6))
    rentals_by_day.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Total Rentals')
    ax.set_title('Total Count of Rentals by Day of the Week')
    st.pyplot(fig)

    # Visualisasi ketiga: Jumlah penyewaan sepeda berdasarkan cuaca
    st.header('Jumlah Penyewaan Sepeda berdasarkan Cuaca')
    weather_names = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Ice'}
    filtered_data['weathersit'] = filtered_data['weathersit'].map(weather_names)
    rentals_by_weather = filtered_data.groupby('weathersit')['cnt'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    rentals_by_weather.plot(kind='bar', color=['lightblue', 'lightgreen', 'orange', 'red'], ax=ax)
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Total Rentals')
    ax.set_title('Total Count of Rentals by Weather')
    st.pyplot(fig)

st.caption('Copyright © M.Fauzhi_Azhima 2024')