#!/bin/bash
export PATH=$PATH:/home/runner/.local/bin/

if [ ! -f "/home/runner/.local/bin/comfy-cli" ]; then
    echo "entrypoint> pip install comfy-cli"
    pip install comfy-cli
fi

if [ ! -d "/home/runner/ComfyUI" ]; then
    echo "entrypoint> install ComfyUI"
    comfy-cli --workspace=/home/runner/ComfyUI --skip-prompt install --nvidia
fi

comfy-cli --workspace=/home/runner/ComfyUI --skip-prompt node install ComfyUI-Login
comfy-cli --workspace=/home/runner/ComfyUI --skip-prompt node install ComfyUI-Crystools

while true; do
    comfy-cli --workspace=/home/runner/ComfyUI launch -- --listen 0.0.0.0
    echo "entrypoint> ComfyUI terminated with exit code $?. Respawning.."
    sleep 10
done
