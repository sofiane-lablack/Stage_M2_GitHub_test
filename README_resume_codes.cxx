Wmass_direct_measurement_240GeV/Wmass1.py
Wmass_direct_measurement_240GeV/runWmass.py

Prend tous les fichiers root en input pour en faire un seul fichier d'output .root qui sera ensuite traité comme s'il s'agissait des données de l'expérience.
Pour faire tourner il faut executer dans le terminal la commande suivante:
$ source runWmass.py
en prenant soin de modifier les input ( tous les fichiers qu'on veut fusionner ) et l'output dans runWmass.py
(Remarque: comprend toutes les branches nécessaires à faire tourner le code du fit cinématique comme l'énergie, l'impulsion des jets...)





Wmass_direct_measurement_365GeV/correlation_matrix.py
Wmass_direct_measurement_365GeV/analysis_tools/fit.py
Le code où il faut ajuster à la main les paramètres des crystalballs pour détermnier les éléments de la matrice de covariance pour le fit cinématique.





Wmass_direct_measurement_365GeV/Wmass1.py
Wmass_direct_measurement_365GeV/runWmass.sh
Pour faire tourner il faut executer dans le terminal la commande suivante:
$ source runWmass.py
en prenant soin de modifier les input ( tous les fichiers d'input .root à la sorti d'heppy dont on veut reconstruire la masse ) et l'output dans runWmass.py
Le code qui applique les cuts (optimales à 365 GeV trouvés durant l'étude durant le stage) sur tous les fichiers d'input .root et reconstruit la masse.






fit_gauss_sgn_bkg240GeV.cxx
Prend en input un seul fichier .root qui est traité comme s'il s'agissait des données de l'expérience. ( à l'aide du code Wmass_direct_measurement_240GeV/runWmass.py)
Fit le coeur à l'aide d'une Gausienne, et sort en output dans le terminal l'erreur
