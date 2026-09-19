# PhD defence slides — English version

**Using graphs for clustering and structure extraction.
Generalisation to higher-order interactions.**

Louis Hauseux — Tuesday 8 September 2026, Learning Centre SophiaTech,
Université Côte d'Azur.

- [Compiled PDF](PhD_Defense_2026-09-08_LouisHauseux.pdf) — 69 numbered slides, 78 pages
  (step-by-step slides count as one)
- [Main source](main.tex)
- Inria Beamer theme in [`theme/`](theme/)

## Origine

Traduction anglaise de [`../soutenance/`](../soutenance/) : mêmes planches, même
thème Inria, mêmes figures, même système de citations maison (`\citb` / `\reffoot`,
publications de Louis en rouge). Le découpage en huit sections et le détail planche
par planche sont décrits dans le [README de la version française](../soutenance/README.md).

Comme les autres dossiers de `Soutenance/`, celui-ci est **autonome et dupliqué** :
`theme/`, `figs/` et `imgs/` y sont recopiés. Une correction faite ici ne se propage
pas à `../soutenance/`, et réciproquement.

## Écarts par rapport à la version française

| Écart | Détail |
|---|---|
| Tout le texte en anglais | 59 `frame`, les 8 titres de section, les titres de planche, le corps des planches et les étiquettes des 34 figures TikZ. Registre visé : anglais académique simple, orthographe britannique |
| Pas de diapositives de secours | Les 20 planches de secours et leur page de garde sont supprimées : le document s'arrête après la bibliographie. 78 pages contre 101 |
| `babel` | `[french]` → `[british]` (orthographe **et** césure britanniques) |
| `\thankyou` | Le thème code « Merci. » en dur ; redéfini en « Thank you. » dans `main.tex`, `theme/` reste identique à celui de la version française |
| `\up` | Macro fournie par `babel-french` seulement : tous ses usages sont retirés (`2\up{e} prix` → `second prize`) et un `\providecommand` sert de filet |
| Typographie | `« … »` → ` ``…'' ` ; virgules décimales → points (`0,735` → `0.735`) ; plus d'espace avant `:` `;` `?` `!` |

**Ce qui n'est pas traduit**, délibérément : les noms propres, les titres de
publications qui sont réellement en français (`[HAL 17]`, `[GRETSI 25]`,
`[Florek 51]`), l'image scannée du rapport de stage 2017 (planche 3), et
« Université Côte d'Azur ». Les clés de citation, les mathématiques, les
coordonnées TikZ et les chemins d'images sont identiques au fichier français,
octet pour octet.

`referencesThesis.bib` n'a pas été recopié : la présentation n'utilise pas
biblatex/bibtex mais le système `\DeclareRef` / `\DeclareMyRef` du préambule.
Les images et figures TikZ qui ne servaient qu'aux planches de secours ont été
écartées (29 fichiers de `imgs/`, 23 de `figs/`).

## Terminologie

La traduction reprend la terminologie anglaise que Louis emploie déjà dans ses
propres exposés et articles, plutôt que d'en inventer une :
`../NEO-AMELEAS_Workshop/` (parties I–II), `../beamer-presentation-neo/`
(graphes signés), `../../EUVIP/LaTeX/` (filtre de Frangi). Quelques choix fixés :

| Français | Anglais | Source |
|---|---|---|
| simplexe $K$-séparant | $K$-splitting simplex | NEO-AMELEAS |
| vitesse de percolation | percolation rate | glosé dans le manuscrit |
| motif (Swendsen--Wang) | bond | présentation NIM |
| $K$-arbre couvrant | $K$-minimum spanning tree ($K$-MST) | NEO-AMELEAS |
| points cœurs / accessibles | core points / border points | NEO-AMELEAS |
| recouvrement faible | weak recovery | présentation NIM |
| *a priori* (nom) | prior | présentation NIM |
| sans apprentissage | training-free | EUVIP |

La dimension ambiante reste `$p$` (et non le `$d$` de NEO-AMELEAS) : dans ce deck
`$d$` désigne déjà la distance.

## Compilation

```bash
make        # latexmk + LuaLaTeX, PDF au nom explicite
make clean
```

Nécessite LuaLaTeX (fontspec dans le thème). Contrairement à la version française,
`texlive-lang-french` n'est pas requis.

## Logos de la page de titre

Inchangés par rapport à `../soutenance/` ; leur provenance et leur recadrage sont
documentés dans le [README de la version française](../soutenance/README.md#logos-de-la-page-de-titre).
