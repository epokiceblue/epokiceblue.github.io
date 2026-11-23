/* Cookie lišta: souhlas s Google Analytics (Consent Mode v2).
   Výchozí stav "denied" se nastavuje přímo v <head> každé stránky před gtag('config').
   Volbu si pamatujeme v localStorage pod klíčem "sz_cookies" ("ano" / "ne"). */
(function () {
    var KLIC = 'sz_cookies';

    function ulozeno() {
        try { return localStorage.getItem(KLIC); } catch (e) { return null; }
    }
    function uloz(hodnota) {
        try { localStorage.setItem(KLIC, hodnota); } catch (e) {}
    }
    function souhlas(ano) {
        if (typeof gtag === 'function') {
            gtag('consent', 'update', { analytics_storage: ano ? 'granted' : 'denied' });
        }
    }

    var css = '' +
        '.sz-cookies{position:fixed;left:24px;bottom:24px;z-index:9999;box-sizing:border-box;' +
        'width:360px;max-width:calc(100vw - 32px);padding:20px 22px 18px;background:#ECE6DB;color:#2F3B2C;' +
        'border:1px solid #DDD3C4;box-shadow:0 10px 30px rgba(31,36,30,.18);font-family:"Montserrat",sans-serif;' +
        'text-align:left;opacity:0;transform:translateY(12px);transition:opacity .35s ease,transform .35s ease;}' +
        '.sz-cookies.sz-videt{opacity:1;transform:none;}' +
        '.sz-cookies h2{margin:0 0 8px;font-family:"Poppins",sans-serif;font-weight:700;font-size:17px;' +
        'text-transform:lowercase;letter-spacing:0;color:#2F3B2C;}' +
        '.sz-cookies p{margin:0 0 16px;font-size:13px;line-height:1.6;color:#3d4639;}' +
        '.sz-cookies a{color:inherit;text-decoration:underline;}' +
        '.sz-cookies-tlacitka{display:flex;gap:10px;}' +
        '.sz-cookies button{flex:1;cursor:pointer;padding:10px 16px;border-radius:999px;' +
        'font-family:"Poppins",sans-serif;font-weight:700;font-size:13px;border:1.5px solid #2F3B2C;transition:background .2s,color .2s;}' +
        '.sz-cookies .sz-ano{background:#2F3B2C;color:#ECE6DB;}' +
        '.sz-cookies .sz-ano:hover{background:#1F241E;}' +
        '.sz-cookies .sz-ne{background:transparent;color:#2F3B2C;}' +
        '.sz-cookies .sz-ne:hover{background:#DDD3C4;}' +
        '@media (max-width:600px){.sz-cookies{left:16px;right:16px;bottom:16px;width:auto;max-width:none;padding:18px 18px 16px;}}';

    function ukaz() {
        if (document.querySelector('.sz-cookies')) return;
        var styl = document.createElement('style');
        styl.textContent = css;
        document.head.appendChild(styl);

        var lista = document.createElement('div');
        lista.className = 'sz-cookies';
        lista.setAttribute('role', 'dialog');
        lista.setAttribute('aria-label', 'Souhlas s cookies');
        lista.innerHTML =
            '<h2>cookies</h2>' +
            '<p>Ráda bych věděla, které fotky a stránky tě tu nejvíc zajímají. ' +
            'K tomu používám Google Analytics. ' +
            '<a href="podminky.html#osobni-udaje">Víc informací</a></p>' +
            '<div class="sz-cookies-tlacitka">' +
            '<button type="button" class="sz-ne">Odmítnout</button>' +
            '<button type="button" class="sz-ano">Přijmout</button>' +
            '</div>';
        document.body.appendChild(lista);
        requestAnimationFrame(function () { lista.classList.add('sz-videt'); });

        function zavri(ano) {
            uloz(ano ? 'ano' : 'ne');
            souhlas(ano);
            lista.classList.remove('sz-videt');
            setTimeout(function () { lista.remove(); }, 400);
        }
        lista.querySelector('.sz-ano').addEventListener('click', function () { zavri(true); });
        lista.querySelector('.sz-ne').addEventListener('click', function () { zavri(false); });
    }

    // Odkaz "nastavení cookies" kdekoliv na webu (class="sz-cookies-nastaveni") lištu znovu otevře.
    document.addEventListener('click', function (e) {
        var odkaz = e.target.closest && e.target.closest('.sz-cookies-nastaveni');
        if (odkaz) { e.preventDefault(); ukaz(); }
    });

    var volba = ulozeno();
    if (volba === 'ano') { souhlas(true); }
    else if (volba !== 'ne') {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ukaz);
        else ukaz();
    }
})();
