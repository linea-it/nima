
# Executar o Container entrando pelo bahs
docker run -it --rm --name nimav7 --volume $PWD/data:/data nima:7 /bin/bash

# Executar o Nima direto espera que os inputs estejam no diretorio data
# docker run -it --rm --name nimav7 --volume $PWD/data:/data nima:7 python run.py

# Para fazer alteraçoes em algum script e testar de forma mais facil, copia o script para a pasta teste e executa com essa instrucao
# docker run -it --rm --name nimav7 --volume /home/glauber/nima/data:/data --volume /home/glauber/nima/teste:/app/teste  nima:7 python teste/run.py
