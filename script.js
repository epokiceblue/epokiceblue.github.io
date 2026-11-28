const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('active');
    });
});

function openTab(evt, tabName) {
    const tabLinks = document.getElementsByClassName("tab-link");
    const tabContent = document.getElementsByClassName("tab-content");

    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].classList.remove("active");
    }
    
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}


function openMenu() {
    document.getElementById('mobileMenuOverlay').classList.add('active');
    document.body.classList.add('menu-open');
    document.documentElement.classList.add('menu-open'); // <html>
}
function closeMenu() {
    document.getElementById('mobileMenuOverlay').classList.remove('active');
    document.body.classList.remove('menu-open');
    document.documentElement.classList.remove('menu-open');
}

// Handle all dropdown menus
const dropdowns = document.querySelectorAll('.dropdown');

dropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector(".dropdown-btn");
    const menu = dropdown.querySelector(".dropdown-menu");

    // open / close when clicking the button
    btn.addEventListener("click", (e) => {
      e.stopPropagation();                 // don't trigger document click
      menu.classList.toggle("active");
    });

    // close when clicking anywhere else
    document.addEventListener("click", () => {
      menu.classList.remove("active");
    });
});

// „jak to u mě probíhá“: na mobilu se kroky rozbalují klepnutím na nadpis
document.querySelectorAll('.process li strong').forEach(title => {
    title.addEventListener('click', () => title.parentElement.classList.toggle('open'));
});

// galerie: fotky se řadí zleva doprava (jako text), do sloupců podle toho, který je zrovna nejkratší
(function () {
    const galleries = document.querySelectorAll('.image-gallery > div');
    if (!galleries.length) return;
    const pocetSloupcu = () => window.matchMedia('(max-width: 32rem)').matches ? 1
        : window.matchMedia('(max-width: 80rem)').matches ? 2 : 4;
    galleries.forEach(g => { g._fotky = Array.from(g.querySelectorAll('img')); g._n = 0; });
    function rozloz() {
        const n = pocetSloupcu();
        galleries.forEach(g => {
            if (g._n === n) return;
            g._n = n;
            g.innerHTML = '';
            if (n === 1) {
                g.classList.remove('galerie-sloupce');
                g._fotky.forEach(img => g.appendChild(img));
                return;
            }
            g.classList.add('galerie-sloupce');
            const sloupce = [], vysky = [];
            for (let i = 0; i < n; i++) {
                const s = document.createElement('div');
                s.className = 'galerie-sloupec';
                g.appendChild(s); sloupce.push(s); vysky.push(0);
            }
            g._fotky.forEach(img => {
                const w = +img.getAttribute('width') || img.naturalWidth || 1;
                const h = +img.getAttribute('height') || img.naturalHeight || 1;
                const i = vysky.indexOf(Math.min(...vysky));
                sloupce[i].appendChild(img);
                vysky[i] += h / w;
            });
        });
    }
    rozloz();
    window.addEventListener('resize', rozloz);
})();

/* měření kliknutí na kontakt a odeslání formuláře (Google Analytics, jen se souhlasem v cookie liště) */
(function () {
    if (typeof gtag !== 'function') return;
    document.addEventListener('click', function (e) {
        var a = e.target.closest ? e.target.closest('a') : null;
        if (!a) return;
        var h = a.getAttribute('href') || '', ev = null;
        if (/contact\.html/.test(h)) ev = 'klik_na_kontakt';
        else if (h.indexOf('mailto:') === 0) ev = 'klik_na_email';
        else if (/instagram\.com/.test(h)) ev = 'klik_na_instagram';
        else if (/facebook\.com/.test(h)) ev = 'klik_na_facebook';
        else if (/o-mne\.html/.test(h)) ev = 'klik_o_mne';
        if (ev) gtag('event', ev, { text_tlacitka: (a.textContent || '').trim().slice(0, 80), stranka: location.pathname, transport_type: 'beacon' });
    }, true);
    var f = document.querySelector('form[action*="formspree"]');
    if (f) f.addEventListener('submit', function () { gtag('event', 'odeslany_formular', { stranka: location.pathname, transport_type: 'beacon' }); });
})();

/* Ochrana fotek: na fotkách nejde pravé tlačítko (Uložit obrázek), přetažení myší ani dlouhý stisk na mobilu. */
(function () {
    var styl = document.createElement('style');
    styl.textContent = 'img{-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;-webkit-user-drag:none;}';
    document.head.appendChild(styl);
    function jeFotka(t) { return t && (t.tagName === 'IMG' || (t.closest && t.closest('picture'))); }
    document.addEventListener('contextmenu', function (e) { if (jeFotka(e.target)) e.preventDefault(); });
    document.addEventListener('dragstart', function (e) { if (jeFotka(e.target)) e.preventDefault(); });
})();
