# NIMA v7

Sobre esta imagem TODO

Github: https://github.com/linea-it/nima

Docker Cloud: https://cloud.docker.com/u/linea/repository/docker/linea/nima

## Requisitos 
Docker: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

## Baixar a imagem do docker cloud. 

```
docker pull linea/nima:7
```

## Execução
Para executar é necessário ter um diretório na maquina host, com os inputs. este diretório sera 
montado como volume no container. 

A execução é feita um Target por vez, cada target deve ter um diretório expecifico com seus inputs. 
neste exemplo o target é 1999 RB216, e o seu diretório é ~/1999_RB216. 

este diretório de exemplo pode ser baixado neste link: TODO   

```
docker run -it --rm --volume ~/1999_RB216:/data linea/nima:7 python run.py
```

Explicando o comando. 

```docker run``` - Cria um container a partir de uma imagem e executa um comando. 

```-it``` - A execução sera interativa, mantem o terminal aberto. 

```--rm``` - Destroi o container logo apos a execução do comando. 

```--volume``` - Este parametro permite montar um diretório da maquina Host para dentro do container, ~/1999_RB216 neste caso é onde estão os inputs e onde vão ficar os resultados,  ":" indica o path do volume dentro do container, para está imagem sempre deve ser /data.

```linea/nima:7``` : Imagem que sera usada na criação do container. linea é o usuario no docker cloud, nima é o repositório, :7 indica a tag que sera usada. uma imagem pode ter varias tags, nesta imagem a tag representa a versão do NIMA. a lista de tags disponiveis pode ser encontrada [neste link](https://cloud.docker.com/u/linea/repository/docker/linea/nima/tags).

```python run.py``` Comando que sera executado dentro container. 


### Script ```run.py```
Este script é responsavel pela execução de todas os programas do NIMA e dos scripts customizados que estão no diretório ```/app/NIMAv7_user```, no inicio da execução procura pelo arquivo **input.txt** que contem os parametros e a lista de inputs,
o output da execução fica no arquivo de log *nima.log*.

### Execução em paralelo ###
Para executar em paralelo varios objetos, basta criar varias instancias do container, cada uma com um diretório de objeto. nesta imagem não é possivel paralelizar o programa NIMA em si, mais o container funciona de forma isolada podendo ter varios rodando simultaneamente. 

## Inputs ##
São necessários 5 inputs, que devem ter o nome do Target sem espaços e sem "_" + a extensão. exemplo para o target **1999 RB216** os inputs são:
```bash
.
└── 1999_RB216
    ├── input.txt
    ├── 1999RB216.eq0
    ├── 1999RB216.rwo
    ├── 1999RB216.txt
    └── 1999RB216.bsp
```

### input.txt ###
A descrição dos parametros está no proprio arquivo, e pode ser vista neste template **TODO**, 
- cada linha representa um parametro.
- valor deve respeitar a quantidade de 67 caracteres.
- Os 5 primeiros parametros, são referentes ao diretório de inputs **não deve ser alterado**.

### Astrometia ###
TODO: 

### Observation ###
TODO:

### Parametros Orbitais ###
TODO:

### BSP ###
TODO:

## Outputs ##
Os arquivos gerados vão estar no mesmo diretório dos inputs. 

```bash
.
├── 1999RB216.bsp
├── 1999RB216.eq0
├── 1999RB216_nima.bsp
├── 1999RB216.rwo
├── 1999RB216.txt
├── CI_ast.dat
├── correl.mat
├── cov.mat
├── diff_bsp-ni.png
├── diff_nima_jpl_Dec.png
├── diff_nima_jpl_RA.png
├── ephembsp.res
├── ephemni.res
├── input.txt
├── JPL137295.bsp
├── nima.log
├── offset_oth.dat
├── offset_oth.obs
├── omc_ast.res
├── omc_sep_all.png
├── omc_sep_recent.png
└── sigyr.res
```
TODO DESCREVER AS PRINCIPAIS SAIDAS
- 1999RB216_nima.bsp:
- diff_bsp-ni.png:
- diff_nima_jpl_RA.png:
- diff_nima_jpl_Dec.png:
- omc_sep_all.png:
- omc_sep_recent.png:



## Monitoramento ##

Para acompanhar a execução do comando ```run.py```, todas as saidas deste script ficam em /data/nima.log, abra um novo terminal na maquina host e execute: 
```
tail -f ~/1999_RB216/nima.log
```

Para Monitorar os container executando, utilize o comando:
```docker ps```
vai gerar uma saida como está:
```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
8fe11cdc522d        linea/nima:7        "bash"              3 seconds ago       Up 1 second                             nostalgic_shtern

```

Também é possivel verificar o consumo de recursos no host em tempo real. ```docker stats```, mostra informações como consumo de CPU, Memória e I/O e Rede.
```
docker stats
```



# Development
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

## Para fazer alteracoes nos script NIMA_V7_user
é necessario descompactar o diretorio nima_v7_user_compiled.tar.gz
fazer a alteracao necessária, compactar novamente o diretório com o mesmo nome, 
remover o diretório descompactado e em seguida rodar o build da imagem.