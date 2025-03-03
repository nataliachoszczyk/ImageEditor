import cv2
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt6.QtGui import QImage, QPixmap

def update_plots(self):
    """Generuje i wyświetla histogram dla kanałów RGB oraz jasności."""
    # if self.edited_image is None:
    #     self.edited_image = self.original_image

    # Konwersja obrazu na tablicę NumPy
    img_array = np.array(self.edited_image)

    # Tworzenie histogramów dla kanałów RGB
    colors = ['red', 'green', 'blue']
    fig, ax = plt.subplots(6, 1, figsize=(6, 12), dpi=80)
    fig.patch.set_facecolor('#333333')
    ax = ax.ravel()

    colvals = ['#ff0000', '#00ff00', '#0000ff']

    for i, color in enumerate(colors):
        histogram, bin_edges = np.histogram(img_array[:, :, i], bins=256, range=(0, 256))
        ax[i].fill_between(bin_edges[:-1], histogram, color=colvals[i], alpha=0.7)
        ax[i].set_xlim([0, 255])
        ax[i].set_yticks([])
        ax[i].set_facecolor('#333333')
        ax[i].tick_params(axis='x', colors='white')
        ax[i].tick_params(axis='y', colors='white')
        ax[i].set_title(f"{color.upper()}", color='white', fontsize=18)


    # Konwersja do skali szarości (poprawna)
    grayscale_values = (0.33 * img_array[:, :, 0] +
                        0.33 * img_array[:, :, 1] +
                        0.33 * img_array[:, :, 2]).astype(np.uint8)

    # Tworzenie histogramu jasności
    histogram, bin_edges = np.histogram(grayscale_values, bins=256, range=(0, 256))
    ax[3].fill_between(bin_edges[:-1], histogram, color="black", alpha=1)
    ax[3].set_xlim([0, 255])
    ax[3].set_yticks([])
    ax[3].set_facecolor('#333333')
    ax[3].tick_params(axis='x', colors='white')
    ax[3].tick_params(axis='y', colors='white')
    ax[3].set_title("Grayscale Histogram", color = 'white', fontsize=18)


    # Projekcja pozioma - sumowanie wartości pikseli wzdłuż wierszy
    horizontal_projection = np.sum(grayscale_values, axis=1)
    ax[4].plot(horizontal_projection, color="#BB86FC", linewidth=4)
    ax[4].set_xlim([0, grayscale_values.shape[0]])
    ax[4].set_yticks([])
    ax[4].set_facecolor('#333333')
    ax[4].tick_params(axis='x', colors='white')
    ax[4].tick_params(axis='y', colors='white')
    ax[4].set_title("Horizontal Projection", color='white', fontsize=18)


    # Projekcja pionowa - sumowanie wartości pikseli wzdłuż kolumn
    vertical_projection = np.sum(grayscale_values, axis=0)
    ax[5].plot(vertical_projection, color="#BB86FC", linewidth=4)
    ax[5].set_xlim([0, grayscale_values.shape[1]])
    ax[5].set_yticks([])
    ax[5].set_facecolor('#333333')
    ax[5].tick_params(axis='x', colors='white')
    ax[5].tick_params(axis='y', colors='white')
    ax[5].set_title("Vertical Projection", color='white', fontsize=18)
    
    
    # Konwersja wykresu do obrazu
    fig.tight_layout()
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = canvas.get_width_height()
    image_data = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8).reshape((height, width, 4))
    image_data = image_data[:, :, [3, 2, 1, 0]]

    # Konwersja NumPy array do QImage
    histogram_image = QImage(image_data.tobytes(), width, height, width * 4, QImage.Format.Format_ARGB32)

    # Wyświetlenie histogramu
    self.histogram_label.setPixmap(
        QPixmap.fromImage(histogram_image).scaled(self.histogram_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    # Zamknięcie figury, aby uniknąć wycieków pamięci
    plt.close(fig)
