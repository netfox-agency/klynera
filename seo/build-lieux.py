#!/usr/bin/env python3
"""Génère les pages de lieu de Klynera.

Le texte se BRANCHE sur quatre axes réels (distance routière, population, densité,
intercommunalité) plutôt que de substituer des noms propres dans un gabarit fixe :
un bloc identique partout ferait BAISSER l'unicité, c'est le défaut des fermes à pages.

Usage :  python3 seo/build-lieux.py
"""
import json, os, re, unicodedata, html

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, "nettoyage-vitres", "index.html")
COMMUNES = json.load(open(os.path.join(RACINE, "seo", "communes.json"), encoding="utf-8"))
BASE = "https://klynera-nettoyage.fr"
NNBSP = " "


def slug(nom):
    s = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fr(n):
    return f"{n:,}".replace(",", NNBSP)


def typo(t):
    t = re.sub(r" +([:;?!])", NNBSP + r"\1", t)
    return re.sub(r"(\w)'(\w)", r"\1’\2", t)


# ─────────── Les cinq axes ───────────
# distance · densité · population · intercommunalité · orientation depuis Le Mans
# Trois formulations par cas, choisies par empreinte du nom : deux communes du même
# profil n'écrivent pas la même phrase.

def empreinte(nom, sel):
    return sum(ord(x) for x in nom + sel)


def pick(pool, cle, c, sel=""):
    v = pool[cle]
    return v[empreinte(c["nom"], sel) % len(v)]


def axes(c):
    km = c["km_route"]
    d = "tres_proche" if km < 7 else "proche" if km < 13 else "moyen" if km < 20 else "loin"
    de = c["densite"]
    h = "urbain" if de > 450 else "pavillon_dense" if de > 200 else "pavillon" if de > 120 else "rural"
    p = c["pop"]
    t = "bourg_important" if p > 5000 else "bourg_moyen" if p > 2500 else "petit_bourg"
    return d, h, t, c["epci"] == "CU Le Mans Métropole"


LEDE = {
 "tres_proche": [
  "{n} est à {km}{nb}km de notre atelier du Mans, au {dir} de la ville : nous y passons plusieurs fois par semaine, et une urgence se cale souvent dans la journée.",
  "Il faut moins d’un quart d’heure pour rejoindre {n} depuis Le Mans. Autant dire que nous y sommes chez nous : vitres, fin de chantier et entretien de bureaux, en ponctuel comme en régulier.",
  "Au {dir} du Mans, à {km}{nb}km : {n} fait partie des communes où nous intervenons le plus souvent. Devis rapide, intervention calée sans attendre."],
 "proche": [
  "Depuis Le Mans, {n} est à {km}{nb}km par la route, au {dir} de la ville. Nous y intervenons régulièrement, en passage ponctuel comme en contrat d’entretien.",
  "{n} se situe à {km}{nb}km au {dir} du Mans. C’est dans notre périmètre quotidien : un devis se planifie dans la semaine, une intervention dans la foulée.",
  "À {km}{nb}km de notre atelier, {n} est une commune que nous desservons sans contrainte particulière, pour des particuliers comme pour des professionnels."],
 "moyen": [
  "{n} se trouve à {km}{nb}km au {dir} du Mans. Nous y groupons nos interventions sur des demi-journées, ce qui évite de facturer un déplacement à vide.",
  "Comptez {km}{nb}km depuis Le Mans pour rejoindre {n}. Nous organisons nos passages par secteur : un peu de souplesse sur la date, et un devis qui ne porte pas le trajet.",
  "À {km}{nb}km au {dir} du Mans, {n} fait partie de notre deuxième couronne d’intervention. Vitres, fin de chantier et bureaux, sur rendez-vous planifié."],
 "loin": [
  "{n} est à {km}{nb}km du Mans, au {dir}, à la limite de notre zone. Nous y venons sur rendez-vous planifié, généralement groupé avec une autre intervention du secteur.",
  "À {km}{nb}km, {n} marque le bord de notre rayon d’intervention. Nous nous y déplaçons volontiers, à condition de caler la date avec un autre chantier proche.",
  "{n} se situe à {km}{nb}km au {dir} du Mans. C’est loin, nous le disons : l’intervention se planifie, elle ne s’improvise pas."],
}

HABITAT = {
 "urbain": [
  "Avec {de}{nb}habitants au km², {n} est une commune dense : beaucoup de collectifs, de commerces de pied d’immeuble et de parties communes à entretenir.",
  "{n} concentre {p} habitants sur {su}{nb}km². Cette densité change la nature du travail : halls, cages d’escalier et vitrines priment sur les maisons individuelles.",
  "La densité de {n} ({de}{nb}hab/km²) en fait un tissu urbain constitué. Les demandes y viennent surtout de syndics, de commerçants et de gestionnaires de locaux."],
 "pavillon_dense": [
  "{n} mêle lotissements récents et petits collectifs. Les grandes baies vitrées y sont la norme, et c’est précisément ce qui se voit quand elles ne sont pas faites.",
  "Avec {de}{nb}habitants au km², {n} est une commune résidentielle construite : maisons groupées, quelques immeubles, et beaucoup de surfaces vitrées récentes.",
  "L’habitat de {n} est dense pour une commune périurbaine. Résultat : des interventions courtes et rapprochées, plutôt que de longues journées sur un seul site."],
 "pavillon": [
  "L’habitat de {n} est surtout pavillonnaire, étalé sur {su}{nb}km². Maisons individuelles, vérandas et abris de jardin : du vitrage accessible de plain-pied dans la plupart des cas.",
  "{n} s’étend sur {su}{nb}km² pour {p} habitants : du pavillonnaire aéré, avec des maisons souvent équipées de vérandas et de grandes baies côté jardin.",
  "Sur {n}, on trouve surtout de la maison individuelle. C’est le cas de figure le plus simple à chiffrer : accès de plain-pied, pas de matériel d’élévation."],
 "rural": [
  "{n} est une commune rurale : un bourg et des hameaux répartis sur {su}{nb}km², avec beaucoup de bâti ancien et de grandes ouvertures exposées aux intempéries.",
  "Avec {de}{nb}habitants au km² sur {su}{nb}km², {n} est une commune étendue et peu dense. Les chantiers y sont dispersés, ce qui demande de les grouper.",
  "Le bâti de {n} est majoritairement ancien, réparti entre un bourg et des écarts. Longères, dépendances et vérandas y forment l’essentiel de la demande."],
}

TISSU = {
 "bourg_important": [
  "Avec {p} habitants, {n} a son propre tissu de commerces, d’écoles et d’entreprises. Nous y travaillons autant pour des professionnels que pour des particuliers.",
  "{p} habitants : {n} n’est pas une commune-dortoir. Commerces de centre-bourg, zones d’activité et équipements publics génèrent une demande professionnelle constante.",
  "La taille de {n} ({p} habitants) explique la variété des demandes : vitrines, bureaux, copropriétés et logements après travaux."],
 "bourg_moyen": [
  "{p} habitants : assez pour un centre-bourg commerçant, assez peu pour que les artisans se connaissent. Le bouche-à-oreille y fait beaucoup.",
  "Avec {p} habitants, {n} a le gabarit d’une commune où l’on revient. Un client satisfait en amène un autre dans la même rue.",
  "{n} compte {p} habitants. La demande s’y répartit entre particuliers et petites structures : commerces, cabinets, artisans."],
 "petit_bourg": [
  "{n} compte {p} habitants. La demande y est surtout résidentielle : vitres, vérandas et remises en état après travaux ou avant un état des lieux.",
  "Avec {p} habitants, {n} est une petite commune. Nous y venons essentiellement pour des particuliers, souvent sur recommandation d’un voisin.",
  "{p} habitants : à cette taille, tout se sait. C’est la meilleure raison de bien faire le travail du premier coup."],
}

EPCI_OUI = [
 "La commune fait partie de Le Mans Métropole, notre zone d’intervention principale : pas de frais de déplacement supplémentaires.",
 "{n} appartient à Le Mans Métropole. C’est le cœur de notre secteur : nous y circulons tous les jours, et le devis ne porte que la prestation.",
 "Rattachée à Le Mans Métropole, {n} est dans notre périmètre de base. Aucun supplément kilométrique n’est appliqué.",
]
EPCI_NON = [
 "{n} relève de {e}. Nous sortons de Le Mans Métropole pour y venir, mais la commune reste dans notre rayon habituel.",
 "Hors Le Mans Métropole, {n} appartient à {e}. Cela ne change rien au tarif : nous groupons simplement les passages sur le secteur.",
 "{n} fait partie de {e}, au {dir} du Mans. Nous y intervenons dans les mêmes conditions que sur la métropole.",
]

SERVICES = {
 "urbain": {
  "vitres": ["Vitrines de commerces et parties communes de collectifs, en passage régulier pour que ce soit toujours net.",
             "Devantures, halls d’entrée et surfaces vitrées des immeubles, entretenus au rythme qui vous convient.",
             "Vitrines commerçantes et vitrages collectifs : le passage fréquent salit vite, le contrat régulier revient moins cher."],
  "chantier": ["Remise en état après travaux dans les logements collectifs et les locaux commerciaux, avant remise des clés.",
               "Livraison de chantier en milieu urbain : appartements, plateaux de bureaux et cellules commerciales.",
               "Après les corps d’état, avant la réception : dépoussiérage complet, traces et sols repris."],
  "bureaux": ["Entretien de bureaux et de locaux professionnels, hors horaires pour ne pas gêner l’activité.",
              "Passage quotidien ou hebdomadaire sur vos locaux, tôt le matin ou après la fermeture.",
              "Bureaux, salles de réunion, sanitaires et parties communes, avec une équipe qui ne change pas."]},
 "pavillon_dense": {
  "vitres": ["Baies vitrées de maisons et vitrines des commerces du bourg, à l’unité ou en contrat d’entretien.",
             "Grandes baies des constructions récentes et devantures du centre : un passage suffit à changer l’allure.",
             "Vitrages de maisons individuelles et de petits collectifs, intérieur comme extérieur."],
  "chantier": ["Nettoyage de fin de chantier sur les constructions neuves et les extensions, nombreuses sur la commune.",
               "Maisons neuves et agrandissements : nous reprenons le vitrage, les sols et les menuiseries avant emménagement.",
               "Remise en état après construction, avec le décapage des résidus de pose que le gros œuvre laisse derrière lui."],
  "bureaux": ["Entretien des locaux professionnels et des cabinets installés sur la commune.",
              "Cabinets, agences et petites entreprises : un entretien calibré sur la surface réelle.",
              "Locaux professionnels du bourg, en passage régulier ou en remise en état ponctuelle."]},
 "pavillon": {
  "vitres": ["Baies vitrées, vérandas et fenêtres de maisons individuelles, accessibles sans nacelle dans la plupart des cas.",
             "Fenêtres, baies et vérandas de plain-pied : le cas le plus simple, et le plus rapide à chiffrer.",
             "Vitrage de maisons individuelles, véranda comprise, en ponctuel ou deux à quatre fois par an."],
  "chantier": ["Remise en état après rénovation ou extension, avant emménagement ou avant une vente.",
               "Après des travaux dans une maison : poussière fine, traces de peinture, sols à reprendre.",
               "Fin de chantier résidentielle, calée sur la date de livraison ou l’état des lieux."],
  "bureaux": ["Entretien de petits locaux professionnels, ateliers et cabinets.",
              "Bureaux d’artisans, cabinets libéraux et petits locaux d’activité.",
              "Locaux professionnels de taille modeste, entretenus à la fréquence qui suffit."]},
 "rural": {
  "vitres": ["Grandes ouvertures de maisons anciennes, vérandas et verrières, souvent très exposées aux intempéries.",
             "Vitrages de longères et de dépendances, que le vent et la pluie salissent plus vite qu’en ville.",
             "Fenêtres anciennes, vérandas et verrières : du verre fragile, traité en conséquence."],
  "chantier": ["Remise en état après rénovation de bâti ancien : poussière de ponçage, traces d’enduit, sols à décaper.",
               "Après une rénovation de longère ou de grange : la poussière de chantier s’y loge partout.",
               "Fin de chantier sur bâti ancien, avec le temps qu’il faut pour ne rien abîmer."],
  "bureaux": ["Entretien de locaux d’entreprise et de bâtiments agricoles ou artisanaux.",
              "Locaux d’activité, ateliers et bureaux d’exploitation.",
              "Bâtiments professionnels de la commune, entretenus selon leur usage réel."]},
}

# ─────────── Paragraphes composés ───────────
# Chaque paragraphe est assemblé à partir de trois clauses indépendantes, tirées sur
# des empreintes distinctes : 4 × 4 × 4 = 64 combinaisons par profil au lieu de 3.

C_DIST = {
 "tres_proche": ["Entre notre atelier du Mans et {n}, il y a {km}{nb}km.",
   "{n} est à {km}{nb}km de notre atelier, au {dir} du Mans.",
   "Moins d’un quart d’heure sépare notre atelier de {n}.",
   "{km}{nb}km de route : {n} est à notre porte."],
 "proche": ["{n} est à {km}{nb}km du Mans, au {dir} de la ville.",
   "Il faut compter {km}{nb}km pour rejoindre {n} depuis notre atelier.",
   "Avec {km}{nb}km, {n} reste dans notre périmètre quotidien.",
   "{n} se situe à {km}{nb}km, au {dir} du Mans."],
 "moyen": ["{n} se trouve à {km}{nb}km au {dir} du Mans.",
   "Il y a {km}{nb}km entre notre atelier et {n}.",
   "{km}{nb}km nous séparent de {n}.",
   "À {km}{nb}km, {n} appartient à notre deuxième couronne."],
 "loin": ["{n} est à {km}{nb}km, au bord de notre zone.",
   "Avec {km}{nb}km de route, {n} marque la limite de ce que nous desservons.",
   "{n} se situe à {km}{nb}km au {dir} du Mans, à l’extrémité de notre rayon.",
   "{km}{nb}km : {n} est la commune la plus éloignée de notre secteur habituel."],
}
C_ORG = {
 "tres_proche": ["Nous y passons plusieurs fois par semaine, ce qui permet d’accepter un petit chantier isolé sans qu’il soit déficitaire.",
   "Cette proximité rend possible ce qui ne l’est pas ailleurs : une seule véranda, une vitrine, un appartement après travaux.",
   "Concrètement, une demande formulée la veille pour une remise de clés le lendemain a toutes ses chances d’aboutir.",
   "Nous n’imposons donc aucun minimum de facturation pour rentabiliser le déplacement."],
 "proche": ["Nous tenons des rendez-vous à l’heure plutôt que des créneaux de trois heures, et nous repassons si un détail vous gêne.",
   "Le délai entre la demande de devis et l’intervention se compte en jours, pas en semaines.",
   "Pour un entretien régulier, le passage se cale sur un jour fixe que nous ne bougeons pas.",
   "Nous y intervenons à la demande, sans avoir besoin d’attendre qu’un autre chantier se présente."],
 "moyen": ["Nous regroupons les chantiers du secteur sur une même demi-journée plutôt que de multiplier les allers-retours.",
   "L’organisation demande un peu de souplesse sur la date : une fenêtre de deux ou trois jours plutôt qu’une date imposée.",
   "Nous y venons chaque semaine, mais en planifiant plutôt qu’en improvisant.",
   "Une demande urgente passe si un autre chantier du secteur est déjà calé dans la semaine."],
 "loin": ["L’intervention se planifie à l’avance, presque toujours groupée avec un autre chantier proche.",
   "Nous préférons annoncer clairement qu’une petite prestation isolée sera mieux servie par un confrère du coin.",
   "Pour un chantier conséquent ou un contrat régulier, la distance ne pose aucun problème.",
   "Nous calons une date ferme plutôt que de promettre une intervention le jour même."],
}
C_PRIX = ["Le devis ne porte donc que le travail réel, jamais un trajet à vide.",
 "Cela se voit sur le chiffrage : nous ne facturons pas de ligne « déplacement ».",
 "C’est ce qui nous permet de tenir un prix aligné sur celui d’une intervention au Mans même.",
 "Le trajet est absorbé par notre organisation, pas répercuté sur votre devis."]

C_BATI = {
 "urbain": ["L’essentiel du travail se joue sur les parties communes et les vitrines.",
   "Halls, cages d’escalier et vitrages de rez-de-chaussée concentrent la demande.",
   "Le bâti collectif domine, et il est vu par beaucoup de monde tous les jours.",
   "La densité concentre les surfaces à entretenir sur peu de mètres carrés au sol."],
 "pavillon_dense": ["Les lotissements récents signifient beaucoup de surfaces vitrées neuves.",
   "Maisons groupées et petits collectifs se répartissent la demande.",
   "Le bâti est récent, avec de grandes baies posées depuis peu.",
   "On y alterne entre baies de maisons et vitrages d’immeubles."],
 "pavillon": ["Presque tout se fait de plain-pied ou à la perche, sans échafaudage ni nacelle.",
   "La maison individuelle domine, avec souvent une véranda côté jardin.",
   "L’accès est rarement un problème, ce qui maintient le coût bas.",
   "Les maisons s’entretiennent facilement, à condition de ne pas trop espacer les passages."],
 "rural": ["Le bâti ancien demande plus de précaution que du neuf.",
   "Longères, dépendances et vérandas forment l’essentiel de la demande.",
   "L’habitat est dispersé entre un bourg et des écarts.",
   "Les vitrages y sont très exposés au vent et à la pluie."],
}
C_CONSEQ = {
 "urbain": ["Une cage d’escalier se dégrade vite quand le passage est important : c’est là qu’un contrat régulier coûte moins cher qu’une remise en état annuelle.",
   "Un vitrage de hall non entretenu se voile en quelques semaines, et le voile finit par s’incruster. Repris tôt, c’est un passage rapide.",
   "La régularité y est plus rentable que le rattrapage, simplement parce que la saleté n’a pas le temps de s’accrocher.",
   "Nous y travaillons surtout pour des syndics, des commerçants et des gestionnaires de locaux."],
 "pavillon_dense": ["Après une construction, il reste presque toujours des résidus de pose sur les vitres : adhésifs, silicone, voile de plâtre. Ce n’est pas du nettoyage courant.",
   "Le verre neuf porte encore les traces du chantier, et un nettoyage ordinaire ne les enlève pas. Nous utilisons une lame et un produit adaptés, jamais d’abrasif.",
   "Deux gestes différents, deux matériels différents, parfois sur la même journée.",
   "Les extensions récentes créent une demande de fin de chantier régulière tout au long de l’année."],
 "pavillon": ["Ce qui pèse sur le devis, c’est la surface vitrée réelle : une véranda change le chiffrage plus qu’on ne l’imagine.",
   "Nous évaluons l’accès au moment du chiffrage, c’est ce qui fait le plus varier un prix sur ce type de maison.",
   "Deux à quatre passages par an suffisent à ne jamais laisser le calcaire s’installer sur le verre.",
   "L’absence de matériel d’élévation raccourcit l’intervention, et le devis suit."],
 "rural": ["Mastic fragile, bois qui a travaillé, verre d’origine parfois irrégulier : on n’attaque pas ça comme une baie récente.",
   "Les menuiseries anciennes supportent mal les produits agressifs. Nous travaillons plus doucement, quitte à y passer plus de temps.",
   "Nous prenons le temps de vérifier l’état des mastics avant de passer la raclette.",
   "La dispersion de l’habitat nous amène à traiter plusieurs adresses du secteur dans la même sortie."],
}

C_MAISON = ["Klynera est installée 40 rue Saint André, au Mans.",
 "Notre atelier est au Mans, 40 rue Saint André.",
 "L’entreprise a une adresse réelle : 40 rue Saint André, 72000 Le Mans.",
 "Klynera n’est pas une plateforme : une adresse au Mans, un SIREN public, un téléphone qui décroche."]
C_EQUIPE = ["Nous ne sous-traitons pas : l’équipe qui vient à {n} est celle qui travaille au Mans.",
 "Vous avez le même interlocuteur du devis à la fin du chantier, à {n} comme ailleurs.",
 "Les mêmes personnes reviennent sur votre site : elles connaissent vos accès et vos exigences.",
 "Aucune sous-traitance, aucun intermédiaire entre vous et celui qui tient la raclette."]
C_DEVIS = ["Le devis pour {n} est gratuit, détaillé poste par poste, et envoyé sous 24{nb}h.",
 "Nous refusons de donner un prix au mètre carré sans avoir vu les lieux : sur du vitrage, l’accès et l’état initial font varier le temps de travail du simple au double.",
 "Le chiffrage est gratuit et sans engagement, et il ne bouge pas entre le devis et la facture.",
 "Nous préférons nous déplacer pour voir avant d’annoncer un prix, plutôt que d’annoncer un prix qui changera."]


FAQ = [
 ("Intervenez-vous à {n} ?",
  ["Oui. {n} est à {km}{nb}km de notre atelier du Mans, au {dir} de la ville, dans notre zone d’intervention habituelle. Nous y réalisons du nettoyage de vitres, du nettoyage de fin de chantier et de l’entretien de bureaux, pour les particuliers comme pour les professionnels.",
   "Oui, {n} fait partie des communes que nous desservons. Comptez {km}{nb}km depuis Le Mans. Les trois prestations y sont disponibles : vitrerie, remise en état de fin de chantier et entretien de locaux.",
   "Oui. Nous intervenons à {n} toute l’année, en ponctuel comme en contrat régulier, sur les mêmes prestations qu’au Mans."]),
 ("Facturez-vous un déplacement jusqu’à {n} ?",
  ["{dep}", "{dep}", "{dep}"]),
 ("Sous combien de temps obtient-on un devis à {n} ?",
  ["Le devis est gratuit et envoyé sous 24{nb}h. Pour une intervention à {n}, nous nous déplaçons pour évaluer l’accès et l’état réel des surfaces quand c’est nécessaire : c’est le seul moyen de chiffrer honnêtement.",
   "Sous 24{nb}h après votre demande. Selon la nature du chantier à {n}, une visite préalable peut être utile : elle est gratuite et sans engagement.",
   "Comptez 24{nb}h. Nous préférons voir les lieux avant de chiffrer un chantier à {n} plutôt que d’annoncer un prix qui bougera ensuite."]),
]

DEPLACEMENT = {
 True: ["Non. {n} fait partie de Le Mans Métropole, notre zone principale : le devis porte uniquement sur la prestation.",
        "Aucun supplément. {n} étant sur Le Mans Métropole, le trajet est intégré à notre fonctionnement normal.",
        "Non, pas de frais de déplacement sur {n} : la commune est dans notre périmètre de base."],
 False: ["Le trajet jusqu’à {n} ({km}{nb}km) est intégré au devis, pas facturé en supplément. Sur les communes les plus éloignées, nous groupons les interventions pour que cela reste sans effet sur le prix.",
         "Non. Les {km}{nb}km jusqu’à {n} sont absorbés par notre organisation : nous regroupons les chantiers du secteur sur une même sortie.",
         "Il n’y a pas de ligne « déplacement » sur nos devis. Pour {n}, à {km}{nb}km, nous calons simplement l’intervention avec un autre chantier proche."],
}


def compose(*morceaux):
    return " ".join(morceaux)


def bloc(pool, cle, c, sel=""):
    return typo(pick(pool, cle, c, sel).format(
        n=c["nom"], km=c["km_route_txt"], p=fr(c["pop"]), de=fr(c["densite"]),
        su=str(c["surface"]).replace(".", ","), e=c["epci"], dir=c["dir"], nb=NNBSP))


# ─────────── Extraction du gabarit ───────────

def gabarit():
    s = open(SRC, encoding="utf-8").read()
    sprite = re.search(r'<svg width="0".*?</svg>', s, re.S).group(0)
    nav = re.search(r'<nav class="nav" id="nav".*?</nav>', s, re.S).group(0)
    form = re.search(r'<section class="section-full section-white" id="devis">.*?</section>', s, re.S).group(0)
    footer = re.search(r'<footer class="footer">.*?</footer>', s, re.S).group(0)
    scripts = re.findall(r'<script src="[^"]*"></script>', s)
    head = re.search(r'<head>(.*?)</head>', s, re.S).group(1)
    # on ne garde du head que ce qui est commun (polices, styles, preload)
    commun = "\n".join(l for l in head.split("\n")
                       if re.search(r'rel="(stylesheet|preload|icon|preconnect)"|charset|viewport|theme-color', l))
    return sprite, nav, form, footer, scripts, commun


def page(c, voisines, sprite, nav, form, footer, scripts, commun):
    d, h, t, metro = axes(c)
    n, cp, sl = c["nom"], c["cp"], c["slug"]
    url = f"{BASE}/nettoyage-{sl}/"
    titre = typo(f"Nettoyage à {n} ({cp}) · vitres, chantier, bureaux · Klynera")
    desc = typo(f"Entreprise de nettoyage à {n} ({cp}) : vitres, fin de chantier et bureaux. "
                f"À {c['km_route_txt']}{NNBSP}km du Mans. Devis gratuit sous 24{NNBSP}h.")
    def rend(txt):
        return typo(txt.format(n=n, km=c["km_route_txt"], p=fr(c["pop"]), de=fr(c["densite"]),
                               su=str(c["surface"]).replace(".", ","), e=c["epci"],
                               dir=c["dir"], nb=NNBSP,
                               dep=rend_dep()))

    def rend_dep():
        return pick({"d": DEPLACEMENT[metro]}, "d", c, "dep").format(
            n=n, km=c["km_route_txt"], nb=NNBSP)

    sv = {k: pick(SERVICES[h], k, c, "sv") for k in ("vitres", "chantier", "bureaux")}

    schemas = [
        {"@context": "https://schema.org", "@type": "Service",
         "name": f"Nettoyage à {n}",
         "serviceType": "Nettoyage de vitres, fin de chantier et bureaux",
         "provider": {"@id": f"{BASE}/#business"},
         "areaServed": {"@type": "City", "name": n,
                        "address": {"@type": "PostalAddress", "addressLocality": n,
                                    "postalCode": cp, "addressCountry": "FR"}},
         "url": url, "description": desc},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Zone d’intervention", "item": BASE + "/zone-intervention/"},
            {"@type": "ListItem", "position": 3, "name": n, "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": typo(q.format(n=n)),
             "acceptedAnswer": {"@type": "Answer",
                                "text": rend(pick({"a": a}, "a", c, q))}}
            for q, a in FAQ]},
    ]
    ld = "\n".join('<script type="application/ld+json">\n' + json.dumps(s, ensure_ascii=False, indent=2) + '\n</script>'
                   for s in schemas)

    faq_html = "\n".join(
        f'''    <details class="faq-item reveal">
      <summary><span>{typo(q.format(n=n))}</span><span class="faq-plus" aria-hidden="true">+</span></summary>
      <div class="faq-body"><p>{rend(pick({"a": a}, "a", c, q))}</p></div>
    </details>''' for q, a in FAQ)

    v = voisines
    reperes = f'''    <dl class="loc-reperes reveal">
      <div class="loc-repere"><dt>Habitants</dt><dd>{fr(c["pop"])}<small>{fr(c["densite"])} au km²</small></dd></div>
      <div class="loc-repere"><dt>Superficie</dt><dd>{str(c["surface"]).replace(".", ",")} km²<small>code INSEE {c["code"]}</small></dd></div>
      <div class="loc-repere"><dt>Depuis Le Mans</dt><dd>{c["km_route_txt"]} km<small>au {c["dir"]}</small></dd></div>
      <div class="loc-repere"><dt>Intercommunalité</dt><dd style="font-size:1rem">{c["epci"]}<small>code postal {cp}</small></dd></div>
    </dl>'''
    voisinage = typo(
        f"Autour de {n}, nous desservons également {v[0]['nom']} ({v[0]['km_route_txt']}{NNBSP}km du Mans), "
        f"{v[1]['nom']} ({v[1]['km_route_txt']}{NNBSP}km) et {v[2]['nom']} ({v[2]['km_route_txt']}{NNBSP}km). "
        f"Regrouper plusieurs adresses d\u2019un même secteur sur une seule sortie nous permet de ne pas "
        f"répercuter le trajet, et c\u2019est aussi ce qui rend possible une intervention rapide quand "
        f"un client de {n} appelle la veille pour le lendemain.")

    voisins_html = "\n".join(f'      <a href="/nettoyage-{v["slug"]}/">{v["nom"]}</a>' for v in voisines)

    f = form.replace("Nouvelle demande de devis · klynera-nettoyage.fr",
                     f"Demande de devis · {n} ({cp}) · klynera-nettoyage.fr")

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

<header class="svc-hero svc-hero--plain">
  <div class="svc-hero-inner">
    <div class="svc-hero-body">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span>·</span><a href="/zone-intervention/">Zone d’intervention</a><span>·</span><span>{n}</span></nav>
      <h1>Nettoyage à {n}, <em>vitres, chantier et bureaux.</em></h1>
      <p class="lp-lede">{bloc(LEDE, d, c)}</p>
      <div class="lp-ctas">
        <a class="btn btn-primary" href="#devis">Demander un devis</a>
        <a class="lp-phone" href="tel:+33671671635"><svg class="ico"><use href="#i-phone"/></svg>06 71 67 16 35</a>
      </div>
      <div class="lp-proof">
        <span><svg class="ico"><use href="#i-check"/></svg>Devis gratuit sous 24{NNBSP}h</span>
        <span><svg class="ico"><use href="#i-check"/></svg>{n} ({cp}) · {c["km_route_txt"]}{NNBSP}km du Mans</span>
      </div>
    </div>
  </div>
</header>

<main id="contenu">

<section class="section-full section-white">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Nos prestations</p>
      <h2 class="section-title">Ce que nous faisons à {n}</h2>
    </header>
    <div class="loc-services">
      <a class="loc-service reveal" href="/nettoyage-vitres/">
        <span class="icbox"><svg class="ico"><use href="#i-sparkle"/></svg></span>
        <h3>Nettoyage de vitres</h3>
        <p>{typo(sv["vitres"])}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
      <a class="loc-service reveal" href="/nettoyage-fin-de-chantier/">
        <span class="icbox"><svg class="ico"><use href="#i-sparkle"/></svg></span>
        <h3>Fin de chantier</h3>
        <p>{typo(sv["chantier"])}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
      <a class="loc-service reveal" href="/nettoyage-bureaux/">
        <span class="icbox"><svg class="ico"><use href="#i-sparkle"/></svg></span>
        <h3>Nettoyage de bureaux</h3>
        <p>{typo(sv["bureaux"])}</p>
        <span class="lien">Voir la prestation <svg class="ico"><use href="#i-arrow"/></svg></span>
      </a>
    </div>
  </div>
</section>

<section class="section-full section-dark">
  <div class="section-inner">
    <header class="section-head reveal">
      <p class="eyebrow">Sur place</p>
      <h2 class="section-title">Intervenir à {n}</h2>
    </header>
    <div class="lp-steps">
      <div class="lp-step reveal"><span class="lp-step-n">01</span><div><h3>La distance</h3><p>{bloc(LEDE, d, c)}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">02</span><div><h3>Le bâti</h3><p>{bloc(HABITAT, h, c)}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">03</span><div><h3>Le tissu local</h3><p>{bloc(TISSU, t, c)}</p></div></div>
      <div class="lp-step reveal"><span class="lp-step-n">04</span><div><h3>Le rattachement</h3><p>{rend(pick({"e": EPCI_OUI if metro else EPCI_NON}, "e", c, "epci"))}</p></div></div>
    </div>
{reperes}
    <p class="section-lede reveal" style="margin-top:34px;max-width:900px">{voisinage}</p>
  </div>
</section>

<section class="section">
  <div class="lp-cols">
    <div class="prose reveal">
      <h2>Depuis Le Mans jusqu’à {n}</h2>
      <p>{rend(compose(pick(C_DIST, d, c, "d1"), pick(C_ORG, d, c, "d2"), pick({"x": C_PRIX}, "x", c, "d3")))}</p>
      <h2>Ce qu’on rencontre à {n}</h2>
      <p>{rend(compose(pick(C_BATI, h, c, "b1"), pick(C_CONSEQ, h, c, "b2")))}</p>
      <h2>Qui intervient</h2>
      <p>{rend(compose(pick({"x": C_MAISON}, "x", c, "m1"), pick({"x": C_EQUIPE}, "x", c, "m2"), pick({"x": C_DEVIS}, "x", c, "m3")))}</p>
    </div>
    <aside class="lp-price reveal">
      <p class="eyebrow">Devis</p>
      <h2>Combien coûte un nettoyage à {n}</h2>
      <p>Le prix dépend de la surface, de l’accès, de l’état initial et de la fréquence. Nous ne donnons pas de tarif au mètre carré sans avoir vu les lieux : ce serait un chiffre inventé. Le devis est gratuit, détaillé poste par poste, et envoyé sous 24{NNBSP}h.</p>
      <a class="btn btn-primary" href="#devis">Demander un devis gratuit</a>
    </aside>
  </div>
</section>

<section class="section" id="faq-page" style="padding-top:0">
  <header class="section-head reveal">
    <p class="eyebrow">Questions fréquentes</p>
    <h2 class="section-title">Nettoyage à {n}, <em>en pratique</em></h2>
  </header>
  <div class="faq">
{faq_html}
  </div>
  <div class="reveal">
    <p class="eyebrow" style="margin-top:56px">Communes voisines</p>
    <div class="loc-voisines">
{voisins_html}
      <a href="/zone-intervention/">Toute la zone</a>
    </div>
  </div>
</section>

{f}

</main>

{footer}

{chr(10).join(scripts)}
</body>
</html>
'''


def main():
    sprite, nav, form, footer, scripts, commun = gabarit()
    for c in COMMUNES:
        c["slug"] = slug(c["nom"])
        c["km_route_txt"] = str(int(round(c["km_route"])))
    n_ok = 0
    for i, c in enumerate(COMMUNES):
        # voisines : les 4 plus proches géographiquement dans la sélection
        autres = sorted((x for x in COMMUNES if x is not c),
                        key=lambda x: abs(x["km"] - c["km"]) + abs(x["pop"] - c["pop"]) / 8000)[:4]
        d = os.path.join(RACINE, f"nettoyage-{c['slug']}")
        os.makedirs(d, exist_ok=True)
        html_page = page(c, autres, sprite, nav, form, footer, scripts, commun)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html_page)
        n_ok += 1
    print(f"{n_ok} pages de lieu générées")


if __name__ == "__main__":
    main()
