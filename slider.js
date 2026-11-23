/* Slider fotek na hlavní stránce: plynulý posun, který jde chytit a potáhnout prstem i myší.
   Po puštění se za chvilku zase sám rozjede. Fotky jsou ve stopě dvakrát, takže smyčka je bez skoku. */
(function () {
    var stopa = document.querySelector('.slide_track');
    if (!stopa) return;
    stopa.classList.add('js-ovladany');

    var x = 0, posledni = performance.now();
    var tahne = false, pohnul = false, startX = 0, startPozice = 0, pokracujOd = 0, mysNad = false;

    function polovina() { return stopa.scrollWidth / 2; }
    function rychlost() { // px za sekundu: celý okruh za 100 s (PC) / 80 s (mobil)
        return polovina() / (window.innerWidth <= 768 ? 80 : 100);
    }
    function snimek(t) {
        var dt = Math.min(t - posledni, 100) / 1000;
        posledni = t;
        if (!tahne && !mysNad && t > pokracujOd) x += rychlost() * dt;
        var h = polovina();
        if (h > 0) x = ((x % h) + h) % h;
        stopa.style.transform = 'translate3d(' + (-x) + 'px,0,0)';
        requestAnimationFrame(snimek);
    }

    stopa.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'mouse' && e.button !== 0) return;
        tahne = true; pohnul = false;
        startX = e.clientX; startPozice = x;
        try { stopa.setPointerCapture(e.pointerId); } catch (err) {}
    });
    stopa.addEventListener('pointermove', function (e) {
        if (!tahne) return;
        var dx = e.clientX - startX;
        if (Math.abs(dx) > 5) pohnul = true;
        x = startPozice - dx;
    });
    function pust() {
        if (!tahne) return;
        tahne = false;
        pokracujOd = performance.now() + 1200; // chvilku počká a pak se zase rozjede
    }
    stopa.addEventListener('pointerup', pust);
    stopa.addEventListener('pointercancel', pust);
    stopa.addEventListener('click', function (e) { if (pohnul) { e.preventDefault(); e.stopPropagation(); } }, true);
    stopa.addEventListener('dragstart', function (e) { e.preventDefault(); });

    // na počítači se při najetí myší zastaví (jako dřív)
    stopa.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') mysNad = true; });
    stopa.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') { mysNad = false; pust(); } });

    requestAnimationFrame(snimek);
})();
