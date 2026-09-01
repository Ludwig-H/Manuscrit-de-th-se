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
   K-MST et mosaïque de Delaunay d'ordre K.
4. **La percolation comme mesure de performance** (Partie II, chap. III) —
   percolation continue, inconsistance en dimension ≥ 2, vitesse de
   percolation et tableau comparatif HGP / Robust SL / DBSCAN.
5. **Applications LiDAR 3D et 4D** — anomalies (Naval Group) ; puis l'état de
   l'art panoptique, qui *est* un clustering : une bonne segmentation sémantique
   suivie d'un regroupement classique (ALPINE, Sautier *et al.* 2025, premier au
   classement panoptique officiel de SemanticKITTI sans aucune annotation
   d'instance), la 4D tenant en un point (Geo-4D, Oh *et al.* 2025 : même schéma,
   plus une association géométrique entre trames — le détail passe en secours) ;
   enfin nos deux diapositives de résultats — nos *a priori* faibles injectés
   dans la hiérarchie, et le suivi d'instances sur SemanticKITTI, sans
   apprentissage.
6. **Données davantage structurées** (Partie III) — détection de communautés sur
   graphes signés (cadre bayésien, Swendsen–Wang signé, généralisation aux
   interactions d'ordre supérieur, puis une diapositive en trois temps sur le
   théorème principal : on part de Sankararaman–Baccelli — la percolation est
   nécessaire au recouvrement faible et $\theta$ borne la fraction recouvrable —,
   un argument de couplage la retrouve exactement dans le cadre bayésien, et la
   dynamique triangulaire donne une borne strictement meilleure) et
   détection de fissures, en quatre diapositives suivant le papier EUVIP 2026 :
   le contexte et un exemple FIND (où l'on dit que la fusion multimodale se fait
   **au niveau de l'opérateur**, sur les hessiennes et non sur les réponses) ;
   la **hessienne lue sur une ellipse** — axes propres $e_1,e_2$, demi-axes
   $1/\sqrt{|\lambda_1|}$ et $1/\sqrt{|\lambda_2|}$, angle $\theta$ ;
   l'**alignement**, ce que le graphe ajoute au filtre classique, avec les deux
   cas (directions concordantes / croisées) et sa formule encadrée ;
   puis la chaîne d'extraction
   illustrée par les cartes intermédiaires du papier (seuillage → composantes →
   arbre couvrant minimal → centralité pondérée en $\mathcal O(|V|)$ → squelette)
   et le résultat FIND, avec l'extension triangulaire d'ordre 2 en perspective ;
   GRETSI 2025 → EUVIP 2026 → ISPRS en cours.
7. **Perspectives : la voie hiérarchique** — quatre blocs, une illustration par
   diapositive, le détail renvoyé en secours.
   *(a)* Retour au début de l'exposé : le théorème d'impossibilité de Kleinberg
   dans les notations du manuscrit (`PartI/ChapII.tex` : $\mathcal C : (\mathcal X, d)$
   vers une partition ; axiomes (i) invariance d'échelle, (ii) richesse,
   (iii) cohérence), puis la réponse de Carlsson–Mémoli — la sortie devient une
   **ultramétrique** $T : (\mathcal X, d) \mapsto (\mathcal X, u)$, et chacune des
   trois paires d'axiomes se réalise par un choix de **coupe** dans l'arbre du
   Single-Linkage.
   *(b)* La **dynamique hiérarchique** : horloges $\xi_e \sim \mathrm{Exp}(|W_e|)$,
   filtration $\Pi_\beta$, avec $\Pi_1$ = partition gelée de Swendsen–Wang ;
   Glauber aux feuilles, Swendsen–Wang aux racines, toute coupe laissant la loi
   *a posteriori* invariante ; puis la **coupe critique** $\beta_c$, celle où les
   amas gelés percolent. Source :
   `Presentation-MathNet-2026-06-15/research/hierarchical-swendsen-wang`.
   *(c)* **Modèles de fondation et SAM** : ce qu'est un modèle de fondation et la
   condition rarement dite d'une unité de calcul stable ; l'architecture
   asymétrique de SAM et son interface d'invites ; l'adaptation LoRA
   $W = W_0 + BA$ et CrackSAM (Ge *et al.* 2024) ; puis deux idées de guidage par
   la hiérarchie du graphe de Frangi — invites ponctuelles par centralité
   décroissante, et biais additif indexé par la distance dans l'arbre
   (**informer** l'attention, pas la **contraindre**).
   *(d)* Le **modèle de fondation 3D** qui manque : ce qu'un socle partagé
   débloquerait (la révolution robotique), l'unité de calcul absente, le nuage de
   points comme artefact du capteur, puis le polyèdre comme alphabet et la
   hiérarchie comme grammaire.
   **Rien n'y est présenté comme acquis** : les sources sont
   `E-HGP/tests/SemanticKITTI/Zoltan/HierarchicalSelfAttention` (statut
   `foundation_claim = not_yet_earned`) et
   `ISPRS/CrackSAM-HierarchicalSelfAttention` (no-go de conception, sans dépense
   GPU). Sur la dynamique hiérarchique, la borne rigoureuse $0{,}809439$ vient du
   canal triangulaire et **non** de cette dynamique : c'est un programme.
8. **Conclusion, publications** — deux piliers et quatre contributions,
   perspectives dans le fil de la thèse, liste des publications et des dépôts
   logiciels.
9. **Diapositives de secours** (après le « Merci »), suivant la chronologie de la
   présentation : stylométrie 5 auteurs, banc d'essai SIPU, huiles d'olive et leur
   matrice de confusion, protocole des vitesses, fenêtre gaussienne K→∞,
   haplotypes, cadre bayésien/Gibbs, Swendsen–Wang détaillé, modèle
   Sankararaman–Baccelli, hiérarchie d'horloges, **Kruskal des horloges vers le
   dendrogramme**, **la coupe critique $\beta_c$ en détail** (formule explicite,
   condition d'existence $p \ge (1+q_c)/2$, pondération des fusions par
   $\eta_u = \tanh^2(L_u/2)$, et la réserve : la coupe critique n'est pas
   sélectionnée par l'information), échelle des seuils GSBM, calibration SBM,
   validation 10⁶ nœuds, VT-GraF, robustesse, transferts, sensibilité,
   CrackSAM-GeoLoRA, **la suite progressive de guidage de SAM** (plafond par
   oracle, invites natives, biais additif), **ce que HSA exige contre ce que
   donne le graphe de Frangi**, **la chaîne complète de la partition au
   $K$-polyèdre** (Culbertson–Guralnik–Stiller et les recouvrements), puis les
   quatre dernières diapositives de la voie hiérarchique (ce qui reste à
   démontrer ; ce que la thèse fournit déjà à la segmentation en jetons ; les
   bras de contrôle H0–H8 qui réfuteraient le pari hiérarchique ; efficacité
   contre continuité, en chiffres — illustrée par `equilibre_continuite`).

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
en bas de la diapositive.

**Règle** : toute diapositive qui affiche un crochet `[…]` porte le `\reffoot`
correspondant. Seule exception, la diapositive « Publications », où chaque
crochet est déjà suivi du titre, du lieu et de l'année sur la diapositive
elle-même.

## Provenance des figures

- `figs/*.tex` — blocs TikZ extraits (et francisés) de
  `../NEO-AMELEAS_Workshop/main.tex` et `../beamer-presentation-neo/main.tex`.
  Les figures propres à cette présentation (`graphe_signe`, `sw_motifs`,
  `frangi_hessienne`, `frangi_alignement`, `chaine_objets_cibles`, `polyedre_facettes`,
  `alphabet_fondation`, `verrou_portee`, `hierarchie_surfaces`,
  `equilibre_continuite`, `programme_falsification`, `hsa_chenille`,
  `pipeline_polyfm`) sont dessinées pour cette présentation, sans image importée.
  Celles de la partie 7 refondue (`kleinberg_axiomes`, `kleinberg_coupes`,
  `fondation_jetons`, `sam_architecture`, `lora_adaptation`,
  `invites_centralite`, `informer_pas_contraindre`, `revolution_3d`) le sont
  également ; `horloges_kruskal` est adaptée et francisée de
  `Presentation-MathNet-2026-06-15/beamer-presentation-reunion-2026-07-16/hierarchical_sw_frames.tex`.
  `kleinberg_impossibilite.tex` est l'ancienne planche unique, remplacée par le
  diptyque `kleinberg_axiomes` / `kleinberg_coupes` : elle n'est plus appelée.
  `frangi_ordre2.tex` n'est plus appelée non plus depuis la refonte du bloc
  Frangi, l'ordre 2 y étant désormais une ligne de perspective ; `frangi_termes.tex`
  (les trois vignettes courbure / élongation / alignement) a été remplacée par
  `frangi_hessienne.tex` quand la diapositive est devenue mathématique.
- **L'ellipse de `frangi_hessienne`** est définie par ses axes ($e_1,e_2$) et ses
  demi-axes ($1/\sqrt{|\lambda_k|}$), et non comme un ensemble de niveau : sur une
  crête $\lambda_1$ est proche de zéro et de signe quelconque, si bien que
  $\{u : u^{\top}\mathcal H_\sigma u = 1\}$ serait une hyperbole. Ne pas réintroduire
  cette écriture sur la diapositive.
- **Cartes intermédiaires FIND** (`Int_1FIND`, `Cluster_1FIND`,
  `Betweenness_1FIND`, à côté de `FrangiSim_1FIND` et `Resultat_1FIND`) —
  recopiées telles quelles de `EUVIP/LaTeX/` : ce sont les figures du papier
  EUVIP 2026, donc la chaîne montrée en soutenance est exactement celle publiée.
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
