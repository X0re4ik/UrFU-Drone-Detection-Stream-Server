#!/bin/bash

VIDEO_PATH="./fullchain.mp4"

RTSP_URL="rtmp://5.44.46.74:1935/live/input1"

ffmpeg -re -stream_loop -1 -i "${VIDEO_PATH}" \
    -vcodec libx264 -preset veryfast -tune zerolatency \
    -acodec aac -f flv "${RTSP_URL}"