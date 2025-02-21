from PIL import Image

class ImageImporter:
    @staticmethod
    def load_image(image_path):
        return Image.open(image_path).convert("RGB")