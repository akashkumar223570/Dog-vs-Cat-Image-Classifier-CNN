import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# ------------------------
# Page Config
# ------------------------

st.set_page_config(
    page_title="Petwise Classifier",
    page_icon="🐶",
    layout="wide"
)

# ------------------------
# Custom CSS
# ------------------------

st.markdown("""
<style>

.main {
background-color:#0f172a;
color:white;
}

.block-container {
padding-top:2rem;
}

.title {
font-size:30px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# Load Model
# ------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("/teamspace/studios/this_studio/Cat_vs_Dog/CNN_Project/cats_dogs_cnn_model.h5")

model = load_model()

# ------------------------
# Header
# ------------------------

st.markdown("<div class='title'>🐶 Petwise Classifier</div>", unsafe_allow_html=True)
st.write("Upload an image and the AI will identify whether it is a **Cat or Dog**.")

# ------------------------
# Upload Section
# ------------------------

uploaded_file = st.file_uploader("Drop your image here", type=["jpg","jpeg","png"])

# ------------------------
# Prediction Function
# ------------------------

def predict_image(image):

    img = image.resize((150,150))
    img = np.array(img)/255
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    prob = float(prediction[0][0])

    if prob > 0.5:
        label = "Dog 🐶"
        confidence = prob
    else:
        label = "Cat 🐱"
        confidence = 1 - prob

    return label, confidence, prob

# ------------------------
# Result Section
# ------------------------

if uploaded_file:

    image = Image.open(uploaded_file)

    label, confidence, prob = predict_image(image)

    col1, col2 = st.columns(2)

    # Image Section
    with col1:

        st.markdown("### Uploaded Image")
        st.image(image, width=450)

    # Prediction Section
    with col2:

        st.markdown("### Prediction")
        st.success(label)

        st.markdown("### Confidence Score")
        st.metric(label="Model Confidence", value=f"{confidence*100:.2f}%")

        st.progress(confidence)

        # Probability Graph
        import matplotlib.pyplot as plt

        st.markdown("### Class Probabilities")

        labels = ["Dog 🐶", "Cat 🐱"]
        values = [prob, 1-prob]

        fig, ax = plt.subplots(figsize=(3.5,1.8))

        bars = ax.barh(labels, values, height=0.3)

        # Highlight predicted class
        for i, v in enumerate(values):
            if v == max(values):
                bars[i].set_color("#4CAF50")   # green
            else:
                bars[i].set_color("#9E9E9E")   # gray

        # Percentage labels
        for i, v in enumerate(values):
            ax.text(v + 0.02, i, f"{v*100:.1f}%", va='center')

        ax.set_xlim(0,1)
        ax.set_xlabel("Probability")
        ax.set_title("Model Prediction Confidence")

        st.pyplot(fig)