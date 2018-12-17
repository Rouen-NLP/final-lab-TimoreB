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

|Categorie|Nombre moyenne de lettre|slt|
|-----------------------------------|------|---|
|  Advertisement |  700 |Séquence de mots paragraphés. ON peut distinguer des phrases par moment.|
|  Email         |  686 |Les séquences reconnus sont de très bonnes qualité. Mots récurrents : From, To, Sent, Date,...|
|  Forms        | 991  |Beaucoup de caractères seuls ou disparates. Peu de mots formés.|
|  lettres      | 1407 |Appréciation d|
|  Mémos         | 1302 |a|
|  Notes         | 250  |a|
|  News          | 3774 |a|
| Report        | 1870 |a|
|  CV            | 2646 |a|
|  Scientique    | 2744 |a|

### Les fichiers textes de l'OCR
Même si il aurait été faisable de travailler sur les fichiers images uniquement, nous sommes en cours de Text Analysis, et une analyse de  fichier texte sera préférable. Bien que cet argument ne soit pas scientifique, il fut pris en compte pour la décision de traiter le texte. 
