#!/bin/bash
# Script de compilation du manuscrit de thèse

# Aller dans le dossier du manuscrit
cd "Manuscrit_de_these/Manuscrit these Louis Hauseux" || exit 1

# Lancer la compilation avec latexmk en mode LuaLaTeX
echo "Compilation en cours..."
latexmk -pdflua -interaction=nonstopmode main.tex

# Vérifier si la compilation a réussi
if [ $? -eq 0 ]; then
    echo "Compilation réussie !"
    # Copier le PDF généré vers la racine
    cp main.pdf ../../Manuscrit_de_these.pdf
    echo "Le PDF mis à jour a été copié à la racine sous le nom Manuscrit_de_these.pdf"
else
    echo "Erreur lors de la compilation."
    exit 1
fi
