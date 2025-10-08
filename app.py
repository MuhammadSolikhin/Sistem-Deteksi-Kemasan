import streamlit as st
from PIL import Image
import datetime

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Sistem Deteksi Cacat Kemasan")

# --- FUNGSI & LOGIKA ---
# Di sini Anda bisa menambahkan fungsi untuk memuat model ML Anda
def run_detection_model(images):
    """
    Fungsi placeholder untuk menjalankan model deteksi.
    Ganti logika di dalam fungsi ini dengan pemanggilan model Anda.
    """
    # Simulasi hasil deteksi
    keterangan_hasil = "Terdeteksi 2 kemasan cacat ringan (goresan) dan 1 kemasan cacat berat (sobek)."
    score_hasil = 75.0 
    
    # Mengembalikan hasil
    return keterangan_hasil, score_hasil

# --- INISIALISASI SESSION STATE ---
# Session state digunakan untuk menyimpan status antar interaksi pengguna

# Status login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Status hasil deteksi
if 'detection_done' not in st.session_state:
    st.session_state.detection_done = False

# Menyimpan file yang diupload
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
    
# Menyimpan hasil deteksi
if 'detection_result' not in st.session_state:
    st.session_state.detection_result = {"keterangan": "", "score": 0.0}

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    
    # Membuat 3 kolom: kolom_kosong1, kolom_form, kolom_kosong2
    # Rasio [1, 2, 1] berarti kolom tengah 2x lebih lebar dari kolom samping
    col1, col2, col3 = st.columns([1, 2, 1])

    # Semua elemen login kita letakkan di kolom tengah (col2)
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Menambah sedikit spasi dari atas
        st.title("Login")
        st.subheader("Sistem Deteksi Cacat Kemasan")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            login_button = st.form_submit_button(
                "Login", 
                use_container_width=True # Membuat tombol selebar kolom
            )

            if login_button:
                if username == "user" and password == "password":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau password salah")
                    
# --- HALAMAN UTAMA APLIKASI (SETELAH LOGIN) ---
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("User")
        # Anda bisa ganti dengan nama user yang login
        st.write(f"Selamat datang, User!") 
        
        if st.button("Logout"):
            # Reset semua state saat logout
            st.session_state.logged_in = False
            st.session_state.detection_done = False
            st.session_state.uploaded_images = []
            st.rerun()

    # --- KONTEN UTAMA ---
    
    # Jika deteksi BELUM dilakukan, tampilkan halaman upload
    if not st.session_state.detection_done:
        st.title("Sistem Deteksi Cacat Kemasan")
        
        uploaded_files = st.file_uploader(
            "Upload gambar kemasan di sini",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        if st.button("DETEKSI", type="primary"):
            if uploaded_files:
                st.session_state.uploaded_images = uploaded_files
                
                # Menampilkan spinner saat "model" berjalan
                with st.spinner('Sedang mendeteksi gambar...'):
                    # Buka gambar menggunakan PIL
                    pil_images = [Image.open(image) for image in uploaded_files]
                    
                    # ==========================================================
                    # === DI SINI LETAKKAN LOGIKA MODEL DETEKSI ANDA ===
                    # Panggil fungsi model Anda dengan pil_images sebagai input
                    keterangan, score = run_detection_model(pil_images)
                    # ==========================================================
                    
                    # Simpan hasil ke session state
                    st.session_state.detection_result['keterangan'] = keterangan
                    st.session_state.detection_result['score'] = score
                    
                st.session_state.detection_done = True
                st.rerun() # Muat ulang untuk menampilkan halaman hasil
            else:
                st.warning("Mohon upload gambar terlebih dahulu.")

    # Jika deteksi SUDAH dilakukan, tampilkan halaman hasil
    else:
        st.title("HASIL DETEKSI")
        
        # Menampilkan Tanggal
        st.write(f"**Tanggal :** {datetime.date.today().strftime('%d-%m-%Y')}")
        st.divider()

        # Menampilkan Foto
        st.subheader("Hasil Foto")
        if st.session_state.uploaded_images:
            # Membuat kolom sebanyak jumlah gambar (maksimal 4 kolom agar rapi)
            cols = st.columns(min(len(st.session_state.uploaded_images), 4))
            for i, uploaded_image in enumerate(st.session_state.uploaded_images):
                with cols[i % 4]:
                    st.image(uploaded_image, caption=f"Gambar {i+1}", use_column_width=True)
        
        st.divider()

        # Menampilkan Keterangan dan Skor
        st.subheader("Keterangan :")
        st.write(st.session_state.detection_result['keterangan'])
        
        st.subheader("Score :")
        st.metric(label="Tingkat Kerusakan", value=f"{st.session_state.detection_result['score']}%")

        if st.button("Deteksi Lagi"):
            # Reset state untuk kembali ke halaman upload
            st.session_state.detection_done = False
            st.session_state.uploaded_images = []
            st.rerun()