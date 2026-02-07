# This program was modified by Ashton Phillips / N01704940  # IMPROVEMENT: Required lab header identifying modifier

import socket  # IMPROVEMENT: Import socket library for UDP communication
import argparse  # IMPROVEMENT: Import argparse for command-line arguments
import struct  # IMPROVEMENT: Import struct for packing sequence numbers
import os  # IMPROVEMENT: Import os for file handling

parser = argparse.ArgumentParser()  # IMPROVEMENT: Create argument parser
parser.add_argument('--target_ip', default='127.0.0.1')  # IMPROVEMENT: Set default target IP
parser.add_argument('--target_port', type=int, required=True)  # IMPROVEMENT: Target port argument
parser.add_argument('--file', required=True)  # IMPROVEMENT: File to send argument
args = parser.parse_args()  # IMPROVEMENT: Parse command-line arguments

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IMPROVEMENT: Create UDP socket
client_socket.settimeout(1.0)  # IMPROVEMENT: Set timeout for retransmissions

seq_num = 0  # IMPROVEMENT: Initialize sequence number counter

with open(args.file, 'rb') as f:  # IMPROVEMENT: Open file in binary mode
    while True:  # IMPROVEMENT: Loop until file ends
        chunk = f.read(1024)  # IMPROVEMENT: Read 1024-byte chunk
        if not chunk:  # IMPROVEMENT: Check for end-of-file
            break  # IMPROVEMENT: Exit loop when file is done

        header = struct.pack('!I', seq_num)  # IMPROVEMENT: Pack sequence number into 4 bytes
        packet = header + chunk  # IMPROVEMENT: Combine header and data

        while True:  # IMPROVEMENT: Stop-and-Wait loop
            client_socket.sendto(packet, (args.target_ip, args.target_port))  # IMPROVEMENT: Send packet
            try:  # IMPROVEMENT: Attempt to receive ACK
                ack, _ = client_socket.recvfrom(4)  # IMPROVEMENT: Receive ACK packet
                ack_num = struct.unpack('!I', ack)[0]  # IMPROVEMENT: Unpack ACK sequence number
                if ack_num == seq_num:  # IMPROVEMENT: Verify correct ACK
                    break  # IMPROVEMENT: Proceed to next packet
            except socket.timeout:  # IMPROVEMENT: Handle timeout
                continue  # IMPROVEMENT: Retransmit packet

        seq_num += 1  # IMPROVEMENT: Increment sequence number

eof_packet = struct.pack('!I', 0xFFFFFFFF)  # IMPROVEMENT: Create EOF packet with special sequence number
client_socket.sendto(eof_packet, (args.target_ip, args.target_port))  # IMPROVEMENT: Send EOF packet

client_socket.close()  # IMPROVEMENT: Close UDP socket
