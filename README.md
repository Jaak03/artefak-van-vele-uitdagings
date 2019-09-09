# artefak-van-vele-uitdaging
My artefak om skrywers vir hangeskrewe dokumente te identifiseer.

<h2>Mikpunt:</h2>
Die cutting edge op die oomblik is 'n akkuraatheid van 98% se kant vir 100 skrywers deur 'n CNN te gebruik. Wat ek hier mik voor is om soortgelyke of beter akkuraatheid te kry deur die CNN met addisionele data te help. Uiteindelik sal die akkuraatheid moet beter, of die metode sal heelwat vinniger as die voriges moet uitvoer, om dit as nuwe kennis te klassifiseer.

<h2>Komponente:</h2>
Ek gaan die neurale netwerke deel oorwegend in die Colab omgewing met Jupyter notebooks doen. Die ekstra features wat ek beoog om ook in die netwerk in te lees gaan ek op die drive skep en dit dan in die Colab omgewing inlaai.

root.py:
- Probeer om die file so klein as moontlik te hou. Sy werk is maar net om die ander scripts te koordineer.

base/c_output.py
- Maak die outputs bietjie meer kleurvol dat dit kan uitstaan in die console. Die kleure is:
  - Pers -> comments
  - Groen -> state boodskappe
  - Geel -> warnings
  - Rooi -> foutboodskappe
