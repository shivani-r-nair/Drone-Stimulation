# Drone-Simulation
A real-time quadcopter drone simulation system built using PyBullet physics engine and Python, featuring live teleoperation control through keyboard input over a socket-based communication system.

The project simulates a Crazyflie-style drone model with realistic physics and allows users to control movement, altitude, and orbit behavior in a 3D environment.

⚙️ Key Features
🎮 Real-time keyboard teleoperation control (Arrow keys + U/J)
🔄 Circular orbit mode (clockwise & reverse)
📡 Socket-based communication between controller and simulator
📈 Smooth velocity ramping for realistic drone motion
🧠 PID-based altitude hold system
🧱 Physics-based simulation using PyBullet
🖥️ Live GUI visualization

🎯 Controls
Arrow Keys → Move drone (Forward/Backward/Left/Right)
U / J → Increase / Decrease altitude
C → Start orbit (clockwise)
O → Reverse orbit
T → Altitude hold ON
Y → Altitude hold OFF

🚀 Objective
To simulate a stable and controllable drone system with real-time input handling, physics-based motion, and modular control logic that can be extended toward real robotics applications.
