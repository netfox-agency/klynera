// Reveals au scroll : IntersectionObserver + fallback rect (fiable même si l'onglet est throttlé)
const reveals = () => document.querySelectorAll(".reveal:not(.visible)");

function revealCheck() {
  const vh = window.innerHeight;
  reveals().forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.top < vh - 40 && r.bottom > 0) el.classList.add("visible");
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
);
document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

// L'IntersectionObserver gère la suite ; un seul check initial pour ce qui est déjà visible.
window.addEventListener("resize", revealCheck);
revealCheck();

// Mode capture (?all&s=section) : tout visible sans transition, scroll instantané,
// pour screenshots outillés
const captureParams = new URLSearchParams(location.search);
if (captureParams.has("all")) {
  document.documentElement.style.scrollBehavior = "auto";
  document.body.classList.add("capture");
  document.querySelectorAll(".reveal").forEach((el) => {
    el.style.transition = "none";
    el.classList.add("visible");
  });
  const target = captureParams.get("s");
  if (target) {
    const el = document.getElementById(target);
    if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY);
  }
  const shift = captureParams.get("shift");
  if (shift) document.body.style.transform = `translateY(-${shift}px)`;
}

// Manifeste : révélation caractère par caractère au scroll
const aboutReveal = document.getElementById("about-reveal");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (aboutReveal && !reducedMotion) {
  const text = aboutReveal.textContent;
  aboutReveal.setAttribute("aria-label", text.trim());
  aboutReveal.innerHTML = "";
  const frag = document.createDocumentFragment();
  for (const ch of text) {
    const s = document.createElement("span");
    s.className = "ch";
    s.setAttribute("aria-hidden", "true");
    s.textContent = ch;
    frag.appendChild(s);
  }
  aboutReveal.appendChild(frag);
  const chars = aboutReveal.querySelectorAll(".ch");
  const aboutCheck = () => {
    const r = aboutReveal.getBoundingClientRect();
    const progress = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.45)));
    const count = Math.floor(chars.length * progress);
    chars.forEach((c, i) => c.classList.toggle("on", i < count));
  };
  window.__aboutCheck = aboutCheck;
  aboutCheck();
  if (new URLSearchParams(location.search).has("all")) {
    chars.forEach((c) => c.classList.add("on"));
  }
}

// Nav fixe : fond encre dès qu'on quitte le hero.
// Barre mobile : n'apparaît qu'après le hero (ses CTA suffisent au premier écran).
const nav = document.getElementById("nav");
const mobileBar = document.querySelector(".mobile-bar");
const heroEl = document.querySelector(".hero");
const barThreshold = () => (heroEl ? heroEl.offsetHeight * 0.6 : 300);
function navCheck() {
  if (heroEl) nav.classList.toggle("nav-solid", window.scrollY > 40);
  if (mobileBar) mobileBar.classList.toggle("on", window.scrollY > barThreshold());
}
// Listener de scroll unique pour toute la page, throttlé sur une frame
let scrollScheduled = false;
window.addEventListener("scroll", () => {
  if (scrollScheduled) return;
  scrollScheduled = true;
  requestAnimationFrame(() => {
    navCheck();
    if (window.__aboutCheck) window.__aboutCheck();
    scrollScheduled = false;
  });
}, { passive: true });
navCheck();

// Les CTA par métier préremplissent la prestation du formulaire
const prestationSelect = document.querySelector('select[name="prestation"]');
if (prestationSelect) {
  document.querySelectorAll("[data-prestation]").forEach((link) => {
    link.addEventListener("click", () => {
      prestationSelect.value = link.dataset.prestation;
    });
  });
}

// ─── Traçabilité de la source (premier contact conservé) ───
// utm_*, gclid, referrer et page d'entrée sont capturés à l'arrivée puis
// injectés dans chaque envoi de formulaire : chaque lead arrive avec sa source.
const SRC_KEY = "klynera_src";
(function captureSource() {
  try {
    const q = new URLSearchParams(location.search);
    // Dernier levier identifié gagne : une arrivée avec utm/gclid remplace la
    // source stockée ; sinon on conserve le premier contact connu.
    if (localStorage.getItem(SRC_KEY) && !q.get("utm_source") && !q.get("gclid")) return;
    const src = {
      utm_source: q.get("utm_source") || "",
      utm_medium: q.get("utm_medium") || "",
      utm_campaign: q.get("utm_campaign") || "",
      utm_term: q.get("utm_term") || "",
      gclid: q.get("gclid") || "",
      referrer: document.referrer || "direct",
      landing: location.pathname,
      first_visit: new Date().toISOString().slice(0, 16),
    };
    if (!src.utm_source && src.gclid) { src.utm_source = "google"; src.utm_medium = "cpc"; }
    if (!src.utm_source && /google\./.test(src.referrer)) { src.utm_source = "google"; src.utm_medium = "organic"; }
    if (!src.utm_source && /bing\.|duckduckgo\.|qwant\./.test(src.referrer)) { src.utm_medium = "organic"; }
    localStorage.setItem(SRC_KEY, JSON.stringify(src));
  } catch (e) { /* stockage indisponible : on continue sans */ }
})();
function getSource() {
  try { return JSON.parse(localStorage.getItem(SRC_KEY)) || {}; } catch (e) { return {}; }
}

// Événements de conversion (dataLayer) : lead, clics téléphone, clics devis.
// Inoffensif tant que GTM n'est pas branché ; prêt pour Google Ads / GA4.
window.dataLayer = window.dataLayer || [];
function track(event, params) {
  window.dataLayer.push(Object.assign({ event }, params));
}
document.querySelectorAll('a[href^="tel:"]').forEach((a) => {
  a.addEventListener("click", () => track("phone_click", Object.assign({ location: a.className, page: location.pathname }, getSource())));
});
document.querySelectorAll('a[href="#contact"]').forEach((a) => {
  a.addEventListener("click", () => track("cta_devis_click", { location: a.className || a.textContent.trim() }));
});

// Envoi du formulaire sans quitter la page (Web3Forms : FormData + Accept JSON)
const form = document.querySelector(".contact-form");
if (form) form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  const error = form.querySelector(".form-error");
  error.classList.remove("visible");
  btn.disabled = true;
  const btnLabel = btn.textContent;
  btn.textContent = "Envoi en cours…";
  try {
    const fd = new FormData(form);
    const src = getSource();
    fd.set("source", [src.utm_source, src.utm_medium, src.utm_campaign].filter(Boolean).join(" / ") || "direct ou inconnu");
    fd.set("page_du_lead", location.pathname);
    fd.set("page_d_entree", src.landing || "");
    fd.set("referrer", src.referrer || "");
    if (src.gclid) fd.set("gclid", src.gclid);
    if (src.first_visit) fd.set("premiere_visite", src.first_visit);
    const res = await fetch(form.action, {
      method: "POST",
      body: fd,
      headers: { Accept: "application/json" },
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.message || "failed");
    form.querySelectorAll(".form-row, label, button, .form-note").forEach((el) => {
      el.style.display = "none";
    });
    form.querySelector(".form-success").classList.add("visible");
    track("generate_lead", Object.assign({ prestation: prestationSelect ? prestationSelect.value : "page", page: location.pathname }, getSource()));
  } catch {
    error.classList.add("visible");
    btn.disabled = false;
    btn.textContent = btnLabel;
  }
});

// Stagger léger sur les grilles
document
  .querySelectorAll(".svc-grid, .reviews-sub")
  .forEach((grid) => {
    [...grid.children].forEach((child, i) => {
      child.style.transitionDelay = `${i * 90}ms`;
    });
  });
