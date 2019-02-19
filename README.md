# NIMA v7

This image contains scripts and source codes to run NIMA v7. NIMA is a numerical code that improves the ephemerides of small bodies in the solar system from positions provided by the user and from the observational history of these bodies.

Github: https://github.com/linea-it/nima

Docker Cloud: https://cloud.docker.com/u/linea/repository/docker/linea/nima

NIMA paper: https://www.aanda.org/articles/aa/abs/2015/12/aa26498-15/aa26498-15.html

## Requirements 
Docker: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

## Baixar a imagem do docker cloud. 

```
docker pull linea/nima:7
```

## Execução
Para executar é necessário ter um diretório na maquina host, com os inputs. este diretório sera 
montado como volume no container. 

A execução é feita um Target por vez, cada target deve ter um diretório especifico com seus inputs. 
neste exemplo o target é 1999 RB216, e o seu diretório é ~/1999_RB216. 

este diretório de exemplo pode ser baixado [neste link](https://github.com/linea-it/nima/blob/master/example.zip)    

```
docker run -it --rm --volume ~/1999_RB216:/data linea/nima:7 python run.py
```

Explicando o comando. 

```docker run``` - Cria um contêiner a partir de uma imagem e executa um comando. 

```-it``` - A execução sera interativa, mantem o terminal aberto. 

```--rm``` - Destroi o contêiner logo apos a execução do comando. 

```--volume``` - Este parâmetro permite montar um diretório da maquina Host para dentro do contêiner, ~/1999_RB216 neste caso é onde estão os inputs e onde vão ficar os resultados,  ":" indica o path do volume dentro do contêiner, para está imagem sempre deve ser /data.

```linea/nima:7``` : Imagem que sera usada na criação do contêiner. linea é o usuário no docker cloud, nima é o repositório, :7 indica a tag que sera usada. uma imagem pode ter varias tags, nesta imagem a tag representa a versão do NIMA. a lista de tags disponíveis pode ser encontrada [neste link](https://cloud.docker.com/u/linea/repository/docker/linea/nima/tags).

```python run.py``` Comando que sera executado dentro container. 


### Script ```run.py```
Este script é responsável pela execução de todas os programas do NIMA e dos scripts customizados que estão no diretório ```/app/NIMAv7_user```, no inicio da execução procura pelo arquivo **input.txt** que contem os parâmetros e a lista de inputs,
o output da execução fica no arquivo de log *nima.log*.

### Execução em paralelo ###
Para executar em paralelo vários objetos, basta criar varias instancias do contêiner, cada uma com um diretório de objeto. nesta imagem não é possível paralelizar o programa NIMA em si, mais o contêiner funciona de forma isolada podendo ter vários rodando simultaneamente. 

## Inputs ##
São necessários 5 inputs, que devem ter o nome do Target sem espaços e sem "_" mais a extensão. exemplo para o target **1999 RB216** os inputs são:
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
A descrição dos parâmetros está no próprio arquivo, e pode ser vista [neste template](https://github.com/linea-it/nima/blob/master/input_template.txt). 
- cada linha representa um parâmetro.
- valor deve respeitar a quantidade de 67 caracteres.
- Os 5 primeiros parâmetros, são referentes ao diretório de inputs **não deve ser alterado**.

### Astrometric positions ###
The user must provide a ascii file per object with astrometric positions which were determined using some astrometric package. See the example for the case [1999RB216](https://github.com/linea-it/nima/blob/master/example/1999RB216.txt) for knowing the format of this file. The columns are composed by:

- Right Ascension (col. 1-3) in HH MM SS format
- Declinations (col. 4-6) in DD MM SS format
- Magnitude determined (col. 7)
- Modified Julian Date (col. 8)
- Code of the observer location (col. 9). See [IAU code](http://www.minorplanetcenter.net/iau/lists/ObsCodes.html)
- Reference stellar catalogue (col. 10). See [MPC code](https://minorplanetcenter.net/iau/info/CatalogueCodes.html)

### Observations ###
Positions already determined from the observational history of objects. It can be downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/)

### Orbital elements ###
Orbital elements are the parameters required to uniquely identify a specific orbit. It can be downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/) or [MPC](https://www.minorplanetcenter.net/).

### Object ephemeris ###
The state vector of a given body at any time is derived from [bsp](https://github.com/linea-it/nima/blob/master/example/1999RB216.bsp) (Binary Spacecraft and Planet Kernel) file which contents the object ephemeris. Bsp files can be downloaded using the script [smb_spk](https://github.com/linea-it/nima/blob/master/smb_spk) through expect language.

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
TODO: DESCREVER AS PRINCIPAIS SAÍDAS
- 1999RB216_nima.bsp:
- diff_bsp-ni.png:
- diff_nima_jpl_RA.png:
- diff_nima_jpl_Dec.png:
- omc_sep_all.png:
- omc_sep_recent.png:



## Monitoramento ##

Para acompanhar a execução do comando ```run.py```, todas as saídas deste script ficam em /data/nima.log, abra um novo terminal na maquina host e execute: 
```
tail -f ~/1999_RB216/nima.log
```

Para Monitorar os contêiner executando, utilize o comando:
```docker ps```
vai gerar uma saída como está:
```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
8fe11cdc522d        linea/nima:7        "bash"              3 seconds ago       Up 1 second                             nostalgic_shtern

```

Também é possível verificar o consumo de recursos no host em tempo real. ```docker stats```, mostra informações como consumo de CPU, Memória e I/O e Rede.
```
docker stats
```



# Development
## Build da Imagem Docker 
```
docker build -t linea/nima:7 .
```

O script principal é o run.py para fazer alterações nele é preciso 
copiá-lo para outra pasta editar e testar na outra pasta e depois sobre escrever o run.py na raiz. 

para rodar o run.py em outro diretório 
```
docker run -it --rm --name nima --volume ~/data:/data --volume ~/teste:/app/teste  linea/nima:7 python teste/run.py
```

## Para fazer alterações nos script NIMA_V7_user
é necessário descompactar o diretório nima_v7_user_compiled.tar.gz
fazer a alteração necessária, compactar novamente o diretório com o mesmo nome, 
remover o diretório descompactado e em seguida rodar o build da imagem.
