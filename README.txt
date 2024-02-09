


RUN PYTHON FROM SHELL
    Bisogna avere python istallato
    Aprire il terminale o shell
    Puntare alla directory del progetto esp.( cd "C:\User\...\GecoInt> )
    verificare che python sia installato con il comando " python --version "
    eseguire l'aggiornamento con il comando " pip3 install --upgrade pip "
    installlare le librerie con il comando " pip install -r requirements.txt "
    eseguire l'app con " python run.py "

INSTALLARE PYTHON
    Andare sul sito ufficiale http://www.python.org
    Nella voce “Downloads” del menù, cliccare su OS desiderato
    
    (su windows)
    Durante l’installazione selezionate la voce “Add Python 3.9 to PATH“
        oppure aggiungere Python alla variabile di ambiente PATH manualmente
    
BUILD DOCKER FILE
To build and run this dockerfile follow the following steps:
    install Docker from https://www.docker.com/get-started/
    open shell
    point to the directory of project esp.( cd "C:\User\...\GecoInt> )
    docker build . --file Dockergecoint --tag gecoint:alpinepyp
    docker images
    docker run -d -p 8180:8180 --name gecoint IMAGEID
                    oppure
    docker save -o ./GecointContainer gecoint:alpinepyp
