import base64
import io

def convert_image_to_base64(image):
    """Convert the uploaded image file to a base64-encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format=image.format)  # You might need to adjust the format based on the actual image type
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str