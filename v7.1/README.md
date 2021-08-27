# NIMA v7.1

This image contains scripts and source codes to run NIMA v7. NIMA is a numerical code that improves the ephemerides of small bodies in the solar system from positions provided by the user and from the observational history of these bodies.

Github: https://github.com/linea-it/nima

Docker Cloud: https://cloud.docker.com/u/linea/repository/docker/linea/nima

NIMA paper: https://www.aanda.org/articles/aa/abs/2015/12/aa26498-15/aa26498-15.html

## Requirements

Docker: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

## Download the image from docker cloud

```shell
docker pull linea/nima:7
```

## Running

To run NIMA through the docker it is necessary to have a directory on the host machine, with the inputs. This directory will be mounted as a volume in the container.

The code runs one Target at a time, each target must have a specific directory with its inputs.
In this example the target is 1999 RB216, and its directory is ~/1999_RB216. 

This sample directory can be downloaded from this [link](https://github.com/linea-it/nima/blob/master/example.zip)

```shell
docker run -it --rm --volume ~/1999_RB216:/data linea/nima:7.1 python run.py
```

Explaining the command.

` ` ` docker run ` ` ` - It creates a container from an image and executes a command. 

` ` ` -it ` ` ` - The execution will be interactive, keeps the terminal open. 

` ` ` --rm ` ` ` - Removes the container as soon as the command is executed.

` ` ` --volume ` ` ` - This parameter allows to mount a Host machine directory into the container. In this case, ~/1999_RB216 is where the inputs are and where the results will be, ":" indicates the path of volume inside the container (for this image should always be /data).

` ` ` linea/nima:7 ` ` ` : Image that will be used to create the container. linea is the user in docker cloud, nima is the repository, :7 indicates the tag which will be used. An image can have several tags, in this image the tag represents the version of NIMA. The list of available tags can be found in [This link](https://cloud.docker.com/u/linea/repository/docker/linea/nima/tags).

` ` ` python run.py ` ` ` Command that will be executed inside container.

Another way to run is using the --path parameter in the run.py script
this parameter is used when it is not possible to mount the /data directory or when it is necessary to use absolute paths. the inputs directory must be mounted in the container.

in this example "/tmp/1999RB216" is the directory as the inputs, it is mounted in the container keeping the same absolute path, and then it is passed as a parameter to the script. internally the script will create a symbolic link from the absolute path to /data.

```shell
docker run -it --rm --name nima --volume /tmp/1999RB216:/tmp/1999RB216 linea/nima:7.1 python run.py --path /tmp/1999RB216/
```

### Script run.py

This script is responsible for running all NIMA programs and custom scripts that are in the directory `` `/app/NIMAv7_user` ``. The file **input.txt**, that contains the parameters and the list of inputs, is searched in the beginning of the execution and the respective output is in the log file *nima.log*

### Parallel Execution

To execute multiple objects in parallel, simply create multiple instances of the container, each one with a directory of objects. In this image it is not possible to parallelize the NIMA program itself, but the container works in isolated form and may have several executions simultaneously.

## Inputs

5 inputs are required, they must have the target name (without spaces and without "_") and its extension. For example: the target **1999 RB216** has the following inputs:

```shell
.
└── 1999_RB216
    ├── input.txt
    ├── 1999RB216.eq0
    ├── 1999RB216.rwo
    ├── 1999RB216.txt
    └── 1999RB216.bsp
```

### input.txt

The description of the parameters is in the file itself, and it can be seen in [this template](https://github.com/linea-it/nima/blob/master/input_template.txt). 
* Each line represents one parameter.
* The value of the parameter has a limit of 67 characters
* The first five parameters refer to the input directory **should not be changed!**.

### Astrometric positions

The user must provide an ascii file per object with astrometric positions which were determined using some astrometric package. See the example for the case [1999RB216.txt](https://github.com/linea-it/nima/blob/master/example/1999RB216.txt) for knowing the format of this file. The columns are composed by:

* Right Ascension (col. 1-3) in HH MM SS format
* Declinations (col. 4-6) in DD MM SS format
* Observed magnitude (col. 7)
* Julian Date (col. 8)
* Code of the observer location (col. 9). See [IAU code](http://www.minorplanetcenter.net/iau/lists/ObsCodes.html)
* Reference stellar catalogue (col. 10). See [MPC code](https://minorplanetcenter.net/iau/info/CatalogueCodes.html)

### Observational history

Positions already determined from the observational history of objects. [1999RB216.rwo](https://github.com/linea-it/nima/blob/master/example/1999RB216.rwo) and [1999RC216.rwm](https://github.com/linea-it/nima/blob/master/example/1999RC216.rwm) are examples of observation files which were downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/) and [MPC](https://www.minorplanetcenter.net/) respectively.

Note that this files have to keep the original formats and the user only has to define the extension of file names:

* *.rwo* for AstDyS source
* *.rwm* for MPC source

AstDyS must be considered as the first option for getting the observation history (and orbital elements too).

### Orbital elements

Orbital elements are the parameters required to uniquely identify a specific orbit. [1999RB216.eq0](https://github.com/linea-it/nima/blob/master/example/1999RB216.eq0) and [1999RC216.eqm](https://github.com/linea-it/nima/blob/master/example/1999RC216.eqm) are examples of files with orbital elements which were downloaded from [AstDyS](http://hamilton.dm.unipi.it/astdys2/) and [MPC](https://www.minorplanetcenter.net/) respectively.

In the case of MPC the user has to create a ascii file with the next parameters (one parameter per line):

01. Provisional name of object
02. Object number ("no" if unnumbered object)
03. Designation name of object ("no" if unnamed object)
04. Epoch
05. Epoch JD
06. Argument of perihelion (degrees)
07. Mean anomaly (degrees)
08. Ascending node (degrees)
09. Inclination (degrees)
10. Eccentricity 
11. Semimajor axis (au)
12. Absolute magnitude
13. Phase slope

In the [site](https://minorplanetcenter.net/db_search/show_object?object_id=1999+RC216) are all the parameters above mentioned for the case of object *1999 RC216*.

### Object ephemeris

The state vector of a given body at any time is derived from [bsp](https://github.com/linea-it/nima/blob/master/example/1999RB216.bsp) (Binary Spacecraft and Planet Kernel) file which contents the object ephemeris. Bsp files can be downloaded using the script [smb_spk](https://github.com/linea-it/nima/blob/master/smb_spk) through expect language.

## Outputs

The output files will be in the same directory where inputs are.

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

Main output files

* 1999RB216_nima.bsp: Ephemeris of object generated by NIMA. **It is the output file more important of NIMA**.
* diff_nima_jpl_RA.png: Difference between NIMA and JPL ephemeris in RA.
* diff_nima_jpl_Dec.png: Difference between NIMA and JPL ephemeris in Decl.
* diff_bsp-ni.png: Difference (in kilometers) between bsp and numerical integration

## Monitoring

To monitor the execution of the command ` ` ` run.py ` ` `, all output from this script is in /data/nima.log, open a new terminal on the host machine and execute: 

```bash
tail -f ~/1999_RB216/nima.log
```

To monitor the execution of containers, use the command:

```bash
docker ps
```

It will generate an output as:

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
8fe11cdc522d        linea/nima:7        "bash"              3 seconds ago       Up 1 second                             nostalgic_shtern

```

You can also check resource consumption on the host in real time. `` `docker stats` ``, shows information such as CPU, Memory and I/O and Network consumption.

```bash

docker stats
```

## Development

## Build the Docker Image

```bash

docker build -t linea/nima:7.1 .

```

The main script is *run.py* and to do changes in it you need to copy it to another folder, edit and test it in that folder and then overwrite the *run.py* in the root.

To execute *run.py* in another directory

```bash

docker run -it --rm --name nima --volume ~/data:/data --volume ~/teste:/app/teste  linea/nima:7.1 python teste/run.py
```

## To do changes in NIMA_V7_user script

01. nima_v7_user_compiled.tar.gz must be unpacked
02. To do the necessary change
03. Pack the directory with the same name
04. Remove the unpacked directory
05. Execute the build of image
