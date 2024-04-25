#!/bin/bash

function setup_node {
  local base_dir=$1
  local node_dir=$2
  local git_repo=$3

  # Navigate to the specified base directory
  cd $base_dir

  # Check if the node directory exists, clone if it doesn't, and install requirements
  if [ ! -d "$node_dir" ]; then
    git clone --depth=1 --no-tags --recurse-submodules --shallow-submodules $git_repo $node_dir &&
    cd $node_dir &&
    pip install -r requirements.txt
  fi
}

# Base directory for custom nodes
custom_nodes_base="/home/runner/ComfyUI/custom_nodes/"

# Setup ComfyUI in its base directory
setup_node "/home/runner/" "ComfyUI" "-b cleanup_if_idle https://github.com/liusida/ComfyUI.git"

setup_node $custom_nodes_base "ComfyUI-Manager" "https://github.com/ltdrdata/ComfyUI-Manager.git"

# Setup ComfyUI-Login in the custom_nodes directory
setup_node $custom_nodes_base "ComfyUI-Login" "https://github.com/liusida/ComfyUI-Login.git"

# Setup ComfyUI-Crystools in the custom_nodes directory
setup_node $custom_nodes_base "ComfyUI-Crystools" "https://github.com/crystian/ComfyUI-Crystools.git"

# Copy extra_model_paths.yaml over
cp "/home/scripts/extra_model_paths.yaml" "/home/runner/ComfyUI/"


# Start
echo "########################################"
echo "[INFO] Starting ComfyUI..."
echo "########################################"

export PATH="${PATH}:/home/runner/.local/bin"
export PYTHONPYCACHEPREFIX="/home/runner/.cache/pycache"

cd /home/runner

python3 ./ComfyUI/main.py --listen --port 8188 ${CLI_ARGS}