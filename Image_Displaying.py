import sys
import os
import threading
import time
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QObject, pyqtSignal

class ImageCaptureThread(QObject):
    image_captured = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.stop_event = threading.Event()
        self.num_images_processed = 0

    def run(self):
        image_paths = [os.path.join(self.folder_path, filename) for filename in os.listdir(self.folder_path) if filename.endswith('.jpg') or filename.endswith('.png')]
        for image_path in image_paths:
            self.image_captured.emit(image_path)
            self.num_images_processed += 1
            time.sleep(0.5)  # 500ms delay between each image
        self.finished.emit()

    def stop(self):
        self.stop_event.set()


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(400, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    folder_path = "photo"  # Change this to your image folder path

    main_window = ImageViewer()
    main_window.show()

    image_thread = ImageCaptureThread(folder_path)
    image_thread.image_captured.connect(main_window.display_image)
    image_thread_thread = threading.Thread(target=image_thread.run)
    image_thread_thread.start()

    sys.exit(app.exec())
    image_thread.stop()
    image_thread_thread.join()
