from PyQt6.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import io
from filters.BrightAdjuster import BrightAdjuster
from imageHandler.ImageImporter import ImageImporter
from imageHandler.ImageSaver import ImageSaver

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.original_image = None
        self.edited_image = None
        self.adjuster = None
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        image_layout = QHBoxLayout()
        control_layout = QVBoxLayout()

        # Labels for images
        self.original_label = QLabel("Original Image")
        self.edited_label = QLabel("Edited Image")

        # Display placeholder images initially
        self.display_image(None, self.original_label)
        self.display_image(None, self.edited_label)

        # Brightness slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)   # 0.5x brightness
        self.slider.setMaximum(300)  # 1.5x brightness
        self.slider.setValue(150)    # Default (no change)
        self.slider.valueChanged.connect(self.update_brightness)

        # Save button
        save_button = QPushButton("Save Edited Image")
        save_button.clicked.connect(self.save_image)

        # Import button
        import_button = QPushButton("Import IMG")
        import_button.clicked.connect(self.import_image)

        # Add widgets to layouts
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.edited_label)

        control_layout.addWidget(QLabel("Adjust Brightness:"))
        control_layout.addWidget(self.slider)
        control_layout.addWidget(import_button)
        control_layout.addWidget(save_button)

        main_layout.addLayout(image_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)
        self.resize(800, 400)

        
    def display_image(self, pil_image, label):
        if pil_image is None:
            label.setText("No Image")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return
        
        # Convert PIL image to QPixmap
        byte_array = io.BytesIO()
        pil_image.save(byte_array, format='PNG')
        q_image = QImage.fromData(byte_array.getvalue())
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio))

        
    def update_brightness(self):
        value = self.slider.value() - 150  # Shift the value to range from -50 to 50
        self.edited_image = self.adjuster.adjust_brightness(value)
        self.display_image(self.edited_image, self.edited_label)

    def import_image(self):
        # Open file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if image_path:
            # Load the image using the ImageImporter
            self.original_image = ImageImporter.load_image(image_path)
            self.adjuster = BrightAdjuster(self.original_image)
            self.edited_image = self.original_image
            self.display_image(self.original_image, self.original_label)
            self.display_image(self.edited_image, self.edited_label)

    def save_image(self):
        # Save the edited image
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
        if save_path:
            ImageSaver.save_image(self.edited_image, save_path)