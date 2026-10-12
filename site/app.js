/* ============================================================
   MessMate — landing interactions
   Scroll progress · reveals · live kitchen demo · scrollytelling
   ============================================================ */
(() => {
  "use strict";

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- scroll progress + nav state ---------- */
  const progressBar = document.getElementById("progressBar");
  const nav = document.getElementById("siteNav");

  const onScroll = () => {
    const doc = document.documentElement;
    const max = doc.scrollHeight - window.innerHeight;
    const ratio = max > 0 ? window.scrollY / max : 0;
    progressBar.style.width = `${(ratio * 100).toFixed(2)}%`;
    nav.classList.toggle("scrolled", window.scrollY > 24);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- reveal on scroll ---------- */
  const revealEls = document.querySelectorAll("[data-reveal]");
  if (prefersReduced) {
    revealEls.forEach((el) => el.classList.add("revealed"));
  } else {
    const revealIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, i) => {
          if (entry.isIntersecting) {
            entry.target.style.transitionDelay = `${Math.min(i * 70, 280)}ms`;
            entry.target.classList.add("revealed");
            revealIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => revealIO.observe(el));
  }

  /* ---------- number tween ---------- */
  const tween = (el, target, fmt) => {
    const from = parseFloat(el.dataset.value || "0") || 0;
    el.dataset.value = String(target);
    if (prefersReduced) { el.textContent = fmt(target); return; }
    const start = performance.now();
    const dur = 550;
    const step = (now) => {
      const t = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = fmt(from + (target - from) * eased);
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const fmtKg = (v) => `${v.toFixed(1)} kg`;
  const fmtRs = (v) => `₹${Math.round(v).toLocaleString("en-IN")}`;

  /* ---------- hero: live kitchen demo ---------- */
  const COHORT = 240;
  const RATE_PER_KG = 85;
  const BUFFER = 1.08;

  const mealBtns = Array.from(document.querySelectorAll(".meal"));
  const rDiners = document.getElementById("rDiners");
  const rCook = document.getElementById("rCook");
  const rSaved = document.getElementById("rSaved");
  const rCountdown = document.getElementById("rCountdown");
  const rNextMeal = document.getElementById("rNextMeal");

  const readMeal = (btn) => ({
    on: btn.classList.contains("is-on"),
    count: Number(btn.dataset.count),
    grams: Number(btn.dataset.grams),
    name: btn.dataset.meal,
  });

  const renderDemo = () => {
    const meals = mealBtns.map(readMeal);
    const active = meals.filter((m) => m.on);
    const diners = active.reduce((s, m) => s + m.count, 0);
    const cookKg = active.reduce((s, m) => s + (m.count * m.grams) / 1000 * BUFFER, 0);
    const blindKg = meals.reduce((s, m) => s + (COHORT * m.grams) / 1000 * BUFFER, 0);
    const savedKg = Math.max(blindKg - cookKg, 0);

    tween(rDiners, diners, (v) => `${Math.round(v)}`);
    tween(rCook, cookKg, fmtKg);
    tween(rSaved, savedKg, (v) => `${fmtKg(v)} · ${fmtRs(v * RATE_PER_KG)} saved`);
  };

  mealBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const on = btn.classList.toggle("is-on");
      btn.setAttribute("aria-pressed", String(on));
      renderDemo();
    });
  });

  /* countdown to next cutoff */
  const CUTOFFS = [
    { name: "Breakfast", h: 6, m: 15 },
    { name: "Lunch", h: 9, m: 45 },
    { name: "Snacks", h: 15, m: 15 },
    { name: "Dinner", h: 18, m: 45 },
  ];

  const tickCountdown = () => {
    const now = new Date();
    let target = null;
    let label = "";
    for (const c of CUTOFFS) {
      const t = new Date(now);
      t.setHours(c.h, c.m, 0, 0);
      if (t > now) { target = t; label = c.name; break; }
    }
    if (!target) {
      target = new Date(now);
      target.setDate(target.getDate() + 1);
      target.setHours(6, 15, 0, 0);
      label = "Breakfast";
    }
    const diff = Math.max(0, target - now);
    const hh = String(Math.floor(diff / 3.6e6)).padStart(2, "0");
    const mm = String(Math.floor((diff % 3.6e6) / 6e4)).padStart(2, "0");
    const ss = String(Math.floor((diff % 6e4) / 1000)).padStart(2, "0");
    rNextMeal.textContent = label;
    rCountdown.textContent = `${hh}:${mm}:${ss}`;
  };
  tickCountdown();
  setInterval(tickCountdown, 1000);
  renderDemo();

  /* ---------- scrollytelling: a day on MessMate ---------- */
  const steps = Array.from(document.querySelectorAll(".day-step"));
  const clockEl = document.getElementById("dayClock");
  const phaseEl = document.getElementById("dayPhase");
  const statusEl = document.getElementById("dayStatus");
  const barFill = document.getElementById("dayBarFill");
  const daySection = document.getElementById("day");

  const setStep = (step) => {
    steps.forEach((s) => s.classList.toggle("active", s === step));
    if (!step) return;
    clockEl.textContent = step.dataset.clock;
    phaseEl.textContent = step.dataset.phase;
    statusEl.textContent = step.dataset.status;
  };

  const stepIO = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) setStep(entry.target);
      });
    },
    { rootMargin: "-42% 0px -42% 0px", threshold: 0 }
  );
  steps.forEach((s) => stepIO.observe(s));

  const updateDayBar = () => {
    const rect = daySection.getBoundingClientRect();
    const total = rect.height - window.innerHeight;
    const passed = Math.min(Math.max(-rect.top, 0), Math.max(total, 1));
    barFill.style.width = `${((passed / Math.max(total, 1)) * 100).toFixed(1)}%`;
  };
  window.addEventListener("scroll", updateDayBar, { passive: true });
  updateDayBar();
  setStep(steps[0]);

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll(".faq-item").forEach((item) => {
    const q = item.querySelector(".faq-q");
    const a = item.querySelector(".faq-a");
    q.addEventListener("click", () => {
      const open = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach((other) => {
        if (other !== item) {
          other.classList.remove("open");
          other.querySelector(".faq-q").setAttribute("aria-expanded", "false");
          other.querySelector(".faq-a").style.maxHeight = "0px";
        }
      });
      item.classList.toggle("open", !open);
      q.setAttribute("aria-expanded", String(!open));
      a.style.maxHeight = !open ? `${a.scrollHeight}px` : "0px";
    });
  });

  /* ---------- marquee: duplicate track for seamless loop ---------- */
  const track = document.getElementById("marqueeTrack");
  if (track) track.innerHTML += track.innerHTML;
})();
