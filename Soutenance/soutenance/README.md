# Soutenance de thèse — mardi 8 septembre 2026

**Utilisation de graphes pour la classification et l'extraction de structures.
Généralisation à des interactions d'ordre supérieur.**

Louis Hauseux — Learning Centre SophiaTech, Université Côte d'Azur.

- [PDF compilé](Soutenance_These_2026-09-08_LouisHauseux.pdf)
- [Source principale](main.tex)
- Thème Beamer Inria dans [`theme/`](theme/)

## Compilation

```bash
make        # latexmk + LuaLaTeX, PDF au nom explicite
make clean
```

Nécessite LuaLaTeX (fontspec dans le thème) et le module français de babel
(`texlive-lang-french`).

## Structure de la présentation

1. **Prologue** — l'énigme de 2017 : stage chez B. Błaszczyszyn (Inria Paris,
   Dyogene), homologie persistante, stylométrie (matrice de Gram, 5 auteurs),
   heuristique des composantes « simplexe-connexes » ; la question fondatrice
   « pourquoi cela marche-t-il si bien ? ».
2. **Du *Single-Linkage* à ses fondements** (Partie I du manuscrit) — modèle de
   Hartigan, estimateur K-NN, graphe géométrique ≡ MST élagué, Robust SL,
   (H)DBSCAN.
3. **Monter en ordre : la hiérarchie K-NN exacte** (Partie II) — contre-exemple
   des six points, complexe de Čech, K-polyèdres, condition de Gabriel,
   K-MST et mosaïque de Delaunay d'ordre K, huiles d'olive.
4. **La percolation comme mesure de performance** (Partie II, chap. III) —
   percolation continue, inconsistance en dimension ≥ 2, vitesse de
   percolation et tableau comparatif HGP / Robust SL / DBSCAN.
5. **Applications LiDAR 3D et 4D** — anomalies (Naval Group), segmentation
   panoptique 4D (SemanticKITTI), sans apprentissage.
6. **Données davantage structurées** (Partie III) — détection de communautés sur
   graphes signés (cadre bayésien, Swendsen–Wang signé, généralisation aux
   interactions d'ordre supérieur, puis une diapositive en trois temps sur le
   théorème principal : on part de Sankararaman–Baccelli — la percolation est
   nécessaire au recouvrement faible et $\theta$ borne la fraction recouvrable —,
   un argument de couplage la retrouve exactement dans le cadre bayésien, et la
   dynamique triangulaire donne une borne strictement meilleure) et
   détection de fissures (résultats multimodaux, puis construction du graphe de
   Frangi par paires et extension triangulaire d'ordre 2 ; GRETSI 2025 → EUVIP
   2026 → ISPRS en cours).
7. **Perspectives : la voie hiérarchique** — le théorème d'impossibilité de
   Kleinberg, énoncé par ses trois axiomes, puis une diapositive distincte sur le
   changement de sortie vers la hiérarchie (Carlsson–Mémoli, puis
   Culbertson–Guralnik–Stiller et les recouvrements) ; la hiérarchie d'horloges
   des dynamiques de clusters ; le manque d'un modèle de fondation pour la 3D ;
   le nuage de points comme artefact du capteur ; les $K$-polyèdres et leur espace d'échelle
   comme alphabet candidat ; deux diapositives simples sur la contre-épreuve
   CrackSAM–HSA et un programme progressif de guidage de SAM. **Rien n'y est
   présenté comme acquis** : les sources sont
   `E-HGP/tests/SemanticKITTI/Zoltan/HierarchicalSelfAttention` (statut
   `foundation_claim = not_yet_earned`) et
   `ISPRS/CrackSAM-HierarchicalSelfAttention` (résultat négatif de conception).
8. **Conclusion, publications** — deux piliers et quatre contributions,
   perspectives dans le fil de la thèse, liste des publications et des dépôts
   logiciels.
9. **Diapositives de secours** (après le « Merci »), suivant la chronologie de la
   présentation : stylométrie 5 auteurs, banc d'essai SIPU, confusion huiles
   d'olive, protocole des vitesses, fenêtre gaussienne K→∞, état de l'art
   LiDAR, haplotypes, cadre bayésien/Gibbs, Swendsen–Wang détaillé, modèle
   Sankararaman–Baccelli, hiérarchie d'horloges, échelle des seuils GSBM,
   calibration SBM, validation 10⁶ nœuds, VT-GraF, robustesse, transferts,
   sensibilité, CrackSAM-GeoLoRA, puis les cinq diapositives de la voie hiérarchique
   (ce qui reste à démontrer ; ce que la thèse fournit déjà à la segmentation
   en jetons ; pourquoi le résultat négatif HSA est un problème de conception ; les bras de contrôle
   H0–H8 qui réfuteraient le pari hiérarchique ; efficacité contre continuité,
   en chiffres).

Les figures de la dynamique hiérarchique proviennent de GitHub
`Ludwig-H/Presentation-MathNet-2026-06-15/research` (SVG convertis) ; celles
de CrackSAM-GeoLoRA de l'import `ISPRS/CrackSAM-GeoLoRA/` de ce dépôt.

## Charte graphique

- **Bleu canard Inria** (`inria-2024-bleu-canard`) : les données (points, nuages, feuilles)
- **Rouge Inria** (`inria-rouge`) : les structures extraites (arêtes, dendrogrammes,
  squelettes, racines, arêtes gelées de Swendsen–Wang) et les travaux de l'auteur
  (citations, et le liseré des encadrés qui portent la contribution propre sur la
  diapositive « La percolation borne le recouvrement des communautés »)
- **Gris foncé** (`gris_fonce_inria`) : éléments neutres (coupes, légendes, littérature)
- **Encadrés de formules** (`\formulebox`) : liseré rouge Inria, fond gris 4 %
- Courbes matplotlib : palette d'origine, annotations aux couleurs des courbes

## Système de citations

Citations entre crochets définies dans le préambule (`\DeclareRef` /
`\DeclareMyRef`) : `\citb{cle}` affiche `[Label]` (en **rouge** pour les
publications de Louis), `\reffoot{cle1,cle2}` affiche les références complètes
en bas de la diapositive de première citation.

## Provenance des figures

- `figs/*.tex` — blocs TikZ extraits (et francisés) de
  `../NEO-AMELEAS_Workshop/main.tex` et `../beamer-presentation-neo/main.tex`.
  Les figures propres à cette présentation (`graphe_signe`, `sw_motifs`,
  `frangi_ordre2`, `chaine_objets_cibles`, `polyedre_facettes`,
  `alphabet_fondation`, `verrou_portee`, `hierarchie_surfaces`,
  `equilibre_continuite`, `programme_falsification`, `hsa_chenille`,
  `pipeline_polyfm`) sont dessinées pour cette présentation, sans image importée.
- **Convention des graphes signés** (`graphe_signe`, `sw_pas`, `sw_motifs`) —
  celle du manuscrit (`PartIII/ChapII.tex`, figure « Interprétation d'un poids
  $w$ réel ») et de `../beamer-presentation-neo/` : trait plein pour une
  interaction attractive, pointillés pour une interaction répulsive, trait gras
  pour une arête satisfaite, trait gras rouge Inria pour une arête gelée. Les
  styles TikZ correspondants (`posedge`, `negedge`, `freeze`) sont déclarés dans
  le préambule de `main.tex` ; l'arête gelée est un `freeze` coloré en
  `inria-rouge`, et une arête non satisfaite est tracée en `line width=0.6pt`
  pour rester distinguable d'une arête satisfaite en projection.
- `imgs/` — images rassemblées depuis les présentations existantes, le
  manuscrit (`img/`), le dossier `EUVIP/LaTeX/`, et extraites des PDF
  (présentation Mathnet-Dyogene 2025, rapport de stage 2017, NEO-AMELEAS)
  via `pdfimages`, recomposées sur fond blanc au besoin.
- Le tableau des vitesses de percolation reprend
  `Manuscrit_de_these/…/PartII/ChapIII.tex` (tab:percolation_horizontal).
