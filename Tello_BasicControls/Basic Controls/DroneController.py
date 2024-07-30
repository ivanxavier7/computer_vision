from djitellopy import Tello
import pygame
import cv2
import time


class DroneController:
    def __init__(self, speed=50, retry_limit=5, command_delay=0.5):
        self.tello = Tello()
        self.speed = speed
        self.retry_limit = retry_limit
        self.command_delay = command_delay
        self.tello.connect()
        self.tello.streamon()

    def send_command_with_retry(self, command_func, *args):
        for attempt in range(self.retry_limit):
            try:
                command_func(*args)
                time.sleep(self.command_delay)
                return
            except Exception as e:
                print(f"Attempt {attempt + 1}/{self.retry_limit} failed with error: {e}")
                time.sleep(1)
        print(f"Command {command_func.__name__} with args {args} failed after {self.retry_limit} attempts")

    def handle_keys(self, keys):
        if keys[pygame.K_w]:
            self.send_command_with_retry(self.tello.move_forward, self.speed)
        elif keys[pygame.K_s]:
            self.send_command_with_retry(self.tello.move_back, self.speed)

        if keys[pygame.K_a]:
            self.send_command_with_retry(self.tello.move_left, self.speed)
        elif keys[pygame.K_d]:
            self.send_command_with_retry(self.tello.move_right, self.speed)

        if keys[pygame.K_UP]:
            self.send_command_with_retry(self.tello.move_up, self.speed)
        elif keys[pygame.K_DOWN]:
            self.send_command_with_retry(self.tello.move_down, self.speed)

        if keys[pygame.K_LEFT]:
            self.send_command_with_retry(self.tello.rotate_counter_clockwise, 30)
        elif keys[pygame.K_RIGHT]:
            self.send_command_with_retry(self.tello.rotate_clockwise, 30)

        if keys[pygame.K_l]:
            self.send_command_with_retry(self.tello.land)
        elif keys[pygame.K_t]:
            self.send_command_with_retry(self.tello.takeoff)

    def get_frame(self):
        frame_read = self.tello.get_frame_read()
        frame = frame_read.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return frame

    def end(self):
        self.tello.streamoff()
        self.tello.end()
