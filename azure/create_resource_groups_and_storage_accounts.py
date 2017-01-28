#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess

REGION = "eastus"
RES_GR_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"

users = pd.read_json("users.json", orient="records")

for _, row in users.iterrows():
    row = dict(row)
    user = row["user"]
    userId = row["userId"]
    resGrName = RES_GR_TEMPLATE.format(user)
    # create res gr
    subprocess.check_output(
        """
        az group create \
        -n "{n}" \
        -l "{l}"
        """.format(n=resGrName, l=REGION),
        shell=True
    )
    # assign user to his res gr
    subprocess.check_output(
        """
        az role assignment create \
        --assignee {userId} \
        --role Contributor \
        --resource-group {rg}
        """.format(userId=userId, rg=resGrName),
        shell=True
    )
    # create storage account
    storName = STORAGE_ACCOUNT_TEMPLATE.format(user)
    subprocess.check_output(
        """
        az storage account create \
        -l {l} \
        -n {n} \
        -g {g} \
        --sku Standard_LRS
        """.format(l=REGION, n=storName, g=resGrName),
        shell=True
    )
    print user, "done"
