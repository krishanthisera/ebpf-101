# Use the official Golang image as the base image
FROM golang:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    clang \
    llvm \
    libelf-dev \
    iproute2 \
    iputils-ping \
    linux-headers-generic

# Crete a symnlink for the asm headers
RUN ln -s /usr/include/asm-generic /usr/include/asm

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Run go generate
CMD ["go", "generate", "./..."]