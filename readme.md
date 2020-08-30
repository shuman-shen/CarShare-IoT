# Car Sharing IoT

A car sharing service powered by Raspberry Pi 4 Model B.

This project consists two parts: 

1. Server side
  - A backend providing RESTful API endpoints and WebSocket communications.
  - A frontend built on React TypeScript and Ant Design for both user and staff access.
  - Server hosted on Pi 4B.
2. Car side
  - A Raspberry Pi 4B installed on every car to facilitate open/lock control of the car.
  - Track car location and sync in real-time with the server.
  - Extra login features including facial and QR code recognition.
  
Tools:

- Python (Flask, Socket.io, OpenCV2, Google Speech API)
- React TypeScript (Google Maps API, Google Calendar API)
- Raspberry Pi Bluetooth, USB camera, USB microphone
