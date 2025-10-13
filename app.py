import streamlit as st
from PIL import Image
import datetime
import io

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Sistem Deteksi Cacat Kemasan")

# --- KODE CSS UNTUK GAYA TAMPILAN ---
st.markdown(
    """
    <style>
    /* Mengatur lebar sidebar */
    [data-testid="stSidebar"] {
        width: 250px !important;
    }
    
    /* Mengubah warna tombol terakhir di sidebar menjadi hitam (tombol logout) */
    [data-testid="stSidebar"] .stButton:last-child button {
        background-color: #FF4B4B;
        color: white;
    }

    /* Mengatur font dan perataan tengah untuk judul utama */
    .main-title {
        text-align: center;
        color: #1a751a; /* Warna hijau */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Contoh font */
        font-size: 2.5em; /* Ukuran font lebih besar */
        font-weight: bold;
        margin-bottom: 0px; /* Kurangi margin bawah */
    }

    /* Mengatur perataan tengah untuk sub-heading/deskripsi */
    .main-description {
        text-align: center;
        color: #555555;
        font-size: 1.1em;
        margin-top: 5px; /* Sedikit jarak dari judul */
        margin-bottom: 30px; /* Jarak yang cukup ke konten berikutnya */
    }

    /* CSS untuk placeholder profil di sidebar */
    .profile-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .profile-image-frame {
        width: 100px; /* Lebar frame */
        height: 100px; /* Tinggi frame */
        border-radius: 50%; /* Membuat lingkaran */
        overflow: hidden; /* Memastikan gambar tidak keluar dari lingkaran */
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #5C6F87; /* Warna latar belakang lingkaran */
    }
    .profile-image-frame img {
        width: 60px; /* Ukuran ikon user */
        height: 60px;
        filter: invert(100%) brightness(150%); /* Membuat ikon putih */
    }
    .profile-name {
        font-size: 1.2em;
        font-weight: bold;
        color: black; /* Warna teks putih */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNGSI & LOGIKA ---
def run_detection_model(images):
    """Fungsi placeholder untuk menjalankan model deteksi."""
    keterangan_hasil = f"Terdeteksi {len(images)} gambar. Ditemukan 1 kemasan cacat berat (sobek)."
    score_hasil = 65.0
    return keterangan_hasil, score_hasil

# --- INISIALISASI SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'detection_done' not in st.session_state:
    st.session_state.detection_done = False
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'detection_result' not in st.session_state:
    st.session_state.detection_result = {"keterangan": "", "score": 0.0}
if 'camera_open' not in st.session_state:
    st.session_state.camera_open = False
if 'history' not in st.session_state:
    st.session_state.history = []
if 'viewing_history_id' not in st.session_state:
    st.session_state.viewing_history_id = None

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    # (Bagian login tidak berubah)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("Login")
        st.subheader("Sistem Deteksi Cacat Kemasan")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            if login_button:
                if username == "user" and password == "password":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau password salah")

# --- HALAMAN UTAMA APLIKASI (SETELAH LOGIN) ---
else:
    # --- SIDEBAR (SUDAH DIPERBARUI DENGAN FOTO PROFIL) ---
    with st.sidebar:
        # Foto Profil Placeholder
        st.markdown(
            """
            <div class="profile-container">
                <div class="profile-image-frame">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg" alt="Profile Placeholder">
                </div>
                <div class="profile-name">Admin</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()

        st.info("Aplikasi ini menggunakan AI untuk mendeteksi cacat pada kemasan produk secara otomatis.")

        with st.expander("Lihat Contoh Penggunaan"):
            st.markdown("""
            1.  **Upload Gambar**: Pilih hingga 5 gambar kemasan.
            2.  **Gunakan Kamera**: Ambil gambar langsung.
            3.  **Mulai Deteksi**: Tekan tombol 'DETEKSI'.
            4.  **Lihat Hasil**: Hasil analisis akan ditampilkan.
            5.  **Cek Histori**: Hasil otomatis tersimpan di histori.
            """)
        
        st.divider()

        st.header("Histori Deteksi")
        if not st.session_state.history:
            st.write("Belum ada histori.")
        else:
            for i, record in enumerate(reversed(st.session_state.history)):
                if st.button(f"Hasil {record['timestamp']}", key=f"history_{i}"):
                    st.session_state.viewing_history_id = record['id']
                    st.session_state.detection_done = True 
        
        if st.session_state.viewing_history_id is not None:
            if st.button("Lakukan Deteksi Baru", type="primary"):
                st.session_state.viewing_history_id = None
                st.session_state.detection_done = False
                st.rerun()
        
        st.write("") 
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    # --- KONTEN UTAMA (SUDAH DIPERBARUI DENGAN HEADING BARU) ---
    if st.session_state.viewing_history_id is not None:
        # (Detail histori tidak berubah, hanya judulnya akan mengikuti gaya CSS)
        history_record = next((h for h in st.session_state.history if h['id'] == st.session_state.viewing_history_id), None)
        if history_record:
            st.markdown(f"<h1 class='main-title'>DETAIL HISTORI</h1>", unsafe_allow_html=True) # Gunakan class main-title
            st.markdown(f"<p class='main-description'>Hasil deteksi dari {history_record['timestamp']}</p>", unsafe_allow_html=True)
            st.divider()
            st.subheader("Hasil Foto")
            cols = st.columns(min(len(history_record['images']), 5))
            for i, img_bytes in enumerate(history_record['images']):
                with cols[i % 5]:
                    st.image(img_bytes, caption=f"Gambar {i+1}", use_container_width=True)
            st.divider()
            st.subheader("Keterangan :")
            st.write(history_record['result']['keterangan'])
            st.subheader("Score :")
            st.metric(label="Tingkat Kerusakan", value=f"{history_record['result']['score']}%")
        else:
            st.error("Data histori tidak ditemukan.")
    elif not st.session_state.detection_done:
        # Heading baru untuk halaman deteksi
        st.markdown("<h1 class='main-title'>SISTEM DETEKSI CACAT KEMASAN</h1>", unsafe_allow_html=True)
        st.markdown("<p class='main-description'>Upload gambar atau ambil foto untuk melakukan deteksi kemasan.</p>", unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader("Upload gambar dari perangkat Anda (Maks. 5 gambar)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if len(uploaded_files) > 5:
            st.warning("Anda hanya dapat mengupload maksimal 5 gambar. Hanya 5 gambar pertama yang akan diproses.")
            uploaded_files = uploaded_files[:5]
        st.write("")
        camera_photo = None
        if not st.session_state.camera_open:
            if st.button("📸 Buka Kamera"):
                st.session_state.camera_open = True
                st.rerun()
        else:
            camera_photo = st.camera_input("Ambil gambar dengan kamera")
        st.write("")
        if st.button("DETEKSI", type="primary", use_container_width=True):
            images_to_process = uploaded_files or ([camera_photo] if camera_photo else None)
            if images_to_process:
                st.session_state.uploaded_images = images_to_process
                with st.spinner('Sedang mendeteksi gambar...'):
                    pil_images = [Image.open(image) for image in images_to_process]
                    keterangan, score = run_detection_model(pil_images)
                    st.session_state.detection_result = {'keterangan': keterangan, 'score': score}
                    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    image_bytes_list = []
                    for img in images_to_process:
                        img_byte_arr = io.BytesIO()
                        if hasattr(img, 'getvalue'):
                            img_byte_arr.write(img.getvalue())
                        else:
                            Image.open(img).save(img_byte_arr, format='PNG')
                        image_bytes_list.append(img_byte_arr.getvalue())
                    st.session_state.history.append({
                        'id': timestamp,
                        'timestamp': timestamp,
                        'result': st.session_state.detection_result,
                        'images': image_bytes_list
                    })
                st.session_state.detection_done = True
                st.session_state.camera_open = False
                st.rerun()
            else:
                st.warning("Mohon upload atau ambil gambar terlebih dahulu.")
    else:
        # Heading baru untuk halaman hasil deteksi
        st.markdown("<h1 class='main-title'>HASIL DETEKSI</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='main-description'>Ringkasan hasil deteksi pada {datetime.datetime.now().strftime('%d-%m-%Y')}</p>", unsafe_allow_html=True)
        st.divider()
        st.subheader("Hasil Foto")
        if st.session_state.uploaded_images:
            cols = st.columns(min(len(st.session_state.uploaded_images), 5))
            for i, uploaded_image in enumerate(st.session_state.uploaded_images):
                with cols[i % 5]:
                    st.image(uploaded_image, caption=f"Gambar {i+1}", use_container_width=True)
        st.divider()
        st.subheader("Keterangan :")
        st.write(st.session_state.detection_result['keterangan'])
        st.subheader("Score :")
        st.metric(label="Tingkat Kerusakan", value=f"{st.session_state.detection_result['score']}%")
        if st.button("Deteksi Lagi"):
            st.session_state.detection_done = False
            st.session_state.uploaded_images = []
            st.session_state.camera_open = False
            st.rerun()