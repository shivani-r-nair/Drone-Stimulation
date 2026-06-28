import socket
import pygame

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5000))

pygame.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Drone Teleop")

last_command = ""

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    command = "STOP"

    if keys[pygame.K_UP]:
        command = "FORWARD"

    elif keys[pygame.K_DOWN]:
        command = "BACKWARD"

    elif keys[pygame.K_LEFT]:
        command = "LEFT"

    elif keys[pygame.K_RIGHT]:
        command = "RIGHT"

    elif keys[pygame.K_u]:
        command = "UP"

    elif keys[pygame.K_j]:
        command = "DOWN"

    elif keys[pygame.K_c]:
        command = "ORBIT"

    elif keys[pygame.K_o]:
        command = "ORBIT_REVERSE"

    elif keys[pygame.K_t]:
        command = "ALT_HOLD"

    elif keys[pygame.K_y]:
        command = "ALT_RELEASE"

    if command != last_command:
        client.send(command.encode())
        print("Sending:", command)
        last_command = command

    pygame.time.delay(20)

client.close()
pygame.quit()