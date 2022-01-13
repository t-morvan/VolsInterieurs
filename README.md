# VolsInterieurs

La convention citoyenne pour le climat proposait d’interdire les vols intérieurs dès lors qu’il existe une alternative en train en moins de 4h; 
la proposition de loi climat a finalement retenu une durée de 2h30 faisant passer de 18 à 5 les lignes impactées par la mesure. 
On se propose ici de construire une carte interactive qui permettrait d’explorer différents seuils et de visualiser les lignes affectées.

Le résultat est à tester sur :
https://observablehq.com/@tmorvan/vols-interieurs-et-trains

et le code correspondant se trouve dans le notebook `vols.ipynb`

## Sources des données :
### Lignes aériennes
On utilise les données fournies par Eurostat : https://ec.europa.eu/eurostat/databrowser/view/avia_par_fr/default/table?lang=en (tableur `flights.csv`)

Elles contiennent les liaisons aériennes et leurs fréquentations par année. On fait attention à ne garder que les lignes actives en 2019/2020.


### Temps de parcours en train
On a recours à l'API de la SNCF qui donne accès au moteur de calcul d'itinéraires (https://www.digital.sncf.com/startup/api). Elle repose sur sur l'API de Navitia (https://www.navitia.io/) construite pour traiter des données de mobilité.

#### 1. Récupération des villes correspondant aux aéroports. 

Si on fournit directement l'aéroport à l'API, le temps de transit vers la gare la plus proche va être pris en compte dans le calcul et ce n'est pas souhaitable. On obtiendrait par exemple pour Paris-Lyon, la somme des trajets suivants :  

* Roissy/Orly - Gare de Lyon en RER/métro 
* Gare de Lyon- Part Dieu en TGV 
* Part Dieu Lyon St-Exupéry en Rhône Express.

Le plus simple reste de chercher manuellement le code administratif de la ville correspondant à l'Aéroport 
(tableur `gares.csv`).

#### 2. Calcul du temps de trajet

On récupère tous les trajets  de la journée en cours et on retient le plus court. 

## Remarques:
1. Le requête a été effectuée pendant le confinement et tous les trajets n'étaient probablement pas assurés, ce qui a pour effet de potentiellement sur-estimer les temps de trajet minimaux (TO DO : actualiser)
2. Il pourrait être intéressant de comparer les durées train vs avion. Pour obtenir les durées en avion, plusieurs pistes : une estimation grossière à partir de la distance et de la vitesse moyenne d'un avion (+ atterrissage/décolage),
du scraping sur des sites de réservation, obtenir l'accès académique à la base EuroControl (https://www.eurocontrol.int/news/new-eurocontrol-rnd-data-archive-launched)
