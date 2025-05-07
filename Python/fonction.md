L’image montre un **robot parallèle plan à 3 branches**, où chaque branche $A_iB_i$ agit comme un actionneur linéaire (vérin) entre un point fixe $A_i$ et un point mobile $B_i$. L’effecteur est au centre du triangle formé par les $B_i$.

Voici l’interprétation géométrique des **quantités γᵢ, dᵢ, eᵢ** mentionnées dans la figure :

---

### 🔸 **Angles γ₁, γ₂, γ₃** :

Ce sont les **angles d’orientation des glissières $A_iB_i$**, mesurés par rapport à un repère global (souvent l’axe x).

**Formule générale :**

$$
\gamma_i = \text{angle}(B_i - A_i)
= \arctan2(B_{iy} - A_{iy}, B_{ix} - A_{ix})
$$

---

### 🔸 **Distances $d_1, d_2, d_3$** :

Ce sont les **bras de levier** des moments des glisseurs par rapport au centre de l'effecteur (le point au centre du triangle des $B_i$).

**Formule :**

$$
d_i = \vec{r}_i^\perp \cdot \vec{u}_{\gamma_i}
$$

où :

* $\vec{r}_i$ est le vecteur du centre de l’effecteur jusqu’à $B_i$,
* $\vec{u}_{\gamma_i} = [-\sin(\gamma_i), \cos(\gamma_i)]$ est le vecteur **orthogonal** à la direction de $A_iB_i$,
* donc $d_i$ est la distance perpendiculaire du centre de l'effecteur à la droite $A_iB_i$ (positive ou négative selon l’orientation).

---

### 🔸 **Distances $e_1, e_2, e_3$** :

Ce sont les **bras de levier** des moments par rapport aux points $O_i$, les centres des liaisons actives.

**Formule :**

$$
e_i = \left\| \vec{O_iA_i} \times \frac{\vec{A_iB_i}}{\|\vec{A_iB_i}\|} \right\|
$$

Autrement dit, $e_i$ est la distance perpendiculaire entre la liaison active $O_i$ et la glissière $A_iB_i$. On peut aussi l’interpréter comme :

$$
e_i = \text{distance de } O_i \text{ à la droite } A_iB_i
$$

---

### En résumé (formules compactes) :

| Paramètre  | Définition                                                                                |
| ---------- | ----------------------------------------------------------------------------------------- |
| $\gamma_i$ | $\arctan2(B_{iy} - A_{iy}, B_{ix} - A_{ix})$                                              |
| $d_i$      | $\vec{r}_i^\perp \cdot \vec{u}_{\gamma_i}$, ou distance ortho à $A_iB_i$ depuis le centre |
| $e_i$      | Distance perpendiculaire entre $O_i$ et la droite $A_iB_i$                                |

Souhaitez-vous que je vous aide à écrire un code Python pour calculer ces valeurs à partir de coordonnées ?