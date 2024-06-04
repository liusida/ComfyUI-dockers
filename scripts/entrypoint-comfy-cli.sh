#!/bin/bash
# export PATH=$PATH:/home/runner/.local/bin/

cd /home/runner
echo "entrypoint> Starting..."

if [ ! -d "venv" ]; then
    python -m venv --prompt=comfy venv
    . venv/bin/activate
    pip install --upgrade pip
    echo "entrypoint> Installing comfy-cli in virtual environment..."
    pip install comfy-cli
else
    . venv/bin/activate
fi

if [ ! -d "ComfyUI" ]; then
    echo "entrypoint> Install ComfyUI and node ComfyUI-Login, ComfyUI-Crystools..."
    comfy-cli --workspace=./ComfyUI --skip-prompt install --nvidia
    comfy-cli --workspace=./ComfyUI --skip-prompt node install ComfyUI-Login
    comfy-cli --workspace=./ComfyUI --skip-prompt node install ComfyUI-Crystools
fi

# Copy extra_model_paths.yaml over
cp "/home/scripts/extra_model_paths.yaml" "/home/runner/ComfyUI/"


while true; do
    if [ "$VSCODE_DEBUG" = "true" ]; then
        echo "entrypoint> VSCODE_DEBUG is set to true. Sleeping for 15 seconds to allow manual debugging..."
        sleep 99999
    else
        comfy-cli --workspace=./ComfyUI --skip-prompt launch -- --listen 0.0.0.0 --port 8188 ${CLI_ARGS}
        echo "entrypoint> ComfyUI terminated with exit code $?. Respawning..."
        sleep 15
    fi
done