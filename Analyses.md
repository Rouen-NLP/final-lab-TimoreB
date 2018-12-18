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

## Analyse du problème et choix de la solution

Mon problème est un problème de classification de textes. Dans mon cas, chaque document est relié à une situation : Celle d'un procès de l'industrie du tabac. De plus, chaque texte doit correspondre à une catégorie. Ainsi, je crains qu'un classifieur bayesien, dont une des hypothèses est l'indépendance des mots entre eux, ne soit pas performant. Comme ce fut une solution très utilisé, je tiens à quand même la tester, comme élément de comparaison. J'aimerais ensuite essayer une Multi Layer Perceptron Classifier.  Le but va être de déterminer par gridsearch ses paramètres optimaux. 




 
