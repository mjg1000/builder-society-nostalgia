import streamlit as st
from PIL import Image, UnidentifiedImageError
import io # Used to handle the uploaded file bytes

# --- Attempt to import optional libraries ---
try:
    import imageio.v3 as iio
    IMAGEIO_AVAILABLE = True 
except ImportError:
    IMAGEIO_AVAILABLE = False 
    
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass 

# --- UI Setup ---
st.set_page_config(layout="centered")

# --- ⭐ 1. UPDATED CSS BLOCK ---
st.markdown(
    """
    <style>
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #f6d365, #fda085, #e73c7e, #23a6d5);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    /* This makes the title white */
    .stApp h1 {
        color: #FFFFFF;
    }

    /* --- NEW RULES FOR FONT STYLING --- */

    /* Style for the '🎵 Your Song...' subheader */
    .stApp [data-testid="stSubheader"] {
        font-size: 1.6rem;      /* Increase font size */
        font-weight: 600;       /* Make it bolder */
        color: #FFFFFF;         /* Make it white */
    }
    
    /* Style for the 'Now playing...' caption */
    .stApp [data-testid="stCaption"] {
        font-size: 1.1rem;      /* Increase font size */
        font-weight: 500;       /* Make it slightly bold */
        color: #E0E0E0;         /* Make it a light gray/off-white */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
# --- END OF STYLE CODE ---


st.title("🖼️ Memoria: The Path to Relive")

if not IMAGEIO_AVAILABLE:
    st.warning("ImageIO library not found. Some formats (like scientific or video) may not load.")

uploaded_file = st.file_uploader(
    "Upload your picture (any format)", 
    type=None 
)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    img = None
    error_message = ""

    # (Backend logic for image opening remains the same)
    try:
        img = Image.open(io.BytesIO(file_bytes))
    except UnidentifiedImageError:
        error_message = "Pillow could not identify this image format."
    except Exception as e:
        error_message = f"An error occurred with Pillow: {e}"

    if img is None and IMAGEIO_AVAILABLE:
        st.info("Pillow failed. Trying with ImageIO...")
        try:
            img = iio.imread(file_bytes)
        except Exception as e:
            error_message = f"Pillow failed. ImageIO also failed: {e}"
    elif img is None and not IMAGEIO_AVAILABLE:
        error_message += " (ImageIO not installed to try other formats.)"

    # 3. THE RESULT:
    if img is not None:
        st.success(f"Successfully loaded '{uploaded_file.name}'")
        st.image(img, caption="Your Uploaded Image", use_container_width=True)
        
        # --- ⭐ 2. SONG NAME SECTION ---
        st.divider() 
        st.subheader("🎵 Your Song from that Day")
        
        # This line displays the song name (no ** needed)
        st.caption("Now playing: BTS - MIC Drop") 

        # This line is your player
        st.audio(r"C:/Users/anrad/Videos/Kpop💜/BTS/MIC Drop.mp4", format="video/mp4")
        
    else:
        st.error(f"Could not read image: {error_message}")