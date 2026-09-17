# Démonstration pour le site web de l'équipe-projet Ayana

**Utilisation de graphes pour la classification et l'extraction de structures.
Généralisation à des interactions d'ordre supérieur.**

Louis Hauseux — septembre 2026.

- [PDF compilé](Demo_Ayana_LouisHauseux.pdf) — 68 planches numérotées, 77 pages (les planches à étapes comptent pour une)
- [Source principale](main.tex)
- Thème Beamer Inria dans [`theme/`](theme/)

## Origine

Ces planches reprennent **exactement** celles de
[`../soutenance/`](../soutenance/) : même thème Inria, même système de citations
maison (`\citb` / `\reffoot`, publications de Louis en rouge), mêmes figures.
Le découpage en huit sections et le détail planche par planche sont décrits dans
le [README de la présentation d'origine](../soutenance/README.md).

Comme les autres dossiers de `Soutenance/`, celui-ci est **autonome et
dupliqué** : `theme/`, `figs/` et `imgs/` y sont recopiés. Une correction faite
ici ne se propage pas à `../soutenance/`, et réciproquement.

## Écarts par rapport à la présentation d'origine

| Écart | Détail |
|---|---|
| Ni date, ni lieu | Sous-titre, `\date` (donc le pied de page de chaque planche) et métadonnées PDF réduits à « septembre 2026 » ; le Learning Centre SophiaTech et l'Université Côte d'Azur comme lieu ne sont plus cités |
| Aucune mention du contexte de soutenance | Page de titre : le sous-titre « Soutenance de thèse » est retiré, ainsi que les lignes **rapporteurs** et **examinateurs** ; l'encadrement devient « Travaux dirigés par… et co-encadrés par… » |
| « les deux idées » | Planche « Quand la structure n'est plus (seulement) la géométrie » : « Les deux idées **de la thèse** appliquées… » → « Les deux idées appliquées… » |
| Pas de diapositives de secours | Les 20 planches de secours (et leur page de garde) sont supprimées : le document s'arrête après la bibliographie |
| Planche 65 retirée | « Travaux de l'auteur présentés aujourd'hui » (la liste complète des références de l'auteur, juste après le « Merci ») |
| `[HAL 17]` sur la planche **Publications** | Nouvelle rubrique « Rapport de recherche » en tête de la planche, pour compenser le retrait de la planche 65 ; la référence complète reste donnée en pied de la planche 3 (prologue) par `\reffoot{hal17}` |

`referencesThesis.bib` n'a pas été recopié : la présentation n'utilise pas
biblatex/bibtex mais le système `\DeclareRef` / `\DeclareMyRef` du préambule.
Les images et les figures TikZ qui n'étaient utilisées que par les planches
supprimées ont également été écartées (29 fichiers de `imgs/`, 23 de `figs/`).

## Compilation

```bash
make        # latexmk + LuaLaTeX, PDF au nom explicite
make clean
```

Nécessite LuaLaTeX (fontspec dans le thème) et le module français de babel
(`texlive-lang-french`).

## Logos de la page de titre

Inchangés par rapport à `../soutenance/` : République française $+$ Inria (du
thème) et Université Côte d'Azur en haut, 3IA Côte d'Azur et DS4H en bas au
centre. La provenance des trois fichiers de `imgs/` et leur recadrage sont
documentés dans le [README de la présentation d'origine](../soutenance/README.md#logos-de-la-page-de-titre).
