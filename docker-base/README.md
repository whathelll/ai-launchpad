# Docker Base
The purpose of this directory is to provide a base image for all projects in subdirectories to use in dev containers.


## Build the image
```bash
# for ARM64 (MacOS)
docker buildx build -t ai-launchpad -f Dockerfile_arm .

# for x86
docker buildx build -t ai-launchpad -f Dockerfile_x86 .
```

