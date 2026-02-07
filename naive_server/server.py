# This program was modified by Ashton Phillips / N01704940  # IMPROVEMENT: Author identification comment

import socket  # IMPROVEMENT: Import socket library
import argparse  # IMPROVEMENT: Import argparse for command-line parsing
import struct  # IMPROVEMENT: Import struct for unpacking headers

parser = argparse.ArgumentParser()  # IMPROVEMENT: Create argument parser
parser.add_argument('--port', type=int, required=True)  # IMPROVEMENT: Port to listen on
parser.add_argument('--output', required=True)  # IMPROVEMENT: Output file name
args = parser.parse_args()  # IMPROVEMENT: Parse arguments

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IMPROVEMENT: Create UDP socket
server_socket.bind(('', args.port))  # IMPROVEMENT: Bind socket to specified port

expected_seq = 0  # IMPROVEMENT: Expected next sequence number
buffer = {}  # IMPROVEMENT: Buffer for out-of-order packets

with open(args.output, 'wb') as f:  # IMPROVEMENT: Open output file in binary write mode
    while True:  # IMPROVEMENT: Receive packets indefinitely
        packet, client_addr = server_socket.recvfrom(2048)  # IMPROVEMENT: Receive UDP packet
        seq_num = struct.unpack('!I', packet[:4])[0]  # IMPROVEMENT: Extract sequence number

        if seq_num == 0xFFFFFFFF:  # IMPROVEMENT: Check for EOF packet
            break  # IMPROVEMENT: Stop receiving data

        data = packet[4:]  # IMPROVEMENT: Extract payload data

        server_socket.sendto(struct.pack('!I', seq_num), client_addr)  # IMPROVEMENT: Send ACK

        if seq_num == expected_seq:  # IMPROVEMENT: Check for expected packet
            f.write(data)  # IMPROVEMENT: Write data to file
            expected_seq += 1  # IMPROVEMENT: Increment expected sequence

            while expected_seq in buffer:  # IMPROVEMENT: Flush buffered packets in order
                f.write(buffer.pop(expected_seq))  # IMPROVEMENT: Write buffered data
                expected_seq += 1  # IMPROVEMENT: Increment expected sequence

        elif seq_num > expected_seq:  # IMPROVEMENT: Out-of-order packet
            buffer[seq_num] = data  # IMPROVEMENT: Store packet in buffer

        else:  # IMPROVEMENT: Duplicate packet
            pass  # IMPROVEMENT: Ignore duplicate packet

server_socket.close()  # IMPROVEMENT: Close server socket