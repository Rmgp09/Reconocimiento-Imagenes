# image_processing.py
import cv2

class ImageProcessor:
    def load_image(self, file_path):
        try:
            image = cv2.imread(file_path)
            return image
        except Exception as e:
            print(f"Error cargando la imagen: {e}")
            return None

    def detect_anomalies(self, image):
        # Convertimos la imagen a escala de grises y aplicamos un suavizado
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Aplicamos un umbral para detectar áreas de interés
        _, thresholded = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

        # Encontramos contornos en la imagen
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        diagnosis = "No se detectaron anomalías."

        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 5000:  # Área aproximada para simular detección de "anomalías"
                # Clasificamos el área como "tumor" o "quiste" según un criterio de ejemplo
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)

                if aspect_ratio > 0.75:
                    label = "Posible Tumor"
                else:
                    label = "Posible Quiste"
                
                diagnosis = f"Anomalía detectada: {label}"

                # Dibujamos el contorno y el diagnóstico en la imagen
                cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return image, diagnosis
