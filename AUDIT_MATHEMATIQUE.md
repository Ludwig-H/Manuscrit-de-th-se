# Audit mathématique du manuscrit de thèse

- **Manuscrit audité :** `Manuscrit_de_these/Manuscrit these Louis Hauseux/main.tex`
- **Date de l'audit :** 10 juillet 2026
- **Version compilée :** 248 pages, LuaLaTeX/Biber
- **Nature de l'audit :** lecture statique de toutes les sources actives, contrôle des définitions, des preuves, des changements d'échelle, des hypothèses, des conclusions expérimentales et de la compilation.

Sauf mention contraire, les chemins `PartI/...`, `PartII/...` et `PartIII/...` sont relatifs au répertoire `Manuscrit_de_these/Manuscrit these Louis Hauseux/`. Les numéros indiqués sont les lignes des sources TeX, non les pages du PDF.

## 1. Conclusion exécutive

Le manuscrit contient plusieurs résultats justes et des idées géométriques solides. En particulier, le résultat MST--composantes de sous-niveau, le coeur du théorème HGP--estimateur $K$-NN, le TCL fini-dimensionnel du champ d'occupation et plusieurs lemmes de géométrie discrète résistent à l'audit.

En revanche, **une révision mathématique majeure est nécessaire avant dépôt ou soutenance dans l'état actuel**. Six problèmes bloquants affectent des résultats centraux ou des dépendances entre chapitres :

1. les conventions $K$, voisinage, rayon et facteur $1/2$ sont incompatibles entre RSL, DBSCAN, HGP, les modèles de percolation et les simulations ;
2. le passage du TCL fini-dimensionnel à la percolation des ensembles d'excursion gaussiens n'est pas démontré ;
3. HGP produit des familles chevauchantes et parfois partielles, mais est ensuite traité comme un dendrogramme ou un arbre ultramétrique ;
4. le théorème généralisant le niveau de référence d'un tirage aléatoire est faux ;
5. le théorème abstrait de réversibilité de la dynamique de type Swendsen--Wang est faux sous les hypothèses énoncées ;
6. le « complexe de Delaunay d'ordre $K$ » utilisé est le nerf des cellules d'ordre $K$, non la mosaïque de Delaunay standard invoquée dans la preuve algorithmique.

Les trois premiers points se propagent aux principales conclusions de la partie II ; les deux suivants affectent les théorèmes d'impossibilité et de dynamique de la partie III. Les tableaux et figures comparant RSL et DBSCAN doivent être recalculés ou au minimum réétiquetés après fixation de la convention sur $K$.

### Échelle de gravité

- **Critique** : énoncé faux, objet mal identifié ou rupture logique affectant un résultat central ou plusieurs chapitres.
- **Majeur** : preuve non valide ou hypothèses essentielles absentes ; résultat localement réparable.
- **Modéré** : imprécision formelle, quantificateur, convention ou affirmation excessive qui doit être corrigé.
- **Mineur** : notation, terminologie, référence ou problème de production du PDF.

## 2. Blocages critiques

### C1. RSL, DBSCAN et $K$-NN ne décrivent pas le même objet

**Emplacements :**

- `PartI/ChapI.tex:449-471` ;
- `PartI/ChapIII.tex:167-249` ;
- `PartII/ChapIII.tex:158-183, 331-353, 562-563, 616-619, 883-955`.

#### Diagnostic

Quatre conventions se superposent.

1. La formule $\lvert B(x,r)\cap X\rvert\ge K$ compte $x$ lui-même, alors que le texte parle de « $K$ voisins ». Le paramètre écrit $K$ signifie donc $K-1$ autres points.
2. La boule est ouverte dans une définition où un minimum est demandé. Sur un échantillon fini, l'ensemble des rayons admissibles peut être de la forme $(d,\infty)$, sans minimum. Il faut employer un infimum ou une boule fermée.
3. La définition

   \[
   u^{\rm RSL}(x,y)=\frac12\min_\omega\max_{e\in\omega}
   \max\{r_K(e^-),r_K(e^+),d(e^-,e^+)\}
   \]

   implique, au niveau $u^{\rm RSL}\le r$, la condition $r_K(x)\le 2r$, et non $r_K(x)\le r$ annoncée ensuite.
4. Dans la partie II, les coeurs sont sélectionnés dans une boule de rayon $r$, mais reliés lorsque leurs boules de rayon $r$ se rencontrent, soit à distance au plus $2r$. C'est un RSL de portée $\alpha=2$. Un DBSCAN standard de paramètre $\varepsilon=r$ relie coeurs et points accessibles à distance au plus $r$.

La présentation attribue en outre à Chaudhuri--Dasgupta un Single-Linkage sur la distance de *mutual reachability*. Leur algorithme RSL utilise deux paramètres $k,\alpha$ : sommets actifs si $r_k(x)\le r$, arêtes si $d(x,y)\le\alpha r$. L'identification n'est donc pas générale. Voir le [papier original de Chaudhuri et Dasgupta](https://papers.nips.cc/paper_files/paper/2010/file/b534ba68236ba543ae44b22bd110a1d6-Paper.pdf).

#### Contre-exemple interne décisif

Dans le modèle fermé de la partie II, avec le comptage actuel et $K=2$, tout point $y$ situé à distance au plus $r$ d'un coeur $x$ contient au moins $x$ et $y$ dans sa propre boule. Il est donc lui-même coeur. La catégorie des points de bord DBSCAN est vide. Dans la définition ouverte de la partie I, le même argument vaut pour $d(x,y)<r$ ; à l'égalité, il faut d'abord remplacer le minimum inexistant par un infimum. Par conséquent, dans le modèle de la partie II,

\[
\Theta^{\rm dbscan}=\Theta^{\rm core}
\]

Cela contredit `PartII/ChapIII.tex:562-563` et les valeurs différentes du tableau `:616-619`. Les expériences semblent utiliser « $K$ voisins hors soi », donc un seuil $K+1$ dans les formules de comptage sous Palm.

#### Impact

- les seuils critiques et les comparaisons RSL/DBSCAN ne correspondent pas aux définitions ;
- les expériences étiquetées $K=2$ ne testent vraisemblablement pas le modèle théorique $K=2$ ;
- les événements gaussiens et leurs quantiles sont décalés ;
- les résultats de consistance cités pour RSL ne s'appliquent pas directement ;
- l'identification DBSCAN--HDC et les interprétations « coeur/bord » deviennent fausses.

#### Correction minimale

1. Distinguer le compte d'évaluation générique $N_r^{\rm eval}(y)=\#(X\cap\overline B(y,r))$, utilisé par HGP et l'estimateur $K$-NN en un point quelconque, du compte *leave-one-out* $N_r^{\rm loo}(x)=\#((X\setminus\{x\})\cap\overline B(x,r))$ pour un point échantillonné.
2. Employer $q$ pour le nombre d'autres voisins et réserver $K=q+1$ au comptage incluant soi, ou faire l'inverse mais sans alterner.
3. Définir séparément

   \[
   G^{\rm RSL}_{r,\alpha}:\quad N_r^{\rm loo}(x)\ge q,\quad d(x,y)\le\alpha r
   \]

   et $G^{\rm DBSCAN}_\varepsilon$, avec coeur et accessibilité au même $\varepsilon$.
4. Réserver $r_{\rm Cech}$, $\varepsilon_{\rm DBSCAN}$ et $r_{\rm RSL}$ à des rayons distincts, avec les conversions explicites.
5. Vérifier la convention réellement codée, puis recalculer ou réétiqueter tous les tableaux et figures concernés.

### C2. Le passage au champ gaussien ne prouve pas la percolation

**Emplacements :** `PartII/ChapIII.tex:683-795, 883-981, 991-1010`.

#### Diagnostic

Le TCL établi à `:683-764` donne correctement la convergence de toute famille finie de variables d'occupation, avec covariance déterminée par le volume d'intersection des boules. C'est une convergence des lois fini-dimensionnelles.

Elle ne donne pas :

- la tension (*tightness*) d'un champ interpolé ;
- la convergence fonctionnelle locale ;
- la stabilité topologique des ensembles d'excursion ;
- la convergence d'événements de connexion à longue portée ;
- la convergence d'un seuil de percolation en volume infini ;
- le contrôle uniforme nécessaire au passage au processus de Palm.

Le texte admet d'ailleurs explicitement une convergence globale à `:943-957`. Même cette convergence ponctuelle d'une fonction de répartition ne suffit pas à inverser les quantiles sans continuité, franchissement strict du niveau et contrôle des queues. Les $a_c^{\rm cc}$ utilisés à `:968` ne sont définis que dans un passage commenté, et $U_p$ n'est pas défini dans l'analyse de haut rappel.

#### Impact

Les seuils asymptotiques, la convergence des quantiles et la formule sur la vitesse de percolation $v_K=1-O(K^{-1/2})$ ne sont pas des conséquences démontrées du TCL. Ils doivent être présentés comme conjectures, hypothèses ou résultats conditionnels.

#### Correction minimale

- conserver le TCL comme théorème autonome validé ;
- isoler un énoncé nommé « Hypothèse de remplacement global » ;
- reformuler tous les résultats ultérieurs sous cette hypothèse ;
- ajouter un lemme distinct d'inversion des quantiles avec continuité et unicité du franchissement ;
- écrire $1-v_K=O(K^{-1/2})$ pour expliciter le signe et le contenu de la notation informelle $v_K=1-O(K^{-1/2})$ ;
- qualifier les équivalents de haut rappel de conjecturaux et préciser le régime conjoint en $K,\varepsilon_K,a_K$.

### C3. HGP n'est pas un dendrogramme

**Emplacements :**

- `PartII/ChapI_et_II_fusionnes.tex:21, 570-588, 647` ;
- `PartI/ChapIV.tex:14-19, 221, 239, 275-277, 313-319`.

#### Diagnostic

Les $K$-polyèdres peuvent se chevaucher et certains points ne sont dans aucun polyèdre. Pour $K\ge2$, la famille au rayon zéro peut même être vide. Il ne s'agit donc ni de partitions, ni de recouvrements de $X$ au sens usuel, ni d'un dendrogramme. Une ultramétrique ne peut pas être lue directement sur cet objet.

Le chapitre IV de la partie I utilise pourtant HGP comme un arbre sur lequel exécuter la programmation dynamique de sélection de type HDBSCAN. Cette opération suppose une laminarité qui n'a pas été établie.

#### Impact

La sortie, la fonction de perte et l'algorithme de sélection de clusters ne sont pas définis sur l'objet effectivement construit. L'égalité annoncée avec une hiérarchie DBSCAN est également trop forte : DBSCAN ne produit une hiérarchie brute qu'après fixation de toutes les conventions, et HDBSCAN ajoute encore condensation et `min_cluster_size`.

#### Correction minimale

Deux voies sont possibles.

1. **Disjonction préalable :** définir une règle déterministe qui transforme chaque famille chevauchante en partition, prouver la laminarité au cours de $r$, puis appliquer la programmation dynamique.
2. **Objet de recouvrements :** assumer que la sortie est un DAG de composantes indexées et définir une optimisation spécifique à ce DAG. Il ne faut alors plus parler d'ultramétrique ou de dendrogramme.

Il faut également remplacer « recouvrement » par « famille chevauchante partielle » tant que les singletons/bruits ne sont pas réintroduits.

### C4. Le niveau de référence aléatoire généralisé est faux

**Emplacement :** `PartIII/ChapII.tex:397-465`, en particulier `:420-433`.

#### Diagnostic et contre-exemple

Le fait prétend qu'une configuration équilibrée et invariante par permutation des labels a asymptotiquement le même niveau de recouvrement qu'un tirage iid uniforme.

Pour $K=2$, soit $a\in\{\pm1\}^n$ une configuration déterministe équilibrée et soit

\[
\Sigma\sim\operatorname{Unif}\{a,-a\}.
\]

La loi est invariante par permutation des deux noms de labels et les proportions sont exactement $1/2$. Pourtant, modulo permutation des labels,

\[
\operatorname{ov}_n(\Sigma,a)=1
\]

presque sûrement. Le niveau de référence vaut donc 1, et non $1/2$.

Le même contre-exemple invalide l'affirmation selon laquelle, pour des proportions non uniformes, la meilleure prédiction est nécessairement une configuration constante. L'invariance des noms de labels ne donne aucune échangeabilité spatiale des sommets.

#### Correction minimale

- restreindre le théorème à l'a priori iid uniforme ; ou
- supposer explicitement

  \[
  \sup_a\Pr\!\left(\operatorname{ov}_n(\Sigma_n,a)
  \ge \frac1K+\varepsilon\right)\longrightarrow0 ;
  \]
- pour des proportions non uniformes, définir les proportions ordonnées modulo permutation et imposer une échangeabilité des sommets conditionnellement aux tailles.

### C5. La réversibilité de la dynamique abstraite n'est pas démontrée

**Emplacements :** `PartIII/ChapII.tex:731-844, 982-988`.

#### Diagnostic

La balance de produit donnée traite $\sum_b U_b$, alors que la preuve remplace ensuite cette somme par

\[
U=U_0+\sum_b U_b.
\]

Aucune balance détaillée n'est imposée au noyau de recoloriage pour la mesure $e^{-U_0}$. La compatibilité écrite ne garantit pas non plus qu'un recoloriage réalise la transition $\sigma\to\sigma'$. Enfin, la seule condition $P_b^\sigma(\varnothing)>0$ ne rend pas la chaîne irréductible : elle ne dit rien sur les transitions du noyau lorsque toutes les pièces sont vides.

#### Impact

Le théorème abstrait est faux sous les hypothèses présentes. Les règles triangulaires à `:982-988` ne sont pas validées par simple renvoi à ce théorème, et les conclusions de réversibilité/irréductibilité à `:793-844` restent à établir.

#### Correction minimale

Introduire explicitement un noyau de recoloriage $R_\omega$ et demander

\[
e^{-U_0(\sigma)}R_\omega(\sigma,\sigma')
=e^{-U_0(\sigma')}R_\omega(\sigma',\sigma),
\]

avec support compatible avec les contraintes gelées. Pour l'irréductibilité, exiger que $R_\varnothing$ soit irréductible sur le support de la mesure cible. Une formulation par mesure jointe d'Edwards--Sokal serait plus sûre. Les règles triangulaires doivent ensuite être vérifiées état par état par un tableau de rapports.

### C6. Le complexe d'ordre $K$ est mal identifié

**Emplacement :** `PartII/ChapIV.tex:638-717`.

#### Diagnostic

Le texte prend le nerf complet des cellules de Voronoï d'ordre $K$, puis l'appelle mosaïque de Delaunay d'ordre $K$. La mosaïque standard est le complexe cellulaire dual et n'est en général pas simpliciale dès la dimension 3. Une intersection non vide de deux cellules ne prouve pas que les cellules sont adjacentes par une facette, donc ne prouve pas l'existence d'une arête dans le $1$-squelette standard.

La preuve à `:671-717` établit seulement l'existence d'un centre

\[
c_\sigma\in\operatorname{Vor}_K(Q_s)\cap\operatorname{Vor}_K(Q_t),
\]

ce qui donne une arête dans le nerf inventé, pas nécessairement dans la mosaïque. La distinction est décrite dans [Edelsbrunner--Osang, *Higher-Order Delaunay Mosaics and Alpha Shapes*](https://research-explorer.ista.ac.at/download/12086/12322/2023_Algorithmica_Edelsbrunner.pdf).

#### Impact

Le résultat Gabriel--Delaunay d'ordre supérieur et l'algorithme qui en dépend ne sont pas démontrés pour l'objet standard annoncé.

#### Correction minimale

- soit renommer partout l'objet « nerf des cellules de Voronoï d'ordre $K$ » et conserver la preuve d'intersection ;
- soit employer le complexe cellulaire/rhomboïdal standard et établir une vraie adjacence par facette.

## 3. Audit de l'introduction et des conventions globales

### m1. Mélanges gaussiens et $k$-means (modéré)

**Emplacement :** `Introduction.tex:78-85`.

Des covariances arbitraires « devenant petites » ne conduisent pas au $k$-means euclidien. Il faut des covariances communes isotropes $\sigma^2I$, des poids égaux ou contrôlés, puis une interprétation en affectations dures ou une limite appropriée. Avec des covariances différentes, la géométrie est de Mahalanobis et le terme $\log\det\Sigma_c$ intervient.

### M2. Consistance $K$-NN

**Emplacements :** `Introduction.tex:118-122`, `PartI/ChapIII.tex:163, 205, 443`.

La seule condition $K\to\infty$ est insuffisante. Il faut une suite $K_n\to\infty$ et $K_n/n\to0$, ainsi que des hypothèses de régularité sur la densité et ses ensembles de niveau. Pour RSL s'ajoutent $\alpha$, des conditions de séparation et des taux adaptés au théorème cité.

### M3. Portée des résultats d'impossibilité

**Emplacement :** `Introduction.tex:190-204`.

Les phrases selon lesquelles aucune paire de clusters ne peut être récupérée à $K$ fixé en dimension $p\ge2$, ou que la percolation se produit nécessairement « trop tôt », sont trop universelles. Les théorèmes portent sur des modèles, régimes asymptotiques et géométries précises. À $K$ fixé, certaines vallées permettent une séparation fractionnaire ; une pleine consistance demande des hypothèses plus fortes, par exemple un intervalle de densité nulle. Chaque conclusion doit préciser le sens de « récupérer » et renvoyer à son jeu d'hypothèses.

### m4. Unicité du MST et rôle des graphes (modéré)

**Emplacements :** `Introduction.tex:46, 58`.

- Un arbre couvrant minimal n'est pas nécessairement unique. Toute phrase structurelle doit porter sur « tout MST » ou supposer des poids distincts.
- « Les graphes ne suffisent plus » contredit la construction du graphe auxiliaire $\Gamma_K$. Écrire plutôt que les graphes géométriques binaires sur $X$ ne suffisent pas à représenter les chevauchements d'ordre supérieur.

### M5. Paramétrage global par demi-distance

**Emplacements :** `PartI/ChapI.tex:53-62, 186-230, 533` et formules min-max transversales.

Le manuscrit utilise successivement le poids $d(x,y)$ et $d(x,y)/2$, tout en conservant la notation `MST_{\le r}`. Dans le théorème pondéré, elle signifie poids au plus $r$ ; dans la version géométrique, longueur au plus $2r$. Fixer soit $w=d/2$, soit la notation `MST_{\le 2r}`. La formule min-max principale doit adopter la même convention.

### M6. Densités et versions presque partout

Un arbre de clusters défini par les ensembles $\{f\ge\lambda\}$ dépend de la version ponctuelle choisie pour une densité définie seulement presque partout. Il faut choisir une représentante continue, semi-continue supérieure, ou définir l'objet modulo une régularisation canonique.

### M7. Conclusion trop absolue sur les méthodes sans a priori

**Emplacement :** `conclusion.tex:12`.

L'affirmation selon laquelle seule la méthode $K$-NN reste « sans a priori » est fausse : estimateurs à noyau, histogrammes adaptatifs et d'autres estimateurs non paramétriques existent. Préciser le sens exact d'« a priori » : forme paramétrique, bande passante, métrique, ou nombre de clusters.

## 4. Partie I : théorie du clustering hiérarchique

### Chapitre I

#### P1-m1a. Estimateur 1-NN à valeur infinie (modéré)

**Emplacements :** `PartI/ChapI.tex:449-465, 491`.

$\widehat f_1(x)=+\infty$ sur les points de l'échantillon, mais le codomaine annoncé est $\mathbb R_+$. Employer $[0,+\infty]$ ou définir séparément l'estimateur hors échantillon. Définir aussi la valeur lorsque plusieurs distances sont nulles.

#### P1-M2. Paramètres densité/rayon confondus

**Emplacements :** `PartI/ChapI.tex:495-535`.

$L_K$ et $H_{\widehat f_K}$ alternent entre un niveau de densité $\lambda$ et un rayon $r$. La synthèse passe une valeur $\lambda_t$ à un objet défini en $r$, et le cas $r_0=0$ donne $\lambda_0=+\infty$. Il faut deux paramétrisations nommées, une application de conversion et un traitement séparé du niveau initial.

#### P1-M3. Bornes de Delaunay et dégénérescences

**Emplacement :** `PartI/ChapI.tex:126-166`.

La borne planaire $3n-6$ exige une triangulation planaire choisie ou l'absence de quatre points cocirculaires. Avec la définition existentielle des arêtes, un ensemble cocirculaire peut induire davantage d'arêtes. Ajouter la position générale ou fixer une triangulation.

#### P1-m1. Détails formels

- `PartI/ChapI.tex:503-519` : écrire $d(x,C)\le r$, et non « à moins de $r$ », puisque les boules sont fermées.
- `PartI/ChapI.tex:207-210` : la propriété de coupe doit supposer qu'une arête traverse la coupe, ou que le graphe est connexe.
- `PartI/ChapI.tex:186-230, 533` : harmoniser `T_{\le r}`, `MST_{\le r}` et le facteur 2.

#### Résultat validé

La preuve `PartI/ChapI.tex:186-204` montrant que tout MST préserve les composantes de chaque sous-niveau est correcte. Elle ne requiert pas l'unicité du MST.

### Chapitre II

#### P1-m4a. Relations d'équivalence et partitions (modéré)

**Emplacements :** `PartI/ChapII.tex:51-58, 135-148`.

Une relation d'équivalence n'est pas un élément de $\operatorname{Part}(X)$. Les formules doivent retourner la partition quotient $X/{\sim}$, ou travailler dans un ensemble $\operatorname{Eq}(X)$ de relations d'équivalence.

#### P1-M5. Égalités de distances dans Single-Linkage

**Emplacements :** `PartI/ChapII.tex:104-156`.

La récursion suppose d'abord des distances distinctes, puis le résultat est annoncé pour tout espace métrique fini. En cas d'égalités, plusieurs fusions se produisent au même rayon et l'ordre séquentiel peut créer plusieurs partitions au même niveau. Définir directement les composantes du graphe de sous-niveau, ce qui traite les fusions simultanées.

#### Résultats validés

- La correspondance dendrogramme--ultramétrique à `PartI/ChapII.tex:90-195` est correcte après traitement des égalités.
- Les trois axiomes de Carlsson--Mémoli à `:226-239` sont correctement adaptés à la convention de demi-distance. Contrôle effectué contre [Carlsson--Mémoli, JMLR 2010](https://jmlr.csail.mit.edu/papers/volume11/carlsson10a/carlsson10a.pdf).

### Chapitre III

#### P1-M6. Théorème de Hartigan sur Single-Linkage

**Emplacements :** `PartI/ChapIII.tex:109-123`.

La dichotomie de pleine consistance est correctement attribuée, mais les hypothèses sont omises : ensembles de superniveau formés d'unions finies de compacts à intérieurs connexes, métrique bi-lipschitzienne à la métrique euclidienne, et amas $A,B$ contenus dans un même amas ancêtre $S$ pour la conclusion comparée. L'affirmation « seulement fractionnellement consistant » exige en plus une condition quantitative de vallée ; elle n'est pas inconditionnelle. Voir [Hartigan, *Consistency of Single Linkage for High-Density Clusters*](https://www.stat.cmu.edu/~rnugent/PCMI2016/papers/HartiganClusterTree.pdf).

#### P1-m7a. Diagonale de la formule min-max (modéré)

**Emplacements :** `PartI/ChapIII.tex:191-198`.

La formule inclut $x=x'$, mais le maximum sur le chemin vide n'est pas défini. Un chemin artificiellement non vide donnerait une diagonale positive. Restreindre d'abord la formule à $x\ne x'$, puis poser $u(x,x)=0$.

#### P1-M8. DBSCAN, HDC et points couverts

**Emplacements :** `PartI/ChapIII.tex:221-249`.

Les points DBSCAN accessibles ne coïncident pas avec les points couverts par la définition HDC. Pour $K=2$, deux points distants d'une valeur dans $(r,2r]$ produisent une lentille non vide dans $L_2(r)$, sans qu'aucun point échantillonné ne soit coeur au rayon $r$. Seule l'inclusion globale des points accessibles DBSCAN dans l'union des points HDC couverts est immédiate ; une composante DBSCAN ne correspond pas nécessairement à une unique composante de $L_K$. Énoncer exactement cette inclusion et traiter les points frontière adjacents à plusieurs composantes de coeurs.

#### P1-m9a. `min_cluster_size` n'est pas un seuil de percolation (modéré)

**Emplacements :** `PartI/ChapIII.tex:262-271`.

Il s'agit d'un seuil de condensation en taille finie. Le terme « seuil de percolation » suppose un modèle asymptotique et un seuil critique qui ne sont pas fournis ici.

#### P1-M10. Stabilité HDBSCAN et densité

**Emplacements :** `PartI/ChapIII.tex:277-295`.

Le texte identifie l'excès de masse d'une densité à une stabilité paramétrée par $\widehat\lambda=1/r$. En dimension $p$, un estimateur $K$-NN de densité varie comme $r^{-p}$, pas $r^{-1}$. Il faut distinguer le paramètre d'échelle interne à HDBSCAN d'une densité physique.

#### P1-m2. Qualification empirique

**Emplacements :** `PartI/ChapIII.tex:15, 443-465`.

Le seuil empirique $K\gtrsim10$ n'est pas universel. Le qualifier d'observation dépendant des données, de la dimension, de la métrique et des paramètres, et fournir la source ou le protocole.

#### Résultat validé

L'exemple chaîne/simplexe et l'instabilité de Complete/Average Linkage à `PartI/ChapIII.tex:97-103, 153-155` sont conformes aux références citées.

### Chapitre IV

#### P1-m11a. Conditions KKT inversées (modéré)

**Emplacement :** `PartI/ChapIV.tex:36`.

Pour la pénalité de fusion $\ell_2$, si $u_i\ne u_j$, le dual est saturé : $\lVert v_{ij}\rVert=\gamma w_{ij}$. Si $u_i=u_j$, il peut être strictement intérieur. L'interprétation mécanique du texte dit l'inverse.

#### P1-M12. Le chemin de convex clustering peut se scinder

**Emplacements :** `PartI/ChapIV.tex:29-119`.

Avec une pénalité $\ell_2$ et des poids arbitraires, la trajectoire peut comporter des scissions. Elle ne définit pas automatiquement un arbre de coalescences. Ajouter des hypothèses assurant l'agglomération ou parler d'un chemin de partitions non hiérarchique. Ce phénomène est déjà discuté dans [Hocking et al., *Clusterpath*](https://icml.cc/2011/papers/419_icmlpaper.pdf).

#### P1-M13. Complexité de $k$-means

**Emplacement :** `PartI/ChapIV.tex:123`.

« NP-difficile dès que $k\ge2$ et $p\ge2$ » est faux. Le problème est NP-difficile pour $k=2$ lorsque la dimension varie, ou en dimension 2 lorsque $k$ varie. Si $k$ et $p$ sont tous deux fixés, des algorithmes polynomiaux existent.

#### P1-M14. Résultat de Draganov et al. mal transposé

**Emplacements :** `PartI/ChapIV.tex:127-131`.

Le résultat concerne le $(k,z)$-clustering dans une ultramétrique relaxée représentée par un arbre LCA, avec centres contraints aux feuilles. Ce n'est pas le $k$-means euclidien à centroïdes, ni simplement l'objectif euclidien restreint aux coupes de l'arbre d'entrée ; les solutions forment une nouvelle hiérarchie. Reformuler l'objet, la métrique, les centres admissibles et l'hypothèse d'arbre fourni. Voir [Draganov et al., NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/ba1293b663ddd4a29c6854e4d3bf766a-Paper-Conference.pdf).

#### P1-M15. Perte récursive circulaire

**Emplacements :** `PartI/ChapIV.tex:213-219`.

Poser `loss(C)=-\tilde E(C)` est circulaire si $\tilde E$ contient déjà le maximum récursif entre le parent et ses descendants. La récurrence doit comparer une quantité locale $\widehat E(C_{\rm parent})$ à la somme des valeurs optimales des enfants.

## 5. Partie II : géométrie et percolation

### Chapitres I--II fusionnés

#### P2-M1. Familles partielles, naissances et supports

**Emplacements :** `PartII/ChapI_et_II_fusionnes.tex:21, 561-588, 647, 674-733`.

- Ces familles ne recouvrent pas nécessairement $X$ ; à $r=0$, elles peuvent être vides pour $K\ge2$.
- Les polyèdres ne font pas que croître et fusionner : de nouveaux $(K-1)$-simplexes peuvent apparaître, donc de nouvelles composantes naissent.
- Le théorème inclut $r=0$, alors que l'objet discret avait été défini pour $r>0$.
- Point à formaliser : si un « polyèdre » est identifié seulement à l'union de ses sommets, deux composantes indexées distinctes pourraient avoir le même support. Définir d'abord le polyèdre comme composante de $\Gamma_K$, puis son support dans $X$.

#### Résultats validés

- Les seuils de l'exemple géométrique `:242-370, 522-525` sont corrects : $r$, $2r/\sqrt3$, puis $r\sqrt{2+\sqrt3}=AD/2$.
- Le coeur du théorème HGP--$K$-NN `:667-734` est solide : $L_K(r)$ est une union finie de régions témoins convexes et $\Gamma_K$ est leur graphe d'intersection. Ajouter seulement qu'une région témoin connexe rencontrant une composante de $L_K$ y est entièrement contenue.

### Chapitre III : percolation

#### P2-M2. Domination de percolation manquante

**Emplacements :** `PartII/ChapIII.tex:318-327`.

Les événements « le petit cube est inclus dans $L_K^\lambda$ » sont dépendants. Une probabilité marginale proche de 1 n'autorise pas à invoquer directement une percolation de sites indépendante. Il faut une domination d'un champ à dépendance finie, avec taille de blocs et portée explicites. Pour le graphe des coeurs, l'événement de bloc doit en outre garantir l'existence de coeurs connectés ; l'argument actif ne traite que l'union polyédrique.

#### P2-M3. Modèle de densité incomplet

**Emplacements :** `PartII/ChapIII.tex:404-414`.

Pour que $f$ soit une densité et représente deux zones séparées, il faut au minimum : $A\cap B=\varnothing$, une séparation positive, un fond $F$ mesurable de mesure finie, et

\[
\rho\lvert A\cup B\rvert+\rho_0\lvert F\rvert=1.
\]

#### P2-M4. Fusion par corridor non démontrée

**Emplacements :** `PartII/ChapIII.tex:416-431`.

Une traversée supercritique du corridor ne garantit pas qu'elle se raccorde aux composantes géantes suivies dans $A$ et $B$. La condition $r_n\to0$ est posée plus haut à `PartII/ChapIII.tex:374` mais doit être rappelée dans l'énoncé. Il manque surtout une condition `liminf` strictement supercritique, un corridor de largeur positive raccordé à des boîtes intérieures, ainsi que des estimées de traversée et d'attachement. Une hypothèse commentée dans le source signalait déjà cette lacune.

#### P2-M5. « Fraction récupérable juste avant fusion » non définie

**Emplacements :** `PartII/ChapIII.tex:404-480`.

La quantité n'est pas définie comme variable aléatoire ; l'énoncé ne précise ni comment la suite $r_n$ approche la criticité, ni le mode de convergence. Surtout, la preuve approche l'intensité critique par valeurs supérieures, donc après la fusion supposée, alors que « juste avant » exige une approche sous-critique. Une version plausible demanderait une double limite, d'abord thermodynamique puis $\lambda\uparrow\lambda_c$, une règle de suivi des composantes et un théorème ergodique avec contrôle du bord.

#### P2-M6. Borne linéaire globale impossible

**Emplacement :** `PartII/ChapIII.tex:628-631`.

L'énoncé

\[
\exists C>0,\ \forall\lambda\ge\lambda_c,
\quad\Theta(\lambda)\ge C(\lambda-\lambda_c)
\]

est impossible car $\Theta\le1$ tandis que le membre droit diverge. Restreindre $\lambda$ à $[\lambda_c,\lambda_c+\delta]$, ou écrire $C\min\{\lambda-\lambda_c,1\}$ si une telle borne est réellement connue.

#### P2-M7. Protocole numérique de percolation insuffisant

**Emplacements :** `PartII/ChapIII.tex:546-638`.

Il faut expliciter $\lambda=(2r)^p$ dans le modèle binomial d'intensité unité, le traitement du bord, l'interpolation des seuils, les graines, les intervalles de confiance sur les 100 répétitions et les corrections de taille finie. Sans code ni données, les valeurs numériques n'ont pas pu être reproduites.

#### P2-m1. Quantiles extrêmes

**Emplacements :** `PartII/ChapIII.tex:487-510`.

Pour $\alpha=0$ ou 1, les quantiles peuvent valoir 0 ou $+\infty$. Restreindre à $\alpha\in(0,1)$ ou travailler dans $\overline{\mathbb R}_+$.

#### Résultats validés

- Le changement d'échelle de $\Theta$ et la normalisation $\mu=\lambda\omega_p2^{-p}$ à `:124-134` sont corrects.
- L'argument Campbell--Palm à `:254-315` est essentiellement correct si l'union porte sur toutes les composantes non bornées.
- Le TCL fini-dimensionnel et la covariance par volume d'intersection à `:683-764` sont corrects. Seule son extrapolation globale est en défaut.

### Chapitre IV : Delaunay et Gabriel d'ordre supérieur

#### P2-M8. Support et lemme de rétrécissement

**Emplacements :** `PartII/ChapIV.tex:91-102, 498-534`.

L'existence, l'unicité de la boule minimale et un support de taille au plus $p+1$ valent pour tout ensemble fini $A\subset\mathbb R^p$. Seule la conclusion liée à la position générale du nuage doit être restreinte à $A\subseteq X$. L'implication $\rho(\sigma_s^z)<r$ nécessite en outre un lemme de rétrécissement de la boule tangente ; elle ne découle pas directement du résultat cité.

#### P2-M9. Simplexes séparants et MST en cas d'égalité

**Emplacement :** `PartII/ChapIV.tex:248`.

« Les simplexes séparants sont les arêtes du MST » est faux sans départage. Dans un triangle équilatéral, les trois arêtes sont séparantes alors qu'un MST n'en contient que deux. Dire « appartient à au moins un MST », ou fixer un ordre total des arêtes.

#### P2-m10. Connexité du $K$-graphe de Gabriel (conditionnel, modéré)

**Emplacements :** `PartII/ChapIV.tex:590-622`, `PartII/ChapV.tex:328`.

La connexité n'a pas de preuve autonome dans le texte ; le fait de préservation au rayon infini pourrait toutefois l'impliquer pour la composante pertinente. En l'absence de cette déduction formalisée ou d'un contre-exemple, parler d'une forêt couvrante minimale plutôt que d'un MST rend les énoncés sûrs.

#### P2-m2. Induction sur les composantes

**Emplacements :** `PartII/ChapIV.tex:560-586`.

L'induction de préservation doit porter sur une correspondance de composantes indexées, pas seulement sur leurs unions de points, et traiter les naissances simultanées.

#### Résultats validés

- La réduction aux adjacences élémentaires par le graphe de Johnson à `:194-204` est correcte.
- L'implication « séparant $\Rightarrow$ Gabriel » à `:272-541` paraît correcte sous l'hypothèse de support, après ajout du lemme de rétrécissement.

### Chapitre V : algorithmes

#### P2-M11. Vote vers les sommets non défini

**Emplacements :** `PartII/ChapV.tex:53-95`.

Si $T_x=0$, $V_x(c)$ divise par zéro. Si toutes les faces incidentes sont étiquetées bruit, tous les votes sont nuls et `argmax` assigne arbitrairement un cluster, contrairement à l'étiquette $-1$ annoncée. Poser explicitement

\[
\widehat\ell(x)=-1
\quad\text{si}\quad T_x=0
\quad\text{ou}\quad\max_cV_x(c)=0,
\]

puis départager seulement les maxima strictement positifs.

#### P2-M12. Lemme des deux facettes incomplet

**Emplacements :** `PartII/ChapV.tex:234-295`.

Pour $\lvert S\rvert=2$, la preuve active ne montre pas que la facette $\tau_s$ est portée par une arête dont les sommets sont deux $(K-1)$-uplets de l'objet de Delaunay considéré. L'argument pertinent par boule tangente rétrécie est commenté à `:274-276`. Il faut le réactiver, le formaliser et préciser s'il porte sur le nerf ou sur la mosaïque standard distingués en C6. Le résultat d'existence ne fournit pas encore un appariement efficace des facettes ; une recherche quadratique peut subsister.

#### P2-M13. Construction du 2-Gabriel : correction et complexité

**Emplacements :** `PartII/ChapV.tex:312-333`.

Les paires d'arêtes de Delaunay incidentes ne sont que des candidats. L'algorithme omet le test de vacuité de la boule diamétrale. Leur nombre est

\[
\sum_v\binom{\deg(v)}2,
\]

qui peut être $\Theta(n^2)$ dans une triangulation planaire. La complexité $O(n\log n)$ ne découle donc pas de l'algorithme écrit. Ajouter le test Gabriel et donner une borne sensible à la sortie, ou fournir un autre algorithme avec preuve.

#### P2-m14. « Clique percolation » n'est pas la méthode standard (modéré)

**Emplacements :** `PartII/ChapV.tex:597-601`.

La clique percolation usuelle relie deux $K$-cliques partageant $K-1$ sommets. Le manuscrit impose en plus que leur union soit une $(K+1)$-clique. Pour $K=2$, deux arêtes formant un V sont adjacentes selon la définition usuelle mais pas ici. Renommer l'objet « percolation par cofaces » ou « face percolation ». Voir la [définition primaire de Bollobás--Riordan](https://arxiv.org/abs/0804.0867).

#### P2-M15. Comparaison empirique non isolée

**Emplacement :** `PartII/ChapV.tex:487-488`.

La connexité n'est pas la seule différence entre les méthodes comparées : convention `min_samples`/$K$, portée des arêtes, masses sur les faces, vote vers les points et gestion du bruit changent également. Une conclusion causale sur la seule connexité exige une ablation où tout le reste est fixé.

#### P2-m3. Hypothèses et coûts manquants

- `PartII/ChapV.tex:35-51` : la somme définissant $S_\tau$ doit porter uniquement sur les $K$-simplexes retenus, sans réintroduire tous les candidats.
- `PartII/ChapV.tex:107-120` : ajouter $X\subset\mathbb R^2$ et la position générale.
- `PartII/ChapV.tex:604-614` : définir le poids de naissance de Rips $\rho_{\rm VR}(\sigma)=\operatorname{diam}(\sigma)/2$ et inclure le tri des arêtes dans le coût de Kruskal.

#### Résultats validés

- La normalisation des masses à `:53-66` donne une masse totale 1 par point lorsque $T_x>0$.
- L'intercalage Čech--Rips à `:575-591`, avec $\alpha_p=\sqrt{2p/(p+1)}$, et sa conséquence sur les composantes sont corrects.
- Les formules UMAP à `:652-681` sont correctes à constantes additives près dans l'entropie croisée.

## 6. Partie III : modèles bayésiens, dynamiques et application image

### Chapitre I

#### P3-m1. Terminologie et portée

- `PartIII/ChapI.tex:44` : « Gibbs sampler » désigne l'algorithme par lois conditionnelles ; employer « échantillonneur d'une mesure de Gibbs » pour la classe générale.
- `PartIII/ChapI.tex:55-60` : l'irréductibilité doit être demandée sur le support de la mesure. Des contraintes dures interdisent l'irréductibilité sur tout l'espace.
- `PartIII/ChapI.tex:82-87` : la nécessité de percolation démontrée plus loin suppose un a priori uniforme, $K$ fixé et des recoloriages indépendants uniformes. Elle ne vaut pas pour toute dynamique.
- `PartIII/ChapI.tex:114` : un filtre d'image est un opérateur $F:\mathbb R^\Omega\to\mathbb R^\Omega$, éventuellement suivi d'un seuillage, et non une fonction de l'ensemble des pixels vers $[0,1]$.

### Chapitre II : cadre bayésien et dynamiques

#### P3-M1. Cadre mesurable incomplet

**Emplacements :** `PartIII/ChapII.tex:87, 144-210, 236-248`.

- Demander des espaces boréliens standards pour disposer de conditionnelles régulières.
- La formule de Bayes vaut presque partout, sur $Z(x,w)>0$, relativement à une mesure dominante précisée.
- Si $x_i$ est utilisé, poser $\mathcal X_n=\mathcal X^{V_n}$ ou donner des projections mesurables.
- Un noyau algorithmique est typé sur l'espace d'états $\mathsf O_n$, non sur une variable aléatoire $\operatorname{Obs}_n$.

#### P3-M2. Potentiels infinis et constante de partition

**Emplacements :** `PartIII/ChapII.tex:136, 601-631`.

Les potentiels autorisent $\pm\infty$ sans hypothèse $0<Z_n(x,w)<\infty$. Une énergie $-\infty$ donne $Z=+\infty$ ; des contraintes dures frustrées peuvent donner $Z=0$. Le potentiel signé est ensuite défini seulement pour un poids réel. Il faut soit imposer des poids finis, soit définir les contraintes dures, demander $U(\sigma)>-\infty$ pour toute configuration et supposer l'existence d'au moins une configuration d'énergie finie.

#### P3-M3. Une postérieure générale n'est pas automatiquement une mesure de Gibbs locale

**Emplacements :** `PartIII/ChapII.tex:601-619`.

Il faut supposer une factorisation du canal, par exemple

\[
q_n(w\mid x,\sigma)=c_n(x,w)
\exp\!\left[-\sum_e\psi_{e,x,w_e}(\sigma_i,\sigma_j)\right].
\]

La forme signée exige en plus que le canal ne dépende des labels que par égalité/inégalité et que les poids soient les log-rapports de vraisemblance correspondants. Présenter cette construction comme une sous-classe du cadre bayésien général.

#### P3-M4. Hasard frais dans le couplage markovien

**Emplacements :** `PartIII/ChapII.tex:545-563`.

La loi conditionnelle affichée ne détermine pas le couplage avec $\tau_n$. Ajouter

\[
\Sigma_n^{(1)}\perp\!\!\!\perp\tau_n
\mid(X_n,W_n,\Sigma_n).
\]

#### P3-M5. Fusion d'arêtes parallèles à constante près

**Emplacements :** `PartIII/ChapII.tex:851-860`.

Si $P$ est la somme des poids positifs et $N$ celle des modules négatifs,

\[
P\mathbf1_{\ne}+N\mathbf1_{=}
=\min(P,N)+\psi_{P-N}.
\]

La fusion conserve la mesure de Gibbs après suppression d'une constante indépendante de $\sigma$, pas l'énergie exactement.

#### P3-M6. Preuve de la borne de percolation

**Emplacements :** `PartIII/ChapII.tex:1035-1101`.

Pour $\delta$ fixé, le poids maximal des petits clusters ne tend pas nécessairement vers zéro. On dispose de

\[
\sum_{C:\,|C|<\delta n}\left(\frac{|C|}{n}\right)^2\le\delta.
\]

La bonne erreur est donc $O_{\mathbb P}(\sqrt\delta)$, pas $o_{\mathbb P}(1)$ en $n$. Le résultat paraît réparable par Tchebychev conditionnelle, union sur les $K!$ permutations, puis ordre des limites $\limsup_{n\to\infty}$ avant $\delta\downarrow0$.

#### P3-M7. Modèle de graphe spatial mal instancié

**Emplacements :** `PartIII/ChapII.tex:1136-1277`.

Le modèle original cité a un nombre de points poissonien, des positions aléatoires et des arêtes conditionnellement indépendantes. Le manuscrit utilise $|V_n|=n$ déterministe et ne définit ni l'intensité spatiale ni la loi des positions. Il faut soit conditionner explicitement sur $(N_n,X_n)$ et normaliser par $N_n$, soit annoncer une variante à design spatial fixé. Voir [Sankararaman--Baccelli, *Community Detection on Euclidean Random Graphs*](https://abishek90.github.io/CommDet.pdf).

#### P3-M8. Indépendance des arêtes gelées

**Emplacements :** `PartIII/ChapII.tex:1268-1274`.

La réduction à une percolation indépendante exige l'indépendance conditionnelle des observations d'arêtes et des décisions de gel. Il faut aussi distinguer précisément : absence de composante infinie, plus grande composante $o(n)$, et masse totale de composantes macroscopiques nulle.

#### P3-M9. Seuil triangulaire : calcul juste, hypothèses absentes

**Emplacements :** `PartIII/ChapII.tex:1331-1339`.

Les probabilités locales sont

\[
a=p(2p-1),\qquad s=(1-p)(2p-1),\qquad e=4(1-p)^2,
\]

où $s$ vaut pour chacun des trois états à une arête. La condition autoduale $a=e$ donne bien

\[
p_c^\triangle=\frac{7-\sqrt{17}}4.
\]

Le manuscrit doit fournir ce calcul et vérifier les hypothèses du théorème : $ae\ge2s^2$, $a+e>2\sqrt2/(3+2\sqrt2)$, isotropie, indépendance entre triangles et régime de paramètres. Ces inégalités sont satisfaites ici mais doivent apparaître dans la preuve. Voir [Chayes--Lei, *Random Cluster Models on the Triangular Lattice*](https://etakl.net/papers/triangles.pdf).

#### P3-M10. Extrémité de l'intervalle d'amélioration

**Emplacements :** `PartIII/ChapII.tex:1351-1365`.

À la criticité bidimensionnelle des arêtes, il n'existe pas de composante de densité positive. Sous une exhaustion standard du réseau et des conditions de bord compatibles, l'intervalle où seule la dynamique triangulaire apporte strictement une amélioration doit donc être ouvert à gauche :

\[
p\in(p_c^{\rm edge},p_c^\triangle).
\]

Cette conclusion en volume fini reste conditionnée à la formalisation du passage entre absence de cluster infini et $\theta^{\max}=0$ signalée en P3-M8.

#### P3-M11. Valeurs numériques incompatibles avec l'overlap

**Emplacements :** `PartIII/ChapII.tex:1370-1378`.

Pour $K=2$, l'overlap modulo permutation est toujours au moins $1/2$. Les valeurs 0,005 et 0,007 ne peuvent donc pas être $\operatorname{ov}_n$. Les figures semblent afficher

\[
O_n=\left|n^{-1}\sum_i\sigma_i\tau_i\right|,
\qquad \operatorname{ov}_n=\frac{1+O_n}{2}.
\]

Ainsi $O_n=0{,}007$ correspond à $\operatorname{ov}_n=0{,}5035$. Nommer la métrique. Un seul $n=10^6$ et une trajectoire MCMC ne prouvent ni le mélange ni une propriété asymptotique : fournir initialisation, burn-in, répétitions, diagnostics, intervalles et plusieurs tailles. La dynamique « SW-Triangles (Half-Half) » utilisée dans les figures doit aussi être définie : règle de gel, scission des poids, mesure invariante et paramètres.

#### P3-m2. Autres précisions

- `PartIII/ChapII.tex:297-321` : le fait prouve le meilleur *random guess*, pas l'affirmation générale sur tout meilleur algorithme déterministe.
- `:395` : $\operatorname{RG}_n$ dépend de la loi marginale de $\Sigma_n$, donc potentiellement de $X_n$, pas seulement d'un a priori abstrait sur les labels.
- `:1161-1210` : les logarithmes sont indéfinis pour $0/0$ ; imposer $0<f_{\rm out}\le f_{\rm in}<1$ ou définir les valeurs étendues sur le support.
- `:1141, 1277` : harmoniser « théorème 6.1 » et « théorème 3.1 » ; la version longue contrôlée contient un théorème 6 dans la section 3.1.
- `:1615-1619` : partitionner les lectures par chromosome ne reconstruit pas les séquences ; assemblage, consensus et variants restent à traiter.

#### Résultats validés

- L'identité d'overlap pour $K=2$ est correcte.
- Le principe de rééchantillonnage postérieur/Nishimori est correct lorsque l'indépendance conditionnelle requise est énoncée.
- Le calcul transformant les log-rapports du canal en poids signés est correct dans le régime strict $0<f_{\rm out}\le f_{\rm in}<1$.
- La valeur numérique du seuil triangulaire est correcte ; sa justification doit être ajoutée.

### Chapitre III : détection de fissures

#### P3-M12. Réponse de Hessienne non définie ou non comparable entre échelles

**Emplacements :** `PartIII/ChapIII.tex:58-124`.

$R_B$ est indéfini lorsque $\lambda_2=0$. Pour une analyse multi-échelle, une Hessienne normalisée par $\sigma^2$ est usuelle ; sans elle, les amplitudes ne sont pas comparables et le maximum peut favoriser certaines échelles pour une raison purement dimensionnelle. Définir le cas nul avec un $\varepsilon$, puis préciser si $\sigma^2\operatorname{Hess}_\sigma I$ est réellement utilisé.

#### P3-M13. Alignement sans direction de l'arête

**Emplacements :** `PartIII/ChapIII.tex:184-217`.

Le terme compare les orientations locales entre elles, mais jamais avec la direction $x_j-x_i$. Deux fissures parallèles voisines peuvent donc recevoir une forte similarité par une liaison transverse. Avec $\varphi_{ij}=\arg(x_j-x_i)$, ajouter des pénalités sur $\sin(\theta_i-\varphi_{ij})$ et $\sin(\theta_j-\varphi_{ij})$.

#### P3-M14. Centralité dite d'intermédiarité

**Emplacements :** `PartIII/ChapIII.tex:230-249`.

La formule n'est pas la centralité de Freeman. Après suppression de $v$, une branche singleton ne contient aucune arête et reçoit une masse nulle. Le centre d'un chemin de trois sommets ou d'une étoile peut donc avoir centralité zéro. Employer des masses de sommets, inclure l'arête coupée, ou renommer et justifier cette centralité personnalisée.

#### P3-M15. Algorithme sous-spécifié

**Emplacements :** `PartIII/ChapIII.tex:254-274`.

Le seuil minimal de taille, le sens de $\tau_c$, les deux quantiles actuellement notés $\tau$, la gestion des égalités et des MST multiples, puis la projection des composantes duales vers le graphe original ne sont pas définis. La sortie dépend donc d'un départage implicite. Pour $K=2$, $\widehat\Gamma$ est défini comme l'union des pixels des triangles et l'amincissement est dit optionnel, alors que la sortie est ensuite appelée « squelette » ; cette ambiguïté modifie directement Jaccard, Tversky et Wasserstein.

#### P3-M16. Fusion multimodale et division par zéro

**Emplacements :** `PartIII/ChapIII.tex:289-318`.

La normalisation divise par zéro pour une modalité constante ou affine. Elle ne correspond pas non plus à la réponse unimodale définie auparavant. Écarter une modalité de maximum nul ou diviser par $\max(M,\varepsilon)$, harmoniser les réponses et préciser la polarité avant fusion.

#### P3-M17. Distance de Wasserstein non définie

**Emplacements :** `PartIII/ChapIII.tex:360-375`.

Il manque l'ordre $p$, les mesures associées aux squelettes, la normalisation des masses, le coût au sol et le cas d'un ensemble vide. Si « dilaté de 3 pixels » désigne un rayon morphologique 3, dilater les deux squelettes autorise jusqu'à 6 pixels entre axes ; l'élément structurant et son rayon doivent donc être définis. Définir par exemple $W_1$ entre mesures uniformes, coût euclidien en pixels, et une convention explicite pour le vide.

#### P3-M18. Sélection et réglage sur le jeu de test

**Emplacements :** `PartIII/ChapIII.tex:353-357, 457-490`.

« Premières images », exclusions subjectives et retrait de l'image 042 ne constituent pas un protocole reproductible. Les poids semblent sélectionnés et évalués sur les mêmes données. Donner la liste exacte, les critères préenregistrés, les effectifs, une séparation validation/test, la règle d'agrégation et des intervalles de confiance.

#### P3-M19. Expérience de bruit non reproductible

**Emplacements :** `PartIII/ChapIII.tex:492-555`.

Les lois et paramètres du speckle et du bruit gaussien, la normalisation, les graines et le nombre de tirages manquent. La légende annonce 0--100 % pour un axe Wasserstein mesuré en pixels. Spécifier les distributions, répéter les tirages avec incertitudes et corriger les unités.

#### P3-M20. Généralisation expérimentale excessive

**Emplacements :** `PartIII/ChapIII.tex:561-579, 422-423, 638-654`.

Deux exemples qualitatifs ne démontrent ni la supériorité de $K=2$, ni la robustesse, ni une meilleure généralisation. Réintroduire la phrase de limitation actuellement commentée et fournir une ablation $K=1/K=2$ à paramètres identiques sur un ensemble annoté.

#### P3-M21. Invariance par transformation monotone fausse

**Emplacement :** `PartIII/ChapIII.tex:599`.

Même si l'ordre des similarités $S_{ij}$ est conservé, les valeurs

\[
d_{ij}=(1-S_{ij})\|x_i-x_j\|
\]

peuvent changer d'ordre lorsque les longueurs diffèrent, et la centralité utilise directement les sommes de $S_e$. Remplacer l'invariance annoncée par une observation empirique bornée au domaine testé.

#### P3-M22. Test de Fisher non auditable

**Emplacement :** `PartIII/ChapIII.tex:625`.

La seule indication $F=21$, $p<0{,}001$ ne donne ni réponse, ni modèle, ni degrés de liberté, ni effectifs, ni répétitions, ni diagnostic des résidus. Fournir par exemple le modèle $Y\sim R+\sigma_0+R:\sigma_0$, la loi $F_{\nu_1,\nu_2}$, la taille d'effet et les hypothèses contrôlées. Une interaction significative réfute l'additivité de ce modèle ; elle ne teste pas l'« indépendance » de facteurs choisis par l'expérimentateur.

#### P3-m3. Géométrie et types

- `PartIII/ChapIII.tex:21-38` : l'extension 3D exige une Hessienne $3\times3$, trois valeurs propres, une distinction tubes/plaques, des voisinages et une squelettisation 3D. La présenter comme perspective.
- `:142-146` : $E_R$ doit être un ensemble de paires non orientées, par exemple $\{\{i,j\}:i<j,\ldots\}$.
- `:331-339` : une arête hors de tout triangle devient un sommet isolé du graphe dual et donc une composante ; la retirer explicitement si le but est de filtrer ces arêtes.

## 7. Notations et fondations transversales

### T1. Cardinal et mesure

La notation $\lvert A\rvert$ désigne alternativement un cardinal et un volume de Lebesgue. Employer $\#A$ pour les ensembles finis et $\mathcal L^p(A)$ ou $\operatorname{Vol}(A)$ pour le volume.

### T2. Grand (O)

La table de notations décrit $O(g)$ comme un « ordre exact ». Il s'agit d'une borne supérieure asymptotique. Utiliser $\Theta(g)$ pour un ordre bilatéral.

### T3. Symboles surchargés

- $p$ désigne à la fois dimension et probabilité d'arête ;
- $K$ désigne voisins, ordre géométrique et nombre de communautés ;
- $\sigma$ désigne configuration, simplexe et parfois échelle.

Ces surcharges deviennent dangereuses dans les chapitres de transition. Employer $d$ pour la dimension, $q$ pour les voisins hors soi, $k_{\rm comm}$ pour les labels et $s$ ou $\tau$ pour un simplexe.

### T4. Processus de Palm

Écrire $X^0=X\cup\{0\}$ comme si l'on conditionnait un processus de Poisson ordinaire à contenir l'origine masque un événement de probabilité nulle. Formuler le résultat sous la loi de Palm et invoquer Slivnyak : sous cette loi, le processus a même distribution que $X\cup\{0\}$.

### T5. Boules ouvertes, fermées et égalités

Plusieurs théorèmes exacts alternent $<r$, $\le r$, boules ouvertes et fermées. Ces différences sont négligeables presque sûrement sous certaines lois continues, mais pas pour un théorème déterministe ni en présence d'égalités. Chaque définition doit fixer une convention ; les résultats probabilistes peuvent ensuite signaler l'équivalence presque sûre.

## 8. Audit expérimental et reproductibilité

Aucun script, notebook, fichier de données ou environnement de calcul n'est présent dans le dépôt. Les images finales seules ne permettent pas de contrôler :

- la convention effective sur `min_samples` et l'inclusion du point lui-même ;
- les seuils de percolation estimés ;
- les tableaux RSL/DBSCAN/HGP ;
- les trajectoires MCMC et leur mélange ;
- les expériences de détection de fissures ;
- les tests statistiques et les intervalles d'incertitude.

Pour rendre les résultats auditables, joindre au minimum :

1. un fichier d'environnement verrouillé ;
2. les scripts de génération de chaque tableau et figure ;
3. les données ou un script de téléchargement versionné ;
4. les graines et le nombre de répétitions ;
5. une table machine-readable des paramètres ;
6. les résultats bruts avant agrégation ;
7. un test unitaire qui vérifie explicitement le cas $K=2$, avec et sans inclusion du point lui-même.

Tant que ces éléments manquent, les parties numériques doivent être qualifiées d'illustratives plutôt que de validation expérimentale.

## 9. Compilation et intégrité éditoriale

Une reconstruction forcée a été exécutée avec :

```bash
latexmk -g -lualatex -interaction=nonstopmode -file-line-error main.tex
```

Résultat : compilation réussie, PDF de 248 pages, aucune citation ou référence croisée indéfinie, aucune erreur fatale.

Les avertissements restant dans `main.log`/`main.blg` sont :

- 83 avertissements Hyperref « Token not allowed in a PDF string » ;
- 7 destinations PDF dupliquées (`chapter.1`, `section*.2` à `section*.7`) ;
- 5 boîtes débordantes ;
- 3 avertissements `fancyhdr` sur `\headheight` ;
- options `colorlinks` répétées ;
- une année Biber non entière, `year={2026+}`, pour `BibiInformationInference` ;
- plusieurs avertissements de destinations de notes de bas de page.

Ces points ne changent pas les mathématiques mais doivent être nettoyés avant archivage, notamment les destinations dupliquées qui peuvent produire des liens internes incorrects.

## 10. Résultats qui résistent à l'audit

Les points suivants peuvent servir de socle à la révision.

1. **MST et sous-niveaux :** le théorème de conservation des composantes par tout MST est correct.
2. **Dendrogrammes et ultramétriques :** la bijection et l'adaptation des axiomes de Carlsson--Mémoli sont correctes, après gestion des égalités et fixation du facteur $1/2$.
3. **HGP et $K$-NN :** l'identification des composantes de l'union des régions témoins convexes avec celles de leur graphe d'intersection est solide.
4. **Géométrie de l'exemple HGP :** les trois rayons critiques calculés sont corrects.
5. **Percolation :** le changement d'échelle, la normalisation d'intensité et l'argument Campbell--Palm sont corrects avec la précision indiquée.
6. **Limite gaussienne locale :** le TCL fini-dimensionnel et sa covariance par volume d'intersection sont corrects.
7. **Géométrie d'ordre supérieur :** la réduction par le graphe de Johnson et l'implication séparant--Gabriel sont récupérables avec le lemme de support/rétrécissement.
8. **Čech--Rips :** l'intercalage et la conséquence sur les composantes sont corrects.
9. **Masses et UMAP :** la normalisation de masse lorsque $T_x>0$ et les formules UMAP sont correctes aux constantes annoncées.
10. **Cadre bayésien :** l'identité $K=2$, le rééchantillonnage postérieur et l'algèbre des log-rapports sont corrects sous les hypothèses d'indépendance et de finitude précisées.
11. **Seuil triangulaire :** la valeur $(7-\sqrt{17})/4$ est algébriquement correcte ; il reste à intégrer les hypothèses du théorème de percolation corrélé.

## 11. Plan de correction priorisé

### Étape 0 — Geler les conventions et l'implémentation

1. Déterminer ce que les simulations comptent réellement comme voisin.
2. Fixer les boules fermées/ouvertes, l'inclusion de soi, le rayon d'arête et le facteur $1/2$.
3. Donner à RSL ses deux paramètres $k,\alpha$, et à DBSCAN son propre $\varepsilon$.
4. Ajouter le code et un test de non-régression sur $K=2$.

**Aucun recalcul numérique ne devrait précéder cette étape.**

### Étape 1 — Corriger les six blocages

1. Réécrire les définitions RSL/DBSCAN/HGP et recalculer les résultats affectés.
2. Séparer clairement famille chevauchante, partition, dendrogramme et DAG.
3. Transformer la limite gaussienne globale en conjecture/hypothèse ou fournir la preuve manquante.
4. Restreindre le théorème de *random guess* et intégrer le contre-exemple comme garde-fou.
5. Reformuler la dynamique par une mesure jointe et prouver la balance du recoloriage.
6. Choisir entre le nerf d'ordre $K$ et la mosaïque de Delaunay standard, puis adapter le théorème.

### Étape 2 — Réparer les théorèmes centraux locaux

Priorité à :

- la fraction récupérable et l'ordre des doubles limites ;
- la fusion par corridor ;
- la domination de percolation dépendante ;
- la preuve des petits clusters dans le théorème d'impossibilité ;
- les hypothèses de Hartigan et de consistance RSL ;
- le chemin de convex clustering et la programmation dynamique ;
- l'algorithme 2-Gabriel et sa complexité.

### Étape 3 — Refaire l'évaluation empirique

1. Relancer toutes les comparaisons après correction de $K$.
2. Ajouter tailles multiples, répétitions, incertitudes et corrections de bord.
3. Séparer validation et test pour l'application image.
4. Nommer correctement les métriques d'overlap et Wasserstein.
5. Remplacer les affirmations « démontre/valide/robuste » par des conclusions proportionnées aux données.

### Étape 4 — Harmoniser le formalisme et produire le PDF final

1. Unifier les notations, types, boules et égalités.
2. Corriger les références primaires et leurs hypothèses.
3. Nettoyer les avertissements PDF/Biber.
4. Ajouter une annexe « Conventions et dépendances des théorèmes » donnant, pour chaque résultat, les hypothèses exactes utilisées.

## 12. Critère de clôture de l'audit

Le manuscrit pourra être considéré mathématiquement stabilisé lorsque :

- les six blocages critiques auront un énoncé corrigé et une preuve ou un statut explicitement conjectural ;
- les simulations correspondront exactement aux définitions publiées ;
- chaque résultat asymptotique indiquera la suite de paramètres, l'ordre des limites et le mode de convergence ;
- les objets HGP, RSL, DBSCAN, Delaunay et Gibbs ne changeront plus de sens entre chapitres ;
- les résultats numériques seront reproductibles à partir du dépôt ;
- une nouvelle compilation ne produira ni référence indéfinie ni destination PDF dupliquée.

## 13. Limites de cet audit

Cet audit est une revue mathématique statique approfondie, non une formalisation dans un assistant de preuve. Les sources actives ont été lues et les références primaires déterminantes ont été contrôlées ponctuellement. Les expériences n'ont pas pu être reproduites, faute de code, de données et de fichiers de paramètres. Les points marqués « paraît correct » ou « à formaliser » demandent encore une preuve entièrement rédigée dans le manuscrit ; ils n'ont pas été promus au rang de théorèmes validés sans cette réserve.
