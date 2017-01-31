##!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, VNET_NAME, REGION, SUBNET_NAME, NSG_NAME

STUDENT_NAME="admin"
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)
STORAGE_ACCOUNT = STORAGE_ACCOUNT_TEMPLATE.format(STUDENT_NAME)

# # create vnet and subnet
# utils.create_vnet(VNET_NAME, RG_NAME, REGION, SUBNET_NAME)
#
# # create network security group
# utils.create_nsg(NSG_NAME, RG_NAME, REGION)
#
# # create SSH and Jupyter rules
# utils.allow_incoming_port(NSG_NAME, RG_NAME, "allow_ssh", 22, 1000)
# utils.allow_incoming_port(NSG_NAME, RG_NAME, "allow_jupyter", 9999, 1010)

for idx in [1, 2, 3]:
    # create public IP
    IP_NAME = "ip_cluster{0}".format(idx)
    utils.create_public_ip(IP_NAME, RG_NAME)

    # Create network card with fixed private IP
    NIC_NAME = "nic_cluster{0}".format(idx)
    INT_DNS_NAME = "cluster{0}".format(idx)
    IP = "10.0.1.2{0}".format(idx)
    utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

    # create VM
    VM_NAME = INT_DNS_NAME
    # https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-windows-sizes
    VM_SIZE = "Standard_D12_v2"
    PUB_KEY = "~/.ssh/id_rsa.pub"
    DISK_SIZE = 5
    IMAGE_URN = "Canonical:UbuntuServer:14.04.4-LTS:latest"
    utils.create_vm(VM_NAME, RG_NAME, REGION, NIC_NAME, IP_NAME, STORAGE_ACCOUNT, VM_SIZE, PUB_KEY, DISK_SIZE, IMAGE_URN)