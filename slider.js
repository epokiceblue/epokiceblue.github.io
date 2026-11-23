/* Slider fotek na hlavní stránce: plynulý posun, který jde chytit a potáhnout prstem i myší.
   Rychlost se mění plynule (žádné cuknutí): při najetí myší jemně zpomalí a zastaví,
   po odjetí / puštění se hned zase plynule rozjede. Fotky jsou ve stopě dvakrát, takže smyčka je bez skoku. */
(function () {
    var stopa = document.querySelector('.slide_track');
    if (!stopa) return;
    stopa.classList.add('js-ovladany');

    var x = 0;            // aktuální posun (px)
    var v = 0;            // aktuální rychlost (px/s)
    var cil = 0;          // kam se má posun dostat při tažení
    var posledni = performance.now();
    var tahne = false, pohnul = false, startX = 0, startPozice = 0, mysNad = false;
    var stopy = [];       // poslední pohyby prstu/myši kvůli setrvačnosti

    function polovina() { return stopa.scrollWidth / 2; }
    function zakladni() { // px za sekundu: celý okruh za 100 s (PC) / 80 s (mobil)
        return polovina() / (window.innerWidth <= 768 ? 80 : 100);
    }
    function snimek(t) {
        var dt = Math.min(t - posledni, 50) / 1000;
        posledni = t;
        if (tahne) {
            // posun jde za prstem s lehkým vyhlazením
            var k = 1 - Math.exp(-dt * 22);
            var dx = (cil - x) * k;
            x += dx;
            v = dt > 0 ? dx / dt : v;
        } else {
            // rychlost se plynule blíží cílové: 0 při najetí myší, jinak základní
            var chci = mysNad ? 0 : zakladni();
            var k2 = 1 - Math.exp(-dt * (mysNad ? 5 : 2.2));
            v += (chci - v) * k2;
            x += v * dt;
        }
        var h = polovina();
        if (h > 0) {
            var nove = ((x % h) + h) % h;
            if (tahne) { cil += nove - x; startPozice += nove - x; }
            x = nove;
        }
        stopa.style.transform = 'translate3d(' + (-x).toFixed(2) + 'px,0,0)';
        requestAnimationFrame(snimek);
    }

    stopa.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'mouse' && e.button !== 0) return;
        tahne = true; pohnul = false;
        startX = e.clientX; startPozice = x; cil = x;
        stopy = [{ t: e.timeStamp, x: e.clientX }];
        try { stopa.setPointerCapture(e.pointerId); } catch (err) {}
    });
    stopa.addEventListener('pointermove', function (e) {
        if (!tahne) return;
        var dx = e.clientX - startX;
        if (Math.abs(dx) > 5) pohnul = true;
        cil = startPozice - dx;
        stopy.push({ t: e.timeStamp, x: e.clientX });
        if (stopy.length > 6) stopy.shift();
    });
    function pust() {
        if (!tahne) return;
        tahne = false;
        // setrvačnost: slider se po puštění chvilku veze ve směru tahu a plynule přejde do běžné rychlosti
        var a = stopy[0], b = stopy[stopy.length - 1];
        if (a && b && b.t - a.t > 0 && performance.now() - b.t < 120) {
            var hod = -(b.x - a.x) / ((b.t - a.t) / 1000);
            v = Math.max(-2500, Math.min(2500, hod));
        }
        x = cil;
    }
    stopa.addEventListener('pointerup', pust);
    stopa.addEventListener('pointercancel', pust);
    stopa.addEventListener('click', function (e) { if (pohnul) { e.preventDefault(); e.stopPropagation(); } }, true);
    stopa.addEventListener('dragstart', function (e) { e.preventDefault(); });

    // na počítači při najetí myší plynule zastaví, po odjetí se hned rozjede
    stopa.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') mysNad = true; });
    stopa.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') { mysNad = false; pust(); } });

    requestAnimationFrame(snimek);
})();
