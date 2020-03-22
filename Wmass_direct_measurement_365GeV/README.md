### Get started

Clone the git repository
`git clone https://gitlab.cern.ch/mabeguin/Wmass_direct_measurement.git`


### To run the W mass reconstruction

- hadronic channel:
`python Wmass.py`

- semi-leptonic channel:
`python WmassSemiLeptonic.py`


### Structure the code:
    - fonction main(): Ne prend pas d'argument.
        Definie fichier entrée et fichier de sortie
        Appelle la fonction qui genère les histogrammes et la fonction de reconstruction puis enregistre les histogrammes
        
    - gethists(): Dictionnaire d'histogrammes.
        Tous les histogrammes doivent être déclarés ici.
    
    - w_mass_hadronic(): Reconstruit la masse du W.
        A partir du tree donné en input, construit les impulsions avec le code TreeInfo.
        Paire les dijets
        Calcule les masses des deux dijets
        Remplit les histogrammes