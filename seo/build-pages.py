#!/usr/bin/env python3
"""Pages /a-propos/ et /tarifs/."""
import json, os, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bg", os.path.join(D, "build-guides.py"))
bg = importlib.util.module_from_spec(spec); spec.loader.exec_module(bg)
bl, BASE, NB, typo = bg.bl, bg.BASE, bg.NB, bg.typo
RACINE, form = bl.RACINE, bg.form


def ld(*o):
    return "\n".join('<script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=2) + '\n</script>' for x in o)


def fil(*e):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(e)]}


def faq_bloc(q):
    return "\n".join(f'''    <details class="faq-item reveal">
      <summary><span>{typo(a)}</span><span class="faq-plus" aria-hidden="true">+</span></summary>
      <div class="faq-body"><p>{typo(b)}</p></div>
    </details>''' for a, b in q)


def ecrire(slug, url, titre, desc, schemas, corps):
    d = os.path.join(RACINE, slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
        bg.enveloppe(url, typo(titre), typo(desc), ld(*schemas), corps))


def a_propos():
    url = BASE + "/a-propos/"
    q = [("Depuis quand Klynera existe-t-elle ?",
          "L’entreprise est immatriculée sous le SIREN 852 054 519, consultable publiquement sur l’annuaire des entreprises. Vous y trouverez la date de création, la forme juridique et l’activité déclarée."),
         ("Êtes-vous assuré ?",
          "Oui, en responsabilité civile professionnelle. L’attestation est fournie sur simple demande, avant toute intervention. C’est ce qui couvre une vitre cassée ou un sol abîmé pendant un chantier."),
         ("Sous-traitez-vous les interventions ?",
          "Non. La personne qui établit le devis est celle qui intervient. C’est ce qui permet de revenir si un détail ne convient pas, et c’est aussi pourquoi nous avons une zone d’intervention limitée à 25 km."),
         ("Travaillez-vous pour les particuliers et les professionnels ?",
          "Les deux, sans distinction de traitement. Les particuliers représentent surtout la vitrerie et les remises en état ; les professionnels, les vitrines, les bureaux et les livraisons de chantier.")]
    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><span>À propos</span></nav>
      <h1>Une entreprise du Mans, <em>avec une adresse.</em></h1>
      <p class="lp-lede">{typo("Klynera est installée 40 rue Saint André, 72000 Le Mans. SIREN 852 054 519, consultable publiquement. Pas de plateforme, pas d’intermédiaire : vous savez qui vient chez vous.")}</p>
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
      <p class="eyebrow">Identité</p>
      <h2 class="section-title">Ce qui est vérifiable</h2>
      <p class="section-lede">{typo("La plupart des sites de nettoyage n’affichent ni adresse, ni numéro d’entreprise. Voici les nôtres, pour que vous puissiez les contrôler avant de nous appeler.")}</p>
    </header>
    <dl class="loc-reperes reveal">
      <div class="loc-repere"><dt>Raison sociale</dt><dd style="font-size:1rem">Klynera<small>Entreprise individuelle · Pascal Negro</small></dd></div>
      <div class="loc-repere"><dt>SIREN</dt><dd style="font-size:1rem">852 054 519<small>TVA FR72852054519</small></dd></div>
      <div class="loc-repere"><dt>Adresse</dt><dd style="font-size:1rem">40 rue Saint André<small>72000 Le Mans</small></dd></div>
      <div class="loc-repere"><dt>Téléphone</dt><dd style="font-size:1rem">06 71 67 16 35<small>Lun-ven 8 h-18 h · sam 9 h-12 h</small></dd></div>
    </dl>
  </div>
</section>

<section class="section-full section-dark">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Notre façon de travailler</p>
      <h2 class="section-title">Quatre engagements, <em>tenus ou rien</em></h2>
    </header>
    <div class="lp-steps">
      <div class="lp-step reveal"><span class="lp-step-n">01</span><div><h3>Le devis ne bouge pas</h3><p>{typo("Ce qui est chiffré est ce qui est facturé. Si un imprévu apparaît en cours de chantier, nous vous appelons avant d’engager quoi que ce soit, jamais après.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">02</span><div><h3>Aucune sous-traitance</h3><p>{typo("La personne qui vient est celle qui a vu les lieux. C’est plus lent à l’échelle d’une entreprise, c’est la seule façon de répondre de son travail.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">03</span><div><h3>On revient si ça ne va pas</h3><p>{typo("Un détail oublié, une trace au contre-jour : on repasse. C’est possible parce que la zone d’intervention est limitée à 25 km, et c’est la raison principale de cette limite.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">04</span><div><h3>On dit non quand il faut</h3><p>{typo("Un chantier hors de notre zone, une prestation que nous ne maîtrisons pas, un délai intenable : nous le disons. Un client mal servi coûte plus cher qu’un chantier refusé.")}</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="lp-cols">
    <div class="prose reveal">
      <h2>Trois métiers, pas dix</h2>
      <p>Klynera fait du <a href="/nettoyage-vitres/">nettoyage de vitres</a>, du <a href="/nettoyage-fin-de-chantier/">nettoyage de fin de chantier</a> et de l’<a href="/nettoyage-bureaux/">entretien de bureaux</a>. C’est tout, et c’est volontaire. Une entreprise qui annonce quinze prestations en fait correctement trois ou quatre ; les autres sont sous-traitées ou improvisées.</p>
      <p>Ces trois métiers partagent la même exigence de finition et le même matériel de base, ce qui permet de les tenir sérieusement. Pour tout le reste — désinsectisation, débarras, entretien d’espaces verts, remise en état après sinistre — nous vous orientons vers quelqu’un dont c’est le métier.</p>
      <h2>Pourquoi 25 kilomètres</h2>
      <p>Notre <a href="/zone-intervention/">zone d’intervention</a> s’arrête à environ 25 km du Mans. Ce n’est pas un manque d’ambition : c’est la distance au-delà de laquelle nous ne pouvons plus garantir ce qui fait notre intérêt — venir vite, revenir si besoin, et ne pas répercuter le trajet sur le devis.</p>
      <p>Beaucoup de sites annoncent couvrir un département entier ou la France. C’est efficace pour le référencement et vide de sens pour un client : personne ne fait quatre-vingt-dix kilomètres pour laver une vitrine. Nous préférons une zone honnête et tenue.</p>
      <h2>Ce que nous ne faisons pas</h2>
      <p>Nous ne donnons pas de prix au mètre carré avant d’avoir vu les lieux, parce qu’un chiffre annoncé à l’aveugle finit toujours par être corrigé, ou par produire un travail bâclé pour le tenir. Nous ne proposons pas de contrat à durée minimale imposée. Et nous n’affichons pas de témoignages que nous ne pourrions pas rattacher à un client réel.</p>
    </div>
    <aside class="lp-price reveal">
      <p class="eyebrow">Vérifier</p>
      <h2>Contrôlez-nous</h2>
      <p>{typo("Le SIREN 852 054 519 se vérifie en trente secondes sur l’annuaire des entreprises. L’attestation de responsabilité civile professionnelle est fournie sur demande, avant l’intervention. C’est le minimum à exiger de n’importe quel prestataire, nous compris.")}</p>
      <a class="btn btn-primary" href="/guides/choisir-entreprise-nettoyage-le-mans/">Comment choisir un prestataire</a>
    </aside>
  </div>
</section>

<section class="section" id="faq-page" style="padding-top:0">
  <header class="section-head reveal">
    <p class="eyebrow">Questions fréquentes</p>
    <h2 class="section-title">Ce qu’on nous demande <em>avant de signer</em></h2>
  </header>
  <div class="faq">
{faq_bloc(q)}
  </div>
</section>

{form}

</main>'''
    ecrire("a-propos", url, "À propos · Klynera, entreprise de nettoyage au Mans",
           "Klynera, entreprise de nettoyage au Mans : adresse réelle 40 rue Saint André, SIREN 852 054 519, assurance RC Pro. Trois métiers, aucune sous-traitance.",
           [{"@context": "https://schema.org", "@type": "AboutPage", "url": url,
             "mainEntity": {"@id": BASE + "/#business"}},
            fil(("Accueil", BASE + "/"), ("À propos", url)),
            {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": typo(a),
                             "acceptedAnswer": {"@type": "Answer", "text": typo(b)}} for a, b in q]}],
           corps)


def tarifs():
    url = BASE + "/tarifs/"
    q = [("Pourquoi n’affichez-vous pas de prix ?",
          "Parce qu’un prix affiché sans avoir vu les lieux est un prix qu’il faudra corriger. Sur du vitrage, l’accès et l’état initial font varier le temps de travail du simple au double. Nous préférons un devis exact sous 24 h à un tarif d’appel révisé ensuite."),
         ("Le devis est-il payant ?",
          "Non, et la visite préalable non plus. Elle est sans engagement, et elle permet de chiffrer précisément plutôt qu’au jugé."),
         ("Y a-t-il un montant minimum d’intervention ?",
          "Sur Le Mans et la première couronne, non : la proximité permet d’accepter une intervention courte. Sur les communes les plus éloignées, nous groupons les chantiers plutôt que d’imposer un minimum."),
         ("Facturez-vous les déplacements ?",
          "Non. Le trajet est absorbé par notre organisation : nous regroupons les interventions par secteur. Il n’y a pas de ligne « déplacement » sur nos devis."),
         ("Le tarif baisse-t-il avec la fréquence ?",
          "Oui, et pour une raison mécanique : un vitrage ou un local entretenu se nettoie plus vite qu’un local laissé six mois. Le temps passé baisse, le tarif par passage suit.")]

    corps = f'''<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><span>Tarifs</span></nav>
      <h1>Ce qui fait le prix, <em>et pourquoi on ne l’affiche pas.</em></h1>
      <p class="lp-lede">{typo("Nous ne publions pas de tarif au mètre carré. Pas par opacité : parce qu’un chiffre donné sans avoir vu les lieux est un chiffre qu’il faut corriger ensuite. Voici en revanche exactement ce qui fait varier un devis.")}</p>
      <div class="lp-ctas">
        <a class="btn btn-primary" href="#devis">Demander un devis gratuit</a>
        <a class="lp-phone" href="tel:+33671671635"><svg class="ico"><use href="#i-phone"/></svg>06 71 67 16 35</a>
      </div>
    </div>
  </div>
</header>

<main id="contenu">

<section class="section-full section-white">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Les quatre critères</p>
      <h2 class="section-title">Ce qui fait varier un devis</h2>
    </header>
    <ul class="lp-scope reveal">
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>La surface réelle.</strong> Une fenêtre a deux faces, une baie à deux vantaux en a quatre, une véranda ajoute sa toiture. On compte des surfaces à traiter, pas des ouvertures.</span></li>
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>L’accès.</strong> Plain-pied, perche télescopique, échafaudage ou nacelle : c’est le critère qui pèse le plus. À surface égale, il peut doubler le temps de travail.</span></li>
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>L’état initial.</strong> Un vitrage entretenu se lave, un vitrage laissé des années se décape. Le premier passage sur un local négligé coûte plus cher que les suivants.</span></li>
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>La fréquence.</strong> Le tarif par passage baisse avec la régularité, parce qu’un local entretenu se nettoie plus vite et qu’un passage récurrent se cale sur une tournée existante.</span></li>
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>Les postes techniques.</strong> Voile de ciment, traces de peinture, silicone, adhésifs : ce sont des remises en état, pas du nettoyage courant. Ils apparaissent en ligne distincte.</span></li>
      <li><span class="icbox"><svg class="ico"><use href="#i-check"/></svg></span><span><strong>Le créneau.</strong> Le samedi se pratique sans majoration. Le dimanche et les jours fériés relèvent d’une majoration légale, et se réservent aux cas sans autre créneau.</span></li>
    </ul>
  </div>
</section>

<section class="section-full section-dark">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Toujours inclus</p>
      <h2 class="section-title">Ce qui ne se facture jamais en plus</h2>
    </header>
    <div class="lp-steps">
      <div class="lp-step reveal"><span class="lp-step-n">01</span><div><h3>Le déplacement</h3><p>{typo("Aucune ligne « déplacement » sur nos devis, sur l’ensemble de la zone d’intervention. Nous groupons les chantiers par secteur plutôt que de répercuter le trajet.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">02</span><div><h3>Le devis et la visite</h3><p>{typo("Gratuits et sans engagement. La visite est ce qui permet de chiffrer juste : la refuser reviendrait à deviner.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">03</span><div><h3>Les produits et le matériel</h3><p>{typo("Fournis. Les consommables sanitaires dans un contrat d’entretien font l’objet d’une ligne distincte, annoncée à l’avance.")}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">04</span><div><h3>La reprise</h3><p>{typo("Si un détail ne va pas, nous repassons. Ce n’est pas un geste commercial, c’est la contrepartie d’une zone d’intervention limitée à 25 km.")}</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="lp-cols">
    <div class="prose reveal">
      <h2>Ponctuel ou contrat régulier</h2>
      <p>Les deux existent et ne répondent pas au même besoin. Le ponctuel traite un événement : une fin de travaux, une réouverture, un état des lieux, une remise de clés. Le régulier maintient un niveau dans le temps.</p>
      <p>Le calcul à faire n’est pas le prix d’un passage mais le coût sur l’année. Pour un commerce, douze passages mensuels reviennent souvent moins cher que quatre grosses remises en état — avec une vitrine présentable en permanence plutôt que quatre fois par an. Le détail est dans le guide sur <a href="/guides/prix-nettoyage-de-vitres-ce-qui-varie/">ce qui fait varier le prix d’un nettoyage de vitres</a>.</p>
      <h2>Comment lire un devis de nettoyage</h2>
      <p>Un devis utile détaille les postes : surfaces concernées, fréquence, ce qui est inclus et ce qui ne l’est pas. Un forfait global sans détail rend impossible toute discussion le jour où le résultat ne correspond pas à l’attente.</p>
      <p>Si vous comparez plusieurs devis, comparez d’abord les périmètres. Un écart important sur un même périmètre annoncé signifie presque toujours que le périmètre n’est pas le même — vitrages en hauteur exclus, sanitaires non repris, consommables en supplément.</p>
      <h2>Nos devis</h2>
      <p>Gratuits, détaillés poste par poste, envoyés sous 24 h. Ce qui est chiffré est ce qui est facturé : en cas d’imprévu en cours de chantier, nous appelons avant d’engager quoi que ce soit. Et il n’y a pas de durée minimale imposée sur un contrat d’entretien.</p>
    </div>
    <aside class="lp-price reveal">
      <p class="eyebrow">Devis</p>
      <h2>Obtenir un chiffrage</h2>
      <p>{typo("Décrivez votre besoin en quelques lignes : surface approximative, type de local, fréquence souhaitée. Nous rappelons dans la journée et, si le chantier le justifie, nous passons voir les lieux avant de chiffrer.")}</p>
      <a class="btn btn-primary" href="#devis">Demander un devis gratuit</a>
    </aside>
  </div>
</section>

<section class="section" id="faq-page" style="padding-top:0">
  <header class="section-head reveal">
    <p class="eyebrow">Questions fréquentes</p>
    <h2 class="section-title">Sur les prix, <em>franchement</em></h2>
  </header>
  <div class="faq">
{faq_bloc(q)}
  </div>
</section>

{form}

</main>'''
    ecrire("tarifs", url, "Tarifs · ce qui fait le prix d’un nettoyage · Klynera",
           "Ce qui fait varier le prix d’un nettoyage au Mans : surface, accès, état initial, fréquence. Devis gratuit détaillé sous 24 h, sans frais de déplacement.",
           [{"@context": "https://schema.org", "@type": "WebPage", "url": url,
             "about": {"@id": BASE + "/#business"}},
            fil(("Accueil", BASE + "/"), ("Tarifs", url)),
            {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": typo(a),
                             "acceptedAnswer": {"@type": "Answer", "text": typo(b)}} for a, b in q]}],
           corps)


if __name__ == "__main__":
    a_propos(); tarifs()
    print("/a-propos/ et /tarifs/ générées")
