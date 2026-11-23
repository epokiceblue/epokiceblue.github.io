/* Zvětšení fotek v galerii (svatby, portréty, produkty). Koláže se nezvětšují.
   Klik na fotku ji otevře přes obrazovku na poloprůhledném tmavém pozadí.
   Další/předchozí: šipky, klávesy ← →, přejetí prstem. Zavřít: křížek, Esc, klik vedle fotky. */
(function () {
    var fotky = [].slice.call(document.querySelectorAll('.image-gallery img'));
    if (!fotky.length) return;

    var css = '' +
        '.image-gallery img{cursor:zoom-in;}' +
        '.sz-lb{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center;' +
        'background:rgba(15,15,15,.6);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);' +
        'opacity:0;transition:opacity .25s ease;touch-action:pan-y;}' +
        '.sz-lb.sz-videt{opacity:1;}' +
        '.sz-lb img{max-width:calc(100vw - 160px);max-height:calc(100vh - 80px);width:auto;height:auto;display:block;' +
        'box-shadow:0 12px 40px rgba(0,0,0,.35);transition:opacity .2s ease;user-select:none;-webkit-user-drag:none;cursor:default;}' +
        '.sz-lb button{position:absolute;background:transparent;border:1.5px solid #F7F4EE;color:#F7F4EE;border-radius:50%;' +
        'width:48px;height:48px;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;transition:background .2s;}' +
        '.sz-lb button:hover{background:rgba(247,244,238,.15);}' +
        '.sz-lb button svg{width:22px;height:22px;}' +
        '.sz-lb .sz-lb-zavrit{top:20px;right:20px;}' +
        '.sz-lb .sz-lb-pred{left:24px;top:50%;transform:translateY(-50%);}' +
        '.sz-lb .sz-lb-dalsi{right:24px;top:50%;transform:translateY(-50%);}' +
        '@media (max-width:768px){.sz-lb img{max-width:100vw;max-height:calc(100vh - 140px);}' +
        '.sz-lb .sz-lb-pred,.sz-lb .sz-lb-dalsi{top:auto;bottom:20px;transform:none;}' +
        '.sz-lb .sz-lb-pred{left:calc(50% - 60px);}.sz-lb .sz-lb-dalsi{right:calc(50% - 60px);}' +
        '.sz-lb .sz-lb-zavrit{top:14px;right:14px;}}' +
        '@media (prefers-reduced-motion:reduce){.sz-lb,.sz-lb img{transition:none;}}';
    var styl = document.createElement('style');
    styl.textContent = css;
    document.head.appendChild(styl);

    var sipka = function (d) {
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + d + '"/></svg>';
    };
    var lb = null, obr, poradi = [], i = 0, predtimFokus = null, startX = null, startY = null;

    // pořadí fotek tak, jak jdou na stránce shora dolů (galerie skládá fotky do sloupců)
    function seradit() {
        return fotky.slice().sort(function (a, b) {
            var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
            return (ra.top - rb.top) || (ra.left - rb.left);
        });
    }
    function zdroj(img) { return img.currentSrc || img.src; }
    function ukaz(n) {
        i = (n + poradi.length) % poradi.length;
        var f = poradi[i];
        obr.style.opacity = '0';
        var nove = new Image();
        nove.onload = nove.onerror = function () { obr.src = nove.src; obr.alt = f.alt || ''; obr.style.opacity = '1'; };
        nove.src = zdroj(f);
        // předem načíst sousední fotky, ať přepínání neblikne
        [i + 1, i - 1].forEach(function (k) { var s = poradi[(k + poradi.length) % poradi.length]; if (s) { var p = new Image(); p.src = zdroj(s); } });
    }
    function otevri(img) {
        poradi = seradit();
        predtimFokus = document.activeElement;
        lb = document.createElement('div');
        lb.className = 'sz-lb';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-modal', 'true');
        lb.setAttribute('aria-label', 'Zvětšená fotka');
        lb.innerHTML =
            '<img alt="">' +
            '<button type="button" class="sz-lb-pred" aria-label="Předchozí fotka">' + sipka('M15 5l-7 7 7 7') + '</button>' +
            '<button type="button" class="sz-lb-dalsi" aria-label="Další fotka">' + sipka('M9 5l7 7-7 7') + '</button>' +
            '<button type="button" class="sz-lb-zavrit" aria-label="Zavřít">' + sipka('M6 6l12 12M18 6L6 18') + '</button>';
        obr = lb.querySelector('img');
        document.body.appendChild(lb);
        document.documentElement.style.overflow = 'hidden';
        lb.querySelector('.sz-lb-pred').addEventListener('click', function (e) { e.stopPropagation(); ukaz(i - 1); });
        lb.querySelector('.sz-lb-dalsi').addEventListener('click', function (e) { e.stopPropagation(); ukaz(i + 1); });
        lb.querySelector('.sz-lb-zavrit').addEventListener('click', zavri);
        lb.addEventListener('click', function (e) { if (e.target === lb) zavri(); });
        obr.addEventListener('click', function (e) { e.stopPropagation(); });
        lb.addEventListener('touchstart', function (e) { var t = e.touches[0]; startX = t.clientX; startY = t.clientY; }, { passive: true });
        lb.addEventListener('touchend', function (e) {
            if (startX === null) return;
            var t = e.changedTouches[0], dx = t.clientX - startX, dy = t.clientY - startY;
            startX = null;
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) ukaz(dx < 0 ? i + 1 : i - 1);
            else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) zavri(); // stažení dolů zavře
        });
        document.addEventListener('keydown', klavesy);
        ukaz(poradi.indexOf(img));
        requestAnimationFrame(function () { lb.classList.add('sz-videt'); });
        lb.querySelector('.sz-lb-zavrit').focus({ preventScroll: true });
    }
    function zavri() {
        if (!lb) return;
        var stary = lb;
        lb = null;
        document.removeEventListener('keydown', klavesy);
        document.documentElement.style.overflow = '';
        stary.classList.remove('sz-videt');
        setTimeout(function () { stary.remove(); }, 250);
        if (predtimFokus && predtimFokus.focus) predtimFokus.focus({ preventScroll: true });
    }
    function klavesy(e) {
        if (e.key === 'Escape') zavri();
        else if (e.key === 'ArrowRight') ukaz(i + 1);
        else if (e.key === 'ArrowLeft') ukaz(i - 1);
        else if (e.key === 'Tab') { // fokus zůstává v okně
            var b = [].slice.call(lb.querySelectorAll('button')), k = b.indexOf(document.activeElement);
            e.preventDefault();
            b[(k + (e.shiftKey ? -1 : 1) + b.length) % b.length].focus();
        }
    }
    fotky.forEach(function (img) {
        img.setAttribute('tabindex', '0');
        img.addEventListener('click', function () { otevri(img); });
        img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); otevri(img); } });
    });
})();
