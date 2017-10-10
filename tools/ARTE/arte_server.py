"""

   Copyright (c) 2017 Windhover Labs, L.L.C. All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
 3. Neither the name Windhover Labs nor the names of its 
    contributors may be used to endorse or promote products derived 
    from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.

"""
import socket
import sys
import threading
import msg_pb2
import time
from struct import unpack
from struct import pack
from arte_ccsds import *
from arte_time import *

try:
    import socketserver
except Exception:
    print ("python3 socketserver not found. Must be python2.")


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    
    def decode_message(self, telemetry_packet, cur_thread):
        if telemetry_packet.PriHdr.StreamId.bits.app_id == 1:
            print("received shutdown message", cur_thread)
            # notify main so it can initiate shutdown
            ArteServerGlobals.shutdown_notification.set()
    
    def recv_message(self, cur_thread):
        telemetry_packet = CCSDS_TlmPkt_t()
        header = self.request.recv(telemetry_packet.get_packet_size())
        telemetry_packet.set_decoded(header)
        print ("received message timestamp :", telemetry_packet.get_time(), cur_thread)
        self.decode_message(telemetry_packet, cur_thread)
        
    def send_response(self, cur_thread):
        test_response = msg_pb2.next_step()
        # TODO Remove hardcoded test value
        test_response.microseconds = 25
        encoded = test_response.SerializeToString(test_response)
        # prepare header
        command_header = CCSDS_CmdPkt_t()
        command_header.init_packet()
        command_header.set_user_data_length(len(encoded))
        # send encoded header
        self.request.sendall(command_header.get_encoded())
        # send payload
        self.request.sendall(encoded)
        print("server sent response", cur_thread)
        # reset the client connect count
        ArteServerGlobals.client_count = ArteServerGlobals.starting_client_count

    def handle(self):
        # TODO fix this hardcoded timeout
        #self.request.settimeout(15)
        cur_thread = threading.current_thread()
        
        while ArteServerGlobals.shutdown_flag:
            # receive message
            self.recv_message(cur_thread)
            # decrement the client count
            ArteServerGlobals.client_count -= 1
            
            if ArteServerGlobals.client_count == 0:
                # if all clients have connected release any threads that
                # are waiting
                with ArteServerGlobals.condition:
                    print("all clients ready")
                    ArteServerGlobals.condition.notify_all()
                    self.send_response(cur_thread)

            else:
                # wait for all clients to connect
                with ArteServerGlobals.condition:
                    print("client ready, waiting for all clients...")
                    ArteServerGlobals.condition.wait()
                    # send "next step" to all clients
                    self.send_response(cur_thread)
        # we're outside the while loop so the shutdown flag has been 
        # raised
        print("thread done = ", cur_thread.name)
        # notify server_shutdown 
        ArteServerGlobals.shutdown_event.set()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ArteServer(object):
    """

    Args:
        host (str): IP address.
        port (int): Port number.
        client_count (int): Number of clients that will connect. 

    """
    def __init__(self, host, port, client_count):
        self.host = host
        self.port = port
        # this is a static count of total clients
        self.client_count = client_count
        # set the shared client count
        ArteServerGlobals.client_count = self.client_count
        ArteServerGlobals.starting_client_count = self.client_count
        # prevent error 98 Address already in use when relaunching 
        socketserver.TCPServer.allow_reuse_address = True
        self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        # start a thread with the server -- that thread will then start one
        # more thread for each request
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        # exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
        print ("ARTE server loop running in thread: ", self.server_thread.name)
    
    def server_shutdown(self):
        ArteServerGlobals.shutdown_flag = False
        # TODO fix hardcoded timeout
        ArteServerGlobals.shutdown_event.wait(1)

class ArteServerGlobals:
    """Shared data between server and client threads."""
    client_count = 0
    starting_client_count = 0
    condition = threading.Condition()
    shutdown_flag = True
    shutdown_event = threading.Event()
    shutdown_notification = threading.Event()
