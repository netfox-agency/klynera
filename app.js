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

window.addEventListener("scroll", revealCheck, { passive: true });
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
  window.addEventListener("scroll", aboutCheck, { passive: true });
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
window.addEventListener("scroll", navCheck, { passive: true });
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

// Événements de conversion (dataLayer) : lead, clics téléphone, clics devis.
// Inoffensif tant que GTM n'est pas branché ; prêt pour Google Ads / GA4.
window.dataLayer = window.dataLayer || [];
function track(event, params) {
  window.dataLayer.push(Object.assign({ event }, params));
}
document.querySelectorAll('a[href^="tel:"]').forEach((a) => {
  a.addEventListener("click", () => track("phone_click", { location: a.className }));
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
    const res = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.message || "failed");
    form.querySelectorAll(".form-row, label, button, .form-note").forEach((el) => {
      el.style.display = "none";
    });
    form.querySelector(".form-success").classList.add("visible");
    track("generate_lead", { prestation: prestationSelect ? prestationSelect.value : "page" });
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
