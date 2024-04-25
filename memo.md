# build the image using host's network (and proxy)
docker build --network host -t sidaliu/comfyui:latest .

docker push sidaliu/comfyui:latest

# start the container
docker run --rm -it --gpus all -p 56781:8188 -v comfy-1:/home/runner sidaliu/comfyui:latest

# on server
docker-compose up -d
docker-compose restart comfy-2

# remember to come here to update the ComfyUI repo because I am using the cleanup_if_idle version
https://github.com/liusida/ComfyUI/tree/cleanup_if_idle