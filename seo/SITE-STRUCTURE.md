# Klynera · architecture du site

52 pages au total. Existant : 6. À produire : 46.

## Pilier 1 · Services (8 pages, 900-1 100 mots, 100 % unique)

| URL | Requête principale | État |
|---|---|---|
| `/nettoyage-vitres/` | nettoyage de vitres Le Mans | existe, à géolocaliser |
| `/nettoyage-fin-de-chantier/` | nettoyage fin de chantier Le Mans | existe, à géolocaliser |
| `/nettoyage-bureaux/` | nettoyage de bureaux Le Mans | existe, à géolocaliser |
| `/nettoyage-vitrines-commerce/` | nettoyage vitrine commerce Le Mans | à créer |
| `/nettoyage-veranda-verriere/` | nettoyage véranda Le Mans | à créer |
| `/nettoyage-apres-demenagement/` | nettoyage après déménagement Le Mans | à créer |
| `/remise-en-etat-logement/` | remise en état appartement Le Mans | à créer |
| `/nettoyage-parties-communes/` | nettoyage copropriété Le Mans | **à confirmer avec Pascal** |

Les trois dernières lignes supposent que Pascal accepte ces chantiers. À valider avant écriture :
on n'annonce pas une prestation qu'il ne fait pas.

## Pilier 2 · Lieux (29 pages)

`/zone-intervention/` — hub, liste les 28 communes, carte, schema `ServiceArea`.
`/nettoyage-le-mans/` — page de lieu principale, 900 mots, 60 % unique minimum.

### Tier A — Le Mans Métropole, moins de 10 km (17 pages, 550-650 mots)

| URL | Commune | Habitants | Distance | Densité |
|---|---|---|---|---|
| `/nettoyage-allonnes/` | Allonnes | 10 739 | 4.6 km | 590 |
| `/nettoyage-coulaines/` | Coulaines | 8 121 | 6.0 km | 2049 |
| `/nettoyage-change/` | Changé | 6 911 | 7.5 km | 196 |
| `/nettoyage-arnage/` | Arnage | 5 445 | 5.7 km | 502 |
| `/nettoyage-mulsanne/` | Mulsanne | 5 244 | 7.9 km | 342 |
| `/nettoyage-yvre-l-eveque/` | Yvré-l'Évêque | 4 181 | 8.3 km | 151 |
| `/nettoyage-sarge-les-le-mans/` | Sargé-lès-le-Mans | 3 851 | 7.6 km | 276 |
| `/nettoyage-monce-en-belin/` | Moncé-en-Belin | 3 697 | 9.5 km | 210 |
| `/nettoyage-ruaudin/` | Ruaudin | 3 481 | 6.7 km | 251 |
| `/nettoyage-spay/` | Spay | 2 808 | 7.5 km | 199 |
| `/nettoyage-saint-saturnin/` | Saint-Saturnin | 2 774 | 8.9 km | 286 |
| `/nettoyage-rouillon/` | Rouillon | 2 382 | 4.4 km | 258 |
| `/nettoyage-saint-georges-du-bois/` | Saint-Georges-du-Bois | 2 285 | 7.0 km | 314 |
| `/nettoyage-la-chapelle-saint-aubin/` | La Chapelle-Saint-Aubin | 2 256 | 6.5 km | 376 |
| `/nettoyage-saint-pavace/` | Saint-Pavace | 2 007 | 6.5 km | 387 |
| `/nettoyage-etival-les-le-mans/` | Étival-lès-le-Mans | 1 826 | 8.9 km | 177 |
| `/nettoyage-trange/` | Trangé | 1 637 | 8.2 km | 146 |

### Tier B — 10 à 20 km (11 pages, 500-550 mots)

| URL | Commune | Habitants | Distance | Densité |
|---|---|---|---|---|
| `/nettoyage-parigne-l-eveque/` | Parigné-l'Évêque | 5 358 | 14.0 km | 84 |
| `/nettoyage-ecommoy/` | Écommoy | 4 868 | 18.9 km | 170 |
| `/nettoyage-la-suze-sur-sarthe/` | La Suze-sur-Sarthe | 4 693 | 17.3 km | 218 |
| `/nettoyage-laigne-saint-gervais/` | Laigné-Saint-Gervais | 4 252 | 12.7 km | 190 |
| `/nettoyage-savigne-l-eveque/` | Savigné-l'Évêque | 4 031 | 13.0 km | 142 |
| `/nettoyage-la-bazoge/` | La Bazoge | 3 796 | 13.8 km | 165 |
| `/nettoyage-champagne/` | Champagné | 3 666 | 11.1 km | 262 |
| `/nettoyage-cerans-foulletourte/` | Cérans-Foulletourte | 3 341 | 18.9 km | 103 |
| `/nettoyage-guecelard/` | Guécélard | 3 202 | 11.5 km | 263 |
| `/nettoyage-teloche/` | Teloché | 3 067 | 12.0 km | 134 |
| `/nettoyage-montfort-le-gesnois/` | Montfort-le-Gesnois | 2 939 | 17.3 km | 156 |

**Pas de matrice service × ville.** 3 services × 28 communes = 84 pages : au-delà du seuil
d'arrêt, et c'est précisément le gabarit dupliqué des fermes à pages. Chaque page de commune
traite les trois métiers dans un texte unique.

## Pilier 3 · Preuve E-E-A-T (4 pages)

| URL | Rôle |
|---|---|
| `/a-propos/` | Pascal, son parcours, l'adresse réelle, le SIRET. Schema `Person` + `Organization` |
| `/realisations/` | chantiers photographiés, avant/après. Schema `ImageObject` |
| `/avis/` | avis Google repris. Schema `Review` + `AggregateRating` |
| `/tarifs/` | **ce qui fait varier un prix**, sans aucun chiffre inventé. Devis gratuit |

## Pilier 4 · Guides (14 articles, 800-1 200 mots)

Requêtes informationnelles, longue traîne, et matière à citation pour les moteurs IA.

1. À quelle fréquence faire nettoyer les vitres d'un commerce
2. Nettoyage de vitres sans trace : la méthode des professionnels
3. Que comprend exactement un nettoyage de fin de chantier
4. Combien de temps après les travaux faire intervenir un nettoyeur
5. Voile de ciment sur un carrelage neuf : comment on le retire
6. Nettoyage de bureaux : passage en journée ou hors horaires
7. Quelle fréquence d'entretien pour des bureaux selon l'effectif
8. Crédit d'impôt et nettoyage à domicile : ce qui est éligible
9. Nettoyage de véranda : pourquoi la toiture compte plus que les parois
10. Remise en état avant état des lieux : la check-list
11. Entreprise de nettoyage au Mans : comment choisir
12. Nettoyage après sinistre : les premières 48 heures
13. Produits et matériel du lavage de vitres professionnel
14. Nettoyage de fin de chantier : qui paie, le promoteur ou l'artisan

## Maillage interne

- Chaque page de commune → les 3 pages service + `/zone-intervention/` + les 2 communes limitrophes
- Chaque page service → `/nettoyage-le-mans/` + 3 guides du même thème
- Chaque guide → la page service correspondante (ancre exacte)
- `/zone-intervention/` → les 28 communes
- Accueil → les 8 services + `/nettoyage-le-mans/` + `/avis/`

## Schemas par type de page

| Type | Schemas |
|---|---|
| Accueil | `LocalBusiness` + `Organization` + `WebSite` + `FAQPage` |
| Service | `Service` + `BreadcrumbList` + `FAQPage` |
| Lieu | `LocalBusiness` avec `geo` + `areaServed` + `BreadcrumbList` |
| Guide | `Article` + `BreadcrumbList` + `FAQPage` |
| Avis | `LocalBusiness` + `AggregateRating` |
