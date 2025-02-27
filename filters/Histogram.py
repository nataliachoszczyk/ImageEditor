import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt6.QtGui import QImage, QPixmap

def update_histogram(self):
    """Generuje i wyświetla histogram dla kanałów RGB oraz jasności."""
    if self.edited_image is None:
        return

    # Konwersja obrazu na tablicę NumPy
    img_array = np.array(self.edited_image)

    # Konwersja do skali szarości (poprawna)
    grayscale_values = (0.33 * img_array[:, :, 0] +
                        0.33 * img_array[:, :, 1] +
                        0.33 * img_array[:, :, 2]).astype(np.uint8)

    # Tworzenie histogramu
    histogram, bin_edges = np.histogram(grayscale_values, bins=256, range=(0, 256))

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(4, 2), dpi=80)
    ax.set_title("Grayscale Histogram")
    ax.set_xlim([0, 255])
    ax.set_yticks([])

    # Rysowanie histogramu
    ax.fill_between(bin_edges[:-1], histogram, color="black", alpha=1)

    # Konwersja wykresu do obrazu
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = canvas.get_width_height()
    image_data = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8).reshape((height, width, 4))

    # Konwersja NumPy array do QImage
    histogram_image = QImage(image_data.tobytes(), width, height, width*4, QImage.Format.Format_ARGB32)

    # Wyświetlenie histogramu
    self.histogram_label.setPixmap(QPixmap.fromImage(histogram_image))
    self.histogram_label.repaint()

    # Zamknięcie figury, aby uniknąć wycieków pamięci
    plt.close(fig)

