import numpy as np
from PIL import Image
from PyQt6.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, \
    QButtonGroup, QRadioButton, QGridLayout, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import io

from tools.Convolve import convolve

from tools.Brightness import *
from tools.Mask import mask
from tools.Saturation import *
from tools.ContrastAdjuster import adjust_contrast
from tools.EdgeDetect import roberts_cross, sobel_operator, laplace_filter
from tools.Grayscale import apply_grayscale
from tools.Negative import apply_negative
from tools.Sharpen import sharpen
from tools.Threshold import apply_threshold
from tools.Blur import *
from tools.Plots import update_plots
from tools.CreateMatrix import create_matrix

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
        self.showMaximized()

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
        
        self.display_image(None, self.original_label)
        self.display_image(None, self.edited_label)
        self.display_image(None, self.histogram_label)

        # slider styles
        slider_style = """
            QSlider::groove:horizontal { background: #BB86FC; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; border: 2px solid white; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }
            QSlider::handle:horizontal:hover { background: #EEEEEE; }
        """
        
        red_slider_style = """
            QSlider::groove:horizontal { background: red; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; border: 2px solid white; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }
            QSlider::handle:horizontal:hover { background: #EEEEEE; }
        """
        
        green_slider_style = """
            QSlider::groove:horizontal { background: green; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; border: 2px solid white; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }
            QSlider::handle:horizontal:hover { background: #EEEEEE; }
        """
        
        blue_slider_style = """
            QSlider::groove:horizontal { background: blue; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; border: 2px solid white; width: 14px; height: 14px; margin: -6px 0; border-radius: 8px; }
            QSlider::handle:horizontal:hover { background: #EEEEEE; }
        """
        
        # button styles
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
        
        mini_button_style = """
            QPushButton {
                background-color: #BB86FC;
                border-radius: 6px;
                padding: 3px;
                font-size: 13px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover { background-color: #503D61; }
        """
        
        # app style
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

        # brightness slider
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setStyleSheet(slider_style)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(300)
        self.brightness_slider.setValue(150)  # Default (no change)
        self.brightness_slider.sliderReleased.connect(self.update_image)
        
        # RGB sliders
        self.red_slider = QSlider(Qt.Orientation.Horizontal)
        self.red_slider.setStyleSheet(red_slider_style)
        self.red_slider.setMinimum(0)
        self.red_slider.setMaximum(150)
        self.red_slider.setValue(0)  # Default (no change)
        self.red_slider.sliderReleased.connect(self.update_image)
        
        self.green_slider = QSlider(Qt.Orientation.Horizontal)
        self.green_slider.setStyleSheet(green_slider_style)
        self.green_slider.setMinimum(0)
        self.green_slider.setMaximum(150)
        self.green_slider.setValue(0)  # Default (no change)
        self.green_slider.sliderReleased.connect(self.update_image)
        
        self.blue_slider = QSlider(Qt.Orientation.Horizontal)
        self.blue_slider.setStyleSheet(blue_slider_style)
        self.blue_slider.setMinimum(0)
        self.blue_slider.setMaximum(150)
        self.blue_slider.setValue(0)  # Default (no change)
        self.blue_slider.sliderReleased.connect(self.update_image)
        

        #threshold checkbox
        self.threshold_checkbox = QCheckBox("Binary Threshold")
        self.threshold_checkbox.stateChanged.connect(self.update_image)

        # threshold slider
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setStyleSheet(slider_style)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(122)
        self.threshold_slider.sliderReleased.connect(self.update_image)

        # grayscale radio buttons
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
        self.blur_slider.sliderReleased.connect(self.update_image)

        #sharpen slider
        self.sharpen_slider = QSlider(Qt.Orientation.Horizontal)
        self.sharpen_slider.setStyleSheet(slider_style)
        self.sharpen_slider.setMinimum(0)
        self.sharpen_slider.setMaximum(3)
        self.sharpen_slider.setValue(0)
        self.sharpen_slider.sliderReleased.connect(self.update_image)

        # contrast slider
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setStyleSheet(slider_style)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.sliderReleased.connect(self.update_image)

        #edge detector
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
        
        # image layout
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.edited_label)
        
        # right bar layout
        right_bar_layout.addWidget(self.histogram_label)

        # custom kernel
        self.kernel_layout = QHBoxLayout()
        self.kernel_layout.addWidget(QLabel("Custom kernel weights:"))

        # Assuming mini_button_style is already defined, here's an example:

        self.button_3x3 = QPushButton("3x3")
        self.button_3x3.setStyleSheet(mini_button_style)
        self.button_3x3.setCheckable(True)  # Make it checkable

        self.button_5x5 = QPushButton("5x5")
        self.button_5x5.setStyleSheet(mini_button_style)
        self.button_5x5.setCheckable(True)  # Make it checkable

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # Ensure only one button can be checked at a time
        self.button_group.addButton(self.button_3x3)
        self.button_group.addButton(self.button_5x5)

        # Add the buttons to the layout
        self.kernel_layout.addWidget(self.button_3x3)
        self.kernel_layout.addWidget(self.button_5x5)
        right_bar_layout.addLayout(self.kernel_layout)

        # apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet(mini_button_style)
        right_bar_layout.addWidget(self.apply_button)
        self.apply_button.setCheckable(True)
        self.apply_button.clicked.connect(self.update_image)

        # matrix
        self.matrix_container = QFrame()
        self.matrix_container.setFixedSize(300, 150)
        self.matrix_layout = QGridLayout(self.matrix_container)
        self.matrix_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_bar_layout.addWidget(self.matrix_container)
        
        self.button_3x3.clicked.connect(lambda: create_matrix(self.matrix_layout, 3))
        self.button_5x5.clicked.connect(lambda: create_matrix(self.matrix_layout, 5))
        
        self.button_5x5.setDefault(True)
        self.button_5x5.setChecked(True)
        create_matrix(self.matrix_layout, 5)
        
        # import and save buttons
        save_button = QPushButton("Save Edited Image")
        save_button.setStyleSheet(button_style)
        save_button.clicked.connect(self.save_image)

        import_button = QPushButton("Import Image")
        import_button.setStyleSheet(button_style)
        import_button.clicked.connect(self.import_image)
        
        right_bar_layout.addWidget(import_button)
        right_bar_layout.addWidget(save_button)
        
        # threshold
        threshold_layout = QVBoxLayout()
        threshold_layout.addWidget(self.threshold_checkbox)
        threshold_layout.addWidget(QLabel("Binary threshold:"))
        threshold_layout.addWidget(self.threshold_slider)
        
        # grayscale
        grayscale_layout = QVBoxLayout()
        grayscale_layout.addWidget(QLabel("Grayscale Mode:"))
        grayscale_layout.addWidget(self.grayscale_none)
        grayscale_layout.addWidget(self.grayscale_luminosity)
        grayscale_layout.addWidget(self.grayscale_even)

        # blur
        blur_layout = QVBoxLayout()
        blur_layout.addWidget(QLabel(""))
        blur_layout.addWidget(QLabel("Blur Mode:"))
        blur_layout.addWidget(self.blur_none)
        blur_layout.addWidget(self.blur_gauss_radio)
        blur_layout.addWidget(self.blur_box_radio)
        blur_layout.addWidget(self.blur_circular_radio)
        blur_layout.addWidget(QLabel("Blur intensity:"))
        blur_layout.addWidget(self.blur_slider)

        # sharpness
        sharpness_layout = QVBoxLayout()
        sharpness_layout.addWidget(QLabel("Sharpen:"))
        sharpness_layout.addWidget(self.sharpen_slider)

        # edge detection
        edge_layout = QVBoxLayout()
        edge_layout.addWidget(QLabel("Edge Detection:"))
        edge_layout.addWidget(self.edge_none)
        edge_layout.addWidget(self.edge_laplace)
        edge_layout.addWidget(self.edge_sobel)
        edge_layout.addWidget(self.edge_roberts)

        # left layout
        left_layout.addWidget(QLabel("Adjust Brightness:"))
        left_layout.addWidget(self.brightness_slider)
        left_layout.addWidget(QLabel("Adjust RGB Saturation"))
        left_layout.addWidget(self.red_slider)
        left_layout.addWidget(self.green_slider)
        left_layout.addWidget(self.blue_slider)
        
        left_layout.addWidget(QLabel("Adjust Contrast:"))
        left_layout.addWidget(self.contrast_slider)
        left_layout.addWidget(self.negative_checkbox)
        left_layout.addLayout(threshold_layout)
        left_layout.addLayout(grayscale_layout)
        right_layout.addLayout(blur_layout)
        right_layout.addLayout(sharpness_layout)
        right_layout.addLayout(edge_layout)

        # control layout
        control_layout.addLayout(left_layout)
        control_layout.addLayout(right_layout)

        # main layouts
        big_layout.addLayout(main_layout)
        big_layout.addLayout(right_bar_layout)
        
        main_layout.addLayout(image_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(big_layout)
        self.resize(1000, 400)

    def resizeEvent(self, event):
        self.display_image(self.edited_image, self.edited_label)
        self.display_image(self.original_image, self.original_label)
        super().resizeEvent(event)

    def display_image(self, image, label):
        pil_image = Image.fromarray(image) if image is not None else Image.new("RGB", (300, 300))
        label.setText("No Image")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # PIL image to QPixmap
        byte_array = io.BytesIO()
        pil_image.save(byte_array, format='PNG')
        q_image = QImage.fromData(byte_array.getvalue())
        pixmap = QPixmap.fromImage(q_image)

        # scale image to fit QLabel with aspect ratio
        label.setPixmap(
            pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def update_image(self):
        if self.original_image is not None:
            self.edited_image = self.original_image.copy()

            if self.brightness_slider.value() != 150:
                value = self.brightness_slider.value() - 150  # Shift value to range from -150 to 150
                self.edited_image = adjust_brightness(self.edited_image, value)
                
            if self.red_slider.value() != 150:
                value = self.red_slider.value()
                self.edited_image = adjust_red_saturation(self.edited_image, value)
                
            if self.green_slider.value() != 150:
                value = self.green_slider.value()
                self.edited_image = adjust_green_saturation(self.edited_image, value)
        
            if self.blue_slider.value() != 150:
                value = self.blue_slider.value()
                self.edited_image = adjust_blue_saturation(self.edited_image, value)

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

            if self.apply_button.isChecked():
                checked_button = self.button_group.checkedButton()
                if self.button_3x3.isChecked():
                    kernel_size = 3
                else:
                    kernel_size = 5
                print(f"Applying custom kernel of size {kernel_size}")
                kernel = []
                for i in range(kernel_size):
                    row = []
                    for j in range(kernel_size):
                        item = self.matrix_layout.itemAtPosition(i, j)
                        if item is None:
                            print(f"Warning: No widget at ({i}, {j})")
                            continue  # Skip this cell

                        widget = item.widget()
                        if widget:
                            row.append(widget.text())
                    kernel.append(row)
                kernel = np.array(kernel, dtype=np.float32)
                self.edited_image = mask(self.edited_image, kernel)

            self.display_image(self.edited_image, self.edited_label)
            update_plots(self)

    def import_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if image_path:
            self.original_image = np.array(Image.open(image_path).convert("RGB"))
            self.edited_image = self.original_image
            self.display_image(self.original_image, self.original_label)
            self.display_image(self.edited_image, self.edited_label)
        self.update_image()

    def save_image(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        if save_path:
            Image.fromarray(self.edited_image).save(save_path)
