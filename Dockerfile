# Use an official Python runtime as a parent image
FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

RUN --mount=type=cache,target=/var/cache/apt \
    set -eu \
    && apt-get update \
    && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential
    
RUN printf 'CREATE_MAIL_SPOOL=no' >> /etc/default/useradd \
    && mkdir -p /home/runner /home/scripts \
    && groupadd runner \
    && useradd runner -g runner -d /home/runner \
    && chown runner:runner /home/runner /home/scripts

COPY --chown=runner:runner scripts/. /home/scripts/

USER runner:runner
VOLUME /home/runner
WORKDIR /home/runner
EXPOSE 8188
ENV CLI_ARGS=""
CMD ["bash","/home/scripts/entrypoint.sh"]