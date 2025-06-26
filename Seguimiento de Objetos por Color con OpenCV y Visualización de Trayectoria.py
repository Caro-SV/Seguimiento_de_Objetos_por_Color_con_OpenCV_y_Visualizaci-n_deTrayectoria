import cv2 as cv
import numpy as np

# Clase principal que inicializa los componentes del sistema
class VideoManager():
    def __init__(self):
        self.video = capturaVideo()      # Encargada de manejar la cámara y visualización
        self.motion = MotionDetector()   # Detector de movimiento por diferencia de frames
        self.color = ColorDetector()     # Detector de color y centroide del objeto

    def run(self):
        self.video.captura(self.motion, self.color)  # Inicia el ciclo principal

# Clase para capturar video, gestionar la trayectoria y dibujar resultados
class capturaVideo():
    def __init__(self):
        self.cap = cv.VideoCapture(0)     # Abre la cámara (índice 0 por defecto)
        self.trayectoria = []             # Lista para almacenar puntos del recorrido
        self.color_anterior = " "         # Controla el reinicio por cambio de color

    def captura(self, motion, color):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            _, contornos = motion.detect(frame)                          # Detecta movimiento
            _, color_detectado, ptos = color.proceso(contornos, frame)  # Detecta color y centro

            # Si se detecta rojo o azul, actualiza la trayectoria
            if color_detectado.strip().upper() in ["ROJO", "AZUL"]:
                # Reinicia trayectoria si el color cambió
                if color_detectado != self.color_anterior:
                    self.trayectoria = []
                    self.color_anterior = color_detectado

                self.trayectoria.append(ptos)

                # Mantiene máximo 50 puntos
                if len(self.trayectoria) > 50:
                    self.trayectoria.pop(0)

            # Dibuja texto y línea de trayectoria según el color detectado
            if color_detectado.strip().upper() == "ROJO":
                cv.putText(frame, "COLOR DETECTADO: ROJO", (10, 30),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if len(self.trayectoria) >= 2:
                    for i in range(1, len(self.trayectoria)):
                        cv.line(frame, self.trayectoria[i-1], self.trayectoria[i],
                                (0, 0, 255), 2, cv.LINE_8, 0)

            elif color_detectado.strip().upper() == "AZUL":
                cv.putText(frame, "COLOR DETECTADO: AZUL", (10, 30),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                if len(self.trayectoria) >= 2:
                    for i in range(1, len(self.trayectoria)):
                        cv.line(frame, self.trayectoria[i-1], self.trayectoria[i],
                                (255, 0, 0), 2, cv.LINE_8, 0)

            # Muestra el frame con resultados
            cv.imshow("VIDEO CAPTURA", frame)

            # Presionar ESC para salir
            if cv.waitKey(1) == 27:
                self.salir()
                break

    def salir(self):
        self.cap.release()
        cv.destroyAllWindows()

# Clase para detectar movimiento entre frames
class MotionDetector():
    def __init__(self):
        self.prev_gray = None

    def detect(self, frame):
        # Preprocesamiento del frame actual
        self.act_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.act_gray = cv.GaussianBlur(self.act_gray, (21, 21), 0)

        # Si no hay frame previo, inicializarlo
        if self.prev_gray is None:
            self.prev_gray = self.act_gray
            return np.zeros_like(self.act_gray), []

        # Diferencia de frames para detectar cambio (movimiento)
        dif = cv.absdiff(self.act_gray, self.prev_gray)
        _, thresh = cv.threshold(dif, 25, 255, cv.THRESH_BINARY)
        thresh = cv.dilate(thresh, None, iterations=2)

        self.prev_gray = self.act_gray

        # Obtiene contornos del movimiento
        contornos, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return thresh, contornos

# Clase para detectar color predominante en zonas con movimiento
class ColorDetector():
    def __init__(self):
        pass

    def proceso(self, contornos, frame):
        # Crea una máscara negra y dibuja los contornos sobre ella
        mascara_mov = np.zeros_like(frame[:, :, 0])
        cv.drawContours(mascara_mov, contornos, -1, 255, thickness=cv.FILLED)

        # Aplica la máscara al frame para extraer zonas en movimiento
        mov = cv.bitwise_and(frame, frame, mask=mascara_mov)

        # Procesa el color sobre la zona en movimiento
        mask_color, color_detectado, p = self.color(mov)
        return mask_color, color_detectado, p

    def color(self, frame):
        # Convierte el frame a HSV para facilitar la segmentación por color
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Define rangos para el azul (dos rangos para cubrir distintas tonalidades)
        lower_blue1, upper_blue1 = np.array([100, 150, 50]), np.array([130, 255, 255])
        lower_blue2, upper_blue2 = np.array([90, 50, 70]), np.array([110, 150, 255])
        mask1 = cv.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv.inRange(hsv, lower_blue2, upper_blue2)
        mask_blue = cv.bitwise_or(mask1, mask2)

        # Define rangos para el rojo (dos rangos por envolvimiento del hue)
        lower_red1, upper_red1 = np.array([0, 100, 20]), np.array([10, 255, 255])
        lower_red2, upper_red2 = np.array([160, 100, 20]), np.array([179, 255, 255])
        mask3 = cv.inRange(hsv, lower_red1, upper_red1)
        mask4 = cv.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv.bitwise_or(mask3, mask4)

        # Cuenta cantidad de píxeles detectados por color
        red_pixels = cv.countNonZero(mask_red)
        blue_pixels = cv.countNonZero(mask_blue)

        color_detectado = ' '
        cx, cy = 0, 0

        # Si se detecta suficiente rojo, calcula centroide
        if red_pixels > 500:
            color_detectado = 'ROJO'
            cont_red, _ = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if cont_red:
                c = max(cont_red, key=cv.contourArea)
                M = cv.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

        # Si se detecta suficiente azul, calcula centroide
        if blue_pixels > 500:
            color_detectado = 'AZUL'
            cont_blue, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if cont_blue:
                c = max(cont_blue, key=cv.contourArea)
                M = cv.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

        puntos = (cx, cy)
        mask = cv.bitwise_or(mask_blue, mask_red)

        return mask, color_detectado, puntos

# Ejecuta el sistema
sistema = VideoManager()
sistema.run()