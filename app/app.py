from PyQt6.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, \
    QButtonGroup, QRadioButton
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import io
from filters.BrightAdjuster import BrightAdjuster
from filters.Grayscale import Grayscale
from filters.Threshold import Threshold
from imageHandler.ImageImporter import ImageImporter
from imageHandler.ImageSaver import ImageSaver


class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.original_image = None
        self.edited_image = None
        self.adjuster = None
        self.grayscale = None
        self.threshold = None
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
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)  # 0.5x brightness
        self.brightness_slider.setMaximum(300)  # 1.5x brightness
        self.brightness_slider.setValue(150)  # Default (no change)
        self.brightness_slider.valueChanged.connect(self.update_image)

        #Threshold checkbox
        self.threshold_checkbox = QCheckBox("Threshold")
        self.threshold_checkbox.stateChanged.connect(self.toggle_threshold)

        # Threshold slider
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(122)
        self.threshold_slider.valueChanged.connect(self.update_image)

        # Grayscale radio buttons
        self.grayscale_group = QButtonGroup(self)

        self.grayscale_none = QRadioButton("None")
        self.grayscale_luminosity = QRadioButton("Luminosity")
        self.grayscale_even = QRadioButton("Even Values")

        self.grayscale_group.addButton(self.grayscale_none, 0)
        self.grayscale_group.addButton(self.grayscale_luminosity, 1)
        self.grayscale_group.addButton(self.grayscale_even, 2)

        self.grayscale_none.setChecked(True)  # Default selection
        self.grayscale_group.buttonToggled.connect(self.update_image)

        # Save button
        save_button = QPushButton("Save Edited Image")
        save_button.clicked.connect(self.save_image)

        # Import button
        import_button = QPushButton("Import IMG")
        import_button.clicked.connect(self.import_image)

        # Add widgets to layouts
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.edited_label)

        threshold_layout = QVBoxLayout()
        threshold_layout.addWidget(self.threshold_checkbox)
        threshold_layout.addWidget(QLabel("Threshold:"))
        threshold_layout.addWidget(self.threshold_slider)

        grayscale_layout = QVBoxLayout()
        grayscale_layout.addWidget(QLabel("Grayscale Mode:"))
        grayscale_layout.addWidget(self.grayscale_none)
        grayscale_layout.addWidget(self.grayscale_luminosity)
        grayscale_layout.addWidget(self.grayscale_even)


        control_layout.addWidget(QLabel("Adjust Brightness:"))
        control_layout.addWidget(self.brightness_slider)
        control_layout.addLayout(grayscale_layout)
        control_layout.addLayout(threshold_layout)
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

    def update_image(self):
        """Apply filters to the image and display the edited image."""
        if self.original_image:
            self.edited_image = self.original_image.copy()

            if self.brightness_slider.value() != 150:
                value = self.brightness_slider.value() - 150  # Shift value to range from -150 to 150
                self.edited_image = self.adjuster.adjust_brightness(value)

            grayscale_mode = self.grayscale_group.checkedId()

            if grayscale_mode == 1:
                self.edited_image = self.grayscale.apply(self.edited_image, 'luminosity')
            elif grayscale_mode == 2:
                self.edited_image = self.grayscale.apply(self.edited_image, 'even')

            if self.threshold_checkbox.isChecked():
                self.edited_image = self.threshold.apply(self.edited_image, self.threshold_slider.value())

            self.display_image(self.edited_image, self.edited_label)

    def toggle_grayscale(self):
        """Apply grayscale filter when checkbox is toggled."""
        self.update_image()

    def toggle_threshold(self):
        """Apply threshold filter when checkbox is toggled."""
        self.update_image()

    def import_image(self):
        # Open file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if image_path:
            # Load the image using the ImageImporter
            self.original_image = ImageImporter.load_image(image_path)
            self.adjuster = BrightAdjuster(self.original_image)
            self.grayscale = Grayscale()
            self.threshold = Threshold()
            self.edited_image = self.original_image
            self.display_image(self.original_image, self.original_label)
            self.display_image(self.edited_image, self.edited_label)

    def save_image(self):
        # Save the edited image
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if save_path:
            ImageSaver.save_image(self.edited_image, save_path)
