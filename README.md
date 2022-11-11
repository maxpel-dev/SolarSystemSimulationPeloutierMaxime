# Simulation du système solaire en Python
<p>
Projet réalisé par <b>Maxime PELOUTIER</b> dans le cadre du cours d'Algorithmie en LP DIM.
</p>
<p>
La simulation se base sur des données récupérées depuis l'api https://api.le-systeme-solaire.net/ pour afficher diffrentes planètes du système solaire ainsi que leurs satellites naturels dans une simulation d'orbite héliocentrique affichée grâce à des fonctionnalités de pygame.
</p>
<p>
Pour compromettre réalisme des proportions et qualité d'affichage, des échelles arbitraires de distances et de dimensions ont été mises en place (voir les constantes dans main.py).
Plusieurs modes de vues sont disponibles (se référer à la section <b>Paramétrage</b>.)
</p>

# Paramétrage
De nombreux paramètres sont ajustables dans `main.py`. Des commentaires expliquent leurs impacts.<br>
Je conseille d'abord de tester les différentes valeurs de VIEW (1, 2 et 3) pour les vues préconçues. Ensuite, libre à vous de jouer avec les différents paramètres (variables en MAJUSCULES).

# Lancement
Une fois les paramètres souhaités choisis, lancez simplement `main.py`.

# Contrôles
<li> <b>Flèche du haut (↑) ou Z</b> pour augmenter la vitesse de la simulation.
<li> <b>Flèche du bas (↓) ou S</b> pour diminuer la vitesse de la simulation.
<li> <b>E</b> pour afficher/cacher les orbites des planètes.
<li> <b>R</b> pour afficher/cacher les orbites des satellites.