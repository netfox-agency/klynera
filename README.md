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
