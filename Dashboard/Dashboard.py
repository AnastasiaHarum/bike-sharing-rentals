import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set gaya visualisasi
sns.set_style("whitegrid")
# Pilih palet warna pink
pink_palette = sns.color_palette(["#FF69B4", "#FFB6C1", "#FFC0CB", "#FF1493", "#DB7093"])
sns.set_palette(pink_palette)

# Judul pada dashboard
def main():
    st.markdown("""
        <h1 style='font-family: "Dancing Script", cursive; color: pink;'>
        Bike Rental Dashboard 🎀
        </h1>
        """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()

# Inisialisasi state untuk menyimpan data yang difilter jika belum ada
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Path gambar
image_path = "data/logo.jpg" 

# Tampilkan gambar di sidebar
st.sidebar.image(image_path, caption="Since 2024", use_column_width=True)

# Menambahkan sidebar header
st.sidebar.header("Pilih Opsi")

# Dropdown untuk pilihan
selected_option = st.sidebar.selectbox(
    "Pilih salah satu opsi:",
    ["Daftar Isi", "Data Bike Hour dan Day", "Data Statistik", "Profil"]
)

# Tentukan folder dan file data
#data_folder = "data" 
#data_file_name_1 = "cleaned_bikeshare_day.csv"
#data_file_name_2 = "cleaned_bikeshare_hour.csv"

# Tentukan path untuk kedua file
#data_file_path_1 = os.path.join(data_folder, data_file_name_1)
#data_file_path_2 = os.path.join(data_folder, data_file_name_2)

# Menampilkan data berdasarkan opsi yang dipilih
# Opsi 1
if selected_option == "Daftar Isi":
    st.subheader("Daftar Isi")
    st.markdown("""
    1. **Daftar Isi**
    2. **Data Bike Hour dan Data Bike Day**
    3. **Statistik Data**
    4. **Profil**
    """)


# Opsi 2
elif selected_option == "Data Bike Hour dan Day":
    # Baca kedua file CSV
    data_gabungan1 = pd.read_csv("Dashboard/cleaned_bikeshare_day.csv")
    data_gabungan2 = pd.read_csv("Dashboard/cleaned_bikeshare_hour.csv")

    # Tampilkan masing-masing data tanpa penggabungan
    st.write("Data Bike Share Day")
    st.write(data_gabungan1)
        # Grafik untuk data harian berdasarkan tahun
    st.markdown("<h4 style='text-align: center;'>Grafik Jumlah Penyewaan Sepeda per Tahun (Data Harian)</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data_gabungan1, x='year', y='count', ci=None, palette='pastel')
    plt.title("Jumlah Penyewaan Sepeda per Tahun (Data Harian)")
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Penyewaan")
    # Menambahkan legenda di dalam grafik
    legend_labels = {
        0: "Tahun 0 (2011)",
        1: "Tahun 1 (2012)"
    }
    # Membuat custom legend
    handles = [
        plt.Line2D([0], [0], color='C0', lw=4, label=legend_labels[0]),
        plt.Line2D([0], [0], color='C1', lw=4, label=legend_labels[1])
    ]
    # Menambahkan legenda di dalam grafik
    plt.legend(handles=handles, title="Keterangan Tahun", loc='upper right', bbox_to_anchor=(1, 1))
    st.pyplot(plt)

    #Data per hour
    st.write("Data Bike Share Hour")
    st.write(data_gabungan2)
    # Grafik untuk data per jam berdasarkan tahun
    st.markdown("<h4 style='text-align: center;'>Grafik Jumlah Penyewaan Sepeda per Tahun (Data Per Jam)</h4>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data_gabungan2, x='year', y='count', ci=None, palette='pastel')
    plt.title("Jumlah Penyewaan Sepeda per Tahun (Data Per Jam)")
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Penyewaan")
    # Menambahkan legenda di dalam grafik untuk data per jam
    plt.legend(handles=handles, title="Keterangan Tahun", loc='upper right', bbox_to_anchor=(1, 1))
    st.pyplot(plt)

    # Menampilkan sumber data dengan tautan yang dapat diklik
    st.write("Sumber: [Kaggle Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)")


# Opsi 3
elif selected_option == "Data Statistik":
    # Baca file data
    day_df = pd.read_csv("Dashboard/cleaned_bikeshare_day.csv")
    hour_df = pd.read_csv("Dashboard/cleaned_bikeshare_hour.csv")

    # Konversi kolom 'dateday' menjadi tipe datetime
    day_df['dateday'] = pd.to_datetime(day_df['dateday'])
    hour_df['dateday'] = pd.to_datetime(hour_df['dateday'])

    # Rentang waktu
    min_date = day_df['dateday'].min().date()
    max_date = day_df['dateday'].max().date()

    # Sidebar untuk rentang waktu
    st.sidebar.title("Rentang Waktu")
    start_date, end_date = st.sidebar.date_input("Pilih Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

    # Filter data berdasarkan rentang waktu
    filtered_day_df = day_df[(day_df['dateday'].dt.date >= start_date) & (day_df['dateday'].dt.date <= end_date)]

    # Dashboard Header
    st.subheader(f"Rentang Waktu: {start_date} – {end_date}")

    # Kalkulasi total penyewaan
    total_casual = filtered_day_df['casual'].sum()
    total_registered = filtered_day_df['registered'].sum()
    total_rentals = filtered_day_df['count'].sum()

    # Tampilkan metrik
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Casual User", f"{total_casual:,}")
    with col2:
        st.metric("Registered User", f"{total_registered:,}")
    with col3:
        st.metric("Total User", f"{total_rentals:,}")

    
# Menyiapkan data bulanan
    filtered_day_df['month'] = filtered_day_df['dateday'].dt.month_name()  # Menambahkan kolom nama bulan
    monthly_rentals = filtered_day_df.groupby('month')['count'].sum()

    # Atur urutan bulan sesuai kalender
    ordered_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_rentals = monthly_rentals.reindex(ordered_months, fill_value=0)

    # Membuat grafik menggunakan Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linestyle='-', color='#FF69B4')  # Warna pink

    # Menambahkan label angka di setiap titik data
    for i, value in enumerate(monthly_rentals.values):
        plt.text(i, value, f'{value}', ha='center', va='bottom', color='black')  # Teks angka berwarna hitam

    # Menambahkan judul dan label sumbu
    st.subheader("Monthly Rentals") 
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Rentals", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)

    # Menyiapkan data cuaca
    weather_rentals = filtered_day_df.groupby('weathersit')['count'].sum()

    # Membuat grafik dengan warna soft (pastel) dan menampilkan angka di atas setiap bar
    plt.figure(figsize=(10, 6))

    # Warna soft (pastel) untuk setiap bar
    colors = sns.color_palette("pastel", len(weather_rentals))

    # Plot bar chart
    bars = plt.bar(weather_rentals.index, weather_rentals.values, color=colors)

    # Menambahkan judul dan label sumbu
    st.subheader("Weatherly Rentals") # Judul berwarna pink
    plt.xlabel("Weather Situation", fontsize=12)
    plt.ylabel("Number of Rentals", fontsize=12)

    # Menambahkan angka di atas setiap bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=10)

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)

   # Menyiapkan data untuk weekday, workingday, holiday
    weekday_rentals = filtered_day_df.groupby('weekday')['count'].sum()
    workingday_rentals = filtered_day_df.groupby('workingday')['count'].sum()
    holiday_rentals = filtered_day_df.groupby('holiday')['count'].sum()

# Fungsi untuk membuat bar chart dengan warna berbeda dan angka di atas bar
    def create_bar_chart(data, title, xlabel, is_binary=False):
        plt.figure(figsize=(10, 6))
        
        # Warna berbeda untuk setiap bar (menggunakan palet pastel)
        colors = sns.color_palette("pastel", len(data))
        
        # Membuat bar chart
        bars = plt.bar(data.index, data.values, color=colors)
        
        # Menambahkan judul dan label sumbu 
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel("Number of Rentals", fontsize=12)
        
        # Menambahkan angka di atas setiap bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=10)
        
        # Jika datanya binary (0 dan 1), set label sumbu X ke 0 dan 1
        if is_binary:
            plt.xticks([0, 1], ['0', '1'])
        
        # Menampilkan grafik di Streamlit
        st.pyplot(plt)

    # Membuat bar chart untuk weekday rentals
    st.subheader("Weekday Rentals")
    create_bar_chart(weekday_rentals, "Weekday Rentals", "Weekday")

    # Membuat bar chart untuk workingday rentals (0 dan 1)
    st.subheader("Workingday Rentals")
    create_bar_chart(workingday_rentals, "Workingday Rentals", "Workingday", is_binary=True)

    # Membuat bar chart untuk holiday rentals (0 dan 1)
    st.subheader("Holiday Rentals")
    create_bar_chart(holiday_rentals, "Holiday Rentals", "Holiday", is_binary=True)

# Opsi 4
elif selected_option == "Profil":
# Tampilkan gambar logo
    image_path = "data/logo2.png"
    st.image(image_path, use_column_width=True)
    # Buat tiga kolom
    col1, col2, col3 = st.columns(3)

    with col1:
        # Ubah footer dengan gaya yang lebih menarik
        st.markdown("<h style='color: #FF69B4;'>Copyright © Anastasia Harum Mawadah</h>", unsafe_allow_html=True)

    with col2:
        # Profil GitHub 
        github_url = "https://github.com/AnastasiaHarum"
        github_badge = f'''
        <a href="{github_url}" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-Follow-pink?style=for-the-badge&logo=github" alt="GitHub">
        </a>'''
        # Menampilkan badge GitHub di Streamlit
        st.markdown(github_badge, unsafe_allow_html=True)

    with col3:
        # Profil LinkedIn
        linkedin_url = "https://www.linkedin.com/in/anastasiahm/"
        linkedin_badge = f'''
        <a href="{linkedin_url}" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-Connect-pink?style=for-the-badge&logo=linkedin" alt="LinkedIn">
        </a>'''
        # Menampilkan badge LinkedIn di Streamlit
        st.markdown(linkedin_badge, unsafe_allow_html=True)

    # CSS untuk menyesuaikan tampilan lebih lanjut
    st.markdown(
        """
        <style>
        /* Gaya untuk footer */
        h5 {
            font-family: 'Dancing Script', sans-serif;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
