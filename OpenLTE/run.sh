#!/bin/bash

TAC=$(( $RANDOM % 65535 ))
PCI=$(( $RANDOM % 255 ))
CELL_ID=$(( $RANDOM % 65025 ))

CMD="write mcc 460
write mnc 01
write tx_gain 80
write rx_gain 50
write band 1
write dl_earfcn 300
write cell_id $CELL_ID
write n_id_cell $PCI
write tracking_area_code $TAC
start"

echo -ne "\n$CMD\n\n"
echo "$CMD" | nc -v 127.0.0.1 30000

