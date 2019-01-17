#!/usr/bin/env bash
sudo rm -fr /etc/redeem/*
sudo cp configs/* /etc/redeem
sudo cp data/* /etc/redeem
sudo ln /etc/redeem/Deltabot_Custom.cfg /etc/redeem/printer.cfg -s
sudo chown -R octo /etc/redeem
sudo systemctl restart redeem