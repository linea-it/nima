# NIMA v7

This image contains scripts and source codes to run NIMA v7. NIMA is a numerical code that improves the ephemerides of small bodies in the solar system from positions provided by the user and from the observational history of these bodies.

Github: https://github.com/linea-it/nima

Docker Cloud: https://cloud.docker.com/u/linea/repository/docker/linea/nima

NIMA paper: https://www.aanda.org/articles/aa/abs/2015/12/aa26498-15/aa26498-15.html

## Requirements 
Docker: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

## Download the image from docker cloud.

```
docker pull linea/nima:7
```

## Execution
To execute it is necessary to have a directory on the host machine, with the inputs. This directory will be mounted as volume in the container. 

Execution is done one Target at a time, each target must have a specific directory with its inputs. 
In this example the target is 1999 RB216, and its directory is ~/1999_RB216. 

This sample directory can be downloaded from this [link](https://github.com/linea-it/nima/blob/master/example.zip)    

```
docker run -it --rm --volume ~/1999_RB216:/data linea/nima:7 python run.py
```

Explaining the command. 

```docker run``` - It creates a container from an image and executes a command. 

```-it``` - The execution will be interactive, keeps the terminal open. 

```--rm``` - It destroy the container as soon as the command is executed.

```--volume``` - This parameter allows to mount a Host machine directory into the container, ~/1999_RB216 in this case it is where the inputs are and where the results will be,  ":" indicates the path of volume inside the container, for this image should always be /data.

```linea/nima:7``` : Image that will be used to create the container. linea is the user in docker cloud, nima is the repository, :7 indicates the tag which will be used. An image can have several tags, in this image the tag represents the version of NIMA. The list of available tags can be found in [This link](https://cloud.docker.com/u/linea/repository/docker/linea/nima/tags).

```python run.py``` Command that will be executed inside container.


### Script ```run.py```
This script is responsible for running all NIMA programs and custom scripts that are in the directory ```/app/NIMAv7_user```, the file **input.txt**, that contains the parameters and the list of inputs, is searched in the beginning of the execution, the execution output is in the log file *nima.log*

### Parallel Execution ###
To execute multiple objects in parallel, simply create multiple instances of the container, each one with an directory of object. in this image it is not possible to parallelize the NIMA program itself, but the container works in isolated form and may have several executions simultaneously.

## Inputs ##
5 inputs are required, they must have the target name (without spaces and without "_") and its extension. For example: the target **1999 RB216** has the next inputs:
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
The description of the parameters is in the file itself, and it can be seen in [this template](https://github.com/linea-it/nima/blob/master/input_template.txt). 
- Each line represents one parameter.
- The value of the parameter has a limit of 67 characters
- The first five parameters refer to the input directory **should not be changed!**.

### Astrometric positions ###
The user must provide a ascii file per object with astrometric positions which were determined using some astrometric package. See the example for the case [1999RB216.txt](https://github.com/linea-it/nima/blob/master/example/1999RB216.txt) for knowing the format of this file. The columns are composed by:

- Right Ascension (col. 1-3) in HH MM SS format
- Declinations (col. 4-6) in DD MM SS format
- Magnitude determined (col. 7)
- Modified Julian Date (col. 8)
- Code of the observer location (col. 9). See [IAU code](http://www.minorplanetcenter.net/iau/lists/ObsCodes.html)
- Reference stellar catalogue (col. 10). See [MPC code](https://minorplanetcenter.net/iau/info/CatalogueCodes.html)

### Observational history ###
Positions already determined from the observational history of objects. [1999RB216.rwo](https://github.com/linea-it/nima/blob/master/example/1999RB216.rwo) and [1999RC216.rwm](https://github.com/linea-it/nima/blob/master/example/1999RC216.rwm) are examples of observation files which were downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/) and [MPC](https://www.minorplanetcenter.net/) respectively.

Note that this files have to keep the original formats and the user only has to define the extension of file names: 

+ *.rwo* for AstDyS source 
+ *.rwm* for MPC source

AstDyS must be considered as the first option for getting the observation history (and orbital elements too).

### Orbital elements ###
Orbital elements are the parameters required to uniquely identify a specific orbit. [1999RB216.eq0](https://github.com/linea-it/nima/blob/master/example/1999RB216.eq0) and [1999RC216.eqm](https://github.com/linea-it/nima/blob/master/example/1999RC216.eqm) are examples of files with orbital elements which were downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/) and [MPC](https://www.minorplanetcenter.net/) respectively.

In the case of MPC the user has to create a ascii file with the next parameters (one parameter per line):

1. Provisional name of object
2. Object number ("no" if unnumbered object)
3. Designation name of object ("no" if unnamed object)
4. Epoch
5. Epoch JD
6. Argument of perihelion (degrees)
7. Mean anomaly (degrees)
8. Ascending node (degrees)
9. Inclination (degrees)
10. Eccentricity 
11. Semimajor axis (au)
12. Absolute magnitude
13. Phase slope

In the [site](https://minorplanetcenter.net/db_search/show_object?object_id=1999+RC216) are all the parameters above mentioned for the case of object *1999 RC216*.

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
