# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature du dépôt

Dépôt LaTeX (pas de code applicatif, pas de tests) : le manuscrit de thèse de Louis Hauseux
(clustering hiérarchique, Single-Linkage, percolation, graphes signés, détection de fissures)
et les présentations Beamer associées. Tout le contenu, les commentaires TeX et les messages de
commit sont **en français** ; conserver cette langue.

## Compilation

L'environnement Codespace ne fournit pas TeX par défaut ; l'installer au besoin via
`sudo apt-get install texlive-luatex texlive-latex-extra texlive-pictures texlive-science latexmk`
(vérifier avec `which lualatex` avant de promettre une compilation).

```bash
# Manuscrit complet (depuis la racine) : compile puis copie le PDF à la racine
./compile.sh
# équivalent manuel, depuis "Manuscrit_de_these/Manuscrit these Louis Hauseux/"
latexmk -pdflua -interaction=nonstopmode main.tex
# reconstruction forcée utilisée pour l'audit
latexmk -g -lualatex -interaction=nonstopmode -file-line-error main.tex

# Présentations : chaque dossier de Soutenance/ est autonome
make            # dans Soutenance/<presentation>/
make clean
```

Le moteur est **LuaLaTeX obligatoirement** (`fontspec`, `\pdfvariable`, police Libertinus en `.otf`) ;
`pdflatex` échouera. La bibliographie du manuscrit passe par **biber/biblatex**, celle des
présentations par **bibtex**. `imakeidx` produit deux index (`noms`, `acronymes`) traités
automatiquement par latexmk.

Les `latexmkrc` des présentations ajoutent `theme//` et `latex-inria-fonts//` à `TEXINPUTS` et
forcent `$pdf_mode = 4` ; les Makefile de `PresentationIA/` et `NEO-AMELEAS_Workshop/` font la même
chose à la main (3 passes lualatex + bibtex). Deux Makefile (`beamer-presentation-neo`,
`beamer-presentation-reunion-2026-07-16`) utilisent `-jobname` pour produire un PDF au nom long
explicite plutôt que `main.pdf`.

`.gitignore` ignore tous les `*.pdf` ; les PDF livrés à la racine et dans `Soutenance/` sont
néanmoins suivis (ajoutés en `-f`). Un `git add` ordinaire ne les mettra pas à jour s'ils ne sont pas
déjà suivis.

## Structure du manuscrit

Racine des sources : `Manuscrit_de_these/Manuscrit these Louis Hauseux/` (le nom contient des
espaces — toujours le citer entre guillemets). `Manuscrit_de_these.zip` est un export figé, pas une
source à modifier.

`main.tex` est le seul point d'entrée : préambule (~340 lignes) + `\include` des chapitres. Le corps
suit trois parties, chacune introduite par un `\part{}` suivi de plusieurs paragraphes de texte
*dans `main.tex` lui-même* (les introductions de partie ne sont pas dans des fichiers séparés) :

- **Partie I** `PartI/ChapI..ChapIV.tex` — Single-Linkage : trois points de vue, axiomatique,
  limites, « hacker » HDBSCAN.
- **Partie II** `PartII/ChapI_et_II_fusionnes.tex`, `ChapIII`, `ChapIV`, `ChapV` — HGP-Clusterer,
  percolation, $K$-arbre couvrant et mosaïque de Delaunay d'ordre $K$.
- **Partie III** `PartIII/ChapI..ChapIII.tex` — cadre bayésien / dynamiques de clusters sur graphes
  signés, filtre de Frangi généralisé pour la détection de fissures.

Fichiers **non inclus** (vestiges, ne pas éditer en croyant modifier le manuscrit) :
`PartII/ChapI.tex`, `PartII/ChapII.tex` (fusionnés dans `ChapI_et_II_fusionnes.tex`),
`PartII/ChapIII_old.tex`, `PartIII/ChapII_old.tex`, `resume.tex`, `acknowledgements.tex`,
`echeancier*.tex`, et `these-ISSS2.cls` (variante `graphicx[draft]` de la classe, non chargée).

Liminaires et annexes inclus : `title.tex`, `jury.tex`, `abstract.tex`, `notations.tex`,
`Introduction.tex`, `conclusion.tex`, `cartographie.tex`, `Annexes_ColloquesFormation.tex`,
`annexe_enseignement.tex`, `annexe_prix.tex`.

## Couche de macros — à respecter impérativement

Trois niveaux : `these-ISSS.cls` (classe imposée par l'école doctorale STIC), `raccourcis.sty`
(macros du manuscrit), `notations.tex` (`\providecommand` spécifiques aux notations mathématiques).

**Théorèmes** — environnements `tcolorbox` via `\newtcbtheorem`, donc **deux arguments
obligatoires** : `\begin{Definition}{Titre affiché}{cle}` ... et le label engendré porte un préfixe
automatique dépendant de l'environnement :

| Environnement | Titre imprimé | Préfixe de label |
|---|---|---|
| `Definition` | Définition | `def:` |
| `Theoreme` | Théorème | `th:` |
| `Fait` | **Proposition** | `fait:` |
| `Resultat` | **Fait (connu)** | `res:` |
| `Propriete` | Propriété | `prop:` |
| `Corollaire` | Corollaire | `cor:` |

Attention aux noms trompeurs : `Fait` s'imprime « Proposition » et `Resultat` s'imprime « Fait
(connu) » (résultat repris de la littérature). Preuves : `\begin{Preuve}[titre optionnel]`.

**Renvois** — ne pas écrire `\ref{}` nu pour ces objets : `\Def[def:x]`, `\Th[th:x]`, `\Res[res:x]`,
`\Fact[fait:x]`, `\Cor[cor:x]`, `\Fig[fig:x]`, `\Tab`, `\Alg`, `\Eq` impriment « Def. 3, p. 42 ».

**Noms propres** — `\nom{Hartigan}` compose en petites capitales *et* indexe dans l'index `noms` ;
`\nom*{...}` compose sans indexer ; `\nom[Cech]{Čech}` force la clé de tri. Les noms composés
(Swendsen--Wang, Fortuin--Kasteleyn, Vietoris--Rips, …) ont des alias déclarés dans
`\IndexNomPropre` : ajouter un alias là plutôt que de créer une entrée d'index divergente, et le
renvoi correspondant dans `\AjouterRenvoisIndexNoms` (appelé une fois en début de document).
`\SansIndex{...}` désactive l'indexation dans un bloc (utilisé pour la ToC, les listes de
figures/tableaux).

**Acronymes** — `\DeclareAcronyme{Macro}{Sigle}{Développement}` crée `\Macro` qui imprime le sigle et
l'indexe dans l'index `acronymes` (`\Macro*` sans indexer). Les acronymes du manuscrit (`\SL`,
`\RSL`, `\HDBSCAN`, `\HGP`, `\MST`, `\KNN`, …) sont déclarés en fin de `raccourcis.sty` ; y ajouter
les nouveaux plutôt que de coder le sigle en dur.

**Correctifs de classe** dans `main.tex` — `these-ISSS.cls` est corrigée en place : `\frontmatter`
redéfini (la version d'origine appelle `\sommairename` non défini sous LuaLaTeX), `\@Part` redéfini
pour numéroter les parties et corriger les en-têtes, `\SortirDesAnnexes` pour quitter le mode annexe
avant les index, `\PrintIndexAnnexe` / `\PrintListOfAlgorithmsClean` pour les listes de fin. Ne pas
« simplifier » ces blocs `\makeatletter` sans recompiler l'intégralité.

## Présentations (`Soutenance/`)

Chaque sous-dossier est un projet Beamer indépendant et **dupliqué** : thème Inria (`theme/`),
`referencesThesis.bib` et `imgs/` sont recopiés dans chacun. Une correction de bibliographie ou de
figure faite dans un dossier ne se propage pas aux autres — le préciser plutôt que de supposer une
source unique. `beamer-presentation-neo/README.md` renvoie à un dossier `../research/` qui n'existe
pas dans ce dépôt.

Attention : `NEO-AMELEAS_Workshop/main.tex` référence des images `../Img_presentation_BrunoLevy/`
absentes du dépôt — ce projet ne recompile pas tel quel ; les images peuvent être récupérées du
`main.pdf` compilé via `pdfimages` (poppler).

Contenu des principaux dossiers :
- `NEO-AMELEAS_Workshop/` — exposé (anglais, 3 juillet 2026) sur les parties I–II de la thèse :
  Hartigan, K-NN, MST/Delaunay, RSL/HDBSCAN, hiérarchie 2-NN exacte, mosaïque de Delaunay d'ordre K,
  applications LiDAR 3D/4D. Base principale des slides de soutenance.
- `beamer-presentation-neo/` — séminaire NIM (25 juin 2026) : détection de communautés sur graphes
  signés, cadre bayésien, dynamiques Swendsen--Wang d'ordre supérieur (travail Asilomar → journal).
- `beamer-presentation-reunion-2026-07-16/` — réunion de travail : version détaillée du couplage
  hiérarchique Swendsen--Wang / weak recovery.
- `PresentationIA/` — exposé « AI for Research & Science » (thème + police Pacifico).
- `Presentation__LH_Mathnet-Dyogene_InriaParis_2025-03-24.pdf` — exposé DYOGENE-MATHNET (mars 2025) :
  origine de la thèse (stage chez B. Błaszczyszyn, homologie simpliciale, clustering stylométrique
  par composantes fortement connexes) ; sert de « teasing » à la soutenance.
- `soutenance/` — slides de la soutenance de thèse (8 septembre 2026, Learning Centre SophiaTech,
  Université Côte d'Azur), en français. `make` produit
  `Soutenance_These_2026-09-08_LouisHauseux.pdf` (LuaLaTeX ; requiert `texlive-lang-french`).
  Les blocs TikZ de `figs/` sont extraits/francisés des autres présentations ; système de citations
  maison (`\citb`/`\reffoot`, publications de Louis en rouge) — voir son `README.md`.

## `ISPRS/CrackSAM-GeoLoRA/` — guidage géométrique de SAM 2 (import)

Import sélectif depuis GitHub `Ludwig-H/Generalized-Frangi-…-FIND-dataset/ISPRS/CrackSAM-GeoLoRA`
(rapport, figures, tableau JSON, présentation du 9 août 2026). Résultat **négatif prouvé
causalement** : sur corpus visible monomodal (Khánh Hà), l'évidence géométrique injectée dans
SAM 2 (LoRA + adaptateur init-zéro) n'apporte rien (contrôle par évidence permutée,
|Δ IoU| < 0,001) ; seule la perte tolérante 3 px gagne. Perspective réelle : le multimodal (FIND).
Ne pas présenter ce travail comme un succès du guidage géométrique.

## `EUVIP/` — papier EUVIP 2026 (détection de fissures)

Dossier figé post-acceptation : camera-ready IEEE et author-version HAL (wrappers
`LaTeX/camera-ready.tex` / `LaTeX/author-version.tex` autour d'un corps commun `LaTeX/main.tex`),
revues CMT dans `Reviews/`, code Python (`code/`, aussi publié sur GitHub `Ayana-Inria/Frangi-EUVIP`).
Règle EUVIP : 6 pages max, la page 6 ne contenant que des références — ne pas déplacer les
acknowledgments. Les images de résultats (`LaTeX/*.png`) sont réutilisables dans les présentations.

## `AUDIT_MATHEMATIQUE.md`

Audit mathématique complet (949 lignes, juillet 2026) du manuscrit : 6 blocages **critiques**
(conventions $K$/rayon/facteur ½ incompatibles entre RSL, DBSCAN et HGP ; passage TCL → percolation
non démontré ; HGP traité à tort comme un dendrogramme ; théorème du niveau de référence aléatoire
faux ; réversibilité Swendsen--Wang non démontrée ; complexe d'ordre $K$ mal identifié), puis un
audit chapitre par chapitre avec numéros de ligne TeX, et un plan de correction priorisé (§11).

Le consulter avant toute modification mathématique : il indique les emplacements exacts, ce qui
résiste à l'audit (§10) et l'ordre des corrections (geler les conventions avant de toucher aux
preuves ou aux expériences). Les numéros de ligne cités datent de l'audit et peuvent avoir dérivé —
vérifier le contexte avant d'éditer. Quand une correction est appliquée, mettre à jour la section
correspondante de l'audit.
