FROM python:2.7

ENV APP_PATH=/app
ENV NIMA_PUBLIC=${APP_PATH}/NIMAv7_public
ENV NIMA_USER=${APP_PATH}/NIMAv7_user
ENV DIR_RESULTS=/data
ENV DIR_INPUTS=/data

RUN apt-get update && apt-get install -y  \
                gfortran \
                csh \
                gnuplot \
                ghostscript \
                libfreetype6-dev \
                pkg-config \
                libxft-dev \
                imagemagick \
                gnuplot \
                vim \
            && rm -rf /var/lib/apt/lists/*

RUN mkdir $APP_PATH

WORKDIR $APP_PATH

RUN pip install --upgrade pip 

RUN pip install numpy==1.11.0 


ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt

COPY . $APP_PATH

# Install NIMA Public
# RUN set -ex \
#         && cd $APP_PATH \
#         && tar -xvf NIMAv7_public.tar.gz \
#         && cd $NIMA_PUBLIC \
#         && cd $NIMA_PUBLIC/data \
#         && ./sc_listobs.sh \
#         && ln -s de432/de432.lnx de.lnx \
#         && ln -s bias.cat bias.dat \
#         \
#         # Instalacao SOFA
#         && cd $NIMA_PUBLIC/lib \
#         && tar -xvf sofa_f-20160503_c.tar.gz \
#         && cd $NIMA_PUBLIC/lib/sofa/20160503_c/f77/src \
#         && make \
#         && cd $NIMA_PUBLIC/lib \
#         && ln -s sofa/20160503_c/f77/src/libsofa.a sofa.a \
#         \
#         # Instalacao do SPICE
#         && cd $NIMA_PUBLIC/lib \
#         && tar -xvf toolkit.tar.Z \
#         && cd $NIMA_PUBLIC/lib/toolkit \
#         && ./makeall.csh \
#         && cd $NIMA_PUBLIC/lib \
#         && ln -s toolkit/lib/spicelib.a spice.a \
#         && rm *.gz *.Z 

# Extract NIMA Public que foi previamente compilado com esta mesma imagem
RUN set -ex \
        && tar -xvf nima_v7_public_compiled.tar.gz


# # Install NIMA User
# RUN set -ex \
#         && cd $APP_PATH \
#         && tar -xvf NIMAv7_user.tar.gz \
#         && cd $NIMA_USER \
#         && mkdir $NIMA_USER/obs \
#         && mkdir $NIMA_USER/data \
#         && ln -s $NIMA_PUBLIC/data/listobsUAI.dat data/listobsUAI.dat \
#         && ln -s $NIMA_PUBLIC/data/de.lnx data/de.lnx \
#         && ln -s $NIMA_PUBLIC/data/bias.dat data/bias.dat \
#         && mkdir $NIMA_USER/ci \
#         && mkdir $NIMA_USER/jplbsp \
#         && mkdir $NIMA_USER/lib \
#         && ln -s $NIMA_PUBLIC/lib/sofa.a lib/sofa.a \
#         && ln -s $NIMA_PUBLIC/lib/spice.a lib/spice.a \
#         && mkdir $NIMA_USER/exe \
#         && mkdir $NIMA_USER/results \
#         && echo "${NIMA_PUBLIC}"|./compil.sh

# Extract NIMA User que foi previamente compilado com esta mesma imagem
RUN set -ex \
        && tar -xvf nima_v7_user_compiled.tar.gz 



# RUN ./install_public.sh

# RUN ./install_user.sh

RUN cd $APP_PATH \
        && rm requirements.txt \
        && rm $APP_PATH/nima_v7_public_compiled.tar.gz \
        && rm $APP_PATH/nima_v7_user_compiled.tar.gz 


# ENTRYPOINT python ${NIMA_USER}/executeNIMAv7.py
