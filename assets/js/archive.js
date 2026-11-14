/* THE INDEX — progressive enhancement.
   Everything below is optional: with JS off the site is fully readable. */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Theme: paper / night ---------- */
  var themeBtn = $("[data-theme-toggle]");
  var themeMeta = $('meta[name="theme-color"]');
  function applyTheme(name, announce) {
    root.setAttribute("data-theme", name);
    if (themeMeta) themeMeta.setAttribute("content", name === "night" ? "#161411" : "#f2ecdf");
    if (themeBtn) {
      var night = name === "night";
      themeBtn.setAttribute("aria-pressed", String(night));
      themeBtn.setAttribute("aria-label", night ? "Turn the lights on" : "Turn the lights off");
      themeBtn.setAttribute("title", night ? "Lights on" : "Lights off");
      var label = $(".iconbtn__label", themeBtn);
      if (label) label.textContent = night ? "Lights on" : "Lights off";
    }
    if (announce) store.set("pv-theme", name);
  }
  var savedTheme = store.get("pv-theme");
  var systemNight = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(savedTheme || (systemNight ? "night" : "paper"), false);
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      applyTheme(root.getAttribute("data-theme") === "night" ? "paper" : "night", true);
    });
  }

  /* ---------- Plain / recruiter mode ---------- */
  var plainBtns = $$("[data-plain-toggle]");
  var resumeBtn = $("[data-resume-link]");
  var details = $$("details.record");
  function setPlain(on, persist) {
    root.setAttribute("data-plain", String(on));
    plainBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String(on));
      b.setAttribute("title", on ? "Back to the archive view" : "Plain, recruiter-friendly view");
      var l = $(".mode__label", b);
      if (l) l.textContent = "Plain view";
    });
    if (resumeBtn) resumeBtn.setAttribute("aria-label", on ? "Open the one-page résumé" : "Open the résumé");
    if (on) {
      details.forEach(function (d) {
        if (!d.open) { d.dataset.wasOpen = "0"; d.open = true; }
        else { d.dataset.wasOpen = "1"; }
      });
    } else {
      details.forEach(function (d) {
        if (d.dataset.wasOpen === "0") d.open = false;
        delete d.dataset.wasOpen;
      });
    }
    if (persist) store.set("pv-plain", on ? "1" : "0");
  }
  setPlain(store.get("pv-plain") === "1", false);
  plainBtns.forEach(function (b) {
    b.addEventListener("click", function () { setPlain(root.getAttribute("data-plain") !== "true", true); });
  });
  $$("[data-plain-off]").forEach(function (b) {
    b.addEventListener("click", function () { setPlain(false, true); });
  });

  /* ---------- Author card drawer ---------- */
  var cabinet = $("[data-drawer]");
  if (cabinet) {
    var handle = $(".cabinet__handle", cabinet);
    var cardBack = $(".card__face--back", cabinet);
    var setDrawer = function (open) {
      cabinet.setAttribute("data-open", String(open));
      if (cardBack) {
        if (open) cardBack.removeAttribute("inert");
        else cardBack.setAttribute("inert", "");
      }
      if (handle) {
        handle.setAttribute("aria-expanded", String(open));
        var t = $(".cabinet__handle-text", handle);
        if (t) t.textContent = open ? "Turn the card back" : "Turn the card over";
      }
    };
    setDrawer(cabinet.getAttribute("data-open") === "true");
    if (handle) {
      handle.addEventListener("click", function () {
        setDrawer(cabinet.getAttribute("data-open") !== "true");
      });
    }
  }

  /* ---------- Mobile navigation ---------- */
  var menuBtn = $(".menu");
  var nav = $("#site-nav");
  if (menuBtn && nav) {
    var lastFocus = null;
    var setNav = function (open) {
      nav.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
      if (open) {
        lastFocus = document.activeElement;
        var first = $("a", nav);
        if (first) first.focus();
      } else if (lastFocus) {
        lastFocus.focus();
      }
    };
    menuBtn.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
    $$("a", nav).forEach(function (a) {
      a.addEventListener("click", function () { setNav(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) setNav(false);
      if (e.key === "Tab" && nav.classList.contains("is-open")) {
        var f = $$("a", nav).filter(function (a) { return a.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    document.addEventListener("click", function (e) {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(e.target) || menuBtn.contains(e.target)) return;
      setNav(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 880 && nav.classList.contains("is-open")) setNav(false);
    });
  }

  /* ---------- Scroll spy + reading progress ---------- */
  var navLinks = $$('#site-nav a[href^="#"]');
  var sections = navLinks.map(function (a) {
    return document.getElementById(a.getAttribute("href").slice(1));
  }).filter(Boolean).sort(function (a, b) {
    return a.compareDocumentPosition(b) & 4 ? -1 : 1;
  });
  var syncNav = function () {
    if (!sections.length) return;
    var line = window.scrollY + window.innerHeight * 0.35;
    var current = null;
    sections.forEach(function (s) {
      var top = s.getBoundingClientRect().top + window.scrollY;
      if (top <= line) current = s;
    });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8) {
      current = sections[sections.length - 1];
    }
    navLinks.forEach(function (a) {
      if (current && a.getAttribute("href") === "#" + current.id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  };

  var bar = $(".progress span");
  if (bar) {
    var ticking = false;
    var draw = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + "%";
      syncNav();
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(draw); }
    }, { passive: true });
    draw();
  } else if (sections.length) {
    window.addEventListener("scroll", syncNav, { passive: true });
    syncNav();
  }
  window.addEventListener("hashchange", function () {
    window.setTimeout(syncNav, 60);
  });
  window.addEventListener("load", syncNav);

  /* ---------- Record search + filters ---------- */
  var tools = $("[data-tools]");
  var records = $$(".record");
  if (tools && records.length) {
    var input = $("[data-search]", tools);
    var chips = $$("[data-filter]", tools);
    var count = $("[data-count]", tools);
    var empty = $("[data-empty]");
    var activeFilter = "all";

    var matches = function (rec, q) {
      if (activeFilter !== "all" && (rec.dataset.tags || "").indexOf(activeFilter) === -1) return false;
      if (!q) return true;
      return (rec.textContent || "").toLowerCase().indexOf(q) !== -1;
    };
    var update = function () {
      var q = (input && input.value || "").trim().toLowerCase();
      var shown = 0;
      records.forEach(function (rec) {
        var ok = matches(rec, q);
        if (ok) { rec.removeAttribute("hidden"); shown++; }
        else { rec.setAttribute("hidden", ""); }
      });
      if (count) count.textContent = shown + (shown === 1 ? " record" : " records");
      if (empty) empty.hidden = shown !== 0;
    };
    if (input) input.addEventListener("input", update);
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        activeFilter = chip.dataset.filter;
        chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
        update();
      });
    });
    var clearBtn = $("[data-clear]");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        if (input) { input.value = ""; input.focus(); }
        activeFilter = "all";
        chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.filter === "all")); });
        update();
      });
    }
    document.addEventListener("keydown", function (e) {
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") {
        e.preventDefault();
        if (input) input.focus();
      }
      if (e.key === "Escape" && document.activeElement === input) {
        input.value = "";
        update();
        input.blur();
      }
    });
    update();
  }

  /* ---------- Copy email ---------- */
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var value = btn.getAttribute("data-copy");
      var status = $("[data-copy-status]");
      var done = function () {
        if (status) { status.textContent = "Copied " + value; setTimeout(function () { status.textContent = ""; }, 2600); }
        btn.setAttribute("aria-label", "Email address copied");
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done, function () { window.location.href = "mailto:" + value; });
      } else {
        window.location.href = "mailto:" + value;
      }
    });
  });

  /* ---------- Details: reflect state for styling (no-op for a11y) ---------- */
  $$("details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) d.setAttribute("data-state", "open");
      else d.removeAttribute("data-state");
    });
  });
})();
