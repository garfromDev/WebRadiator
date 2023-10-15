# WebRadiator
Interface web pour radiator


## CONFIGURATION
- SECRET_KEY : pour 
- RADIATOR_TEST_ENVIRONMENT : True pour éviter les accès au harware
- SQLALCHEMY_DATABASE_URI : path du fichier contenant la base SQLLite

## Installation
venev activé dans le terminal de Pycharm, sinon
activation de l'environnement : source ~/workspace/venv/WebRadiator/bin/activate

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
https://sysadmin.cyklodev.com/deployer-une-application-flask/

lancement du server avec la config Pycharm,
localhost:5000/  
arrêter avec ^C

Pour isolation du server / programm raspberry, passer par un fichier  (log pour avoir temperature et mode actuel,
userinteraction.json pour donner les ordre, mais qui du FTP -> débrancher le FTP et modifier appli iOS)

autre solution : intégrer le flask et le programme raspberry, à voir si ça marche

Pour développer le flask, on va imaginer un objet Radiator qui expose une interface, on verra après comment il agit


POur la phase de test, user stephane mdp chat

== Base de donnée
commit
flask db stamp head
flask db migrate
flask db upgrade
