FROM ubuntu:latest

SHELL [ "/bin/bash" , "-c" ]

# ubuntu basics programming c++ and python
RUN apt update && apt upgrade -y 
RUN apt install vim -y
RUN apt install build-essential -y
RUN apt install -y python3
RUN apt install python3-pip -y
RUN apt install git -y
RUN apt-get update && apt-get install -y sudo curl
RUN pip3 install beautifulsoup4 requests fastapi uvicorn ultralytics opencv-python --break-system-packages
RUN pip3 install --no-cache-dir torch torchvision torchaudio matplotlib scikit-learn pandas notebook --break-system-packages
RUN apt update && apt install -y libgl1 libglib2.0-0


# postgresql 
RUN apt update && apt install -y postgresql
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
RUN echo "export LANG=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LANGUAGE=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc

# Install Node 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

#jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
# ENV DEBIAN_FRONTEND=noninteractive

# # Create a new Vite React project & install Tailwind
# RUN npm create vite@latest my-robot-dashboard -- --template react && \
#     cd my-robot-dashboard && \
#     npm install && \
#     npm install -D tailwindcss postcss autoprefixer && \
#     npx tailwindcss init -p
