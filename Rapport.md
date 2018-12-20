# Classification des documents du procès des groupes américains du tabac


## Contexte 

Le gouvernement américain a attaqué en justice cinq grands groupes américains du tabac pour avoir amassé d'importants bénéfices en mentant sur les dangers de la cigarette. Le cigarettiers  se sont entendus dès 1953, pour "mener ensemble une vaste campagne de relations publiques afin de contrer les preuves de plus en plus manifestes d'un lien entre la consommation de tabac et des maladies graves". 

Dans ce procès 14 millions de documents ont été collectés et numérisés. Afin de faciliter l'exploitation de ces documents par les avocats, vous êtes en charge de mettre en place une classification automatique des types de documents. 

Un échantillon aléatoire des documents a été collecté et des opérateurs ont classé les documents dans des répertoires correspondant aux classes de documents : lettres, rapports, notes, email, etc. Vous avez à votre disposition : 

- les images de documents : http://data.teklia.com/Images/Tobacco3482.tar.gz
- le texte contenu dans les documents obtenu par OCR (reconnaissance automatique) : Tobacco3482-OCR.tar.gz  (dans ce git)
- les classes des documents définies par des opérateurs : Tobacco3482.csv (dans ce git)


## Analyse des données

### Les images 

Les images sont en **niveaux de gris**, je n'en ai pas vu de colorisée.

En observant une _petite_ quantité d'images, on peut s'aperçevoir que la qualité des images est inégale entre les images. On peut avoir des images dont la **lecture humaine est réalisable** (lisible par tous), et d'autre ou  cela va s'avérer **plus compliqué**. De plus, entre une pub (Advertisement) et un rapport (report) on ne va pas retrouver la même quantité d'écriture, il va y avoir des dessins ou photographies pour la pub, ce qu'on ne devrait pas forcément retrouver dans le rapport. Ce sont des paramètres qui vont influcer la qualité de la prédiction de l'OCR. 


### Les fichiers textes de l'OCR

On a autant d'images que de textes, c'est à dire : 3482. Nous ne trouvons donc pas dans un cas de "Big data" avec une charge énorme de données. Lors du split, nous répartirons donc nos données en prenant 60% du set pour train, 20% pour valid, et 20% pour test.

En projetant en histogramme puis en camambert (pie) on s'aperçoit qu'on a une inégale répartition de chaque document (Peu de CV et Notes, et au contraire beaucoup d'Emails et de lettres).

On peut faire une analyse comme suite des fichiers textes, par catégorie : 


|Categorie|Nombre moyenne de lettre|Commentaire|
|-----------------------------------|------|---|
|  Advertisement |  700 |Séquence de mots paragraphés. ON peut distinguer des phrases par moment.|
|  Email         |  686 |Les séquences reconnus sont de très bonnes qualité. Structuré + Mots récurrents : From, To, Sent, Date,...|
|  Forms        | 991  |Beaucoup de caractères seuls ou disparates. Peu de mots formés.|
|  lettres      | 1407 |Appréciation de bonne qualité. On retrouve également une structure propre aux lettre|
|  Mémos         | 1302 |Qualité inégale.|
|  Notes         | 250  |Très courts par rapport aux autres catégories. Qualité inégale, dépend de la note|
|  News          | 1870 | Paragraphes courts. Peu de phrases complètes.|
| Report        | 3774 |Texte plus longs que les autres catégories. Paragrpahes longs. Phrases complètes|
|  CV            | 2646 |Texte structuré (Deux dates consécutives, mots récurrents : Name, Experiments...), beaucoup de caractère non lues. Appréciation de  l'OCR inégale|
|  Scientique    | 2744 |Appréciation inégale|


Même si il aurait été faisable de travailler sur les fichiers images uniquement, nous sommes en cours de Text Analysis, et une analyse de  fichier texte sera préférable. Bien que cet argument ne soit pas scientifique, il fut pris en compte pour la décision de traiter le texte. On voit que chaque catégorie a des caractéristiques propres. Mais si un même texte peut ressemble à un texte d'une autre catégorie, la différence entre deux textes de deux catégories existent. Je trouve que les distinctions entre deux images est moins simples. En effet, je trouve que l'entropie interne entre les images d'une même catégorie assez forte par moment. Phénomene que je retrouve moins avec les textes.

J'ai également choisi de ne pas faire de pré processing sur mes données textes. En effet, les sauts de lignes constituent pour moi une caractéristique du document (la "structure"), et je pense qu'il peut etre reconnu par le classifieur. De plus, les mots ou lettres n'ayant pas de sens, n'apparaissent que dans certaines catégories donc je pense qu'ils peuvent aider notre classifieur et sont importants.

## Analyse du problème et choix de la solution

Mon problème est un problème de classification de textes. Dans mon cas, chaque document est relié à une situation : Celle d'un procès de l'industrie du tabac. De plus, chaque texte doit correspondre à une catégorie. Ainsi, je crains qu'un classifieur bayesien, dont une des hypothèses est l'indépendance des mots entre eux, ne soit pas performant. Comme ce fut une solution très utilisé, je tiens à quand même la tester, comme élément de comparaison. J'aimerais ensuite essayer une Multi Layer Perceptron Classifier.  Le but va être de déterminer par gridsearch ses paramètres optimaux. 


## Performance de la solution proposée / Comparaison avec le classifieur bayesien. 

J'ai tout d'abord opter pour un représentation **BagOfWords** avec la fonction **CountVectorizer** plutôt qu'une représentation *TF IDF*. La représentation TFIDF introduit le poids de certains mots, ce qui aurait pu etre intéréssant dans mon modele, car comme je le disais plus haut, il existe plusieurs mots récurrents dans certaines catégories : From,To, ... Cependant, en comparant les deux représentations, je me suis aperçu que les résultats étaient moins bon avec le TF IDF, j'ai donc tourné mon code avec COunt Vectorizer. 

J'ai entrainé deux modèles différents : Un classifieur Bayesien et un MLP Classifier. Le classifieur devait me servir de modele de référence et de comparaison. J'ai déterminé rapidement le NB optimal avec un grid search. J'ai fait varié le uniquement le smoothing ($ \alpha $) et le max_df et max_features pour le vectorizer.  

J'ai ensuite choisie un MLP layer perceptron, avec un solver Adam. Même si j'ai lu que parfois (https://arxiv.org/abs/1705.08292), le solver SGD avait une généralisation meilleure, j'ai gardé le paramètre Adam car il était retenu par le GridSearch. Le nombre de couche a été limité à 50 car les performances avec plus de layers étaient similaires, et le temps de calcul était ensuite drastiquement augmenté au fur et a mesure que le nombre de couches augmentaient. Ainsi 50 neurones était un choix adapté.

### Analyses de la performance

|                .      |  NB    | MLP    |
|----------------------|--------|--------|
| Training             |  0.876 | 0.995  |
| Validation           |  0.745 | 0.776  |
| Test                 | 0.709  | 0.766  |
| Cross Validation (5) | 0.684  | 0.699  |

Sur les résultats d'accuracy, on voit que notre modèle MLP est meilleur de le Naives Bayes. En effet, on gagne plusieurs \% de précision par rapport en passant du NB au MLP. Cette affirmation est validée par la validation croisée, qui donne un leger avantage au modèle MLP. (J'ai pris la moyenne des 5 cross validation). Cependant, on voit que le modèle MLP à une tendance plus forte à surapprendre les données de train. En effet, on a 99,5\% de précision sur le set de train, contre 87,6\%. Ainsi, les garanties de performance sont plus incertaines.

### Analyse des prédictions

On a ensuite procédé un accuracy et classification report. On peut ainsi voir quelles sont les classes mieux appréhender par les différentes méthodes. On s'aperçoit que les deux modèles n'ont aucune difficulté à détecter un CV, et ne se trompe que très rarement en classifiant un document en tant que CV. Cependant, on observe également le même type de confusion entre deux catégories : Lettre et Mémo. L'erreur la plus fréquente est une inversion entre mémo et lettre  par le classifieur. La catégorie lettre est celle qui entraine le plus de confusion, puisqu'elle est régulièrement appelé à tord.

## Pistes d'améliorations

Parmi les premieres idées que l'on aurait pu avoir, on retrouve  le fait d'utiliser une combinaison de classfieurs. IL aurait été intéréssant dans cette combinaison d'avoir un classifieur qui se base sur un CountVectorizer et un sur une représentation TFIDF. En effet, mon MLP et le NB se base sur le CountVectorizer et ils présentent tous les deux les mêmes erreurs. Ainsi, introduire d'autres classifieurs avec un systeme de vote qui s'appuyerait sur les faiblesses et les qualités de chaque classifieurs seraient intéréssant.

De plus, un pré processing des données et des fichiers textes peut également être une piste. En effet, j'ai pris le partie de n'effectuer aucun changement sur mes fichiers textes. Considérant que les erreurs de l'OCR sur une catégorie ne se reproduiraient pas sur une autre catégorie. Il en est de même pour les sauts de lignes, parfois, plusieurs sauts de ligne successifs apparaissaient, pour moi, ils faisaient partie de la structure du document, et devaient être gardé. Cependant, les enlever peut peut-être permettre de créer des sequences nouvelles, plus facilement reconnaissable par notre classifieur.







 
