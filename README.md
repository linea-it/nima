# NIMA v7


## Para executar usar este comando
```
docker run -it --rm --name nima --volume /home/glauber/nima/data:/data linea/nima:7 python run.py
```
Os dados de entrada do Objeto devem estar no diretório data.

Os resultados ficam no diretório data. 



## Build da Imagem Docker 
```
docker build -t linea/nima:7 .
```

O script principal é o run.py para fazer alterações nele é preciso 
copialo para outra pasta editar e testar na outra pasta e depois sobreescrever o run.py na raiz. 

para rodar o run.py em outro diretório 
```
docker run -it --rm --name nima --volume /home/glauber/nima/data:/data --volume /home/glauber/nima/teste:/app/teste  linea/nima:7 python teste/run.py
```

