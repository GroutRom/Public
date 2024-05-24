1. Accéder au répertoire du projet :
        cd HTTPSession

2. Exécuter la commande pour s'assurer que le script entrypoint.sh est exécutable :
        sudo chmod +x entrypoint.sh

3. Construire l'image Docker en exécutant la commande suivante :
    docker compose build

4. Lancer le conteneur Docker :
    docker compose up 

5. Accéder  aunavigateur Web et ouvrir l'URL suivante :
    http://localhost:8000


exemple requête POST : http://127.0.0.1:8000/session/?mode=email
{
    "user": {
        "email": "name@email.com"
    },
    "device": {
        "type": "mobi", // ou 'othr'
        "vendor_uuid": "deae564e-a9b6-44cf-a000-f39e69a1b5bf" //facultatif pour 'othr'
        
        possibilité d'utiliser "https://devtools.best/uuid" pour générer des uuid facilement 
        
    }
}

exemple requête PATCH ou PUT :http://127.0.0.1:8000/session/70a48e1a-feda-4687-8cfc-a6c223f32da9/
{
    "otp_code": "861026" //logger.info
}
