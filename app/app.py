import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
from PyQt6.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, \
    QButtonGroup, QRadioButton
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt
import io

from filters.Brightness import adjust_brightness
from filters.ContrastAdjuster import adjust_contrast
from filters.EdgeDetect import roberts_cross, sobel_operator, laplace_filter
from filters.Grayscale import apply_grayscale
from filters.Negative import apply_negative
from filters.Sharpen import sharpen
from filters.Threshold import apply_threshold
from filters.Blur import *
from filters.Plots import update_plots

# TODO no image label
# TODO dodatkowe na 5 
# TODO uporządkować przyciski i ich nagłówki
# TODO Możliwość tworzenia dowolnych wag filtrów - O CO CHODZI?
# TODO eksport aplikacji
# TODO ogarnąć komentarze w kodzie

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.edited_image = None
        self.adjuster = None
        self.grayscale = None
        self.threshold = None
        self.initUI()
        self.update_histogram = update_plots
        self.show()

    def initUI(self):
        # Layouts
        big_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        right_bar_layout = QVBoxLayout()
        image_layout = QHBoxLayout()
        control_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.setMinimumSize(1100, 750)

        # Labels for images
        self.original_label = QLabel("Original Image")
        self.edited_label = QLabel("Edited Image")
        self.original_label.setMinimumSize(300, 300)
        self.edited_label.setMinimumSize(300, 300)
        self.histogram_label = QLabel("Histogram")
        self.histogram_label.setMinimumSize(300, 500)
        self.histogram_label.setMaximumSize(300, 750)
        
        # Display placeholder images initially
        self.display_image(None, self.original_label)
        self.display_image(None, self.edited_label)
        self.display_image(None, self.histogram_label)

        # Brightness slider
        slider_style = """
            QSlider::groove:horizontal { background: #BB86FC; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; border: 2px solid white; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }
            QSlider::handle:horizontal:hover { background: #EEEEEE; }
        """
        
        
        self.setStyleSheet("""
            QWidget {
                background-color: #333333;
                color: white;
            }            
            
            QCheckBox, QRadioButton {
                color: white;
                font-size: 14px;
                padding: 2px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #BB86FC;
                border-radius: 3px;
                background-color: #444444;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #BB86FC;
                border-radius: 10px;
                background-color: #444444;
            }

            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #BB86FC;
                border: 2px solid #BB86FC;
            }

            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background-color: transparent;
                border: 2px solid #BB86FC;
            }

            QCheckBox::indicator:hover, QRadioButton::indicator:hover {
                border: 2px solid #FFFFFF;
            }
        """)

        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setStyleSheet(slider_style)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(300)
        self.brightness_slider.setValue(150)  # Default (no change)
        self.brightness_slider.valueChanged.connect(self.update_image)

        #Threshold checkbox
        self.threshold_checkbox = QCheckBox("Binary Threshold")
        self.threshold_checkbox.stateChanged.connect(self.update_image)

        # Threshold slider
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setStyleSheet(slider_style)
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

        # negative checkbox
        self.negative_checkbox = QCheckBox("Negative")
        self.negative_checkbox.stateChanged.connect(self.update_image)

        # blur toggle
        self.blur_group = QButtonGroup(self)

        self.blur_none= QRadioButton("None")
        self.blur_gauss_radio = QRadioButton("Gaussian")
        self.blur_box_radio = QRadioButton("Box")
        self.blur_circular_radio = QRadioButton("Circular")

        self.blur_group.addButton(self.blur_none, 0)
        self.blur_group.addButton(self.blur_gauss_radio, 1)
        self.blur_group.addButton(self.blur_box_radio, 2)
        self.blur_group.addButton(self.blur_circular_radio, 3)

        self.blur_none.setChecked(True)  # Default selection
        self.blur_group.buttonToggled.connect(self.update_image)

        # gaussian blur slider
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setStyleSheet(slider_style)
        self.blur_slider.setMinimum(1)
        self.blur_slider.setMaximum(11)
        self.blur_slider.setValue(1)
        self.blur_slider.valueChanged.connect(self.update_image)

        #sharpen slider
        self.sharpen_slider = QSlider(Qt.Orientation.Horizontal)
        self.sharpen_slider.setStyleSheet(slider_style)
        self.sharpen_slider.setMinimum(0)
        self.sharpen_slider.setMaximum(3)
        self.sharpen_slider.setValue(0)
        self.sharpen_slider.valueChanged.connect(self.update_image)

        # contrast slider
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setStyleSheet(slider_style)
        self.contrast_slider.setMinimum(0)  # Min is 0 for no contrast
        self.contrast_slider.setMaximum(100)  # Max is 100 for 200% contrast
        self.contrast_slider.setValue(50)  # Default to 50% (no change)

        # Connect slider value change to update image function
        self.contrast_slider.valueChanged.connect(self.update_image)

        #edgedetector
        self.edge_group = QButtonGroup(self)

        self.edge_none = QRadioButton("None")
        self.edge_laplace = QRadioButton("Laplace")
        self.edge_sobel = QRadioButton("Sobel")
        self.edge_roberts = QRadioButton("Roberts")

        self.edge_group.addButton(self.edge_none, 0)
        self.edge_group.addButton(self.edge_laplace, 1)
        self.edge_group.addButton(self.edge_sobel, 2)
        self.edge_group.addButton(self.edge_roberts, 3)

        self.edge_none.setChecked(True)
        self.edge_group.buttonToggled.connect(self.update_image)

        button_style = """
            QPushButton {
                background-color: #BB86FC;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover { background-color: #503D61; }
        """
        
        # Save button
        save_button = QPushButton("Save Edited Image")
        save_button.setStyleSheet(button_style)
        save_button.clicked.connect(self.save_image)

        # Import button
        import_button = QPushButton("Import Image")
        import_button.setStyleSheet(button_style)
        import_button.clicked.connect(self.import_image)

        # Add widgets to layouts
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.edited_label)
        
        right_bar_layout.addWidget(self.histogram_label)
        right_bar_layout.addWidget(import_button)
        right_bar_layout.addWidget(save_button)
        
        threshold_layout = QVBoxLayout()
        threshold_layout.addWidget(self.threshold_checkbox)
        threshold_layout.addWidget(QLabel("Binary threshold:"))
        threshold_layout.addWidget(self.threshold_slider)

        grayscale_layout = QVBoxLayout()
        grayscale_layout.addWidget(QLabel("Grayscale Mode:"))
        grayscale_layout.addWidget(self.grayscale_none)
        grayscale_layout.addWidget(self.grayscale_luminosity)
        grayscale_layout.addWidget(self.grayscale_even)

        blur_layout = QVBoxLayout()
        blur_layout.addWidget(QLabel(""))
        blur_layout.addWidget(QLabel("Blur Mode:"))
        blur_layout.addWidget(self.blur_none)
        blur_layout.addWidget(self.blur_gauss_radio)
        blur_layout.addWidget(self.blur_box_radio)
        blur_layout.addWidget(self.blur_circular_radio)
        blur_layout.addWidget(QLabel("Blur intensity:"))
        blur_layout.addWidget(self.blur_slider)

        sharpness_layout = QVBoxLayout()
        sharpness_layout.addWidget(QLabel("Sharpen:"))
        sharpness_layout.addWidget(self.sharpen_slider)

        edge_layout = QVBoxLayout()
        edge_layout.addWidget(QLabel("Edge Detection:"))
        edge_layout.addWidget(self.edge_none)
        edge_layout.addWidget(self.edge_laplace)
        edge_layout.addWidget(self.edge_sobel)
        edge_layout.addWidget(self.edge_roberts)


        left_layout.addWidget(QLabel("Adjust Brightness:"))
        left_layout.addWidget(self.brightness_slider)
        left_layout.addWidget(QLabel("Adjust Contrast:"))
        left_layout.addWidget(self.contrast_slider)
        left_layout.addWidget(self.negative_checkbox)
        left_layout.addLayout(threshold_layout)
        left_layout.addLayout(grayscale_layout)
        right_layout.addLayout(blur_layout)
        right_layout.addLayout(sharpness_layout)
        right_layout.addLayout(edge_layout)


        control_layout.addLayout(left_layout)
        control_layout.addLayout(right_layout)

        big_layout.addLayout(main_layout)
        big_layout.addLayout(right_bar_layout)
        
        main_layout.addLayout(image_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(big_layout)
        self.resize(1000, 400)

    def resizeEvent(self, event):
        """Automatically resizes images when the window is resized."""
        self.display_image(self.edited_image, self.edited_label)
        self.display_image(self.original_image, self.original_label)
        super().resizeEvent(event)

    def display_image(self, image, label):
        pil_image = Image.fromarray(image) if image is not None else Image.new("RGB", (300, 300))
        label.setText("No Image")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Convert PIL image to QPixmap
        byte_array = io.BytesIO()
        pil_image.save(byte_array, format='PNG')
        q_image = QImage.fromData(byte_array.getvalue())
        pixmap = QPixmap.fromImage(q_image)

        # Scale image to fit QLabel while maintaining aspect ratio
        label.setPixmap(
            pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def update_image(self):
        """Apply filters to the image and display the edited image."""
        if self.original_image is not None:
            self.edited_image = self.original_image.copy()

            if self.brightness_slider.value() != 150:
                value = self.brightness_slider.value() - 150  # Shift value to range from -150 to 150
                self.edited_image = adjust_brightness(self.edited_image, value)

            if self.contrast_slider.value() != 50:
                value = self.contrast_slider.value() /50
                self.edited_image = adjust_contrast(self.edited_image,value)

            grayscale_mode = self.grayscale_group.checkedId()

            if grayscale_mode == 1:
                self.edited_image = apply_grayscale(self.edited_image, 'luminosity')
            elif grayscale_mode == 2:
                self.edited_image = apply_grayscale(self.edited_image, 'even')

            if self.threshold_checkbox.isChecked():
                self.edited_image = apply_threshold(self.edited_image, self.threshold_slider.value())

            if self.negative_checkbox.isChecked():
                self.edited_image = apply_negative(self.edited_image)

            blur_mode = self.blur_group.checkedId()
            if blur_mode == 1:
                self.edited_image = blur(self.edited_image, self.blur_slider.value() *2-1, 'gaussian')
            elif blur_mode == 2:
                self.edited_image = blur(self.edited_image,  self.blur_slider.value() *2-1, 'box')
            elif blur_mode == 3:
                self.edited_image = blur(self.edited_image,  self.blur_slider.value() *2-1, 'circular')

            if self.sharpen_slider.value() != 0:
                self.edited_image = sharpen(self.edited_image, self.sharpen_slider.value())

            edge_mode = self.edge_group.checkedId()
            if edge_mode == 1:
                self.edited_image = laplace_filter(self.edited_image)
            elif edge_mode == 2:
                self.edited_image = sobel_operator(self.edited_image)
            elif edge_mode == 3:
                self.edited_image = roberts_cross(self.edited_image)

            self.display_image(self.edited_image, self.edited_label)
            update_plots(self)

    def import_image(self):
        # Open file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if image_path:
            # Load the image
            self.original_image = np.array(Image.open(image_path).convert("RGB"))
            self.edited_image = self.original_image
            self.display_image(self.original_image, self.original_label)
            self.display_image(self.edited_image, self.edited_label)
        self.update_image()

    def save_image(self):
        # Save the edited image
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if save_path:
            Image.fromarray(self.edited_image).save(save_path)
