# Generuje stránky blogu (blog/index.html a články) z jednoho místa.
# Spuštění: python3 blog/gen_blog.py  (z kořene repozitáře)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
CSSV = 6
src = open('podminky.html', encoding='utf-8', newline='').read()
hdr = src[src.index('<button class="mobile-menu-btn"'):src.index('<main')]
hdr = hdr.replace('\r\n', '\n').replace('href="', 'href="../')
hdr = hdr.replace('href="../blog/"', 'href="./"')
hdr = hdr.replace('\r\n', '\n')
assert hdr.count('href="./"') == 2, 'odkaz na blog v menu nenalezen'
foot = src[src.index('<footer'):src.index('</footer>') + 9].replace('\r\n', '\n')
foot = foot.replace('href="', 'href="../').replace('href="../http', 'href="http').replace('href="../mailto', 'href="mailto')
LISTA = '''<nav class="lista" aria-label="Menu"><a href="../index.html">hlavní stránka</a><a href="../svatby.html">portfolio</a><a href="../cenik.html">ceník</a><a href="./">blog</a><a href="../contact.html">kontakt</a></nav>'''
SKRIPTY = '''<script>(function(){var l=document.querySelector('.lista'),h=document.querySelector('.black_background');function f(){l.classList.toggle('vidět',window.scrollY>(h.offsetHeight+60));}window.addEventListener('scroll',f,{passive:true});f();})();</script>
<script src="../script.js?v=5"></script>'''
WEB = 'https://sofiezborilova.cz/'

def head(title, desc, url, ogimg, body_class='', extra=''):
    return f'''<!DOCTYPE html>
<html lang="cs">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FYSGC77GVP"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    var szVolba = null; try {{ szVolba = localStorage.getItem('sz_cookies'); }} catch (e) {{}}
    gtag('consent', 'default', {{ analytics_storage: szVolba === 'ano' ? 'granted' : 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' }});
    gtag('js', new Date());

    gtag('config', 'G-FYSGC77GVP');
    </script>
    <script src="../cookies.js?v=1" defer></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title}</title>
    <link rel="canonical" href="{WEB}{url}">
    <link rel="icon" href="../favicon.ico?v=2" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png?v=2">
    <link rel="icon" type="image/png" sizes="192x192" href="../favicon-192.png?v=2">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png?v=2">
    <meta property="og:type" content="{'article' if extra else 'website'}">
    <meta property="og:locale" content="cs_CZ">
    <meta property="og:site_name" content="Sofie Zbořilová – fotografka Brno">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{WEB}{url}">
    <meta property="og:image" content="{WEB}{ogimg}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="628">
    <link rel="stylesheet" href="../contact.css?v=9">
    <link rel="stylesheet" href="blog.css?v={CSSV}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,700;1,300;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../paticka.css?v=1">{extra}
</head>
<body class="{body_class}">
    '''

def zapis(fn, html):
    with open('blog/' + fn, 'w', encoding='utf-8', newline='') as f:
        f.write(html.replace('\r\n', '\n').replace('\n', '\r\n'))

def img(p, alt, c='', lazy=True):
    return f'<img{" class=" + chr(34) + c + chr(34) if c else ""} src="../{p}" alt="{alt}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>'

MEDAILON = f'''<div class="medailon">{img('fotky/sofie-zborilova-fotografka-portret.webp', 'Sofie Zbořilová, fotografka z Brna', lazy=False)}<div><h3>ahoj, jsem sofi</h3><p>Fotím svatby, rodiny a značky v Brně a Bratislavě. Mám ráda přirozené momenty, jemné barvy a lidi, kteří se nebojí být sami sebou.</p><a class="tlacitko" href="../contact.html">napiš mi</a><span class="odkazy"><a href="../portrety.html">portfolio</a><a href="../cenik.html">ceník</a></span></div></div>'''

# ---------- seznam článků (nejnovější nahoře) ----------
CLANKY = [
    dict(soubor='univerzalni-lokace-na-foceni.html', kat='rady před focením', cas='3 min',
         titul='univerzální lokace na focení, které máte na dosah',
         foto='fotky_portrety/rodinne-foceni-doma-na-gauci.jpg', foto_alt='Rodiče s miminkem na gauči doma, rodinné focení v obýváku',
         perex='Často mi lidé píšou, že kolem sebe nemají žádné hezké místo na focení. A pokaždé se usměju, protože krásné fotky nevznikají díky místu, ale díky vám.'),
    dict(soubor='jak-u-me-probiha-rodinne-a-parove-foceni.html', kat='rady před focením', cas='4 min',
         titul='jak u mě probíhá rodinné a párové focení',
         foto='fotky_portrety/parove-foceni-beh-pres-louku.jpg', foto_alt='Pár běží přes louku pod košilí, hravé párové focení',
         perex='Nečekejte, že se budu přehnaně chválit. Chci vám přiblížit, jakým způsobem přistupuji k rodinnému a párovému focení.'),
    dict(soubor='co-si-vzit-na-sebe-na-foceni.html', kat='rady před focením', cas='5 min',
         titul='co si vzít na sebe na focení: 7 tipů, aby ti to slušelo',
         foto='fotky_blog/portret-zeny-v-kosili-s-kockami.jpg', foto_alt='Portrét ženy v košili s kočkami',
         perex='Oblečení hraje na fotkách obrovskou roli. Proto jsem sepsala pár rad a základních pravidel, kterých je fajn se při výběru outfitu držet.'),
]

def karta(c):
    return f'''<a class="p-karta" href="{c['soubor']}" data-kat="{c['kat']}">{img(c['foto'], c['foto_alt'])}<span class="kategorie">{c['kat']} · {c['cas']} čtení</span><h3>{c['titul']}</h3><p>{c['perex']}</p><span class="cist">číst dál</span></a>'''

def konec(soubor):
    dalsi = [c for c in CLANKY if c['soubor'] != soubor][:3]
    o = '<section class="konec">' + MEDAILON
    if dalsi:
        o += f'<div class="dalsi"><h2>mohlo by tě zajímat</h2><p class="podnadpis">Další články, které se ti můžou hodit.</p><div class="karty">{"".join(karta(c) for c in dalsi)}</div></div>'
    return o + '</section>'

def stranka(fn, hlava, telo):
    zapis(fn, hlava + hdr + LISTA + '\n<main class="blog">\n' + telo + '\n</main>\n' + foot + '\n' + SKRIPTY + '\n</body>\n</html>\n')

# ---------- článek: co si vzít na sebe na focení ----------
PAL = {'jarní focení': [('vanilková', '#F2DE9C'), ('šalvějová', '#A9B98F'), ('korálová', '#E3826B'), ('prachově modrá', '#9FB6CB'), ('pudrově růžová', '#EDC5C0'), ('eukalyptová', '#7F958C')],
       'letní focení': [('bílá', '#FFFFFF'), ('lněná', '#D8C7AA'), ('starorůžová', '#B07A74'), ('levandulová', '#B8A6CA'), ('blankytná', '#6CA0CF'), ('námořnická', '#1F3A5F')],
       'podzimní focení': [('hořčicová', '#A97C2E'), ('karamelová', '#C78F5E'), ('rezavá', '#9A4A2E'), ('olivová', '#9D9167'), ('švestková', '#6E4F57'), ('čokoládová', '#5C3B2A')],
       'zimní focení': [('smetanová', '#F2EBDD'), ('šedohnědá', '#9A8B7E'), ('oříšková', '#8C6A4E'), ('vínová', '#5C1F2E'), ('lesní zelená', '#3E5A3F'), ('espresso', '#2B211D')]}
def svetla(h):
    r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return 0.299 * r + 0.587 * g + 0.114 * b > 170
def palety():
    o = '<div class="palety">'
    for s, cs in PAL.items():
        o += f'<div class="paleta-sezona"><h3>{s}</h3><p class="pod">paleta barev</p><div class="barvy">'
        o += ''.join(f'<div class="barva{" svetla" if svetla(h) else ""}" style="background:{h}"><span>{n}</span></div>' for n, h in cs)
        o += '</div><p class="web">sofiezborilova.cz</p></div>'
    return o + '</div>'

TIPY = [('neonove-barvy', 'neonové barvy, loga a nápisy'), ('zemite-barvy', 'zemité barvy a palety'), ('materialy', 'materiály a textury'),
        ('rozevlate-obleceni', 'rozevláté oblečení'), ('doplnky', 'doplňky'), ('sladit', 'sladit, nebo nesladit?'), ('srdcovka', 'tvoje srdcovka'),
        ('vyber-fotografa', 'bonus: výběr fotografa')]
OBSAH = '<div class="obsah-obal"><nav class="obsah" aria-label="Obsah článku"><b>v článku najdeš</b><ol>' + ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in TIPY) + '</ol></nav></div>'

def dvojice(a, b):
    return f'<div class="b-dvojice"><figure>{img(*a)}</figure><figure>{img(*b)}</figure></div>'

C = next(c for c in CLANKY if c['soubor'] == 'co-si-vzit-na-sebe-na-foceni.html')
TITLE = 'Co si vzít na sebe na focení: 7 tipů, aby ti to slušelo | Sofie Zbořilová'
DESC = 'Nevíš, co si vzít na sebe na focení? 7 tipů od fotografky z Brna: jaké barvy a materiály volit, jak se sladit na rodinné či párové focení a palety barev pro každé roční období.'
LD = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Co si vzít na sebe na focení: 7 tipů, aby ti to slušelo",
      "description": DESC, "inLanguage": "cs", "datePublished": "2026-11-25", "dateModified": "2026-11-25",
      "image": WEB + "fotky_sdileni/co-si-vzit-na-sebe-na-foceni.jpg", "mainEntityOfPage": WEB + "blog/" + C['soubor'],
      "author": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB},
      "publisher": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB}}
EXTRA = '\n    <script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False) + '</script>'

P = 'fotky_portrety/'; R = 'fotky_produktove/'; BL = 'fotky_blog/'
T = f'''<section class="b-hero">{img(P + 'hrave-rodinne-foceni-venku.jpg', 'Hravé rodinné focení venku', lazy=False)}{img(P + 'cernobily-portret-zeny-oslava-narozenin.jpg', 'Žena v černých šatech a saku si chytá podpatek, černobílý portrét ve studiu', lazy=False)}{img(P + 'rodice-drzi-dcery-vanocni-foceni.jpg', 'Rodiče drží dcery v náručí, vánoční rodinné focení ve studiu', lazy=False)}
<div class="b-hero-text"><span class="kategorie">rady před focením · 5 min čtení</span><h1>co si vzít na sebe na focení: 7 tipů, aby ti to slušelo</h1></div></section>
<div class="uzky b-clanek"><p class="b-perex">Oblečení hraje na fotkách obrovskou roli. Proto jsem sepsala pár rad a základních pravidel, kterých je fajn se při výběru outfitu držet. Platí pro portrétní, párové i rodinné focení.</p>
{OBSAH}
<h2 id="neonove-barvy" class="prvni">1. nech doma neonové barvy, loga a nápisy</h2><p>Tohle je základ všeho, a pokud si máš zapamatovat jediné pravidlo, je to tohle. Na fotkách má jít hlavně o tebe a o chvíli, kterou se snažíme zachytit, takže nedopusť, aby tě oblečení překřikovalo. Výrazné a křiklavé barvy se navíc odrážejí do obličeje, a to fakt nechceme. A hlavně se vyhni velkým logům a nápisům. Malé nenápadné logo nevadí, ale když to jde úplně bez, je to určitě lepší.</p></div>
{dvojice((P + 'maminka-liba-miminko-rodinne-foceni-doma.jpg', 'Rodiče s miminkem ve světlém oblečení bez nápisů, rodinné focení doma'), (P + 'rodinne-foceni-v-prirode-hrave-brno.jpg', 'Rodina ve světlém oblečení na focení v přírodě u Brna'))}
<div class="uzky b-clanek"><h2 id="zemite-barvy">2. zemité barvy tě nikdy nezklamou</h2><p>Když vůbec nevíš, co si vzít na sebe a jak zkombinovat barvy, sáhni po zemitých tónech. S nimi nikdy nešlápneš vedle. Fotím hlavně v přírodě a tam se hodí obzvlášť. Mám ráda i pastelové barvy, na fotkách vypadají skvěle.</p><p>Pro inspiraci přikládám paletu barev ke každému ročnímu období. Ber ji opravdu jen jako inspiraci, většina barev se hodí skoro vždycky. Mysli ale na místo, kde budeme fotit, aby se tvoje oblečení nebilo s pozadím.</p></div>
{palety()}
<div class="uzky b-clanek"><h2 id="materialy">3. materiály a textury</h2><p>Neboj se kombinovat. Na fotkách vypadají skvěle různé textury, třeba kůže, koženka, džínovina, len nebo pletenina. Outfit tak jednoduše ozvláštníš.</p></div>
<figure class="foto-vyska">{img(P + 'lifestylovy-portret-zeny-v-prirode.jpg', 'Černobílý portrét ženy v károvaných šatech na louce')}</figure>
<div class="uzky b-clanek"><h2 id="rozevlate-obleceni">4. nech své oblečení rozevlát</h2><p>Co se nejvíc hodí pro uvolněné fotky? Uvolněné oblečení, ve kterém se budeš cítit dobře. Super jsou volné šaty, které doplníš třeba páskem. Pro pány lehká košile přehozená přes tričko. Pohodlné oblečení je mnohem lepší než se mačkat v něčem upnutém, co tě všude stahuje. A navíc krásně zachytí pohyb.</p>
<h2 id="doplnky">5. neboj se doplňků ani „nevšedního“ outfitu</h2><p>Focení je skvělá příležitost obléct se podle svých představ a pořádně se vystrojit. Vezmi si to, v čem se cítíš dobře a přirozeně. Nezapomeň ani na doplňky, pokud je běžně nosíš: šálu, klobouk, sluneční brýle, čepici nebo zajímavé sponky do vlasů. Naopak se vyhni výrazným sportovním hodinkám a gumičkám zapomenutým na ruce (můj věčný problém vždy a všude).</p></div>
{dvojice((R + 'brandove-foceni-pohyb-saty.jpg', 'Žena v pohybu ve volných dlouhých šatech'), (R + 'brandovy-portret-s-kloboukem.jpg', 'Portrét ženy s kloboukem jako doplňkem'))}
<div class="uzky b-clanek"><h2 id="sladit">6. sladit, nebo nesladit?</h2><p>Nemyslím kafe, to rozhodně nesladit, žejo? Ale možná řešíš, jak vymyslet oblečení, když se fotíte ve víc lidech. Rozhodně nemusíte mít stejně barevná trička a vypadat jak přes kopírák. Sladila bych se ale aspoň do jednoho stylu, aby nepřišla slečna v elegantních šatech a její partner ve sportovním. Buď jedno, nebo druhé.</p><p>Stejně tak u barev: zkuste se držet aspoň zemité palety. Černou, bílou, šedou, béžovou, tlumenou zelenou nebo hnědou doma určitě najdete. Dětem se neboj dopřát i výraznější barvy, jen ne křiklavé.</p></div>
<figure class="foto-sirsi">{img(P + 'prirozene-rodinne-foceni-v-pohybu.jpg', 'Rodina sladěná do jednoho stylu na focení v přírodě')}</figure>
<div class="uzky b-clanek"><h2 id="srdcovka">7. vezmi si na focení svou srdcovku</h2><p>Máš oblečení nebo doplněk, který vystihuje tvou osobnost a je pro tebe fakt důležitý? Tak ho nezapomeň doma. Mám ráda, když se do fotek dostanou i věci, na kterých ti opravdu záleží. Míša si třeba vzala košili s kočkama, kterou miluje a všichni si ji s ní spojují. Kačí zase přinesla šátek z cest po Indii. Pojďme do fotky vložit kousek tvého příběhu.</p></div>
{dvojice((BL + 'portret-zeny-v-kosili-s-kockami.jpg', 'Míša v oblíbené košili s kočkami'), (BL + 'tehotenske-foceni-se-satkem-z-indie.jpg', 'Kačí na těhotenském focení se šátkem z Indie'))}
<div class="uzky b-clanek bonus"><span class="kategorie">bonusový tip</span><h2 id="vyber-fotografa">vyber si fotografa, který ti s tím pomůže</h2>
<p>Než skončím, ráda bych ti dala ještě jeden tip navíc. Musím ho zmínit, protože je hodně důležitý, možná vůbec nejdůležitější z celého článku.</p>
<p>Dobrý fotograf tě s oblečením nenechá v tom samotné a pomůže ti ho vybrat. U mě to funguje takhle: před focením ti pošlu základní pravidla, tedy v podstatě tenhle článek.</p><p>Když si pořád nevíš rady, třeba u rodinného focení, připravím vám moodboard s inspirací. Z každé fotky si vezmete něco málo a zkombinujete to s tím, co máte doma, takže nemusíte nic kupovat. Nebo mi oblečení doma vyfotíš a kombinaci vymyslíme spolu.</p><p>U párového nebo portrétního focení často vymýšlíme i celý koncept. Fotky můžeme lehce naladit do retro stylu, do kovbojského stylu nebo do čehokoli, co je ti blízké. Vyber si proto fotografa, který ví, co dělá, a se vším ti pomůže.</p></div>
<section class="zelena"><div class="uzky"><p>Tohle bylo mých 7 tipů a jeden bonusový, kterých se můžeš držet. Chtěla bych ale zdůraznit, že není až tak důležité, kde fotíme a jak vypadáš, ale hlavně jak se cítíš. Soustřeď se hlavně na to, ať tě focení baví. Jak budou fotky vypadat, nech na mně.</p><p>Když si s výběrem nebudeš vědět rady, napiš mi. Moc ráda ti s oblečením pomůžu. A jestli chceš vidět, jak to vypadá v praxi, sleduj mě na Instagramu <a href="https://www.instagram.com/sofiezbo/">@sofiezbo</a>.</p>
<p class="sdilet"><span>Znáš někoho, komu by tenhle článek pomohl? Klidně mu ho pošli.</span><button type="button" id="sdilet">sdílet článek</button></p></div></section>
{konec(C['soubor'])}
<script>document.getElementById('sdilet').addEventListener('click',function(){{var b=this,u=location.href.split('#')[0];if(navigator.share){{navigator.share({{title:document.title,url:u}}).catch(function(){{}});}}else if(navigator.clipboard){{navigator.clipboard.writeText(u).then(function(){{b.textContent='odkaz zkopírován';setTimeout(function(){{b.textContent='sdílet článek';}},2500);}});}}}});</script>'''
stranka(C['soubor'], head(TITLE, DESC, 'blog/' + C['soubor'], 'fotky_sdileni/co-si-vzit-na-sebe-na-foceni.jpg', 'pres-vlnu', EXTRA), T)


# ---------- článek: jak u mě probíhá rodinné a párové focení ----------
def hero(fotky, kat, titul):
    return '<section class="b-hero">' + ''.join(img(f, a, lazy=False) for f, a in fotky) + f'\n<div class="b-hero-text"><span class="kategorie">{kat}</span><h1>{titul}</h1></div></section>'
def obsah(body):
    return '<div class="obsah-obal"><nav class="obsah" aria-label="Obsah článku"><b>v článku najdeš</b><ol>' + ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in body) + '</ol></nav></div>'
def kolaz(a, b, c):
    return f'<div class="b-kolaz">{img(*a, c="ka")}{img(*b, c="kb")}{img(*c, c="kc")}</div>'
def sdileni(): 
    return '<p class="sdilet"><span>Znáš někoho, komu by tenhle článek pomohl? Klidně mu ho pošli.</span><button type="button" id="sdilet">sdílet článek</button></p>'
SDILET_JS = """<script>document.getElementById('sdilet').addEventListener('click',function(){var b=this,u=location.href.split('#')[0];if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){b.textContent='odkaz zkopírován';setTimeout(function(){b.textContent='sdílet článek';},2500);});}});</script>"""
def ld(headline, desc, soubor, obr, publ):
    d = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": headline, "description": desc, "inLanguage": "cs",
         "datePublished": publ, "dateModified": "2026-11-25", "image": WEB + obr, "mainEntityOfPage": WEB + "blog/" + soubor,
         "author": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB}, "publisher": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB}}
    return '\n    <script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'

C2 = next(c for c in CLANKY if c['soubor'] == 'jak-u-me-probiha-rodinne-a-parove-foceni.html')
B2 = [('styl', 'můj styl a vaše představa'), ('autenticita', 'nebudu vás měnit'), ('rande', 'focení jako rande'), ('prochazka', 'budeme chodit'),
      ('nic-neni-spatne', 'nic není špatně'), ('mluvte', 'nebojte se mluvit'), ('tisk', 'fotky v ruce')]
T2 = f"""{hero([(P + 'parove-foceni-beh-pres-louku.jpg', 'Pár běží přes louku, hravé párové focení'), (P + 'dokumentarni-rodinne-fotky-deti-brno.jpg', 'Maminka se synem v kvetoucí louce, dokumentární rodinné focení'), (P + 'parove-foceni-v-trave-u-lesa.jpg', 'Pár sedí v trávě na kraji lesa, uvolněné párové focení')], 'rady před focením · 4 min čtení', 'jak u mě probíhá rodinné a párové focení')}
<div class="uzky b-clanek"><p class="b-perex">Nečekejte, že se v tomto článku budu přehnaně chválit a navádět vás, abyste šli na focení ke mně a ne ke konkurenci. Ne, fakt ne😂 Tímto článkem vám chci aspoň trochu přiblížit, jakým způsobem přistupuji k rodinnému a párovému focení (ale většina platí i na portrétní🤫). Zkusím to rozřadit do bodů, aby to pro vás bylo víc přehledné.</p>
{obsah(B2)}
<h2 id="styl" class="prvni">1. víte, jaký mám styl, ale…</h2><p>Předpokládám, že když se přihlásíte na focení, tak víte, jaký mám styl a jak nejspíš budou výsledné fotky vypadat. Ale pokud máte jinou představu, moc ráda si ji vyslechnu! Když se mnou bude rezonovat nebo mi bude připadat zajímavá a super, ráda s vámi vyzkouším něco, na co nejsem zvyklá.</p><p>V případě, že se naše představy vůbec nepotkají a ani jedna strana nebude chtít ustoupit, je v pořádku, když oslovíte jiného fotografa. Ráda vám nějakého doporučím, pokud mě napadne někdo, s kým si stylem sednete víc✨ Nemám ráda, když se fotografové berou jako konkurence, naopak si myslím, že je fajn si předávat práci. Zároveň věřím, že si klient musí s fotografem sednout, jde to totiž na výsledných fotkách poznat♥️</p>
<h2 id="autenticita">2. nebudu vás měnit a strojit do něčeho, co nejste</h2><p>Při focení ode mě často uslyšíte věty jako: „Dělejte, jako kdybych tady nebyla a vy jste nevnímali nic okolo vás… jen sebe navzájem.“ nebo „Nebojte si s vaší holčičkou hrát, dělat blbosti, vzájemně se lechtat nebo si zahrát na babu.“ Důležitější je totiž pro mě autenticita než to, jestli pózujete přesně podle pravidel. Často si taky můžete všimnout, že v určitých momentech při focení mlčím. To je právě kvůli tomu, že vám chci dát prostor a zároveň se snažím vytvořit místo, které pro vás bude bezpečné.</p><p>Až se budete na fotky po pár letech dívat, které vám vyhrknou slzy do očí? Ty s velkým, ale falešným úsměvem, kde vypadáte jako z časopisu… nebo ty, ze kterých září radost, spokojenost a jsou na nich zaznamenány vaše společné chvíle? Přesně. Tak tady máte odpověď na to, proč k vašemu focení přistupuji takovým způsobem😊</p></div>
{kolaz((P + 'autenticke-rodinne-foceni.jpg', 'Autentické rodinné focení'), (P + 'rodinne-foceni-lechtani-ve-studiu.jpg', 'Rodiče lechtají dceru, hravé rodinné focení ve studiu'), (P + 'holcicky-polstarova-bitva-studio.jpg', 'Holčičky s polštáři běhají po studiu'))}
<div class="uzky b-clanek"><h2 id="rande">3. rande?</h2><p>Jeden z mých nejoblíbenějších tipů, co vám dávám, je, abyste si z focení udělali rande. A myslím to více způsoby. Zaprvé to může znamenat, že focení zařadíte do vašeho společně stráveného času a před ním nebo po něm si zajdete na rande (na kafe, procházku, do kina, cokoli…). A to neplatí jen pro páry, ale i pro rodiny!</p><p>A zadruhé tím myslím to, abyste vzali na rande i mě! Divný? Trochu. Ale věřte mi, že výsledný fotky za to stojí!! Kam rádi společně chodíte? Co spolu rádi děláte? Co vás vystihuje? Máte nějakej společnej koníček? Nebo kde jste měli vaše první rande? Říkejte, přehánějte. Plno z těchto věcí můžeme zakomponovat dohromady a voilà, místo obyčejných fotek máte ty vaše, jedinečný a s duší✨</p></div>
<figure class="foto-vyska">{img(P + 'parove-foceni-ve-meste-pizza.jpg', 'Pár na rande ve městě s pizzou, párové focení')}</figure>
<div class="uzky b-clanek"><h2 id="prochazka">4. počítejte s tím, že budeme chodit</h2><p>Pokud budeme fotit někde venku, bude to tak trochu procházka. Má to několik benefitů. Projdeme více míst a lokací, a tak vás fotky (a doufám, že ani focení!) nebudou nudit. Na čerstvým vzduchu a při chůzi si pročistíte hlavu, a pokud nejste na focení zvyklí a máte z toho stres, může vám to dost pomoct.</p><p>Máte prostor na to, abyste si mezi focením odpočinuli a abychom se o sobě vzájemně něco dozvěděli. Baví mě se o vás dozvídat, jací jste, jaký je váš příběh, co vás baví… hlavně, když se na focení vracíte🫶🏻 Na kamarádském přístupu si zakládám, a tak je pro mě důležité, abychom si vzájemně důvěřovali.</p></div>
<figure class="foto-sirsi">{img(P + 'parove-foceni-v-rozkvetlem-sadu.jpg', 'Pár v objetí v rozkvetlém sadu na jaře')}</figure>
<div class="uzky b-clanek"><h2 id="nic-neni-spatne">5. nic není špatně, aneb starosti a perfekcionismus nechte doma</h2><p>Nemusíte se každou chvíli kontrolovat. Pokud bude něco špatně, jsem tam od toho já, abych upozornila a případně opravila.</p><p>Když nevíte, co před foťákem dělat, jak se před ním chovat, a máte z toho strach, opravdu nemusíte mít žádné obavy. Navedu vás, pomůžu vám. Nejsem tam proto, abych si o vás myslela něco špatného, že něco nevíte nebo neznáte. Jsem váš kámoš a vždycky vám ráda podám pomocnou ruku.</p><p>Vaše dítě nemá náladu a dělá vše, jen ne a ne stát na místě? Nevadí, vždyť to děti dělají! Tak si s ním budeme chvíli hrát, budeme mu naslouchat, necháme ho, ať nám ukáže, co je v té hlíně tak zajímavého! Vždyť to jsou ty nejkrásnější okamžiky, kdy děti objevují svět a my bychom se od nich mohli v tolika věcech učit. Tady máte přesně tu autenticitu, o které jsem psala na začátku, tak se ji nesnažte přehlížet a nechte mě, ať vám zaznamenám i takové momenty. Později se už opakovat nebudou♥️</p></div>
{dvojice((P + 'dokumentarni-rodinne-foceni-brno.jpg', 'Dokumentární rodinné focení v Brně'), (P + 'rodinne-foceni-bez-pozovani-brno.jpg', 'Rodinné focení bez pózování v Brně'))}
<div class="uzky b-clanek"><h2 id="mluvte">6. líná huba…</h2><p>Nebojte se mluvit. Nebojte se nesouhlasit. Při focení vám budu nabízet moje tipy, nápady nebo osvědčené postupy. Pokud vám to ale nesedí a necítíte se v takových věcech dobře, tak to vůbec nevadí. Hlavně mi to řekněte a vymyslíme jinou cestu, která vám bude vyhovovat. Focení by pro vás mělo být příjemné a určitě ne něco, do čeho se nutíte. Tak se prosím nepřetvařujte, i kdyby to bylo kvůli tomu, že nechcete moje nápady urazit. Nebojte, já to ustojím a naopak budu ráda za to, že si řeknete🌸</p>
<h2 id="tisk">7. fotky nemusí být jen v mobilu</h2><p>Myslete na to, že fotky pořád můžete mít fyzicky v ruce. Na závěr jsem vám chtěla dát malý tip: nezapomeňte si fotky tisknout! V mobilu i v počítači se lehce ztratí, a i když se to tak nemusí zdát, nejsou nesmrtelné (soucítím se všemi, komu se taky někdy záhadně vymazaly soubory🙃).</p><p>Mám domluvenou 15% slevu na tisk fotek na <a href="https://www.kvalitnifotky.cz/" rel="noopener">kvalitnifotky.cz</a> s kódem <b>SOFIEZBORILOVA</b>, kde si můžete z focení sestavit knížku nebo album, nebo si je nechat vytisknout na velké formáty. Dám ale ruku do ohně, že tisk fotek máte k dispozici v každém aspoň trochu větším městě (např. v drogerii DM nebo Rossmann), takže by to mělo být lehce dostupné. Věřte mi, mít vaše fotky fyzicky v ruce je úplně jiný zážitek♥️</p></div>
<section class="zelena"><div class="uzky"><p>Doufám, že jsem vám můj přístup aspoň trochu přiblížila a snad je vám sympatický✨ Kdybyste se ke mně chtěli objednat, můžete přes <a href="../contact.html">kontaktní formulář</a> nebo můj <a href="https://www.instagram.com/sofiezbo/">Instagram</a>. Budu se těšit na každého z vás a budu ráda, když mi k tomu napíšete i něco o sobě, co bychom mohli do focení zakomponovat!</p><p>S.</p>
{sdileni()}</div></section>
{konec(C2['soubor'])}
{SDILET_JS}"""
DESC2 = 'Jak u mě probíhá rodinné a párové focení: můj styl, autenticita místo pózování, focení jako rande, procházka, děti bez stresu a tip na tisk fotek. Fotografka Sofie Zbořilová, Brno.'
stranka(C2['soubor'], head('Jak u mě probíhá rodinné a párové focení | Sofie Zbořilová', DESC2, 'blog/' + C2['soubor'], 'fotky_sdileni/jak-u-me-probiha-rodinne-a-parove-foceni.jpg', 'pres-vlnu',
        ld('Jak u mě probíhá rodinné a párové focení', DESC2, C2['soubor'], 'fotky_sdileni/jak-u-me-probiha-rodinne-a-parove-foceni.jpg', '2024-02-05')), T2)


# ---------- článek: univerzální lokace ----------
S_ = 'fotky_svadby/'
C3 = next(c for c in CLANKY if c['soubor'] == 'univerzalni-lokace-na-foceni.html')
B3 = [('svetlo', 'světlo je důležitější než místo'), ('zed', 'zeď, která má charakter'), ('lesik', 'lesík, louka nebo cesta za domem'),
      ('doma', 'u vás doma'), ('mesto', 'ulička, kavárna nebo roh domu')]
def tp(t):
    return f'<p class="t-pribeh">{t}</p>'
def dvojice_org(a, b):
    return f'<div class="b-dvojice organic"><figure>{img(*a)}</figure><figure>{img(*b)}</figure></div>'
T3 = f"""{hero([(P + 'predsvatebni-foceni-ve-vinohradu.jpg', 'Snoubenci procházejí vinohradem, předsvatební focení'), (P + 'cernobily-portret-paru-v-protisvetle.jpg', 'Pár v protisvětle na louce, černobílý párový portrét'), (P + 'autenticke-parove-fotky-ve-meste.jpg', 'Autentické párové fotky ve městě')], 'rady před focením · 3 min čtení', 'univerzální lokace na focení, které máte na dosah')}
<div class="uzky b-clanek"><p class="b-perex">Často mi lidé při domlouvání focení píšou:</p>
<blockquote class="b-citat">„My tady kolem sebe nemáme žádné hezké místo na focení… Všude je to jen pole, silnice nebo dětské hřiště.“</blockquote>
<p>A pokaždé se usměju. Protože krásné fotky nevznikají díky místu, ale primárně díky vám. ✨</p>
<p>Jasně, rozkvetlá louka nebo západ slunce nad lesem vypadají kouzelně. Pravda ale je, že i naprosto obyčejná lokace může na fotkách působit nádherně, když víte, jak ji využít.</p>
{obsah(B3)}
<h2 id="svetlo" class="prvni">1. světlo je důležitější než místo</h2><p>Místo nemusí být dokonalé, pokud má dobré světlo. Stačí obyčejná ulice, okraj parku nebo vaše zahrada. Když se tam světlo opírá pod správným úhlem, fotky budou mít krásně měkký a přirozený nádech.</p>
<p class="b-poznamka">💡 Pro tip: zkuste se rozhlédnout kolem domu hodinu před západem slunce. Uvidíte, jak se všechno mění.</p></div>
{dvojice_org((P + 'romanticke-predsvatebni-foceni.jpg', 'Snoubenci při západu slunce na zahradě za farou, předsvatební focení'), (P + 'parove-foceni-pri-zapadu-slunce.jpg', 'Pár v objetí na louce při západu slunce'))}
<div class="uzky b-clanek">
<h2 id="zed">2. zeď, která má charakter</h2><p>Někdy to chce jen čisté pozadí, které nechá vyniknout vás. Starší omítka, cihlová zeď, světlý beton nebo třeba vrata garáže, všechno to může fungovat skvěle.</p>
<p class="b-poznamka">📷 Na takových fotkách vyniknou emoce, pohyb a vaše propojení, protože nic kolem neruší pozornost.</p>
</div>
{kolaz((BL + 'predsvatebni-foceni-za-farou-roztazene-ruce.jpg', 'Snoubenci tančí s roztaženýma rukama na zahradě za farou'), (BL + 'predsvatebni-foceni-za-farou-stara-vrata.jpg', 'Snoubenci u starých dřevěných vrat a cihlové zdi, předsvatební focení'), (BL + 'predsvatebni-foceni-za-farou-detail.jpg', 'Detail snoubenců u dřevěných vrat'))}
<div class="uzky b-clanek">{tp('Tohle předsvatební focení jsme fotili přímo ve vesnici snoubenců, na louce, nebo spíš zahradě za farou, která stojí hned u kostela, kde měli obřad. Byla tam i stará dřevěná vrata, která vytvořila krásnou texturu. Vystačili jsme si s málem a fotky jsou navíc spojené s místem jejich svatby.')}<h2 id="lesik">3. lesík, kousek louky nebo cesta za domem</h2><p>Myslíte si, že kolem vás není nic zajímavého? Možná byste se divili, jak kouzelně může na fotkách působit i obyčejná louka, úzká cesta za domem nebo pár stromů. Když se spojí přirozené světlo a vaše energie, vzniknou ty nejautentičtější snímky.</p><p>Navíc to má výhodu: děti se tam můžou proběhnout, pes klidně vběhne do záběru a všechno působí naprosto přirozeně.</p></div>
<figure class="foto-vyska">{img(S_ + 'novomanzele-v-zelene-krajine-prostejov.jpg', 'Ženich drží nevěstu ve vzduchu v zelené krajině s kopečky nedaleko Olomouce')}</figure>
<div class="uzky b-clanek">{tp('Tohle místo kousek od Olomouce jsem vybrala speciálně na svatební focení. Chtěla jsem, abychom ho měli v blízké dojezdové vzdálenosti, a přitom aby udělalo obrovský wow efekt. Stačí pár zelených kopečků.')}<h2 id="doma">4. u vás doma, na dvorku nebo za domem</h2><p>I váš domov může být krásnou kulisou. Zahrada plná zeleně, dřevěný plot, staré schody, koutek s květinami. Nebo váš obývák, ve kterém trávíte společné chvíle, to všechno má duši. Fotky z takového prostředí působí osobně a autenticky a může to být naprosto kouzelné.</p>
<p class="b-poznamka">💬 A bonus? Nemusíte nikam jezdit! 😁</p>
<p>Focení doma má ještě jeden přesah. Domov se časem mění: přijde rekonstrukce, nový nábytek, jiný obraz na zdi, nebo se odstěhujete. Až se na fotky podíváte za pár let, třeba i za třicet, řeknete si: „Ježiš, tady nám visel tenhle obraz a tohle byl náš koberec, úplně jsme na to zapomněli.“ Fotky tak mají o to větší váhu a o to větší příběh.</p>
<p>A i když máte pocit, že váš byt nebo dům není dost hezký, nevadí. Vždycky najdeme nějaké zákoutí, kde to bude fungovat. Místo udělá hodně, ale není to všechno.</p></div>
{dvojice_org((P + 'rodinne-foceni-doma-na-gauci.jpg', 'Rodiče s miminkem na gauči ve svém obýváku, rodinné focení doma'), (P + 'rodice-s-miminkem-doma.jpg', 'Maminka dává miminku pusu na ručičku, tatínek ho drží, rodinné focení doma'))}
<div class="uzky b-clanek">{tp('Tahle rodinka svůj byt zhruba půl roku po focení prodala, aby se mohla nastěhovat do vysněného domečku. Byt ale měli strašně rádi, a tak jsou pro ně tyhle fotky teď o to důležitější. Díky nim se můžou vrátit na místo, kam se už nejspíš nepodívají, ale kde prožili spoustu důležitých chvil.')}<h2 id="mesto">5. ulička, kavárna nebo roh domu</h2><p>I když miluju fotit v přírodě, i město je plné nenápadných zákoutí, která na fotkách působí kouzelně. Starší ulička, klidná boční cesta nebo roh domu s pěknou texturou zdi, to všechno může vytvořit nádherné pozadí, které vypadá přirozeně a nadčasově. A navíc to můžete spojit i s něčím užitečným, třeba že si po focení půjdete vychutnat něco dobrého do kavárny a uděláte si hezkej celej den. ☕️</p></div>
<figure class="foto-sirsi">{img(P + 'predsvatebni-foceni-paru-ve-meste-brno.jpg', 'Snoubenci se líbají na Staré radnici nad střechami Brna, předsvatební focení')}</figure>
<div class="uzky b-clanek">{tp('Tenhle pár mě vzal na místa, kam spolu rádi chodí na rande. Tuhle fotku jsme fotili na Staré radnici v Brně. I takhle se dá vybrat lokace: podle toho, co je vám blízké.')}</div>
<section class="zelena"><div class="uzky"><p>Takže pokud máte pocit, že „nemáte kde fotit“, věřte mi, že máte. Kouzlo není v místě, ale v pohledu, který se na něj dívá. A já věřím, že i z obyčejné cesty dokážeme vytvořit kousek vašeho příběhu. 🌿</p>
<p>📩 Chcete si zachytit své vzpomínky, ať už jste kdekoli? <a href="../contact.html">Napište mi</a>, společně najdeme místo, na kterém vzniknou fotky, co si zamilujete. ❤️</p>
<p>V Brně mám míst projitých plno! Takže pokud ke mně budete chtít přijít na focení, pošlu vám tipy na místa včetně fotek a bližších informací. ❤️✨</p><p>S láskou,<br>S.</p>
{sdileni()}</div></section>
{konec(C3['soubor'])}
{SDILET_JS}"""
DESC3 = 'Nemáte kde fotit? Univerzální lokace na focení, které máte na dosah: dobré světlo, zeď s charakterem, louka za domem, váš domov i městská zákoutí. Fotografka Sofie Zbořilová, Brno.'
stranka(C3['soubor'], head('Univerzální lokace na focení, které máte na dosah | Sofie Zbořilová', DESC3, 'blog/' + C3['soubor'], 'fotky_sdileni/univerzalni-lokace-na-foceni.jpg', 'pres-vlnu',
        ld('Univerzální lokace na focení, které máte na dosah', DESC3, C3['soubor'], 'fotky_sdileni/univerzalni-lokace-na-foceni.jpg', '2025-11-07')), T3)

# ---------- přehled blogu ----------
kategorie = []
for c in CLANKY:
    if c['kat'] not in kategorie: kategorie.append(c['kat'])
filtr = ''
if len(kategorie) > 1:
    filtr = '<div class="filtr"><button class="aktivni" data-kat="">vše</button>' + ''.join(f'<button data-kat="{k}">{k}</button>' for k in kategorie) + '</div>'
    filtr += '''<script>document.querySelectorAll('.filtr button').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('.filtr button').forEach(function(x){x.classList.toggle('aktivni',x===b);});document.querySelectorAll('.p-karta').forEach(function(k){k.style.display=(!b.dataset.kat||k.dataset.kat===b.dataset.kat)?'':'none';});});});</script>'''
O = f'''<section class="p-titul"><h1>blog</h1><p>Příběhy ze svateb, rady před focením a pohled do zákulisí. Píšu o tom, jak fotím, co mě baví a co se ti může hodit.</p>{filtr}</section>
<section class="p-mriz">{''.join(karta(c) for c in CLANKY)}</section>
<section class="konec">{MEDAILON}</section>'''
stranka('index.html', head('Blog | Fotografka Sofie Zbořilová', 'Blog fotografky Sofie Zbořilové z Brna: rady před focením, příběhy ze svateb a pohled do zákulisí focení.', 'blog/', 'fotky_sdileni/sofie-zborilova-fotografka-brno.jpg'), O)
print('hotovo')
