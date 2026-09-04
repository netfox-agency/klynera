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
- ⚠️ Placeholders à remplacer avant mise en ligne : domaine (klynera.fr = hypothèse),
  adresse/ville dans le schema LocalBusiness (addressLocality, areaServed).
  Téléphone : fait (06 71 67 16 35, partout + schema).

## Pages métier (SEO/GEO, 2026-08-13)

- `/nettoyage-vitres/`, `/nettoyage-fin-de-chantier/`, `/nettoyage-bureaux/` :
  contenu unique (~700 mots), FAQ propre (5 questions + schema FAQPage), schema Service
  + BreadcrumbList, formulaire prérempli par page, maillage interne croisé
- Accueil : cartes services -> pages métier (lien de couverture) + lien devis conservé (z-index au-dessus)
- Footer (toutes pages) : liens vers les 3 pages métier
- sitemap.xml (4 URLs) et llms.txt (liens + détails) à jour

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
| service-bureaux.webp | 6197108 |
| standards.webp | 37440103 |
