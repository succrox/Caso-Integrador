"""
Donut 3D Rotatorio con Pygame
==============================

Este programa renderiza un toroide (donut) 3D rotatorio en tiempo real
utilizando proyección 3D y cálculos de iluminación.

Autor: Versión mejorada
Fecha: 2025
Requisitos: pygame, math

Controles:
    - ESC o cerrar ventana: Salir del programa
    - ESPACIO: Pausar/Reanudar rotación
    - R: Reiniciar rotación
    - +/-: Ajustar velocidad de rotación
"""

import math
import pygame
import sys


class Donut3D:
    """
    Clase que representa un toroide (donut) 3D rotatorio.
    
    Atributos:
        width (int): Ancho de la ventana
        height (int): Alto de la ventana
        A (float): Ángulo de rotación en eje X
        B (float): Ángulo de rotación en eje Z
        rotation_speed (float): Velocidad de rotación
        paused (bool): Estado de pausa
    """
    
    def __init__(self, width=800, height=600):
        """
        Inicializa el renderizador del donut 3D.
        
        Args:
            width (int): Ancho de la ventana en píxeles
            height (int): Alto de la ventana en píxeles
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Donut 3D Rotatorio")
        self.clock = pygame.time.Clock()
        
        # Ángulos de rotación
        self.A = 0.0
        self.B = 0.0
        
        # Control de velocidad y pausa
        self.rotation_speed = 1.0
        self.paused = False
        
        # Configuración de renderizado
        self.pixel_size = 4  # Tamaño de cada "píxel" del donut
        self.grid_width = width // self.pixel_size
        self.grid_height = height // self.pixel_size
        
        # Fuente para texto
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Paleta de colores (de oscuro a claro)
        self.colors = [
            (10, 10, 30),    # Muy oscuro
            (20, 20, 60),
            (40, 40, 100),
            (60, 60, 140),
            (80, 100, 180),
            (100, 140, 200),
            (140, 180, 220),
            (180, 200, 240),
            (200, 220, 250),
            (220, 230, 255),
            (240, 245, 255),
            (255, 255, 255)  # Más brillante
        ]
    
    def calculate_point(self, theta, phi):
        """
        Calcula las coordenadas 3D y la luminancia de un punto en el toroide.
        
        Args:
            theta (float): Ángulo del círculo principal (0 a 2π)
            phi (float): Ángulo del círculo secundario (0 a 2π)
            
        Returns:
            tuple: (x_proyectado, y_proyectado, profundidad_z, luminancia)
                   o None si el punto no es visible
        """
        # Precalcular senos y cosenos
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        cos_A = math.cos(self.A)
        sin_A = math.sin(self.A)
        cos_B = math.cos(self.B)
        sin_B = math.sin(self.B)
        
        # Coordenadas del círculo (radio mayor = 2, radio menor = 1)
        circle_x = 2 + cos_theta
        circle_y = sin_theta
        
        # Transformación 3D con rotaciones
        x = circle_x * (cos_B * cos_phi + sin_A * sin_B * sin_phi) - \
            circle_y * cos_A * sin_B
        y = circle_x * (sin_B * cos_phi - sin_A * cos_B * sin_phi) + \
            circle_y * cos_A * cos_B
        z_denominator = circle_x * cos_A * sin_phi + circle_y * sin_A + 5
        
        # Evitar división por cero
        if z_denominator <= 0:
            return None
            
        z = 1 / z_denominator
        
        # Proyección perspectiva
        scale = 150 * z
        x_proj = int(self.grid_width / 2 + scale * x)
        y_proj = int(self.grid_height / 2 - scale * y)
        
        # Verificar si está dentro de los límites
        if not (0 <= x_proj < self.grid_width and 0 <= y_proj < self.grid_height):
            return None
        
        # Cálculo de iluminación
        luminance = cos_phi * cos_theta * sin_B - \
                   cos_A * cos_theta * sin_phi - \
                   sin_A * sin_theta + \
                   cos_B * (cos_A * sin_theta - cos_theta * sin_A * sin_phi)
        
        if luminance <= 0:
            return None
            
        return (x_proj, y_proj, z, luminance)
    
    def render_frame(self):
        """
        Renderiza un frame completo del donut 3D.
        
        Utiliza un z-buffer para determinar qué puntos son visibles
        y aplica iluminación para crear el efecto 3D.
        """
        # Limpiar pantalla con color de fondo oscuro
        self.screen.fill((5, 5, 15))
        
        # Inicializar z-buffer para control de profundidad
        zbuffer = {}
        output = {}
        
        # Iterar sobre todos los puntos del toroide
        theta = 0
        theta_step = 0.02
        phi_step = 0.07
        
        while theta < 2 * math.pi:
            phi = 0
            while phi < 2 * math.pi:
                result = self.calculate_point(theta, phi)
                
                if result:
                    x_proj, y_proj, z, luminance = result
                    idx = (x_proj, y_proj)
                    
                    # Actualizar z-buffer solo si este punto está más cerca
                    if idx not in zbuffer or z > zbuffer[idx]:
                        zbuffer[idx] = z
                        # Mapear luminancia a índice de color (0-11)
                        color_idx = int(luminance * 8)
                        color_idx = max(0, min(11, color_idx))
                        output[idx] = self.colors[color_idx]
                
                phi += phi_step
            theta += theta_step
        
        # Dibujar los píxeles en pantalla
        for (x, y), color in output.items():
            rect = pygame.Rect(
                x * self.pixel_size,
                y * self.pixel_size,
                self.pixel_size,
                self.pixel_size
            )
            pygame.draw.rect(self.screen, color, rect)
        
        # Mostrar información en pantalla
        self.draw_info()
    
    def draw_info(self):
        """Dibuja información de controles y estado en pantalla."""
        info_text = [
            "ESPACIO: Pausar",
            "+/-: Velocidad",
            "R: Reiniciar",
            "ESC: Salir"
        ]
        
        y_offset = 10
        for text in info_text:
            surface = self.small_font.render(text, True, (150, 200, 255))
            self.screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Mostrar velocidad actual
        speed_text = f"Velocidad: {self.rotation_speed:.1f}x"
        speed_surface = self.small_font.render(speed_text, True, (255, 200, 100))
        self.screen.blit(speed_surface, (10, self.height - 30))
        
        # Mostrar estado de pausa
        if self.paused:
            pause_text = self.font.render("PAUSADO", True, (255, 100, 100))
            text_rect = pause_text.get_rect(center=(self.width // 2, 40))
            self.screen.blit(pause_text, text_rect)
    
    def update_rotation(self):
        """Actualiza los ángulos de rotación si no está en pausa."""
        if not self.paused:
            self.A += 0.04 * self.rotation_speed
            self.B += 0.02 * self.rotation_speed
    
    def handle_events(self):
        """
        Maneja los eventos de teclado y ventana.
        
        Returns:
            bool: False si se debe cerrar el programa, True en caso contrario
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.A = 0
                    self.B = 0
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.rotation_speed = min(3.0, self.rotation_speed + 0.1)
                elif event.key == pygame.K_MINUS:
                    self.rotation_speed = max(0.1, self.rotation_speed - 0.1)
        
        return True
    
    def run(self):
        """
        Bucle principal del programa.
        
        Ejecuta continuamente hasta que el usuario cierre la ventana
        o presione ESC.
        """
        running = True
        
        while running:
            running = self.handle_events()
            self.update_rotation()
            self.render_frame()
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """Función principal que inicia el programa."""
    donut = Donut3D(width=800, height=600)
    donut.run()


if __name__ == "__main__":
    main()