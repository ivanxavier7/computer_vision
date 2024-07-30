import pygame
from DroneController import DroneController
import time


class MainApp:
    def __init__(self, width=960, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tello Drone")
        self.drone_controller = DroneController()
        self.running = True

    def run(self):
        while self.running:
            frame = self.drone_controller.get_frame()
            frame_surface = pygame.surfarray.make_surface(frame)
            self.window.blit(frame_surface, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.drone_controller.handle_keys(keys)

            time.sleep(0.1)

        self.cleanup()

    def cleanup(self):
        self.drone_controller.end()
        pygame.quit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
