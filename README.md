<!DOCTYPE html>
<html lang="es">
<body>

  <h1 align="center">Seguimiento de Objetos por Color con Visualización de Trayectoria</h1>

  <p>
    Este proyecto implementa un sistema de visión por computadora en tiempo real que permite detectar objetos en movimiento y seguir su trayectoria según el color predominante (rojo o azul). Al cambiar de color, el sistema reinicia la trayectoria, permitiendo un seguimiento diferenciado por color. Este sistema puede ser usado para fines educativos, de análisis visual o robótica móvil.
  </p>

  <h2>Funcionamiento General</h2>
  <ul>
    <li>Captura video desde la cámara web usando OpenCV.</li>
    <li>Detecta movimiento en la escena mediante diferencia de fotogramas.</li>
    <li>Segmenta colores rojo y azul en el espacio HSV.</li>
    <li>Calcula el centroide del objeto de color dominante.</li>
    <li>Traza en tiempo real la trayectoria del objeto detectado en pantalla.</li>
    <li>Al cambiar de color, reinicia la trayectoria para no mezclar recorridos.</li>
  </ul>

  <h2>Aplicaciones Potenciales</h2>
  <ul>
    <li>Seguimiento visual de robots móviles según color identificador.</li>
    <li>Visualización de trayectorias en pruebas de movimiento.</li>
    <li>Experimentos de detección y análisis de comportamiento visual.</li>
  </ul>

  <h2>Ejemplo de Funcionamiento</h2>
  <p>A continuación se muestra un ejemplo donde el sistema detecta un objeto rojo o azul y traza su trayectoria sobre la imagen:</p>

  <p align="center">
    <img src="https://github.com/user-attachments/assets/698fd727-9800-4516-8f05-f1d21f42e350" alt="Ejemplo de seguimiento por color" width="600">
  </p>
</body>
</html>

