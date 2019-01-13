#!/usr/bin/env bash
sudo rm -fr /etc/redeem/*
sudo cp configs/* /etc/redeem
sudo cp data/* /etc/redeem
sudo systemctl restart redeem