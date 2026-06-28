import socket
import threading
import pybullet as p
import pybullet_data
import time
import math

print("SIM STARTED")

# ---------------- PYBULLET ----------------
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

p.loadURDF("plane.urdf")

drone = p.loadURDF("cf2x.urdf", [0, 0, 1])
p.changeDynamics(drone, -1, linearDamping=0.05, angularDamping=0.05)

# ---------------- STATE ----------------
cmd = "STOP"

vx = vy = vz = 0.0
target_vx = target_vy = target_vz = 0.0

MAX_SPEED = 3.0
SMOOTH = 0.15

# ---------------- ORBIT ----------------
orbit_angle = 0
orbit_radius = 2
orbit_speed = 0.03
orbit_center = [0, 0]
orbit_mode = False

# ---------------- ALT HOLD ----------------
alt_hold = False
target_alt = 1.0
Kp, Ki, Kd = 4.0, 0.02, 1.5
integral = 0
prev_err = 0

# ---------------- SOCKET ----------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen(1)

print("Waiting for teleop...")
conn, addr = server.accept()
print("Connected:", addr)

conn.setblocking(False)

# ---------------- RECEIVE ----------------
def receive():
    global cmd, orbit_mode, orbit_center, alt_hold

    while True:
        try:
            data = conn.recv(1024)
            if data:
                msg = data.decode().strip()

                # ORBIT START
                if msg == "ORBIT":
                    pos, _ = p.getBasePositionAndOrientation(drone)
                    orbit_center = [pos[0], pos[1]]
                    orbit_mode = True

                elif msg == "ORBIT_REVERSE":
                    pos, _ = p.getBasePositionAndOrientation(drone)
                    orbit_center = [pos[0], pos[1]]
                    orbit_mode = True

                elif msg in ["FORWARD", "BACKWARD", "LEFT", "RIGHT", "UP", "DOWN"]:
                    orbit_mode = False

                cmd = msg

        except:
            time.sleep(0.01)

threading.Thread(target=receive, daemon=True).start()

# ---------------- MAIN LOOP ----------------
while True:

    pos, orn = p.getBasePositionAndOrientation(drone)

    # ---------------- ORBIT MODE ----------------
    if orbit_mode and cmd in ["ORBIT", "ORBIT_REVERSE"]:

        if cmd == "ORBIT":
            orbit_angle += orbit_speed
        else:
            orbit_angle -= orbit_speed

        target_x = orbit_center[0] + orbit_radius * math.cos(orbit_angle)
        target_y = orbit_center[1] + orbit_radius * math.sin(orbit_angle)

        target_vx = (target_x - pos[0]) * 4
        target_vy = (target_y - pos[1]) * 4

    else:

        target_vx = target_vy = 0

        if cmd == "FORWARD":
            target_vx = MAX_SPEED
        elif cmd == "BACKWARD":
            target_vx = -MAX_SPEED
        elif cmd == "LEFT":
            target_vy = MAX_SPEED
        elif cmd == "RIGHT":
            target_vy = -MAX_SPEED

    # ---------------- ALTITUDE ----------------
    target_vz = 0

    if cmd == "UP":
        target_vz = MAX_SPEED
    elif cmd == "DOWN":
        target_vz = -MAX_SPEED

    # ---------------- ALT HOLD ----------------
    if cmd == "ALT_HOLD":
        target_alt = pos[2]
        alt_hold = True

    elif cmd == "ALT_RELEASE":
        alt_hold = False

    if alt_hold:
        err = target_alt - pos[2]
        integral += err
        deriv = err - prev_err
        prev_err = err

        target_vz = (Kp * err) + (Ki * integral) + (Kd * deriv)
        target_vz = max(-5, min(5, target_vz))

    # ---------------- SMOOTH ----------------
    vx += (target_vx - vx) * SMOOTH
    vy += (target_vy - vy) * SMOOTH
    vz += (target_vz - vz) * SMOOTH

    # ---------------- APPLY ----------------
    p.resetBaseVelocity(drone, [vx, vy, vz])

    p.stepSimulation()
    time.sleep(1 / 240)