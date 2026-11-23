(function () {
  var html = document.documentElement;
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var topOf = function (el) { return el.getBoundingClientRect().top + window.scrollY; };

  // ---------- heure / date réelles sur les téléphones ----------
  function clock() {
    var d = new Date();
    var t = d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", hour12: false });
    $$(".js-time").forEach(function (e) { e.textContent = t; });
    $$(".js-date").forEach(function (e) { e.textContent = d.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" }); });
  }
  clock(); setInterval(clock, 20000);

  // ---------- bouton Download selon l'OS ----------
  var ua = navigator.userAgent, base = "https://github.com/hugobrother/done/releases/latest/download/", pick = null;
  if (/Windows/.test(ua)) pick = ["done-windows.exe", "Windows"];
  else if (/Macintosh/.test(ua) && !("ontouchend" in document)) pick = ["done-mac.zip", "Mac"];
  else if (/Linux/.test(ua) && !/Android/.test(ua)) pick = ["done-linux", "Linux"];
  if (pick) { var b = $("#dl-stage"); b.href = base + pick[0]; b.textContent = "Get done. for " + pick[1]; }

  if (!window.gsap || !window.ScrollTrigger || reduce) { html.classList.add("static"); return; }
  gsap.registerPlugin(ScrollTrigger);
  if (!location.hash) { try { history.scrollRestoration = "manual"; } catch (e) {} window.scrollTo(0, 0); }

  // ---------- titres découpés en mots ----------
  $$(".split").forEach(function (el) {
    var out = "";
    el.childNodes.forEach(function (n) {
      var cls = n.nodeType === 1 ? n.className : "";
      (n.textContent || "").split(/(\s+)/).forEach(function (w) {
        if (!w.trim()) { out += w; return; }
        out += '<span class="w"><span' + (cls ? ' class="' + cls + '"' : "") + ">" + w + "</span></span>";
      });
    });
    el.innerHTML = out;
  });
  var words = function (id) { return $$(id + " .w>span"); };

  // ---------- scroll : verrou + défilement animé ----------
  var locked = false, lockY = 0, tweening = false;
  function prevent(e) { if (locked) e.preventDefault(); }
  window.addEventListener("wheel", prevent, { passive: false });
  window.addEventListener("touchmove", prevent, { passive: false });
  window.addEventListener("keydown", function (e) { if (locked && [32, 33, 34, 35, 36, 38, 40].indexOf(e.keyCode) > -1) e.preventDefault(); });
  window.addEventListener("scroll", function () { if (locked && !tweening && Math.abs(window.scrollY - lockY) > 1) window.scrollTo(0, lockY); });
  function lock(y) { locked = true; lockY = y; html.classList.add("locked"); }
  function unlock() { locked = false; html.classList.remove("locked"); }
  function scrollToY(y, dur, cb) {
    var o = { y: window.scrollY }; tweening = true;
    gsap.to(o, { y: y, duration: dur, ease: "power2.inOut", onUpdate: function () { window.scrollTo(0, o.y); }, onComplete: function () { tweening = false; if (cb) cb(); } });
  }

  // ---------- vibration du téléphone + ondes ----------
  function buzz(root) {
    var ph = root + " .phone";
    gsap.killTweensOf(ph);
    gsap.fromTo(ph, { x: -6, rotation: -1.2 }, { x: 6, rotation: 1.2, duration: 0.045, repeat: 13, yoyo: true, ease: "none", onComplete: function () { gsap.set(ph, { x: 0, rotation: 0 }); } });
    gsap.fromTo(root + " .rings i", { scale: 0.5, opacity: 0.9 }, { scale: 2.5, opacity: 0, duration: 1, stagger: 0.16, ease: "power2.out", overwrite: true });
    gsap.fromTo(root + " .arc", { opacity: 0 }, { opacity: 1, duration: 0.1, yoyo: true, repeat: 5, ease: "none", overwrite: true });
    try { if (navigator.vibrate && navigator.userActivation && navigator.userActivation.hasBeenActive) navigator.vibrate([50, 40, 50]); } catch (e) {}
  }

  // =====================================================================
  // HERO
  // =====================================================================
  function isDesk() { return innerWidth / innerHeight > 1.05 && (innerWidth >= 900 || innerHeight <= 520); }
  function fitHero() {
    var col = $("#hero .h-dev").getBoundingClientRect();
    var s = isDesk() ? Math.min(0.7 * innerHeight / 600, col.width * 0.6 / 290, 1.1)
                     : Math.min(Math.max(col.height, 0.3 * innerHeight) * 0.96 / 600, innerWidth * 0.56 / 290);
    $("#hphone").style.setProperty("--ps", s.toFixed(3));
  }
  fitHero();

  gsap.set("#hphone .tilt", { rotationY: -18, rotationZ: 4 });
  gsap.from(words("#hero h1"), { yPercent: 110, duration: 1.1, ease: "expo.out", stagger: 0.05, delay: 0.15 });
  gsap.from("#hero .k, #hero .pill", { opacity: 0, y: 20, duration: 0.8, ease: "power3.out", stagger: 0.08, delay: 0.6 });
  gsap.from("#hphone", { y: 160, rotationX: 25, opacity: 0, duration: 1.4, ease: "expo.out", delay: 0.3 });
  gsap.from(".float", { scale: 0, opacity: 0, duration: 0.7, ease: "back.out(2)", stagger: 0.15, delay: 1.1 });
  gsap.to(".float.f1", { y: -14, duration: 2.4, yoyo: true, repeat: -1, ease: "sine.inOut" });
  gsap.to(".float.f2", { y: 12, duration: 2.9, yoyo: true, repeat: -1, ease: "sine.inOut" });

  var idle = gsap.timeline({ repeat: -1, repeatDelay: 0.4, delay: 2.1 });
  idle.fromTo("#h-push1", { y: -40, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0)
      .call(buzz, ["#hphone"], 0.05)
      .fromTo("#h-push2", { y: -40, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 2.3)
      .call(buzz, ["#hphone"], 2.35)
      .to("#h-push1, #h-push2", { opacity: 0, y: -20, duration: 0.4, stagger: 0.08 }, 5)
      .to({}, { duration: 0.8 });
  ScrollTrigger.create({ trigger: "#hero", start: "top bottom", end: "bottom top", onToggle: function (s) { if (s.isActive) idle.play(); else idle.pause(); } });

  // parallaxe souris
  if (matchMedia("(pointer: fine)").matches) {
    var hry = gsap.quickTo("#hphone .tilt", "rotationY", { duration: 0.7, ease: "power3" });
    var hrx = gsap.quickTo("#hphone .tilt", "rotationX", { duration: 0.7, ease: "power3" });
    var f1x = gsap.quickTo(".float.f1", "x", { duration: 0.9, ease: "power3" });
    var f2x = gsap.quickTo(".float.f2", "x", { duration: 1.1, ease: "power3" });
    $("#hero").addEventListener("pointermove", function (e) {
      var px = e.clientX / innerWidth - 0.5, py = e.clientY / innerHeight - 0.5;
      hry(-18 + px * 22); hrx(-py * 14); f1x(px * -40); f2x(px * 60);
    });
  }

  // =====================================================================
  // FILM (scroll en pause la 1re fois). Deux façons de le jouer, même montage :
  //  - "video" : le film pré-calculé (film-wide / film-tall). Zéro calcul → fluide sur n'importe quelle machine.
  //              La vidéo sert d'horloge : la timeline GSAP la suit pour les textes, le compteur, la fin.
  //  - "live"  : la scène SVG animée en direct (secours : format d'écran atypique, vidéo refusée ou en erreur).
  // =====================================================================
  var filmEl = $("#film"), svg = $("#film-svg"), camEl = $("#fCam"), bgEl = $("#fBg"), fgEl = $("#ffg");
  var vid = $("#fvid");
  var filmDone = false, filmPlaying = false, replaying = false, ftl, filmEnd, diveTl;
  var mode = "live", vidKind = null, vidReady = false, active = false, amb = [], TL_DUR = 0, DIVE = 0.7;
  var capFade = null, syncing = false, overDone = false, diving = false, vidFailed = false, lite = 0, gT = 0, gN = 0, gS = 0;
  // repère : 1200 unités = largeur de l'écran ; "safe" = zone entre les bandes noires
  var VP = { ppu: 1, safe: 560, cy: 380 };
  function fitFilm() {
    var W = Math.max(filmEl.clientWidth, 1), H = Math.max(filmEl.clientHeight, 1);
    var bt = $("#fbarT").offsetHeight, bb = $("#fbarB").offsetHeight;
    VP.ppu = W / 1200; VP.safe = (H - bt - bb) / VP.ppu; VP.cy = (bt + (H - bt - bb) / 2) / VP.ppu;
    svg.setAttribute("viewBox", "0 0 1200 " + (H / VP.ppu).toFixed(1));
    fitPov();
  }
  // gros plan : le tel dépasse volontairement sous la bande du bas (on cadre le haut de l'écran)
  function fitPov() {
    var W = filmEl.clientWidth, H = filmEl.clientHeight, bt = $("#fbarT").offsetHeight, safe = H - bt - $("#fbarB").offsetHeight;
    var s = isDesk() ? Math.min(W * 0.3 / 290, safe / (600 * 0.7)) : Math.min(W * 0.84 / 290, safe / (600 * 0.74));
    $("#pvFit").style.transform = "translate(" + ((W - 290 * s) / 2).toFixed(1) + "px," + (bt + safe * 0.045).toFixed(1) + "px) scale(" + s.toFixed(4) + ")";
  }
  fitFilm();
  // un cadre = le rectangle de scène qui doit tenir dans l'image (version large / version portrait)
  function F(x, y, w, h) { return { x: x, y: y, lw: Math.log(w), lh: Math.log(h) }; }
  var camD = F(600, 380, 1200, 560), camM = F(600, 380, 1200, 560);
  camD.r = camM.r = 0;
  var shake = { x: 0, y: 0, r: 0 }, hand = { a: 1 }, blurP = { b: 0 };
  function applyCam() {
    var c = isDesk() ? camD : camM, t = ftl ? ftl.time() : 0;   // dérive calée sur le temps du film : rendu identique à chaque lecture
    var z = Math.min(1200 / Math.exp(c.lw), VP.safe / Math.exp(c.lh));
    // caméra à l'épaule : dérive lente, constante à l'écran quel que soit le zoom
    var dx = (Math.sin(t * 0.83) * 6 + Math.sin(t * 0.31 + 1.3) * 9) * hand.a;
    var dy = (Math.cos(t * 0.67) * 5 + Math.sin(t * 0.23 + 0.4) * 5) * hand.a;
    var x = c.x + (dx + shake.x) / z, y = c.y + (dy + shake.y) / z;
    var r = c.r + Math.sin(t * 0.41) * 0.3 * hand.a + shake.r;
    camEl.setAttribute("transform", "translate(600 " + VP.cy.toFixed(2) + ") rotate(" + r.toFixed(3) + ") scale(" + z.toFixed(4) + ") translate(" + (-x).toFixed(2) + " " + (-y).toFixed(2) + ")");
    bgEl.setAttribute("transform", "translate(" + ((x - 600) * 0.1).toFixed(2) + " " + ((y - 380) * 0.05).toFixed(2) + ")");
    fgEl.style.transform = "translate3d(" + (-(x - 620) * z * VP.ppu * 0.5).toFixed(1) + "px," + (-(y - 400) * z * VP.ppu * 0.5).toFixed(1) + "px,0) scale(" + (0.75 + 0.3 * z).toFixed(3) + ")";
    svg.style.filter = blurP.b > 0.4 && !lite ? "blur(" + blurP.b.toFixed(1) + "px)" : "";
    // si le rendu en direct rame : on coupe les détails coûteux, puis on passe à 30 images/s (régulier plutôt que saccadé)
    if (active) {
      var now = performance.now();
      if (gT && now - gT < 250) { gS += now - gT; if (++gN >= 40) { var avg = gS / gN; gS = gN = 0; if (avg > 24 && lite < 2) setLite(lite + 1); } }
      gT = now;
    }
  }
  function setLite(n) { lite = n; filmEl.classList.add("lite" + n); if (n >= 2) gsap.ticker.fps(30); }
  // le rendu en direct ne tourne QUE pendant que le film joue ; à l'arrêt c'est une image fixe, zéro calcul
  function setActive(on) {
    if (on === active) return; active = on; gT = 0;
    if (on) { gsap.ticker.add(applyCam); amb.forEach(function (a) { a.resume(); }); if (lite >= 2) gsap.ticker.fps(30); }
    else { gsap.ticker.remove(applyCam); amb.forEach(function (a) { a.pause(); }); gsap.ticker.fps(0); }
  }
  applyCam();

  (function buildFilm() {
    var J = { back: "#fBack", torso: ".fTorso", head: "#fHead", uArm: "#fUArm", lArm: "#fLArm", uArmF: "#fUArmF", lArmF: "#fLArmF", thigh: "#fThigh", shin: "#fShin", thighF: "#fThighF", shinF: "#fShinF" };
    var ALL = Object.keys(J);
    var A  = { gx: 540, gy: 520, cx: 540, back: 0,   torso: 8,   head: -3,  uArm: -47,  lArm: -37,  uArmF: -40,  lArmF: -48, thigh: -82,  shin: 82,   thighF: -78,  shinF: 80 };
    var G  = { torso: 14, head: 6, uArm: 4, lArm: -108 };
    var B  = { gx: 385, gy: 532, cx: 375, back: -30, torso: -38, head: 22,  uArm: -16,  lArm: -120, uArmF: -18,  lArmF: -72, thigh: -134, shin: 52.6, thighF: -128, shinF: 44 };
    var C  = { gx: 390, gy: 526, cx: 377, back: -20, torso: -20, head: -4,  uArm: -34,  lArm: -112, uArmF: -30,  lArmF: -66, thigh: -124, shin: 66,   thighF: -118, shinF: 60 };   // sursaut léger
    var LD = { gx: 400, gy: 520, cx: 392, back: -2,  torso: 6,   head: 4,   uArm: -70,  lArm: -75,  uArmF: -50,  lArmF: -60, thigh: -82,  shin: 82,   thighF: -78,  shinF: 80 };
    var COOL = "#9DB7FF", WARM = "#FFB48A", HOT = "#FFD9BF";

    ALL.forEach(function (k) { gsap.set(J[k], { svgOrigin: "0 0" }); });
    gsap.set(".fRing, #fMin, #fHour, #fSquash, #fEye, .fStr, #fHem, #fHemF", { svgOrigin: "0 0" });
    gsap.set("#fHoodHem", { svgOrigin: "0 8" });
    gsap.set("#fIris", { svgOrigin: "806 238" });
    $$(".fRing").forEach(function (r) { r.setAttribute("vector-effect", "non-scaling-stroke"); });

    function setPose(p) {
      gsap.set("#fGuy", { x: p.gx, y: p.gy }); gsap.set("#fChair", { x: p.cx });
      ALL.forEach(function (k) { gsap.set(J[k], { rotation: p[k] }); });
      gsap.set(".fStr", { rotation: -p.torso });
    }
    function center(sel) {   // centre d'un élément, en coordonnées de scène
      var r = $(sel).getBoundingClientRect(), pt = svg.createSVGPoint();
      pt.x = r.left + r.width / 2; pt.y = r.top + r.height / 2;
      return pt.matrixTransform(camEl.getScreenCTM().inverse());
    }
    gsap.set("#fHandPhone", { opacity: 1 });
    setPose(B); var phB = center("#fHpBody");
    setPose(A); gsap.set("#fHandPhone", { opacity: 0 });
    gsap.set("#fPhoneLight, #fFlash", { attr: { cx: phB.x, cy: phB.y } });
    gsap.set(".fRing", { x: phB.x, y: phB.y });

    // ---------- état de départ ----------
    gsap.set("#fT1, #fT2", { attr: { width: 0 } });
    gsap.set("#fPrompt", { y: 92 }); gsap.set("#fPromptBg", { opacity: 0 }); gsap.set("#fCaret", { opacity: 1 });
    gsap.set(".fNew, .fTick", { opacity: 0 });
    gsap.set("#fCheck", { scale: 0, transformOrigin: "50% 50%" });
    gsap.set("#fRings", { opacity: 1 }); gsap.set(".fRing", { opacity: 0 });
    gsap.set(".fWheel, #fSend, #fFlash, #fPhoneLight", { transformOrigin: "50% 50%" });
    gsap.set(".fcap span", { opacity: 0 });
    gsap.set("#fpov", { opacity: 0, visibility: "hidden" });
    gsap.set("#pvRig", { rotation: -5, rotationY: 9, transformPerspective: 1500 });
    gsap.set("#pvPush", { yPercent: -180, opacity: 1 });
    gsap.set("#pvHeart", { scale: 0, transformOrigin: "50% 50%" });

    // ---------- ambiance (uniquement pendant la lecture en direct) ----------
    amb.push(gsap.to("#fThink circle", { y: -2.2, duration: 0.3, yoyo: true, repeat: -1, stagger: 0.1, ease: "sine.inOut" }));
    amb.push(gsap.to("#fCaretCode", { opacity: 0, duration: 0.01, repeat: -1, repeatDelay: 0.5, yoyo: true }));
    amb.push(gsap.to("#fClouds", { x: 70, duration: 9, ease: "none", repeat: -1, yoyo: true }));
    amb.push(gsap.to("#fSteam", { y: -6, opacity: 0.12, duration: 1.6, yoyo: true, repeat: -1, ease: "sine.inOut" }));
    amb.push(gsap.to("#fLedFloor", { opacity: 0.4, duration: 1.9, yoyo: true, repeat: -1, ease: "sine.inOut" }));
    amb.push(gsap.to("#fSpill", { opacity: 0.8, duration: 0.11, yoyo: true, repeat: -1, repeatDelay: 1.3, ease: "none" }));
    amb.push(gsap.to(".fTorso", { scaleX: 1.016, scaleY: 1.006, duration: 1.9, yoyo: true, repeat: -1, ease: "sine.inOut" }));   // il respire
    amb.push(gsap.to(".pv-drift", { x: 7, y: -5, rotation: 0.7, duration: 2.3, yoyo: true, repeat: -1, ease: "sine.inOut" }));
    amb.push(gsap.to(".pv-bg", { x: -14, y: 8, duration: 3.1, yoyo: true, repeat: -1, ease: "sine.inOut" }));
    $$(".fMote").forEach(function (m, i) {
      amb.push(gsap.to(m, { x: 30 + (i % 5) * 9, y: -24 - (i % 4) * 10, duration: 5 + (i % 6), yoyo: true, repeat: -1, ease: "sine.inOut", delay: -i }));
    });
    amb.forEach(function (a) { a.pause(); });

    var tl = ftl = gsap.timeline({ paused: true, onUpdate: function () { gsap.set("#fbar", { scaleX: tl.progress() }); }, onComplete: filmOver });
    function toPose(p, at, dur, ease, keys) {
      (keys || ALL).forEach(function (k) { if (p[k] !== undefined) tl.to(J[k], { rotation: p[k], duration: dur, ease: ease }, at); });
      // les tissus suivent avec un temps de retard : cordons, revers du jean, bas du sweat
      if ((!keys || keys.indexOf("torso") > -1) && p.torso !== undefined) {
        tl.to(".fStr", { rotation: -p.torso, duration: Math.max(dur * 3, 0.9), ease: "elastic.out(1.1,0.28)" }, at + 0.03);
        tl.fromTo("#fHoodHem", { rotation: 0 }, { rotation: 5, duration: dur * 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }, at + 0.05);
      }
      if ((!keys || keys.indexOf("shin") > -1) && p.shin !== undefined) {
        tl.fromTo("#fHem, #fHemF", { rotation: 0 }, { rotation: -9, duration: dur * 0.5, ease: "power2.out" }, at)
          .to("#fHem, #fHemF", { rotation: 0, duration: Math.max(dur * 2.5, 0.7), ease: "elastic.out(1.2,0.3)" }, at + dur * 0.5);
      }
    }
    function cap(id, tIn, tOut) {
      tl.fromTo(id, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, tIn);
      if (tOut) tl.to(id, { opacity: 0, y: -18, duration: 0.25, ease: "power2.in" }, tOut);
    }
    function blink(at) { tl.to("#fEye", { scaleY: 0.1, duration: 0.06, yoyo: true, repeat: 1 }, at); }
    function camTo(d, m, at, dur, ease, rot) {
      tl.to(camD, { x: d.x, y: d.y, lw: d.lw, lh: d.lh, r: rot || 0, duration: dur, ease: ease }, at);
      tl.to(camM, { x: m.x, y: m.y, lw: m.lw, lh: m.lh, r: rot || 0, duration: dur, ease: ease }, at);
    }
    function whip(at) { tl.to(blurP, { b: 7, duration: 0.15, ease: "power2.in" }, at).to(blurP, { b: 0, duration: 0.2, ease: "power2.out" }, at + 0.17); }
    function rim(color, at, dur) { tl.to(".rim", { stroke: color, duration: dur }, at); }

    // ============ PLAN 1 — dans l'écran : il écrit son prompt ============
    tl.set(camD, Object.assign(F(1012, 372, 150, 80), { r: 0 }), 0).set(camM, Object.assign(F(1018, 377, 88, 60), { r: 0 }), 0);
    tl.set(".pv-act i.h", { color: "#fff" }, 0).set("#film-svg, #ffg", { visibility: "visible" }, 0);
    camTo(F(1004, 366, 176, 94), F(1016, 374, 98, 70), 0, 1.25, "none");
    cap("#fc1", 0.15, 2.0);
    tl.to("#fT1", { attr: { width: 46 }, duration: 0.5, ease: "steps(17)" }, 0.2)
      .to("#fCaret", { x: 43, duration: 0.5, ease: "steps(17)" }, 0.2)
      .set("#fCaret", { x: 0, y: 7.6 }, 0.72)
      .to("#fT2", { attr: { width: 50 }, duration: 0.48, ease: "steps(18)" }, 0.74)
      .to("#fCaret", { x: 47, duration: 0.48, ease: "steps(18)" }, 0.74)
      .to("#fSend", { scale: 1.5, duration: 0.09, yoyo: true, repeat: 1 }, 1.27)
      .set("#fCaret", { opacity: 0 }, 1.3)
      .to("#fPrompt", { y: 0, duration: 0.3, ease: "power3.out" }, 1.32)
      .to("#fPromptBg", { opacity: 1, duration: 0.2 }, 1.34)
      .to("#fThink", { opacity: 1, duration: 0.2 }, 1.55);
    camTo(F(1002, 320, 210, 120), F(1017, 326, 100, 130), 1.25, 0.5, "power2.inOut");

    // ============ PLAN 2 — la caméra recule : il prend son tel et s'affale ============
    camTo(F(690, 396, 1010, 540), F(462, 410, 550, 520), 1.7, 1.5, "power3.inOut", -0.6);
    toPose(G, 2.05, 0.3, "power2.inOut");
    tl.set("#fDeskPhone", { opacity: 0 }, 2.35).set("#fHandPhone", { opacity: 1 }, 2.35)
      .to("#fGuy", { x: B.gx, y: B.gy, duration: 0.75, ease: "power2.inOut" }, 2.38)
      .to("#fChair", { x: B.cx, duration: 0.75, ease: "power2.inOut" }, 2.38)
      .to(".fWheel", { rotation: -540, duration: 0.75, ease: "power2.inOut" }, 2.38);
    toPose(B, 2.38, 0.7, "power2.inOut", ["torso", "head", "back"]);
    toPose(B, 2.45, 0.6, "power2.inOut", ["uArm", "lArm", "uArmF", "lArmF"]);
    toPose(B, 2.58, 0.6, "back.out(1.7)", ["thigh", "shin", "thighF", "shinF"]);
    tl.to("#fMug", { y: -7, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.out" }, 3.1)
      .to("#fBack", { rotation: B.back - 6, duration: 0.12, yoyo: true, repeat: 1 }, 3.1)
      .to(shake, { y: 5, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, 3.1)
      .to("#fFaceGlow", { opacity: 1, duration: 0.4 }, 2.8)
      .to("#fPhoneLight", { opacity: 0.85, duration: 0.4 }, 2.8);
    cap("#fc2", 2.7, 6.75);
    blink(3.3);

    // ============ LUMIÈRE — le soir tombe (commence à l'image, se termine pendant le gros plan) ============
    var L0 = 3.25, LL = 2.6;
    tl.to("#fGrade", { fill: "#2C3668", opacity: 0.8, duration: LL, ease: "power1.inOut" }, L0)
      .to("#fSun", { y: 80, duration: LL * 0.7, ease: "power1.in" }, L0)
      .to("#fNightSky", { opacity: 1, duration: LL, ease: "power1.inOut" }, L0)
      .to("#fStars, #fMoon, #fCity", { opacity: 1, duration: 0.8 }, L0 + 1.4)
      .to("#fRays", { opacity: 0, duration: LL * 0.7, ease: "power1.in" }, L0)
      .to("#fRays", { rotation: -15, svgOrigin: "235 100", duration: LL * 0.7, ease: "none" }, L0)
      .to("#fSill, #fLongSh, .rimS", { opacity: 0, duration: LL * 0.7 }, L0)
      .to("#fMotes", { opacity: 0.4, duration: LL }, L0)
      .to("#fMin", { rotation: 810, duration: LL + 0.6, ease: "power1.inOut" }, L0)
      .to("#fHour", { rotation: 67, duration: LL + 0.6, ease: "power1.inOut" }, L0)
      .to("#fLampOn", { keyframes: [{ opacity: 0.7, duration: 0.05 }, { opacity: 0.1, duration: 0.07 }, { opacity: 0.85, duration: 0.05 }, { opacity: 0.35, duration: 0.09 }, { opacity: 1, duration: 0.18 }] }, 5.9)
      .to("#fBulb", { fill: "#FFEFD2", duration: 0.3 }, 5.9)
      // hors champ : l'IA termine
      .set("#fThink", { opacity: 0 }, 6.2).set(".fNew, .fTick", { opacity: 1 }, 6.2).set("#fCheck", { scale: 1 }, 6.2)
      .set("#fMonWarm, #fSpillW", { opacity: 1 }, 6.2).set("#fMonCool", { opacity: 0.4 }, 6.2).set(".rim", { stroke: WARM }, 6.2);

    // ============ PLAN 3 — poussée vers lui puis plongée dans le téléphone ============
    camTo(F(500, 412, 760, 400), F(410, 425, 470, 440), 3.2, 0.6, "sine.in", -1.4);
    var P0 = 3.78;
    whip(P0 + 0.14);
    camTo(F(phB.x, phB.y, 170, 120), F(phB.x, phB.y, 120, 170), P0, 0.5, "power3.in", -7);
    tl.set("#fpov", { visibility: "visible" }, P0 + 0.3)
      .fromTo("#fpov", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, P0 + 0.3)
      .fromTo("#pvRig", { scale: 0.45, rotation: -17, y: 70 }, { scale: 1, rotation: -5, y: 0, duration: 0.65, ease: "power3.out" }, P0 + 0.3)
      .fromTo("#pvFeed", { yPercent: 0 }, { yPercent: 0, duration: 0.01 }, P0)
      .set("#film-svg, #ffg", { visibility: "hidden" }, P0 + 0.55);   // la pièce est cachée derrière le gros plan : inutile de la redessiner

    // ============ GROS PLAN — il scrolle des vidéos débiles, les heures filent ============
    tl.to("#ftime", { opacity: 1, duration: 0.25 }, P0 + 0.5)
      .to({ m: 1062 }, { m: 1197, duration: 2.5, ease: "power1.inOut", onUpdate: function () {
        var m = Math.round(this.targets()[0].m), t = Math.floor(m / 60) + ":" + ("0" + (m % 60)).slice(-2);
        $("#ftimeT").textContent = t; $("#pvClock").textContent = t;
      } }, P0 + 0.55)
      .to("#pbSun, #pvHaloS", { opacity: 0, duration: 1.9, ease: "power1.inOut" }, P0 + 0.5)
      .to("#pbNight, #pvHaloN", { opacity: 1, duration: 1.9, ease: "power1.inOut" }, P0 + 0.5)
      .to("#pbLamp", { keyframes: [{ opacity: 0.7, duration: 0.05 }, { opacity: 0.1, duration: 0.07 }, { opacity: 0.85, duration: 0.05 }, { opacity: 0.35, duration: 0.09 }, { opacity: 1, duration: 0.18 }] }, 5.9);
    [4.75, 5.5, 6.2].forEach(function (t, i) {
      tl.to("#pvThumb", { y: -118, x: -8, duration: 0.26, ease: "power2.out" }, t - 0.06)
        .to("#pvThumb", { y: 0, x: 0, duration: 0.36, ease: "power2.inOut" }, t + 0.24)
        .to("#pvFeed", { yPercent: -100 * (i + 1), duration: 0.42, ease: "power3.out" }, t);
    });
    // double-tap : un like sur les briques
    tl.to("#pvThumb", { scale: 0.95, duration: 0.05, yoyo: true, repeat: 3 }, 5.05)
      .fromTo("#pvHeart", { scale: 0, opacity: 1, rotation: -18, y: 0 }, { scale: 1, rotation: 6, duration: 0.26, ease: "back.out(3)" }, 5.1)
      .to("#pvHeart", { opacity: 0, y: -46, duration: 0.3, ease: "power2.in" }, 5.42)
      .set(".pv-act i.h", { color: "#FF3B6B" }, 5.12)
      .fromTo(".pv-act i.h svg", { scale: 1 }, { scale: 1.45, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 5.12);

    // ============ PING — la notif tombe sur l'écran du téléphone ============
    var T = 6.9;
    cap("#fc3", T, T + 1.25);
    tl.fromTo("#fc3", { scale: 0.5 }, { scale: 1, duration: 0.5, ease: "elastic.out(1,0.5)" }, T)
      .to("#pvThumb", { x: 34, y: 40, duration: 0.2, ease: "power2.out" }, T + 0.02)
      .to("#pvDim", { opacity: 0.4, duration: 0.2 }, T)
      .fromTo("#pvPush", { yPercent: -180 }, { yPercent: 0, duration: 0.5, ease: "back.out(1.7)" }, T)
      .fromTo("#pvRig", { x: -7 }, { x: 7, duration: 0.045, repeat: 13, yoyo: true, ease: "none" }, T + 0.12)
      .set("#pvRig", { x: 0 }, T + 0.12 + 0.045 * 14 + 0.01)
      .fromTo("#pvRig .arc", { opacity: 0 }, { opacity: 1, duration: 0.1, yoyo: true, repeat: 5, ease: "none" }, T + 0.12)
      .call(function () {
        var o = $("#fflashHtml"); o.style.setProperty("--fx", "50%"); o.style.setProperty("--fy", "24%");
        try { if (navigator.vibrate && navigator.userActivation && navigator.userActivation.hasBeenActive) navigator.vibrate([50, 40, 50]); } catch (e) {}
      }, null, T)
      .fromTo("#fflashHtml", { opacity: 0.55 }, { opacity: 0, duration: 0.7, ease: "power2.out", immediateRender: false }, T + 0.05)
      .to("#ftime", { opacity: 0, duration: 0.25 }, T + 0.3);

    // ============ DÉZOOM — retour dans la pièce : il fait nuit, l'IA a fini, petit sursaut ============
    var P1 = T + 0.9;
    whip(P1 + 0.1);
    tl.set("#film-svg, #ffg", { visibility: "visible" }, P1 + 0.12)
      .to("#pvRig", { scale: 0.4, rotation: -15, y: 60, duration: 0.36, ease: "power2.in" }, P1)
      .to("#fpov", { opacity: 0, duration: 0.16, ease: "none" }, P1 + 0.2)
      .set("#fpov", { visibility: "hidden" }, P1 + 0.37);
    camTo(F(650, 396, 1010, 540), F(445, 410, 540, 560), P1 + 0.2, 0.6, "back.out(1.15)", -1);
    tl.fromTo("#fCar", { x: -320, opacity: 0 }, { x: 1150, opacity: 1, duration: 1.1, ease: "power1.inOut" }, P1 + 0.5)
      .to("#fCar", { opacity: 0, duration: 0.2 }, P1 + 1.45)
      .fromTo("#fFlash", { scale: 0.4, opacity: 0.9 }, { scale: 3.2, opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, P1 + 0.25);
    $$(".fRing").forEach(function (r, i) {
      tl.fromTo(r, { scale: 0.4, opacity: 0.8 }, { scale: 4.5, opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false }, P1 + 0.25 + i * 0.14);
    });
    var S = P1 + 0.42;
    tl.to("#fGuy", { x: C.gx, y: C.gy, duration: 0.16, ease: "power3.out" }, S)
      .to("#fChair", { x: C.cx, duration: 0.2, ease: "power3.out" }, S);
    toPose(C, S, 0.16, "power3.out");
    tl.to("#fSquash", { scaleY: 1.03, scaleX: 0.985, duration: 0.1, yoyo: true, repeat: 1 }, S)
      .to("#fEye", { scaleY: 1.5, scaleX: 1.3, duration: 0.1 }, S)
      .to("#fBrow", { y: -5, duration: 0.1 }, S)
      .set("#fMouth", { opacity: 0 }, S).set("#fMouthO", { opacity: 1 }, S)
      .to("#fHpBody", { rotation: 10, duration: 0.05, yoyo: true, repeat: 7, ease: "none", transformOrigin: "50% 50%" }, S - 0.1)
      .to(shake, { x: 5, y: -3, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, S);

    // ============ il repose les pieds, roule au bureau : travelling latéral ============
    var Ld = S + 0.5;
    tl.to("#fGuy", { x: LD.gx, y: LD.gy, duration: 0.3, ease: "power2.inOut" }, Ld)
      .to("#fChair", { x: LD.cx, duration: 0.3 }, Ld)
      .to("#fFaceGlow, #fPhoneLight", { opacity: 0, duration: 0.3 }, Ld);
    toPose(LD, Ld, 0.32, "power2.inOut");
    var Rl = Ld + 0.34;
    camTo(F(712, 392, 930, 500), F(640, 405, 600, 520), Rl - 0.1, 0.85, "power2.inOut", 0.4);
    tl.to("#fGuy", { x: A.gx, y: A.gy, duration: 0.6, ease: "back.out(1.2)" }, Rl)
      .to("#fChair", { x: A.cx, duration: 0.6, ease: "back.out(1.2)" }, Rl)
      .to(".fWheel", { rotation: 0, duration: 0.6, ease: "power2.out" }, Rl)
      .to("#fEye", { scaleX: 1, scaleY: 1, duration: 0.15 }, Rl)
      .to("#fBrow", { y: 0, duration: 0.15 }, Rl)
      .set("#fMouthO", { opacity: 0 }, Rl + 0.2)
      .set("#fMouth", { opacity: 1, attr: { d: "M29,-31 Q35,-24 40,-32" } }, Rl + 0.2);
    toPose({ torso: 18 }, Rl, 0.3, "power2.out", ["torso"]);
    toPose(A, Rl + 0.35, 0.4, "power2.inOut", ["torso"]);
    toPose(G, Rl + 0.3, 0.25, "power2.inOut", ["uArm", "lArm"]);
    tl.set("#fHandPhone", { opacity: 0 }, Rl + 0.55).set("#fDeskPhone", { opacity: 1 }, Rl + 0.55);
    toPose(A, Rl + 0.58, 0.25, "power2.out", ["uArm", "lArm", "uArmF", "lArmF", "head", "back", "thigh", "shin", "thighF", "shinF"]);

    // ============ de retour au travail : lente poussée vers l'écran ============
    cap("#fc4", Rl + 0.45, null);
    var Ty = Rl + 0.85;
    var END_D = F(770, 380, 760, 430), END_M = F(685, 400, 530, 500);
    camTo(END_D, END_M, Ty - 0.05, 1.4, "sine.inOut", 0.9);
    tl.to("#fLArm", { rotation: "-=8", duration: 0.07, yoyo: true, repeat: 15 }, Ty)
      .to("#fLArmF", { rotation: "+=8", duration: 0.07, yoyo: true, repeat: 15 }, Ty + 0.03)
      .to("#fHead", { rotation: "+=4", duration: 0.3, yoyo: true, repeat: 1 }, Ty + 0.2)
      .to({}, { duration: 0.15 }, Ty + 1.2);

    TL_DUR = tl.duration();
    // plongée finale dans le badge orange (jouée en direct, ou déjà incluse à la fin de la vidéo)
    diveTl = gsap.timeline({ paused: true })
      .to([camD, camM], { x: 806, y: 238, lw: Math.log(170), lh: Math.log(110), r: 0, duration: DIVE, ease: "power3.in" }, 0)
      .fromTo("#fIris", { opacity: 1, scale: 1 }, { scale: 95, duration: DIVE, ease: "power3.in", immediateRender: false }, 0);

    // état « film vu » : plan final figé, sans aucun texte qui traîne
    filmEnd = function () {
      diveTl.pause(); stopSync(); diving = false;
      gsap.killTweensOf(["#fbarT", "#fbarB"]);          // (jamais killTweensOf sur un élément animé par la timeline : ça tuerait ses plans)
      if (capFade) { capFade.kill(); capFade = null; }
      gsap.set(camD, Object.assign({ r: 0.9 }, END_D)); gsap.set(camM, Object.assign({ r: 0.9 }, END_M));
      gsap.set("#fIris", { opacity: 0, scale: 1 });
      gsap.set("#fbarT, #fbarB", { yPercent: 0, backgroundColor: "#000" });
      gsap.set(".fcap span, #fstate, #ftime", { opacity: 0 });
      gsap.set("#fbar", { scaleX: 0 });
      gsap.set("#film-svg, #ffg", { visibility: "visible" });
      setActive(false);
      if (useVideo()) { setMode("video"); vid.pause(); seekVid(TL_DUR - 0.03); } else { setMode("live"); applyCam(); }
    };
  })();

  // ---------- vidéo ----------
  var VIDS = { wide: 2.4, tall: 0.74 };   // rapport largeur/hauteur des deux rendus
  function vidExt() {
    if (!vid.canPlayType) return null;
    if (vid.canPlayType('video/mp4; codecs="avc1.64002A"')) return "mp4";    // H.264 : décodé par le matériel partout
    if (vid.canPlayType('video/webm; codecs="vp9"')) return "webm";
    return null;
  }
  function pickVideo() {   // la vidéo dont le format colle le mieux à l'écran ; elle remplit l'image (léger rognage),
    var W = filmEl.clientWidth, H = filmEl.clientHeight - $("#fbarT").offsetHeight - $("#fbarB").offsetHeight;   // ou s'affiche entière si l'écran est trop différent
    if (!vidExt() || W < 10 || H < 10) return null;
    var best = null, bf = 0;
    for (var k in VIDS) { var r = (W / H) / VIDS[k], f = Math.min(r, 1 / r); if (f > bf) { bf = f; best = k; } }
    filmEl.classList.toggle("vcontain", bf < 0.74);
    return best;
  }
  function useVideo() { return !!vidKind && vidReady; }
  function seekVid(t) { try { vid.currentTime = t; } catch (e) {} }
  function setMode(m) { if (mode === m) return; mode = m; filmEl.classList.toggle("vmode", m === "video"); if (m === "video") setActive(false); }
  function stopSync() { if (syncing) { gsap.ticker.remove(vsync); syncing = false; } }
  function loadVideo() {
    var k = vidFailed ? null : pickVideo();
    if (k === vidKind) return;
    if (filmPlaying || replaying) return;            // jamais de changement en pleine lecture
    vidKind = k; vidReady = false; setMode("live");
    if (k) { vid.muted = true; vid.src = "film-" + k + "." + vidExt(); vid.load(); } else { vid.removeAttribute("src"); try { vid.load(); } catch (e) {} }
  }
  function videoFail() {   // fichier absent, format refusé, lecture bloquée… → on repasse en direct sans rien casser
    var was = mode === "video" && (filmPlaying || replaying) && !diving;
    vidFailed = true; vidKind = null; vidReady = false; stopSync(); setMode("live");
    if (was) runFilm();
  }
  vid.addEventListener("loadedmetadata", function () {
    vidReady = true;
    if (!filmPlaying && !replaying) { setMode("video"); seekVid(filmDone ? TL_DUR - 0.03 : 0); }
  });
  vid.addEventListener("error", function () { if (vidKind) videoFail(); });
  // au tout premier geste de l'utilisateur, on « débloque » la vidéo pour que le navigateur accepte ensuite de la lancer seule
  var GEST = ["touchend", "pointerup", "click", "keydown"];
  function prime() {
    GEST.forEach(function (n) { window.removeEventListener(n, prime, true); });
    if (!useVideo() || filmPlaying || replaying || !vid.paused) return;
    var p = vid.play();
    if (p && p.then) p.then(function () { if (!syncing) { vid.pause(); seekVid(filmDone ? TL_DUR - 0.03 : 0); } }).catch(function () {});
  }
  GEST.forEach(function (n) { window.addEventListener(n, prime, true); });
  // la vidéo est l'horloge : la timeline (textes, compteur, barre) se cale dessus à chaque image
  function vsync() {
    var t = vid.currentTime;
    if (!overDone) {
      if (t < TL_DUR - 0.02 && !vid.ended) ftl.time(t, false);
      else { overDone = true; ftl.time(TL_DUR - 0.001, false); filmOver(); }
    } else if (diving && (vid.ended || t >= TL_DUR + DIVE - 0.05)) { diving = false; stopSync(); afterDive(); }
  }
  // (re)lance le film depuis le début : en vidéo si elle est prête, sinon en direct
  function runFilm() {
    overDone = false; diving = false; stopSync();
    if (useVideo()) {
      setMode("video"); ftl.pause(0); seekVid(0);
      var p = vid.play();
      if (p && p.catch) p.catch(function (e) {
        if (!(mode === "video" && (filmPlaying || replaying) && vid.paused && !overDone)) return;
        // lecture auto refusée (économie d'énergie…) : elle sera acceptée au prochain geste (le doigt qui se lève) ; sinon direct
        if (e && e.name === "NotAllowedError") { var done = false, go = function () {
          if (done) return; done = true; GEST.forEach(function (n) { window.removeEventListener(n, go, true); });
          if (!(mode === "video" && (filmPlaying || replaying) && vid.paused && !overDone)) return;
          var q = vid.play(); if (q && q.catch) q.catch(videoFail);
        }; GEST.forEach(function (n) { window.addEventListener(n, go, true); });
          gsap.delayedCall(1.6, function () { if (!done) { done = true; GEST.forEach(function (n) { window.removeEventListener(n, go, true); }); if (mode === "video" && vid.paused && (filmPlaying || replaying) && !overDone) videoFail(); } });
        } else videoFail();
      });
      syncing = true; gsap.ticker.add(vsync);
      // garde-fou : si la vidéo n'a pas démarré au bout de 2,5 s (réseau, économie d'énergie…), on joue en direct
      gsap.delayedCall(3.2, function () { if (syncing && !overDone && vid.currentTime < 0.05) videoFail(); });
    } else { setMode("live"); setActive(true); ftl.restart(); }
  }

  function afterDive() {   // l'orange remplit l'écran → page suivante
    gsap.set("#wipe", { display: "block", yPercent: 0, clipPath: "none" });
    filmDone = true; filmPlaying = false;
    var yy = topOf($("#exp")); lockY = yy; window.scrollTo(0, yy); ScrollTrigger.update();
    filmEnd();
    gsap.fromTo("#stageIn", { scale: 1.14 }, { scale: 1, duration: 1.1, ease: "expo.out" });
    gsap.to("#wipe", { yPercent: -100, duration: 0.8, ease: "power4.inOut", onComplete: function () { gsap.set("#wipe", { display: "none" }); unlock(); } });
  }
  // 1re fois : la caméra plonge dans le badge orange qui devient la page suivante
  function finale() {
    capFade = gsap.to("#fstate, .fcap span", { opacity: 0, duration: 0.2 });
    if (mode === "video") {   // la plongée est dans la vidéo ; les bandes virent à l'orange quand l'image est pleine
      diving = true;
      gsap.to("#fbarT, #fbarB", { backgroundColor: "#D97757", duration: 0.12, delay: DIVE - 0.14 });
      return;
    }
    gsap.to("#fbarT", { yPercent: -101, duration: 0.5, ease: "power3.in" });
    gsap.to("#fbarB", { yPercent: 101, duration: 0.5, ease: "power3.in" });
    diveTl.eventCallback("onComplete", afterDive).invalidate().restart();
  }
  function filmOver() {
    if (replaying) {   // relance : on reste sur le plan final
      replaying = false; capFade = gsap.to(".fcap span", { opacity: 0, duration: 0.5, delay: 0.6 });
      if (mode === "video") { vid.pause(); stopSync(); seekVid(TL_DUR - 0.03); } else setActive(false);
    } else finale();
  }
  function skipFilm() { filmDone = true; ftl.progress(1, true); filmEnd(); }
  function startFilm() {   // 1re fois : scroll bloqué, on est obligé de le voir
    if (filmPlaying) return;
    filmPlaying = true; filmDone = false;
    var y = topOf(filmEl);
    lock(y);
    gsap.set(".fcap span", { opacity: 0 });
    ftl.pause(0);
    scrollToY(y, 0.65, function () { gsap.to("#fstate", { opacity: 1, duration: 0.3 }); runFilm(); });
  }
  // ensuite : dès qu'on revient dessus il se relance tout seul, scroll libre
  function replay() { if (filmPlaying || !filmDone || replaying) return; filmEnd(); replaying = true; runFilm(); }
  function stopReplay() { if (!replaying) return; replaying = false; ftl.pause(); ftl.progress(1, true); filmEnd(); }
  if (window.scrollY > topOf(filmEl) + 10) skipFilm();
  ScrollTrigger.create({ trigger: "#film", start: "top 90%", onEnter: function () { if (!filmDone && !filmPlaying) startFilm(); } });
  ScrollTrigger.create({ trigger: "#film", start: "top 45%", end: "bottom 55%", onEnter: replay, onEnterBack: replay, onLeave: stopReplay, onLeaveBack: stopReplay });
  loadVideo();
  window.__doneFilm = { tl: ftl, dive: diveTl, amb: amb, cam: applyCam, dur: TL_DUR, mode: function () { return mode + (lite ? " lite" + lite : ""); } };

  // liens internes : on saute le film et on défile en douceur
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var t = document.getElementById(a.getAttribute("href").slice(1));
      if (!t || locked) { e.preventDefault(); return; }
      e.preventDefault();
      if (!filmDone) skipFilm();
      scrollToY(Math.max(0, topOf(t)), 1);
    });
  });

  // =====================================================================
  // EXPERIENCE (pilotée par le scroll) : zones texte / appareils séparées
  // =====================================================================
  var stage = $("#stage"), ctx = null;
  var PH = { w: 290, h: 600 }, LP = { w: 728, h: 412 }, PO = { w: 350, h: 84 };

  function layout() {
    var W = stage.clientWidth, H = stage.clientHeight, desk = isDesk(), o = { desk: desk };
    var rel = function (cx, cy, s, extra) { var r = { x: cx - W / 2, y: cy - H / 2, scale: s }; if (extra) for (var k in extra) r[k] = extra[k]; return r; };
    if (desk) {
      var zw = 0.46 * W, zt = Math.max(0.14 * H, 66), zb = 0.93 * H, zh = zb - zt, zcy = zt + zh / 2;
      var zr = { l: 0.50 * W, r: 0.96 * W }, zl = { l: 0.04 * W, r: 0.50 * W };
      // VP1 : ordi + tel dans une zone large à droite (le tel passe devant le coin de l'ordi)
      var z1 = { l: 0.44 * W, r: 0.97 * W }, zw1 = z1.r - z1.l, K = 0.8, OV = 150;
      var sL = Math.min(zw1 / (LP.w + PH.w * K - OV), zh * 0.62 / LP.h), sP = sL * K;
      var lapW = LP.w * sL, lapH = LP.h * sL, phW = PH.w * sP, phH = PH.h * sP;
      var groupW = lapW + phW - OV * sL, gx0 = z1.l + (zw1 - groupW) / 2;
      var lapCx = gx0 + lapW / 2, lapCy = zcy - 0.05 * H;
      var phCx = gx0 + groupW - phW / 2, phCy = Math.min(lapCy + lapH / 2 + 0.07 * H, zb) - phH / 2;
      var ps1 = Math.min(1.05, (zw1 - 16) / PO.w);
      o.vp1 = { laptop: rel(lapCx, lapCy, sL), phone: rel(phCx, phCy, sP, { rotateY: -10, rotateZ: 2 }),
                pop: rel(Math.min(phCx - phW * 0.25, z1.r - PO.w * ps1 / 2), Math.max(phCy - phH / 2 - PO.h * ps1 * 0.2, zt + PO.h * ps1 / 2), ps1, { rotation: -3 }),
                popFrom: rel(phCx, phCy - phH * 0.34, 0.2, { rotation: 0 }) };
      // VP2 : tel dans la zone de gauche, la notif jaillit vers la droite
      var s2 = Math.min(zh * 0.92 / PH.h, 1.15), w2 = PH.w * s2, h2 = PH.h * s2, cx2 = zl.l + zw * 0.40, ps2 = 1.22;
      o.vp2 = { phone: rel(cx2, zcy, s2, { rotateY: 8, rotateZ: -3 }),
                pop: rel(Math.min(cx2 + w2 * 0.5 + 30, 0.53 * W - PO.w * ps2 / 2), zcy - h2 * 0.27, ps2, { rotation: -5 }),
                popFrom: rel(cx2, zcy - h2 * 0.34, 0.25, { rotation: 0 }) };
      // VP3 : tel dans la zone de droite
      var cx3 = zr.l + zw * 0.60, ps3 = 1.08;
      o.vp3 = { phone: rel(cx3, zcy, s2, { rotateY: -12, rotateZ: 3 }),
                pop: rel(Math.max(cx3 - w2 * 0.5 - 20, 0.5 * W + PO.w * ps3 / 2 + 8), zcy - h2 * 0.33, ps3, { rotation: 4 }),
                popFrom: rel(cx3, zcy - h2 * 0.34, 0.25, { rotation: 0 }) };
      // WHO : légende en haut, tel petit en bas, profils autour
      var zt4 = 0.45 * H, zb4 = 0.97 * H, s4 = (zb4 - zt4) * 0.98 / PH.h, w4 = PH.w * s4, cy4 = (zt4 + zb4) / 2;
      var off = w4 / 2 + 36 + 150;
      o.who = { phone: rel(W / 2, cy4, s4, { rotateY: 0, rotateZ: 0 }),
                chips: [rel(W / 2 - off, cy4 - 0.13 * H, 1), rel(W / 2 + off, cy4 - 0.02 * H, 1), rel(W / 2 - off + 30, cy4 + 0.12 * H, 1)] };
      o.cta = { phone: rel(W / 2, -H * 0.9, s4, { rotateY: 0, rotateZ: -14 }) };
    } else {
      var mt = 0.41 * H, mb = 0.975 * H, mh = mb - mt, mcy = mt + mh / 2;
      var msL = Math.min((W - 24) / (LP.w - 60), mh * 0.5 / LP.h), mlW = LP.w * msL, mlH = LP.h * msL;
      var msP = Math.min(mh * 0.62 / PH.h, 0.42 * W / PH.w), mpW = PH.w * msP, mpH = PH.h * msP;
      var mphCx = W - 14 - mpW / 2, mphCy = mb - mpH / 2 - 2;
      var mps = Math.min(1, (W - 24) / PO.w);
      o.vp1 = { laptop: rel(W / 2 - 8, mt + mlH / 2 + 4, msL), phone: rel(mphCx, mphCy, msP, { rotateY: 0, rotateZ: 2 }),
                pop: rel(Math.min(mphCx - 20, W - 12 - PO.w * mps / 2), mphCy - mpH / 2 + 36, mps, { rotation: -2 }),
                popFrom: rel(mphCx, mphCy - mpH * 0.34, 0.2, { rotation: 0 }) };
      var ms = Math.min(mh * 0.97 / PH.h, 0.66 * W / PH.w), mH2 = PH.h * ms, mp2 = Math.min(1.1, (W - 20) / PO.w);
      o.vp2 = { phone: rel(W / 2, mcy, ms, { rotateY: 0, rotateZ: -2 }), pop: rel(W / 2, mcy - mH2 * 0.3, mp2, { rotation: -3 }), popFrom: rel(W / 2, mcy - mH2 * 0.36, 0.25, { rotation: 0 }) };
      o.vp3 = { phone: rel(W / 2, mcy, ms, { rotateY: 0, rotateZ: 2 }), pop: rel(W / 2, mcy - mH2 * 0.3, mp2, { rotation: 3 }), popFrom: rel(W / 2, mcy - mH2 * 0.36, 0.25, { rotation: 0 }) };
      var s4m = Math.min((mb - (mt + 206)) * 0.98 / PH.h, 0.5), h4m = PH.h * s4m;
      o.who = { phone: rel(W / 2, mb - h4m / 2 - 2, s4m, { rotateY: 0, rotateZ: 0 }),
                chips: [rel(W / 2, mt + 34, 1), rel(W / 2, mt + 100, 1), rel(W / 2, mt + 166, 1)] };
      o.cta = { phone: rel(W / 2, -H * 0.9, s4m, { rotateY: 0, rotateZ: -14 }) };
    }
    return o;
  }

  function buildExp() {
    ctx = gsap.context(function () {
      var o = layout(), tl;
      gsap.set("#phone", o.vp1.phone);
      gsap.set("#laptop", Object.assign({ opacity: 1 }, o.vp1.laptop));
      gsap.set("#pop", Object.assign({ opacity: 0 }, o.vp1.popFrom));
      gsap.set("#c1", { opacity: 1 });
      gsap.set("#pm1", { opacity: 1 }); gsap.set("#pm2, #pm3", { opacity: 0 });
      gsap.set(".chip", { xPercent: -50, yPercent: -50, opacity: 0 });

      tl = gsap.timeline({
        defaults: { ease: "power2.inOut" },
        scrollTrigger: { trigger: "#exp", start: "top top", end: "bottom bottom", scrub: 0.8,
          onUpdate: function (s) { gsap.set("#progress", { scaleX: s.progress }); } }
      });
      function capIn(id, at) {
        tl.set(id, { opacity: 1 }, at)
          .fromTo(words(id), { yPercent: 110 }, { yPercent: 0, duration: 0.5, stagger: 0.03, ease: "power3.out", immediateRender: false }, at)
          .fromTo(id + " .k, " + id + " .sub, " + id + " .cta-btns", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, immediateRender: false }, at + 0.15);
      }
      function capOut(id, at) {
        tl.to(words(id), { yPercent: -110, duration: 0.4, stagger: 0.02, ease: "power2.in" }, at)
          .to(id + " .k, " + id + " .sub", { opacity: 0, y: -12, duration: 0.3 }, at)
          .set(id, { opacity: 0 }, at + 0.45);
      }
      function screen(id, at) {
        tl.to("#phone .scr:not(" + id + ")", { opacity: 0, duration: 0.25 }, at).to(id, { opacity: 1, duration: 0.25 }, at);
      }
      function ping(at, sc, silent) {
        tl.fromTo("#pop", Object.assign({ opacity: 0 }, sc.popFrom), Object.assign({ opacity: 1, duration: 0.4, ease: "back.out(1.7)", immediateRender: false }, sc.pop), at);
        if (!silent) tl.call(function () { if (tl.scrollTrigger && tl.scrollTrigger.direction > 0) buzz("#phone"); }, null, at + 0.03);
      }
      function unping(at, sc) { tl.to("#pop", Object.assign({ opacity: 0, duration: 0.25, ease: "power2.in" }, sc.popFrom), at); }
      function toggle(id, at) {
        tl.to(id, { backgroundColor: "#D97757", duration: 0.2 }, at).to(id + " i", { x: 18, duration: 0.25, ease: "back.out(1.6)" }, at);
      }
      function typed(text) {
        var st = { n: 0 };
        return gsap.to(st, { n: text.length, ease: "none", duration: 0.5, onUpdate: function () { $("#typed").textContent = Array.from(text).slice(0, Math.round(st.n)).join(""); } });
      }

      // ---- VP1 : l'IA réfléchit, tu es prévenu quand elle a besoin de toi puis quand elle a fini ----
      tl.to("#umsg", { clipPath: "inset(0 0 0 0%)", duration: 0.5, ease: "power1.out" }, 0.15)
        .to("#arrow", { opacity: 0, duration: 0.1 }, 0.65).to("#stop", { opacity: 1, duration: 0.1 }, 0.65)
        .to("#ai", { opacity: 1, duration: 0.2 }, 0.7)
        .fromTo("#dlg", { opacity: 0, y: 12, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)", immediateRender: false }, 1.1);
      ping(1.25, o.vp1);
      tl.to("#allow", { scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }, 1.9)
        .to("#dlg", { opacity: 0, y: -10, duration: 0.2 }, 2.0);
      unping(2.0, o.vp1);
      tl.to("#dots", { opacity: 0, duration: 0.1 }, 2.15)
        .to("#lines i", { scaleX: 1, duration: 0.25, stagger: 0.07, ease: "power2.out" }, 2.15)
        .to("#stop", { opacity: 0, duration: 0.1 }, 2.45).to("#arrow", { opacity: 1, duration: 0.1 }, 2.45)
        .set("#pm1", { opacity: 0 }, 2.42).set("#pm2", { opacity: 1 }, 2.42);
      ping(2.5, o.vp1);
      capOut("#c1", 3.0); unping(3.0, o.vp1);

      // ---- VP2 : tu scrolles, la notif jaillit du téléphone ----
      tl.to("#laptop", { opacity: 0, x: "-=80", duration: 0.5 }, 3.05)
        .to("#phone", Object.assign({ duration: 0.8 }, o.vp2.phone), 3.05)
        .to("#stage", { backgroundColor: "#1B1210", duration: 0.6 }, 3.05)
        .to("#glow", { x: o.vp2.phone.x, scale: 1.2, duration: 0.8 }, 3.05);
      screen("#s-feed", 3.2);
      capIn("#c2", 3.45);
      ping(4.2, o.vp2);
      tl.to("#stage", { backgroundColor: "#3A1D12", duration: 0.12, yoyo: true, repeat: 1 }, 4.2);
      capOut("#c2", 5.6); unping(5.6, o.vp2);

      // ---- VP3 : tes réglages, fond clair ----
      tl.to("#stage", { backgroundColor: "#F3EEE6", color: "#141413", duration: 0.6 }, 5.75)
        .to("#glow", { opacity: 0.35, x: o.vp3.phone.x, duration: 0.6 }, 5.75)
        .to("#phone", Object.assign({ duration: 0.8 }, o.vp3.phone), 5.75);
      screen("#s-set", 5.95);
      capIn("#c3", 6.2);
      toggle("#tg1", 6.6); toggle("#tg2", 6.85);
      tl.to("#knob", { xPercent: 100, duration: 0.25, ease: "back.out(1.4)" }, 7.2)
        .to("#segA", { color: "#141413", duration: 0.2 }, 7.2).to("#segB", { color: "#ffffff", duration: 0.2 }, 7.2)
        .to("#wave", { scaleY: 0.14, opacity: 0.45, duration: 0.3 }, 7.2)
        .to("#dur0", { opacity: 0, duration: 0.15 }, 7.55).to("#dur2", { opacity: 1, duration: 0.15 }, 7.55)
        .add(typed("Your answer is ready 🎉"), 7.75)
        .set("#pm2", { opacity: 0 }, 8.3).set("#pm3", { opacity: 1 }, 8.3);
      ping(8.4, o.vp3, true); // réglé sur « Silent » : pas de vibration
      capOut("#c3", 9.2); unping(9.2, o.vp3);

      // ---- REASSURANCE : pour qui ----
      tl.to("#stage", { backgroundColor: "#141413", color: "#FAF9F5", duration: 0.6 }, 9.3)
        .to("#glow", { opacity: 1, x: 0, scale: 1.1, duration: 0.6 }, 9.3)
        .to("#phone", Object.assign({ duration: 0.8 }, o.who.phone), 9.3);
      screen("#s-lock", 9.45);
      capIn("#c4", 9.7);
      ["#p1", "#p2", "#p3"].forEach(function (id, i) {
        tl.fromTo(id, { x: o.who.phone.x, y: o.who.phone.y, scale: 0.5, opacity: 0 },
          { x: o.who.chips[i].x, y: o.who.chips[i].y, scale: 1, opacity: 1, duration: 0.55, ease: "back.out(1.5)", immediateRender: false }, 9.95 + i * 0.2);
      });
      capOut("#c4", 11.3);
      tl.to(".chip", { opacity: 0, scale: 0.6, duration: 0.4, stagger: 0.05 }, 11.3);

      // ---- CTA ----
      tl.to("#phone", Object.assign({ duration: 0.8, ease: "power3.in" }, o.cta.phone), 11.4)
        .to("#stage", { backgroundColor: "#D97757", color: "#141413", duration: 0.6 }, 11.6)
        .to("#glow", { opacity: 0, duration: 0.4 }, 11.6);
      capIn("#c5", 12.0);
      tl.to({}, { duration: 0.9 }, 12.6);
    });
  }
  buildExp();

  // légère inclinaison du téléphone avec la souris
  if (matchMedia("(pointer: fine)").matches) {
    var ery = gsap.quickTo("#phone .tilt", "rotationY", { duration: 0.8, ease: "power3" });
    var erx = gsap.quickTo("#phone .tilt", "rotationX", { duration: 0.8, ease: "power3" });
    stage.addEventListener("pointermove", function (e) { ery((e.clientX / innerWidth - 0.5) * 12); erx(-(e.clientY / innerHeight - 0.5) * 8); });

    // curseur + bouton magnétique
    var cur = $("#cursor"), cx = gsap.quickTo(cur, "x", { duration: 0.25, ease: "power3" }), cy = gsap.quickTo(cur, "y", { duration: 0.25, ease: "power3" });
    window.addEventListener("pointermove", function (e) { gsap.set(cur, { opacity: 1 }); cx(e.clientX); cy(e.clientY); });
    $$("a, button, summary").forEach(function (el) {
      el.addEventListener("pointerenter", function () { gsap.to(cur, { scale: 3.2, duration: 0.25 }); });
      el.addEventListener("pointerleave", function () { gsap.to(cur, { scale: 1, duration: 0.25 }); });
    });
    $$(".magnet").forEach(function (el) {
      el.addEventListener("pointermove", function (e) { var r = el.getBoundingClientRect(); gsap.to(el, { x: (e.clientX - r.left - r.width / 2) * 0.35, y: (e.clientY - r.top - r.height / 2) * 0.45, duration: 0.3 }); });
      el.addEventListener("pointerleave", function () { gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1,0.4)" }); });
    });
  }

  // ---------- redimensionnement : on recalcule les zones ----------
  var rt, lastW = innerWidth, lastH = innerHeight;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      if (innerWidth === lastW && Math.abs(innerHeight - lastH) < 120) return; // barre d'adresse mobile : on ignore
      lastW = innerWidth; lastH = innerHeight;
      fitHero(); fitFilm(); loadVideo();
      if (ctx) ctx.revert();
      buildExp(); ScrollTrigger.refresh();
    }, 200);
  });
})();
