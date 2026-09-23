# Klynera · Site vitrine

One-page statique premium pour Klynera, entreprise de nettoyage spécialisée :
vitrerie, fin de chantier et bureaux.

## Stack

- HTML/CSS/JS statique, zéro dépendance
- Fonts : Instrument Sans + Instrument Serif (Google Fonts)
- Icônes : SVG inline (sprite `<symbol>` en haut du body)
- Formulaire : Web3Forms (clé à renseigner dans `index.html`, champ `access_key`)

## Preview

```bash
python3 -m http.server 4201
```

Ou via `.claude/launch.json` : configuration `klynera` (port 4201).

## Mode capture

`?all` rend tous les `.reveal` visibles sans transition (screenshots outillés).
`&shift=NNN` translate la page vers le haut de NNN px, `&s=<id>` scrolle vers une section.

## SEO (fait, passe claude-seo du 2026-08-13)

- Head complet : canonical, robots, Open Graph + Twitter (og.jpg 1200x630), theme-color, preload hero
- JSON-LD : LocalBusiness (+ OfferCatalog 3 services), WebSite, FAQPage (6 questions, utile citations IA)
- robots.txt (crawlers IA autorisés), sitemap.xml, llms.txt (GEO)
- Images : WebP (1,86 Mo -> 600 Ko), width/height anti-CLS, lazy + decoding async
- <main> landmark, fallback <noscript> (contenu visible sans JS)
- Polices auto-hébergées (assets/fonts/, 4 woff2 latin, 78 Ko, préload des 2 critiques) : zéro requête Google Fonts
- Images responsive : srcset hero 960/1440/1920 + services 600/1200, sizes précis
- Title keyword-first, og:image:alt, skip-link clavier, 404.html, _headers Cloudflare (cache immutable + sécurité)
- Domaine de production : **klynera-nettoyage.fr** (sans www ; www ne résout pas). Téléphone : fait.
- ⚠️ Restent à compléter : ville dans le schema LocalBusiness (addressLocality/areaServed),
  clé Web3Forms, boîte contact@klynera-nettoyage.fr (ou adresse de repli), SIRET des mentions.

## Pages métier (SEO/GEO, 2026-08-13)

- `/nettoyage-vitres/`, `/nettoyage-fin-de-chantier/`, `/nettoyage-bureaux/` :
  contenu unique (~700 mots), FAQ propre (5 questions + schema FAQPage), schema Service
  + BreadcrumbList, formulaire prérempli par page, maillage interne croisé
- Accueil : cartes services -> pages métier (lien de couverture) + lien devis conservé (z-index au-dessus)
- Footer (toutes pages) : liens vers les 3 pages métier
- sitemap.xml (4 URLs) et llms.txt (liens + détails) à jour


## Pages métier : rythme éditorial (2026-09-15)

Le corps des 3 pages n'est plus un bloc de prose unique. Il suit le même rythme de
surfaces que l'accueil :

| Surface | Section | Traitement |
|---|---|---|
| **encre** | `.svc-hero` | hero court (62svh) : photo en saignée à droite, texte sur encre |
| **blanc** | Périmètre | `.lp-scope` : checklist 2 colonnes, pastilles `.icbox` |
| **encre sombre** | Déroulé | `.lp-steps` : numéros serif italique azur clair, 2 colonnes |
| papier | Méthode + Budget | `.lp-cols` : prose 1,1fr + `.lp-price` (carte blanche sticky, CTA devis) |
| papier | Témoignage | `.lp-quote` : citation serif pleine largeur, attribution à droite |
| papier | FAQ | `<details>` inchangés |
| blanc | Devis | formulaire inchangé |

Le contenu SEO est repris **au mot près** : aucun h2, aucune phrase, aucun lien interne
n'a été réécrit. Seule la mise en forme change.

### Hero de page métier (`.svc-hero`)

Bande pleine largeur, `min-height: clamp(470px, 62svh, 615px)` — la moitié de l'accueil.
Fond `--ink`, photo du métier en saignée sur les 56 % de droite, texte dans la zone encre.

Pourquoi pas une photo plein cadre avec texte blanc dessus, comme l'accueil : les trois
photos métier ont été mesurées (luminance par blocs sur le cadrage hero). `ph-chantier`
est entre 150 et 241 partout, `ph-bureaux` est tacheté (48 à 176) : aucune zone sombre
où poser du texte blanc. Il aurait fallu un voile global sur la photo, motif rejeté.
Le fond encre donne un contraste parfait sans jamais assombrir l'image.

Seuls des **fondus d'arête** touchent la photo : haut (160 px, pour la nav) et gauche
(vers l'encre, ramp resserrée 17 % → 63 % pour éviter le voile laiteux sur photo claire).
Le sujet reste en pleine lumière à droite. `object-position` réglé par page pour amener
le sujet dans la zone claire : vitres `62% 45%`, chantier `22% 58%`, bureaux `72% 50%`.

Mobile (< 900 px) : la bande se déplie — photo en haut (34svh) puis panneau encre en
dessous, fondu bas vers l'encre, plus un fondu haut pour la nav. Aucune superposition.

`app.js` : le sélecteur du hero devient `.hero, .svc-hero`, donc la nav redevient
transparente en haut de page puis pleine à 40 px, comme sur l'accueil.

Ajouts CSS : `.lp-scope`, `.lp-steps`, `.lp-step`, `.lp-step-n`, `.lp-cols`, `.lp-price`,
`.lp-quote`, `.prose a` (les liens internes n'avaient aucun style : invisibles).

## Typographie française (2026-09-15)

Passe sur les 5 pages, hors `<script>` et `<style>` :
espaces fines insécables (U+202F) avant `: ; ? !` et à l'intérieur des guillemets,
apostrophes courbes (’). 117 espaces fines, 109 apostrophes.

## Traçabilité & mesure de rentabilité (2026-08-17)

- **Source de chaque lead** : utm_source/medium/campaign, gclid, referrer, page d'entrée et
  1re visite capturés à l'arrivée (localStorage, dernier levier identifié gagne) et injectés
  dans chaque envoi Web3Forms → l'email du lead contient sa provenance. Les événements
  dataLayer (`generate_lead`, `phone_click`) portent la même source.
- **tracking/gtm-conteneur-klynera.json** : conteneur GTM prêt à importer (Admin > Importer) :
  variables dataLayer, déclencheurs et tags GA4 pour les 3 événements. ⚠️ Remplacer la
  constante `GA4 ID` (G-XXXXXXXXXX) et l'ID GTM dans index.html.
- **tracking/suivi-leads-klynera.xlsx** : onglet Leads (1 ligne par demande, exemple en ligne 2)
  + onglet Rentabilité (dépense pub et marge à saisir → CPL, coût/chantier, closing, CA, ROAS,
  profit, détail par prestation). À dupliquer dans Google Sheets pour le partager au client.
- **Suivi d'appels** : clics tél trackés côté site ; les appels réels = numéro de transfert
  Google (à activer avec la campagne Ads) ou numéro dédié.

## Reste à faire

- Clé Web3Forms réelle (`VOTRE_CLE_WEB3FORMS`)
- Email réel (téléphone OK : 06 71 67 16 35)
- Domaine + hébergement (Cloudflare Pages recommandé)
- Mentions légales

## Crédits photos (Pexels, libres de droits)

| Fichier | Pexels ID |
|---|---|
| hero.webp (recadré 16:9) | 6195105 |
| service-vitres.webp | 31435403 |
| service-chantier.webp | 3616746 |
| service-bureaux.webp | 9300768 |
| standards.webp | 37440103 |

## Référencement local : phase 1 (2026-09-23)

Plan complet dans `seo/` : `SEO-STRATEGY.md` (analyse SERP réelle + stratégie),
`SITE-STRUCTURE.md` (les 52 pages cibles), `communes.json` (28 communes retenues).

Phase 1 exécutée — injection géographique :
- Schema `LocalBusiness` : `streetAddress` 40 rue Saint André, `addressLocality` Le Mans,
  `postalCode` 72000, `geo` 47.9819/0.1957, `openingHoursSpecification`, `identifier` SIREN.
- `areaServed` : **29 villes** au lieu de « France » (interdit pour un SAB depuis juin 2025).
- Schemas `Service` des 3 pages métier : `areaServed` + `provider` vers le `@id` du business.
- Titles et meta descriptions géolocalisés, 42-60 car. / 137-142 car.
- H1 des 3 pages métier : « … au Mans ».
- NAP visible (adresse, téléphone, horaires) en pied de page sur les 5 pages → `.footer-nap`.
- `llms.txt` : zone d'intervention et NAP.
- Mentions légales : SIREN, TVA, adresse, directeur de publication (placeholders supprimés)
  + passage typographique FR qui les avait oubliées.

⚠️ Seuil du modèle `local-service` : alerte à 30 pages de lieu, **arrêt à 50**.
Un premier calcul donnait 61 communes dans 27 km : écarté, on reste à 29.

## Référencement local : phase 2 (2026-09-23)

16 pages de lieu créées : `/zone-intervention/` (hub, 28 communes listées),
`/nettoyage-le-mans/` (page principale) et 14 pages de commune.

Générateurs reproductibles : `seo/build-lieux.py` et `seo/build-zone.py`.
Données : `seo/communes.json` (14 publiées) et `seo/communes-zone.json` (28 déclarées),
issues de `geo.api.gouv.fr` — population, superficie, densité, code postal,
intercommunalité, distance et orientation réelles depuis Le Mans.

### Pourquoi 14 communes et pas 28

Le texte se branche sur cinq axes (distance, densité, population, intercommunalité,
orientation) avec des paragraphes composés de clauses indépendantes. Malgré ça,
l'unicité éditoriale mesurée sur 28 pages plafonnait à **29,8 %**, sous le seuil de 40 %
du modèle `local-service`. Mesure par sous-ensembles : 8 → 57,3 %, 12 → 45,1 %,
**14 → 40,3 %**, 20 → 35,0 %, 28 → 29,8 %.

Publier 28 pages aurait reproduit exactement le défaut des fermes à pages qu'on veut battre.

⚠️ **Mesurer l'unicité sur les blocs éditoriaux uniquement** (lede, étapes, prose, repères,
FAQ). Mesurée sur tout le `<main>`, elle inclut le formulaire et le pied de page, communs
par nature, et donne un chiffre faussement alarmant.

Pour dépasser 14 communes, il faut du contenu que seul le client peut fournir :
type de bâti dominant, problème récurrent du secteur, un chantier précis, un lieu reconnaissable.

## Référencement local : phases 3 et 4 (2026-09-23)

**37 URLs indexables**, 109 schemas JSON-LD valides, 0 lien interne cassé.

| Bloc | Pages | Générateur |
|---|---|---|
| Accueil + 3 pages service | 4 | — |
| Lieux : hub, Le Mans, 14 communes | 16 | `seo/build-lieux.py`, `seo/build-zone.py` |
| Guides : hub + 14 articles | 15 | `seo/build-guides.py` + `seo/guides.py` |
| Preuve : à propos, tarifs | 2 | `seo/build-pages.py` |

Les 14 guides sont **écrits à la main**, pas générés : 10 722 mots, unicité de 100 %.
Chacun ouvre sur un chapô qui répond directement à la question posée — c'est le format
que les moteurs IA citent — puis 4 à 5 sections et 3 questions fréquentes en `FAQPage`.

### Ce qui a été volontairement écarté

- **`/avis/`** : aucun avis client réel. Publier des témoignages inventés avec un schema
  `AggregateRating` est une fabrication de preuve, et Google sanctionne le faux balisage
  d'avis. La page se fera quand la fiche Google Business Profile existera.
- **`/realisations/`** : aucune photo de chantier réel. Des images de banque présentées
  comme des réalisations seraient un faux.
- **Pages service supplémentaires** (vitrines, véranda, après-déménagement) : les guides
  couvrent déjà ces requêtes avec des URLs dédiées. Ajouter des pages service quasi
  identiques cannibaliserait `/nettoyage-vitres/` et `/nettoyage-fin-de-chantier/`.

### Règle tenue sur tout le contenu

Aucun prix, aucun délai chiffré et aucune référence client ne sont inventés.
`/tarifs/` explique ce qui fait varier un devis sans afficher le moindre montant.
