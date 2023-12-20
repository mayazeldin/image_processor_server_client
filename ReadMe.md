# Specification
The setup script requires a clean install of Ubuntu 22.04

---
### Commands:

Server:
- takes in a host (ip address) and port value
- default values set if arguments not provided
  - host: 127.0.0.1
  - port: 50051

Client:
- takes in host (ip address), port, input (path to image), output, rotate, mean
- default values:
  - host: 127.0.0.1
  - port: 50051
  - rotate: NONE
  - mean: false
- Valid Arguments:
  - host: valid IP address
  - port: valid open port number
  - input: path to existing image
  - rotate: NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG
- Required Arguments:
  - input
  - output

---

### Things To Add
- Memory Safeguarding in Server
  - Currently, when the image is received in a request in the server,
  it writes the contents of the image to a temporary file in disk. 
  Writing to the disk means that bigger images can be processed since
  there is more memory available in the disk than the stack. Writing 
  the image directly to the stack could potentially lead to a stack overflow
  with large images. However, there is still a change that with a very large image,
  the disk can run out of memory and cause the request to fail. With more time, 
  I would want to find a method of processing the image
  in a way that does not require writing the whole image data out to memory and then 
  converting it back to a nlimage.
- Asynchronous code
  - Currently, the server does not perform any tasks asynchronously. This could potentially
  cause the main thread to run slowly since with large images it could take the server a
  while to write the image to memory and perform the various modifications to the image. 
  If I had more time, I would write the server to run in an asynchronous thread
- Rotation Enum
  - Currently, my code only works for 90, 180, and 270 degree rotations. I would want to 
  expand my code to handle more various rotation degrees
