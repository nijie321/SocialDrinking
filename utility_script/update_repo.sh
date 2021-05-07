#!/bin/bash

cd /home/pi/openbehavior/PeerPub/

git reset --hard && git pull --depth 1

git log -1 --pretty=oneline >> /home/pi/SocialDrinking/${BOXID}_update

sleep 30

sudo reboot
