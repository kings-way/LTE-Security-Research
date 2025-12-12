#!/bin/bash

MCC=460
MNC=01
ARFCN=300

TX_GAIN=80
RX_GAIN=50

TAC=$(printf "0x%x" $(( $RANDOM % 65535 )))
PCI=$(( $RANDOM % 255 ))
CELL_ID=$(( $RANDOM % 65025 ))


echo -e "MCC: $MCC\nMNC: $MNC\nARFCN: $ARFCN\nTAC: $TAC\nPCI: $PCI\nCELL_ID: $CELL_ID"

mkdir -p .config/srsran 
cd .config/srsran
cp /usr/share/srsran/enb.conf.example enb.conf
cp /usr/share/srsran/rr.conf.example rr.conf
cp /usr/share/srsran/rb.conf.example rb.conf
cp /usr/share/srsran/sib.conf.example sib.conf

sed -i "s/mcc = .*/mcc=$MCC/g" enb.conf
sed -i "s/mnc = .*/mnc=$MNC/g" enb.conf
sed -i "s/tx_gain = .*/tx_gain=$TX_GAIN/g" enb.conf
sed -i "s/rx_gain = .*/rx_gain=$RX_GAIN/g" enb.conf
sed -i "s/#dl_earfcn = .*/dl_earfcn=$ARFCN/g" enb.conf

sed -i "s/cell_id = .*/cell_id=$CELL_ID/g" rr.conf
sed -i "s/tac = .*/tac=$TAC/g" rr.conf
sed -i "s/pci = .*/pci=$PCI/g" rr.conf

cd ~
./srsenb_patched
