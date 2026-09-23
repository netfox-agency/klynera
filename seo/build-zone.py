#!/usr/bin/env python3
"""Génère /zone-intervention/ et /nettoyage-le-mans/."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
bl = import_module("build-lieux".replace("-", "_")) if False else None

import importlib.util
spec = importlib.util.spec_from_file_location("bl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-lieux.py"))
bl = importlib.util.module_from_spec(spec); spec.loader.exec_module(bl)

RACINE = bl.RACINE
BASE = bl.BASE
NB = bl.NNBSP
typo, slug, fr = bl.typo, bl.slug, bl.fr
PUBLIEES = json.load(open(os.path.join(RACINE, "seo", "communes.json"), encoding="utf-8"))
TOUTES = json.load(open(os.path.join(RACINE, "seo", "communes-zone.json"), encoding="utf-8"))
for c in TOUTES + PUBLIEES:
    c["slug"] = slug(c["nom"]); c["km_route_txt"] = str(int(round(c["km_route"])))
AVEC_PAGE = {c["nom"] for c in PUBLIEES}

sprite, nav, form, footer, scripts, commun = bl.gabarit()


def enveloppe(url, titre, desc, ld, corps):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titre}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a1622">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Klynera">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titre}">
<meta name="twitter:description" content="{desc}">
{commun}
{ld}
</head>
<body class="subpage">
<a class="skip-link" href="#contenu">Aller au contenu</a>

{sprite}

{nav}

{corps}

{footer}

{chr(10).join(scripts)}
</body>
</html>
'''


def ldjson(*objs):
    return "\n".join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>' for o in objs)


def fil(*etapes):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(etapes)]}


# ─────────── /zone-intervention/ ───────────

def zone():
    url = BASE + "/zone-intervention/"
    titre = "Zone d’intervention · Le Mans et la Sarthe · Klynera"
    desc = typo(f"Klynera intervient au Mans et sur {len(TOUTES)} communes de la Sarthe dans un rayon "
                f"de 25{NB}km : nettoyage de vitres, fin de chantier et bureaux. Devis gratuit sous 24{NB}h.")
    pop = 146249 + sum(c["pop"] for c in TOUTES)
    tierA = [c for c in TOUTES if c["tier"] == "A"]
    tierB = [c for c in TOUTES if c["tier"] == "B"]

    def remplir(lst, cols=4):
        n = (-len(lst)) % cols
        return "".join(f'\n      <span class="zone-fill" aria-hidden="true"></span>' for _ in range(n))

    def puce(c):
        n, km = c["nom"], c["km_route_txt"]
        if c["nom"] in AVEC_PAGE:
            return f'      <a href="/nettoyage-{c["slug"]}/">{n} <span>{km}{NB}km</span></a>'
        return f'      <span class="zone-sans">{n} <span>{km}{NB}km</span></span>'

    ld = ldjson(
        {"@context": "https://schema.org", "@type": "Service",
         "name": "Nettoyage au Mans et en Sarthe",
         "provider": {"@id": BASE + "/#business"},
         "url": url, "description": desc,
         "areaServed": [{"@type": "City", "name": "Le Mans"}] +
                       [{"@type": "City", "name": c["nom"],
                         "address": {"@type": "PostalAddress", "addressLocality": c["nom"],
                                     "postalCode": c["cp"], "addressCountry": "FR"}} for c in TOUTES]},
        fil(("Accueil", BASE + "/"), ("Zone d’intervention", url)))

    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><span>Zone d’intervention</span></nav>
      <h1>Où nous intervenons, <em>au Mans et autour.</em></h1>
      <p class="lp-lede">{typo(f"Klynera part du Mans, 40 rue Saint André. Nous couvrons {len(TOUTES)} communes de la Sarthe dans un rayon de 25{NB}km, soit {fr(pop)} habitants. Au-delà, nous le disons plutôt que de promettre une intervention que nous ne tiendrions pas.")}</p>
      <div class="lp-ctas">
        <a class="btn btn-primary" href="#devis">Demander un devis</a>
        <a class="lp-phone" href="tel:+33671671635"><svg class="ico"><use href="#i-phone"/></svg>06 71 67 16 35</a>
      </div>
    </div>
  </div>
</header>

<main id="contenu">

<section class="section-full section-white">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Première couronne</p>
      <h2 class="section-title">Le Mans Métropole, à moins de 10{NB}km</h2>
      <p class="section-lede">{typo(f"Notre secteur quotidien. {len(tierA)} communes, aucune contrainte de planning : un devis se cale dans la semaine, une urgence se trouve souvent dans la journée.")}</p>
    </header>
    <div class="zone-grille reveal">
{chr(10).join(puce(c) for c in tierA)}{remplir(tierA)}
    </div>
  </div>
</section>

<section class="section-full section-dark">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Deuxième couronne</p>
      <h2 class="section-title">De 10 à 25{NB}km du Mans</h2>
      <p class="section-lede">{typo(f"{len(tierB)} communes que nous desservons en groupant les interventions par secteur. Le trajet n’apparaît pas sur le devis : il est absorbé par l’organisation, pas répercuté.")}</p>
    </header>
    <div class="zone-grille reveal">
{chr(10).join(puce(c) for c in tierB)}{remplir(tierB)}
    </div>
  </div>
</section>

<section class="section">
  <div class="lp-cols">
    <div class="prose reveal">
      <h2>Pourquoi une zone, et pas « toute la France »</h2>
      <p>Beaucoup de sites de nettoyage annoncent couvrir un département entier, voire le pays. C’est commode pour le référencement, ça ne veut rien dire pour un client : personne ne fait 90{NB}km pour laver une vitrine. Depuis juin 2025, Google interdit d’ailleurs à une entreprise mobile de déclarer une région ou un pays entier comme zone desservie.</p>
      <p>Notre rayon s’arrête à 25{NB}km parce que c’est la distance au-delà de laquelle nous ne pouvons plus garantir ce qui fait notre intérêt : venir vite, revenir si besoin, et ne pas facturer le trajet. Si vous êtes en dehors, appelez quand même : pour un chantier conséquent ou un contrat régulier, nous nous déplaçons. Pour une vitrine isolée, nous vous dirons franchement qu’un confrère plus proche sera mieux placé.</p>
      <h2>Ce que nous faisons partout dans cette zone</h2>
      <p>Les trois prestations sont disponibles sur l’ensemble du secteur, sans distinction : le <a href="/nettoyage-vitres/">nettoyage de vitres</a> pour les vitrines, baies et vérandas, le <a href="/nettoyage-fin-de-chantier/">nettoyage de fin de chantier</a> après travaux ou avant remise des clés, et le <a href="/nettoyage-bureaux/">nettoyage de bureaux</a> en passage régulier.</p>
    </div>
    <aside class="lp-price reveal">
      <p class="eyebrow">Votre commune</p>
      <h2>Vous n’êtes pas dans la liste ?</h2>
      <p>La liste couvre les communes où nous intervenons le plus souvent. Elle n’est pas fermée : si vous êtes à proximité, appelez, nous vous dirons en une minute si nous pouvons venir et à quelles conditions.</p>
      <a class="btn btn-primary" href="tel:+33671671635">06 71 67 16 35</a>
    </aside>
  </div>
</section>

{form}

</main>'''
    d = os.path.join(RACINE, "zone-intervention"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(enveloppe(url, titre, desc, ld, corps))
    return len(TOUTES)


# ─────────── /nettoyage-le-mans/ ───────────

def le_mans():
    url = BASE + "/nettoyage-le-mans/"
    titre = "Nettoyage au Mans (72000) · vitres, chantier, bureaux · Klynera"
    desc = typo("Entreprise de nettoyage au Mans : vitres, fin de chantier et bureaux. "
                "Adresse réelle 40 rue Saint André, devis gratuit sous 24 h.")
    q = [("Quelle est votre adresse au Mans ?",
          "Klynera est installée 40 rue Saint André, 72000 Le Mans. C’est une adresse réelle, pas une domiciliation : nos véhicules et notre matériel y sont. Le SIREN de l’entreprise est le 852 054 519, vérifiable publiquement."),
         ("Intervenez-vous dans tous les quartiers du Mans ?",
          "Oui, sur l’ensemble de la commune, du centre-ville aux quartiers pavillonnaires en périphérie. Le Mans s’étend sur 53 km² pour 146 249 habitants : nous organisons nos tournées par secteur pour limiter les trajets."),
         ("Travaillez-vous pour les particuliers ou seulement pour les entreprises ?",
          "Les deux. Les particuliers nous appellent surtout pour des vitres, des vérandas et des remises en état après travaux. Les professionnels pour des vitrines, des bureaux et des livraisons de chantier."),
         ("Proposez-vous des interventions hors horaires de bureau ?",
          "Oui, c’est même la règle pour l’entretien de locaux professionnels : nous passons tôt le matin, en soirée ou le week-end pour ne pas gêner votre activité. Nos horaires d’ouverture téléphonique sont du lundi au vendredi de 8 h à 18 h, le samedi de 9 h à 12 h."),
         ("Sous combien de temps peut-on obtenir un devis ?",
          "Sous 24 h. Pour les chantiers qui le justifient, nous nous déplaçons d’abord pour voir les lieux : sur du vitrage, l’accès et l’état initial font varier le temps de travail du simple au double. La visite est gratuite.")]

    ld = ldjson(
        {"@context": "https://schema.org", "@type": "Service",
         "name": "Nettoyage au Mans", "provider": {"@id": BASE + "/#business"}, "url": url,
         "description": desc,
         "areaServed": {"@type": "City", "name": "Le Mans",
                        "address": {"@type": "PostalAddress", "addressLocality": "Le Mans",
                                    "postalCode": "72000", "addressCountry": "FR"}}},
        fil(("Accueil", BASE + "/"), ("Zone d’intervention", BASE + "/zone-intervention/"), ("Le Mans", url)),
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": typo(a),
                         "acceptedAnswer": {"@type": "Answer", "text": typo(b)}} for a, b in q]})

    faq = "\n".join(f'''    <details class="faq-item reveal">
      <summary><span>{typo(a)}</span><span class="faq-plus" aria-hidden="true">+</span></summary>
      <div class="faq-body"><p>{typo(b)}</p></div>
    </details>''' for a, b in q)

    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><a href="/zone-intervention/">Zone d’intervention</a><span>·</span><span>Le Mans</span></nav>
      <h1>Nettoyage au Mans, <em>par une entreprise du Mans.</em></h1>
      <p class="lp-lede">{typo("40 rue Saint André, 72000 Le Mans. Une adresse, un SIREN public, un téléphone qui décroche : vous savez qui vient chez vous. Vitres, fin de chantier et bureaux, pour les particuliers comme pour les professionnels.")}</p>
      <div class="lp-ctas">
        <a class="btn btn-primary" href="#devis">Demander un devis</a>
        <a class="lp-phone" href="tel:+33671671635"><svg class="ico"><use href="#i-phone"/></svg>06 71 67 16 35</a>
      </div>
      <div class="lp-proof">
        <span><svg class="ico"><use href="#i-check"/></svg>Devis gratuit sous 24{NB}h</span>
        <span><svg class="ico"><use href="#i-check"/></svg>SIREN 852 054 519</span>
      </div>
    </div>
  </div>
</header>

<main id="contenu">

<section class="section-full section-white">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Nos prestations</p>
      <h2 class="section-title">Trois métiers, au Mans</h2>
    </header>
    <div class="loc-services">
      <a class="loc-service reveal" href="/nettoyage-vitres/">
        <span class="icbox"><svg class="ico"><use href="#i-vitre"/></svg></span>
        <h3>Nettoyage de vitres</h3>
        <p>{typo("Vitrines du centre-ville, baies vitrées de maisons, verrières et vérandas. En ponctuel ou en contrat régulier, avec un tarif par passage qui baisse à la fréquence.")}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
      <a class="loc-service reveal" href="/nettoyage-fin-de-chantier/">
        <span class="icbox"><svg class="ico"><use href="#i-chantier"/></svg></span>
        <h3>Fin de chantier</h3>
        <p>{typo("Appartements, maisons, plateaux de bureaux et cellules commerciales. Nous intervenons après le dernier corps d’état, avant la pré-visite ou la remise des clés.")}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
      <a class="loc-service reveal" href="/nettoyage-bureaux/">
        <span class="icbox"><svg class="ico"><use href="#i-bureau"/></svg></span>
        <h3>Nettoyage de bureaux</h3>
        <p>{typo("Postes de travail, salles de réunion, sanitaires et parties communes, hors horaires. La même équipe revient sur votre site, elle connaît vos accès.")}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
    </div>
  </div>
</section>

<section class="section-full section-dark">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Le Mans</p>
      <h2 class="section-title">Une ville de 146 249 habitants sur 53 km²</h2>
    </header>
    <div class="lp-steps">
      <div class="lp-step reveal"><span class="lp-step-n">01</span><div><h3>Un centre dense</h3><p>{typo("Le centre-ville et la Cité Plantagenêt concentrent les commerces et le bâti ancien. Vitrines étroites, verre parfois d’origine, accès contraints : on n’y travaille pas comme dans une zone commerciale.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">02</span><div><h3>Des quartiers pavillonnaires</h3><p>{typo("La périphérie mancelle est largement pavillonnaire. Maisons individuelles, vérandas, baies côté jardin : du vitrage accessible de plain-pied, rapide à traiter et simple à chiffrer.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">03</span><div><h3>Des zones d’activité</h3><p>{typo("Les zones d’activité de l’agglomération concentrent bureaux, ateliers et locaux commerciaux. C’est là que l’entretien régulier prend tout son sens : passage fixe, équipe stable, aucune surprise.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">04</span><div><h3>Un chantier permanent</h3><p>{typo("Une ville de cette taille construit et rénove en continu. Les livraisons de chantier y sont notre demande la plus régulière, des promoteurs comme des artisans du bâtiment.")}</p></div></div>
    </div>
    <p class="section-lede reveal" style="margin-top:34px;max-width:900px">{typo("Autour du Mans, nous desservons également 28 communes de la Sarthe. La liste complète est sur la page zone d’intervention.")}</p>
  </div>
</section>

<section class="section">
  <div class="lp-cols">
    <div class="prose reveal">
      <h2>Une entreprise du Mans, pas une plateforme</h2>
      <p>La plupart des sites qui remontent sur « nettoyage Le Mans » ne sont pas des entreprises du Mans. Ce sont des plateformes nationales qui publient la même page pour des centaines de villes et revendent ensuite le contact à un prestataire local, ou des annuaires qui facturent la mise en relation. Rien d’illégal, mais cela veut dire un intermédiaire de plus et personne à rappeler quand ça se passe mal.</p>
      <p>Klynera est au 40 rue Saint André. Le SIREN est public, le numéro de téléphone est celui qui décroche, et la personne qui établit le devis est celle qui vient. C’est aussi ce qui permet de revenir gratuitement si un détail ne vous convient pas, ce qu’aucune plateforme ne peut promettre.</p>
      <h2>Comment se déroule une première demande</h2>
      <p>Vous appelez ou remplissez le formulaire. Nous rappelons dans la journée pour comprendre le besoin : surface, accès, état, fréquence souhaitée. Selon le chantier, nous passons voir les lieux — c’est gratuit et sans engagement. Le devis part sous 24 h, détaillé poste par poste. Il ne bouge pas entre la signature et la facture.</p>
      <h2>Ponctuel ou régulier</h2>
      <p>Les deux existent et ne servent pas la même chose. Le ponctuel répond à un événement : une fin de travaux, une réouverture, un état des lieux. Le régulier maintient un niveau : une vitrine entretenue se nettoie plus vite qu’une vitrine laissée six mois, et le tarif par passage baisse en conséquence. Pour un commerce du centre du Mans, c’est presque toujours le régulier qui revient le moins cher.</p>
    </div>
    <aside class="lp-price reveal">
      <p class="eyebrow">Budget</p>
      <h2>Combien coûte un nettoyage au Mans</h2>
      <p>{typo("Quatre critères font le prix : la surface, l’accès, l’état initial et la fréquence. Nous ne publions pas de tarif au mètre carré, parce qu’un chiffre affiché sans avoir vu les lieux est un chiffre inventé, et qu’il faudrait le corriger ensuite. Le devis est gratuit, détaillé, et envoyé sous 24 h.")}</p>
      <a class="btn btn-primary" href="#devis">Demander un devis gratuit</a>
    </aside>
  </div>
</section>

<section class="section" id="faq-page" style="padding-top:0">
  <header class="section-head reveal">
    <p class="eyebrow">Questions fréquentes</p>
    <h2 class="section-title">Nettoyage au Mans, <em>en pratique</em></h2>
  </header>
  <div class="faq">
{faq}
  </div>
  <div class="reveal">
    <p class="eyebrow" style="margin-top:56px">Autour du Mans</p>
    <div class="loc-voisines">
{chr(10).join(f'      <a href="/nettoyage-{c["slug"]}/">{c["nom"]}</a>' for c in PUBLIEES[:8])}
      <a href="/zone-intervention/">Toute la zone</a>
    </div>
  </div>
</section>

{form}

</main>'''
    d = os.path.join(RACINE, "nettoyage-le-mans"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(enveloppe(url, titre, desc, ld, corps))


if __name__ == "__main__":
    n = zone(); le_mans()
    print(f"/zone-intervention/ ({n} communes listées) et /nettoyage-le-mans/ générées")
