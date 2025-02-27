import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt6.QtGui import QImage, QPixmap

def update_histogram(self):
    """Generates and displays the histogram of the edited image."""
    if self.edited_image is None:
        return

    # Convert image to numpy array (ensure it's grayscale or RGB)
    img_array = np.array(self.edited_image)

    # Create a figure for the histogram
    fig = Figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Plot histograms for RGB channels
    colors = ['red', 'green', 'blue']
    for i, color in enumerate(colors):
        ax.hist(img_array[:, :, i].flatten(), bins=256, color=color, alpha=0.6, histtype='step')

    ax.set_xlim([0, 255])
    ax.set_title("Histogram")

    # Convert plot to an image
    canvas = FigureCanvas(fig)
    canvas.draw()

    # Get the buffer (RGBA data)
    width, height = canvas.get_width_height()
    image_data = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)

    # Reshape to match image dimensions
    image_data = image_data.reshape((height, width, 4))

    # Convert the numpy array into QImage
    histogram_image = QImage(image_data.data, width, height, QImage.Format.Format_ARGB32)

    # Display histogram in QLabel
    self.histogram_label.setPixmap(QPixmap.fromImage(histogram_image))
    self.histogram_label.repaint()
