import socket

def process_data_and_reset(buffer, data):
    # Process the data (e.g., save it to a file or perform some operations)
    decoded_data = data.decode()
    print(f"Received: {decoded_data}")

    # Check if the received data contains the stop signal or exceeds 1 gigabyte
    if decoded_data.strip() == "STOP" or len(buffer) >= 1073741824:
        # Reset the buffer after dumping the data
        buffer.clear()
    else:
        # Add the data to the buffer
        buffer.append(decoded_data)

def main():
    # Server configuration
    host = "127.0.0.1"  # Use your server's IP address or hostname
    port = 12345       # Choose an available port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    # Loop to handle multiple clients
    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            # Receive and process data from the client
            buffer = bytearray()  # Initialize an empty buffer
            while True:
                data = client_socket.recv(4096)  # Buffer size of 4096 bytes (4 KB)
                if not data:
                    break

                # Process data and reset the buffer as needed
                process_data_and_reset(buffer, data)

                # Check if the received data contains the stop signal
                if data.decode().strip() == "STOP":
                    break
        except Exception as e:
            print("Error occurred:", e)
        finally:
            # Close the client socket
            client_socket.close()

        # Further processing or analysis of the dumped data can be done here

if __name__ == "__main__":
    main()
