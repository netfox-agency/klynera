# Klynera · stratégie de référencement
> Établie le 2026-09-23 · skill claude-seo v2.2.0, modèle `local-service`
> Cible : klynera-nettoyage.fr · Le Mans (72000) · vitres, fin de chantier, bureaux

## 1. État de départ (mesuré en production)

| | Klynera |
|---|---|
| Pages indexables | 4 |
| Contenu total | 3 350 mots |
| Mentions d'une ville | **0** |
| `addressLocality` du schema | vide |
| `areaServed` | « France » (interdit pour un SAB depuis juin 2025) |
| Backlinks | 0 |
| Fiche Google Business Profile | inexistante |
| Technique | TTFB 106 ms · 522 Ko · 0 lien cassé · 8/8 alt · 12 schemas |

Le socle technique est excellent. **Tout le déficit est sur la géographie et le volume éditorial.**

## 2. Ce qu'il y a vraiment en page 1 (relevé le 2026-09-23)

Trois familles, deux seulement sont de vrais concurrents.

### a. Les fermes à pages — le gros du bruit
`cleanolia.fr/nos-services/nettoyage-vitres/le-mans/72000`, `nova-clean.fr/.../le-mans-72000`,
`nettoyagevitresarthe.fr`, `grand-nettoyage.fr`, `servicenettoyage.fr`.
Même gabarit publié pour des centaines de communes.

**Page Cleanolia ouverte et mesurée : 300 mots, 0 `<h1>`, 0 `<h2>`, 0 image, 0 schema JSON-LD,
aucun avis, aucun SIRET, aucune adresse.** Elle est en page 1 uniquement par le volume de pages
du domaine. C'est une coquille.

### b. Les annuaires
PagesJaunes (2 positions), StarOfService, TrouverLesBonsFournisseurs. Ils revendent le contact.

### c. Le vrai concurrent : Nova Clean
Page fin de chantier Le Mans mesurée : **2 203 mots, 8 `<h2>`, 16 images, 3 schemas JSON-LD,
avis affichés, SIRET visible.** Bien construit. Son seul angle mort : **aucune adresse de rue
sur la page.**

Autres acteurs locaux réels : TSF Maine, ZS Nettoyage, Franck Nettoyage, Groupe Mirador,
Net Plus, ACL 72, Samsic. Franchises : Maison et Services, ÔDOME.

## 3. L'angle gagnant

On ne bat pas une ferme à pages en publiant plus de pages qu'elle : c'est son terrain, et son
domaine est plus ancien. **On gagne en étant le seul résultat qui prouve.**

Klynera a un atout qu'aucune ferme à pages n'a et que Nova Clean n'affiche pas :
**une adresse réelle au Mans, 40 rue Saint André, et un SIRET public.**

Les quatre leviers, par ordre d'impact :

1. **La géographie** — aujourd'hui absente. C'est le plafond n°1.
2. **La fiche Google Business Profile** — le pack local capte l'essentiel des clics locaux.
   Rappel du modèle : les **horaires d'ouverture sont entrés dans les 5 premiers facteurs de
   classement local** (Whitespark 2026).
3. **La preuve** — adresse, SIRET, avis vérifiables, photos de chantiers réels.
4. **Le volume éditorial** — 29 pages de lieu + 8 pages service + 14 guides.

## 4. Garde-fous appliqués

Le modèle `local-service` du skill impose des seuils. Ils sont respectés :

| Règle | Seuil | Plan |
|---|---|---|
| Pages de lieu | alerte 30 · **arrêt 50** | **16** |
| Page lieu principale | 600 mots, 60 % unique | Le Mans, 900 mots visés |
| Page commune | 500 mots, 40 % unique | 550-650 mots |
| Page service | 800 mots, 100 % unique | 900-1 100 mots |

Deux coupes successives, chacune mesurée :

1. Un premier calcul donnait **61 communes** dans 27 km. Écarté : au-delà de 50 pages de lieu
   on bascule dans le motif reproché aux fermes à pages, et le skill l'interdit.
2. À **28 communes**, l'unicité éditoriale mesurée tombait à **29,8 %**, sous le seuil de 40 %.
   La mesure a été refaite sur des sous-ensembles :

| Communes publiées | Unicité éditoriale | Pages au-dessus du seuil |
|---|---|---|
| 8 | 57,3 % | 8/8 |
| 12 | 45,1 % | 7/12 |
| **14** | **40,3 %** | limite exacte |
| 20 | 35,0 % | 4/20 |
| 28 | 29,8 % | 3/28 |

**Décision : 14 communes publiées**, plus Le Mans et le hub de zone, soit 16 pages de lieu.
Les 14 autres communes restent déclarées dans `areaServed` et listées sur
`/zone-intervention/` sans page dédiée : la zone est couverte, sans contenu creux.

### Le piège à ne pas reproduire
Ajouter un bloc identique sur chaque page de commune en ne changeant que les chiffres **fait
baisser** l'unicité. Chaque page de commune branche son texte sur **quatre axes réels** issus
de `geo.api.gouv.fr` : distance routière depuis Le Mans, population, densité (donc habitat
pavillonnaire ou bourg dense), et appartenance ou non à Le Mans Métropole. Les phrases
diffèrent, pas seulement les noms propres.

## 5. Ce que seul Pascal peut fournir

Le contenu vraiment local ne se génère pas. Quatre questions par zone suffisent à faire passer
une page de « correcte » à « imbattable » :

1. Quels types de bâtiments dominent ici — pavillons, immeubles, zones d'activité, commerces ?
2. Quel problème revient le plus souvent sur ce secteur ?
3. Un chantier précis qu'il y a fait, même sans nommer le client.
4. Un lieu que les gens du coin reconnaissent — une zone commerciale, une rue, un quartier.

À défaut, les pages tiennent debout sur les données publiques, mais restent au niveau de
Nova Clean au lieu de le dépasser.

## 6. Objectifs

| Indicateur | Départ | 3 mois | 6 mois | 12 mois |
|---|---|---|---|---|
| Pages indexées | 4 | 40 | 52 | 52 |
| Requêtes positionnées | ~0 | 80 | 250 | 600 |
| Visites organiques / mois | ~0 | 120 | 450 | 1 200 |
| Demandes de devis / mois | 0 | 4 | 12 | 30 |
| Avis Google | 0 | 10 | 25 | 50 |

Hypothèses : domaine créé en 2026, zéro autorité au départ, GBP créée au mois 1, rythme de
publication tenu. Ce sont des projections, pas des garanties : les positions dépendent
d'algorithmes tiers.

## 7. Préalable bloquant

**Le formulaire de devis ne fonctionne pas** (clé Web3Forms non renseignée) et
**contact@klynera-nettoyage.fr n'existe pas** (aucun MX sur le domaine). Amener du trafic sur
un site dont les deux chemins de contact écrits sont morts revient à financer des prospects
perdus. À régler avant la phase 2.
