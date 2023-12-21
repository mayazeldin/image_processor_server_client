# Specification
The setup script requires a clean install of Ubuntu 22.04

---
### Commands:

Server:
- takes in a host (ip address) and port value
- default values set if arguments not provided
  - host: localhost
  - port: 50051
- valid arguments: 
  - host: Valid Ip address
  - port : valid open port number

Client:
- takes in host (ip address), port, input (path to image), output, rotate, mean
- default values:
  - host: localhost
  - port: 50051
  - rotate: NONE
  - mean: false
- Valid Arguments:
  - host: valid IP address (corresponds to host of server)
  - port: valid open port number (corresponds to port of server)
  - input: path to existing image
  - rotate: NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG
- Required Arguments:
  - input
  - output
- Assumes that a server is running at the specified host and port

---

### Things To Add
- Memory Safeguarding:
  - Currently, when an image request is sent to the server, the image data is written to the stack
  in both the client and the server code. This could potentially lead to a stack overflow if 
  large images are being processed or if there are many image requests being sent to the server.
  I would want to implement the following safeguards:
    1. Add a service queue so that there is a limit to the number of parallel requests against 
    the server
    2. Implement code that can limit the maximum size of an image
    3. Investigate methodology to compress image data that are exchanged between client and server
- Rotation Enum
  - Currently, my code only works for 90, 180, and 270 degree rotations. I would want to 
  expand my code to handle arbitrary angle rotations
- Create Docker File
  - Currently, I have not implemented a Dockerfile that can run my code for user that does 
  not have my production environment. 