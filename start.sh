
# Executar o Container entrando pelo bahs
docker run -it --rm --name nimav7 --volume $PWD/data:/data nima:7 /bin/bash

# Executar o Nima direto espera que os inputs estejam no diretorio data

# docker run -it --rm --name nimav7 --volume $PWD/data:/data nima:7 python run.py