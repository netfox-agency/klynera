#!/usr/bin/env python3
"""Génère les guides et leur hub /guides/."""
import json, os, re, sys, importlib.util

D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bl", os.path.join(D, "build-lieux.py"))
bl = importlib.util.module_from_spec(spec); spec.loader.exec_module(bl)
sys.path.insert(0, D)
from guides import GUIDES

RACINE, BASE, NB, typo = bl.RACINE, bl.BASE, bl.NNBSP, bl.typo
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
<meta property="og:type" content="article">
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


def guide(g):
    sl, titre, h1, desc, chapo, sections, faq, (lien, nom_svc) = g
    url = f"{BASE}/guides/{sl}/"
    t = typo(f"{titre} · Klynera")
    d = typo(desc)

    ld = "\n".join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>' for o in [
        {"@context": "https://schema.org", "@type": "Article", "headline": typo(titre),
         "description": d, "url": url, "inLanguage": "fr-FR",
         "author": {"@id": BASE + "/#business"}, "publisher": {"@id": BASE + "/#business"},
         "datePublished": "2026-09-23", "dateModified": "2026-09-23",
         "image": BASE + "/assets/og.jpg",
         "about": {"@type": "Service", "name": nom_svc},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": typo(titre), "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": typo(q),
             "acceptedAnswer": {"@type": "Answer", "text": typo(a)}} for q, a in faq]}])

    corps_sections = ""
    for h2, paras in sections:
        corps_sections += f"    <h2>{typo(h2)}</h2>\n"
        for p in paras:
            p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
            corps_sections += f"    <p>{typo(p)}</p>\n"

    faq_html = "\n".join(f'''    <details class="faq-item reveal">
      <summary><span>{typo(q)}</span><span class="faq-plus" aria-hidden="true">+</span></summary>
      <div class="faq-body"><p>{typo(a)}</p></div>
    </details>''' for q, a in faq)

    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><a href="/guides/">Guides</a><span>·</span><span>{typo(nom_svc)}</span></nav>
      <h1>{h1}</h1>
    </div>
  </div>
</header>

<main id="contenu">

<article class="article">
  <p class="chapo">{typo(chapo)}</p>
{corps_sections}
  <div class="article-cta">
    <div>
      <h2>Besoin d’un devis ?</h2>
      <p>{typo(f"{nom_svc} au Mans et en Sarthe. Devis gratuit, envoyé sous 24 h.")}</p>
    </div>
    <div class="lp-ctas">
      <a class="btn btn-primary" href="{lien}#devis">Demander un devis</a>
      <a class="lp-phone" href="tel:+33671671635"><svg class="ico"><use href="#i-phone"/></svg>06 71 67 16 35</a>
    </div>
  </div>
</article>

<section class="section" id="faq-page" style="padding-top:0">
  <header class="section-head reveal">
    <p class="eyebrow">Questions fréquentes</p>
    <h2 class="section-title">On nous demande <em>aussi…</em></h2>
  </header>
  <div class="faq">
{faq_html}
  </div>
  <div class="reveal">
    <p class="eyebrow" style="margin-top:56px">À lire aussi</p>
    <div class="loc-voisines">
{chr(10).join(f'      <a href="/guides/{o[0]}/">{typo(o[1])}</a>' for o in GUIDES if o[0] != sl and o[7][0] == lien)}
      <a href="/guides/">Tous les guides</a>
      <a href="{lien}">{typo(nom_svc)}</a>
    </div>
  </div>
</section>

</main>'''
    dd = os.path.join(RACINE, "guides", sl); os.makedirs(dd, exist_ok=True)
    open(os.path.join(dd, "index.html"), "w", encoding="utf-8").write(enveloppe(url, t, d, ld, corps))


def hub():
    url = BASE + "/guides/"
    t = "Guides du nettoyage · vitres, chantier, bureaux · Klynera"
    d = typo(f"{len(GUIDES)} guides pratiques sur le nettoyage de vitres, la fin de chantier et l’entretien de bureaux, écrits par une entreprise du Mans.")
    ld = "\n".join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>' for o in [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Guides du nettoyage",
         "url": url, "description": d, "publisher": {"@id": BASE + "/#business"},
         "hasPart": [{"@type": "Article", "headline": typo(g[1]), "url": f"{BASE}/guides/{g[0]}/"} for g in GUIDES]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": url}]}])

    cartes = "\n".join(f'''      <a class="guide-carte reveal" href="/guides/{g[0]}/">
        <h3>{typo(g[1])}</h3>
        <p>{typo(g[3])}</p>
        <span class="lien">Lire le guide <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>''' for g in GUIDES)

    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><span>Guides</span></nav>
      <h1>Ce qu’on sait faire, <em>expliqué.</em></h1>
      <p class="lp-lede">{typo("Des réponses écrites par des gens qui font le travail : méthodes, fréquences, pièges et ce qui fait varier un prix. Sans jargon et sans chiffre inventé.")}</p>
    </div>
  </div>
</header>

<main id="contenu">
<section class="section-full section-white">
  <div class="section-inner">
    <div class="guides-liste">
{cartes}
    </div>
  </div>
</section>

{form}

</main>'''
    dd = os.path.join(RACINE, "guides"); os.makedirs(dd, exist_ok=True)
    open(os.path.join(dd, "index.html"), "w", encoding="utf-8").write(enveloppe(url, t, d, ld, corps))


if __name__ == "__main__":
    for g in GUIDES:
        guide(g)
    hub()
    print(f"{len(GUIDES)} guides + le hub /guides/ générés")
