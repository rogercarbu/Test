
import streamlit as st
from PIL import Image, ImageFilter

def main():
    st.title("Image Processing App")
    st.write("Upload an image and choose an operation from the sidebar.")

    # Upload image
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display original image
        st.subheader("Original Image")
        image = Image.open(uploaded_image)
        st.image(image, caption="Original", use_column_width=True)

        # Sidebar operations
        st.sidebar.title("Image Operations")
        operation = st.sidebar.selectbox("Choose an operation", ["None", "Grayscale", "Blur"])

        if operation == "Grayscale":
            grayscale_image = image.convert('L')
            st.subheader("Grayscale Image")
            st.image(grayscale_image, caption="Grayscale", use_column_width=True)

        elif operation == "Blur":
            blur_radius = st.sidebar.slider("Select blur radius", 0, 10, 2)
            blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
            st.subheader("Blurred Image")
            st.image(blurred_image, caption=f"Blur radius: {blur_radius}", use_column_width=True)

if __name__ == "__main__":
    main()
