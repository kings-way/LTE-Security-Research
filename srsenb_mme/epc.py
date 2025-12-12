from datetime import datetime
import socket
import string
import sctp
import binascii
from pycrate_asn1dir import S1AP

class EPCServer:
    sctp_socket = None
    fd = None
    addr = None
    omit = None
    target = None

    # cause 7: EPS services not allowed (TC15)
    # cause 8: EPS services and non-EPS services not allowed (TC16)
    TAU_reject_reason = 9
    attach_reject_reason = 2

    def init_server(self, addr) -> None:
        """Creates server socket and saves the socket in the EPCServer obj"""
        self.sctp_socket = sctp.sctpsocket_tcp(socket.AF_INET)
        self.sctp_socket.bind((addr if addr is not None else "127.0.1.100", 36412))
        try:
            self.sctp_socket.listen(5)
        except KeyboardInterrupt:
            print("\nThe program was interrupted while awaiting a connection. Exiting ..")
            exit()
        return

    def accept_wait(self):
        self.fd, self.addr = self.sctp_socket.accept()

    def get_packet(self) -> tuple:
        """Receive a packet on the initialised socket in the EPCServer"""
        try:
            fromaddr, flags, msgret, notif = self.fd.sctp_recv(2048)
        except ConnectionResetError:
            print("Connection reset while receiving packet. Closing connection ..")
            self.close_server()
            return (None,False)
        if len(msgret) == 0:
            return None,False
        s1ap_hex = msgret.hex()
        try:
            # decode using pycrate
            s1ap = S1AP.S1AP_PDU_Descriptions.S1AP_PDU
            s1ap.from_aper(binascii.unhexlify(s1ap_hex))
            return s1ap, (True if flags == sctp.FLAG_EOR else False)
        except Exception as err:
            print("Error during S1AP dissection. Skipping..")

    def send_packet(self,value: string):
        """The function wants the input hexlified. Function is better not used directly, use encode_and_send_packet()"""
        self.fd.sctp_send(bytes.fromhex(value), ppid=socket.htonl(18))

    def encode_and_send_packet(self,s1ap_decoded):
        """encode a message and send it on the preset socket in the EPCServer"""
        s1ap = S1AP.S1AP_PDU_Descriptions.S1AP_PDU
        s1ap.set_val(s1ap_decoded)
        s1ap_hex_out = binascii.hexlify(s1ap.to_aper()).decode('ascii')
        self.send_packet(s1ap_hex_out)
