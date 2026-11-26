# Generuje stránky blogu (blog/index.html a články) z jednoho místa.
# Spuštění: python3 blog/gen_blog.py  (z kořene repozitáře)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
CSSV = 7
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
    <link rel="icon" href="../favicon.ico?v=4" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png?v=4">
    <link rel="icon" type="image/png" sizes="192x192" href="../favicon-192.png?v=4">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png?v=4">
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
    dict(soubor='jak-se-oblect-na-vanocni-foceni.html', kat='rady před focením', cas='4 min',
         titul='jak se obléct na vánoční focení v ateliéru',
         foto='fotky_blog/vanocni-rodinne-foceni-na-gauci-v-atelieru.jpg', foto_alt='Rodina ve světlém oblečení na gauči u vánočního stromku v ateliéru',
         perex='Nevíte, co si vzít na vánoční focení? Mám pro vás pár tipů, jak se obléct tak, aby fotky působily přirozeně, útulně a nadčasově.'),
    dict(soubor='rodinne-foceni-bez-stresu.html', kat='rady před focením', cas='4 min',
         titul='rodinné focení bez stresu: 7 tipů, jak se připravit a užít si to naplno',
         foto='fotky_portrety/holcicky-polstarova-bitva-studio.jpg', foto_alt='Holčičky s polštáři běhají po studiu, hravé rodinné focení',
         perex='Rodinné focení by nemělo být o stresu, ale o pohodě. Děti nemusí stát na místě a vy nemusíte umět pózovat. Pár tipů, jak se připravit a užít si to.'),
    dict(soubor='rodinne-foceni-jako-vzpominka.html', kat='rady před focením', cas='3 min',
         titul='rodinné focení jako vzpomínka: proč má smysl ho dělat pravidelně',
         foto='fotky_blog/rodina-u-potoka-rodinne-foceni.jpg', foto_alt='Rodiče pomáhají synovi přejít potok, rodinné focení v přírodě',
         perex='Čas letí. Všichni to říkáme, ale naplno si to uvědomíme většinou až při pohledu na staré fotky. Proč má smysl fotit rodinu pravidelně a proč to tak miluju.'),
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

# ---------- článek: jak se obléct na vánoční focení ----------
C4 = next(c for c in CLANKY if c['soubor'] == 'jak-se-oblect-na-vanocni-foceni.html')
B4 = [('barvy', 'zemité a tlumené tóny'), ('textury', 'kombinujte textury'), ('pohodli', 'pohodlí je základ'), ('sladit', 'sladit, ale ne úplně'),
      ('doplnky', 'něco navíc'), ('deti', 'oblečení pro děti'), ('sami-sebou', 'buďte sami sebou')]
T4 = f"""{hero([(BL + 'vanocni-foceni-miminko-v-cervenych-satech.jpg', 'Tatínek drží smějící se miminko v červených šatech u vánočního stromku'), (BL + 'cernobila-holcicka-u-vanocniho-stromku.jpg', 'Holčička u vánočního stromku, černobílé vánoční focení v ateliéru'), (BL + 'maminka-s-dcerou-vanocni-foceni.jpg', 'Maminka v zelených šatech s dcerou na klíně, vánoční focení v ateliéru')], 'rady před focením · 4 min čtení', 'jak se obléct na vánoční focení v ateliéru')}
<div class="uzky b-clanek"><p class="b-perex">Nevíte, co si vzít na vánoční focení? Mám pro vás pár tipů, jak se obléct tak, aby fotky působily přirozeně, útulně a nadčasově.</p>
<p>Vánoční focení je pro mě vždycky trochu srdcovka. Jednak proto, že tyhle fotky mají úplně jinou atmosféru než cokoli během roku – a taky proto, že si na chvíli všichni dovolíme zpomalit, přitulit se, a prostě být spolu. 🎄</p>
<p>A protože se mě často ptáte, co si obléct na vánoční focení, sepsala jsem pár tipů, které vám pomůžou, aby fotky působily přirozeně, hřejivě a nadčasově. A hlavně ne kýčovitě.</p>
{obsah(B4)}
<h2 id="barvy" class="prvni">1. držte se přírodních, zemitých a tlumených tónů</h2><p>Bílá, krémová, béžová, hnědá, olivová, khaki, karamelová, vínová nebo třeba jemně šedá – to jsou barvy, které ve vánočně zdobených ateliérech vypadají nádherně. Vyhněte se naopak výrazným červeným, sytě zeleným nebo zlatým tónům – ty by mohly na fotkách až moc poutat pozornost nebo vám odrážet barvy do obličeje… a to nechceme🙏🏻</p>
<p>(Když se tyto barvy vyskytují na oblečení jen v malém množství, např. v nějakém vzoru, tak to nevadí.)</p>
<p class="b-poznamka">👉 Tady platí: méně je víc. Čím jemnější barvy, tím víc vyniknete vy a vaše emoce.</p>
<p>Další tipy na barvy a palety pro každé roční období najdete v článku <a href="co-si-vzit-na-sebe-na-foceni.html">co si vzít na sebe na focení</a>.</p></div>
{dvojice_org((BL + 'vanocni-foceni-rodina-v-zemitych-barvach.jpg', 'Rodina v zemitých barvách u vánočního stromku, maminka v olivově zelených šatech'), (BL + 'holcicka-u-vanocniho-stromku.jpg', 'Holčička v tylové sukni sahá na vánoční stromek'))}
<div class="uzky b-clanek"><h2 id="textury">2. kombinujte textury</h2><p>Když je prostor bílý a minimalistický, skvěle vyniknou různé materiály. Zkuste třeba kombinaci pleteniny, lnu, džínoviny, vlny nebo manšestru. Pletený svetr, jemná košile, dlouhé šaty nebo volné kalhoty – všechno, co působí měkce a pohodlně, se do takového prostředí hodí skvěle.</p></div>
<figure class="foto-vyska">{img(BL + 'vanocni-tehotenske-foceni-v-atelieru-cernobile.jpg', 'Budoucí rodiče v pletených svetrech u vánočního stromku, černobílé těhotenské focení v ateliéru')}</figure>
<div class="uzky b-clanek"><h2 id="pohodli">3. pohodlí je základ</h2><p>Cílem vánočního focení není dokonalost, ale pohoda. Chci, abyste se cítili dobře, mohli se přitulit, sednout si, lehnout, obejmout se. Takže pokud váháte mezi něčím, co „vypadá dobře“, a tím, v čem se cítíte skvěle – vybírejte pohodlí. Na fotkách je totiž vždycky vidět, jak se cítíte.</p>
<p>Pokud jste ale objednaní na delší focení (o délce 1 hodiny), tak je prostor i na více variant oblečení, takže můžete využít různé styly😊</p></div>
<figure class="foto-sirsi">{img(BL + 'rodina-lezi-na-plysovem-medvedovi-vanocni-foceni.jpg', 'Rodina leží na velkém plyšovém medvědovi, pohodové vánoční focení v ateliéru')}</figure>
<div class="uzky b-clanek"><h2 id="sladit">4. sladit, ale ne úplně</h2><p>Pokud přijdete ve dvojici nebo s dětmi, zkuste sladit outfity do jednoho stylu a barevné palety, ale ne do stejného oblečení.</p>
<p>Třeba: maminka v béžových šatech, táta v hnědé košili, dítě v krémovém svetříku a tmavě zelených kalhotech. Dohromady to bude působit přirozeně, měkce a vizuálně sjednoceně – ale ne „přes kopírák“.</p>
<p>Zkuste se prosím vyhnout tomu, aby jeden člen rodiny přišel v teplákách a druhý ve svátečním elegantním oblečení – takový kontrast na focení opravdu nechceme.</p>
<p class="b-poznamka">✨ TIP: Tato rodinka ale ukázala, že existují i výjimky. Nechali si natisknout společné mikiny s perníčkem a i když byli všichni oblečení stejně, vypadalo to kouzelně🥰</p></div>
<figure class="foto-sirsi">{img(BL + 'vanocni-rodinne-foceni-na-gauci-v-atelieru.jpg', 'Rodina ve stejných světlých mikinách s miminkem na gauči u vánočního stromku')}</figure>
<div class="uzky b-clanek"><h2 id="doplnky">5. dopřejte si něco navíc</h2><p>Šála, pletené ponožky, hrnek s kakaem, oblíbená knížka nebo třeba vánoční sušenky – drobnosti, které přinesete, dodají fotkám atmosféru. A pokud máte doma něco, co k vám prostě patří (např. plyšák vašeho dítěte nebo oblíbená deka), klidně to vezměte s sebou.</p></div>
{dvojice_org((BL + 'vanocni-darky-a-svicky-rodinne-foceni.jpg', 'Rodiče s dcerou rozbalují dárky mezi svíčkami, vánoční rodinné focení'), (BL + 'tatinek-v-pletenem-svetru-s-dcerou.jpg', 'Tatínek ve světlém pleteném svetru s dcerou v ateliéru'))}
<div class="uzky b-clanek"><h2 id="deti">6. oblečení pro děti</h2><p>U dětí platí to samé – zvolte tlumené barvy a měkké materiály. Svetříky, lacláče, malé šatičky, overal, klidně i punčochy. Vyhněte se velkým potiskům, logům a nápisům.</p>
<p>A hlavně: nechte je být samy sebou. I když si sundají ponožky nebo rozcuchají vlasy, bude to kouzelný. 🤍</p></div>
{dvojice_org((BL + 'holcicka-v-tutu-sukni-u-stromecku.jpg', 'Holčička v tylové sukni stojí u vánočního stromku'), (BL + 'holcicka-se-smeje-vanocni-foceni-v-atelieru.jpg', 'Smějící se holčička sedí na bílém pufu, vánoční focení v ateliéru'))}
<div class="uzky b-clanek"><h2 id="sami-sebou">7. a nakonec: buďte sami sebou</h2><p>To nejhezčí na focení nejsou outfity, ale vy. Jak se smějete, jak se objímáte, jak vaše děti koukají na světýlka. Oblečení jen podtrhne to, co je uvnitř – a o to mi při focení vždycky jde.</p></div>
<figure class="foto-sirsi">{img(BL + 'vanocni-rodinne-foceni-smich.jpg', 'Rodiče se smějí s dcerou mezi polštáři, přirozené vánoční rodinné focení')}</figure>
<section class="zelena"><div class="uzky"><p>📸 Pokud si nejste jistí, co si vzít, klidně mi napište – moc ráda vám s výběrem pomůžu (nebo pošlu pár ukázek). A hlavně – užijte si samotné focení. Protože u těchto fotek budete jednou vzpomínat na dobu, kdy jste byli spolu. 🌙</p>
<p>Chcete letos taky vánoční fotky, které nebudou kýčovité, ale hřejivé a hlavně vaše? Termíny na vánoční focení v ateliéru se každý rok rychle plní, tak mi napište včas přes <a href="../contact.html">kontaktní formulář</a> nebo <a href="https://www.instagram.com/sofiezbo/">Instagram</a>. Ceny najdete v <a href="../cenik.html">ceníku</a> a ukázky vánočních focení v <a href="../portrety.html">portfoliu</a>. ✨</p>
<p>S láskou,<br>Sofi</p>
{sdileni()}</div></section>
{konec(C4['soubor'])}
{SDILET_JS}"""
DESC4 = 'Jak se obléct na vánoční focení v ateliéru: 7 tipů na barvy, textury, sladění rodiny i oblečení pro děti, aby fotky byly útulné, nadčasové a ne kýčovité. Fotografka Sofie Zbořilová, Brno.'
stranka(C4['soubor'], head('Jak se obléct na vánoční focení v ateliéru: 7 tipů | Sofie Zbořilová', DESC4, 'blog/' + C4['soubor'], 'fotky_sdileni/jak-se-oblect-na-vanocni-foceni.jpg', 'pres-vlnu',
        ld('Jak se obléct na vánoční focení v ateliéru', DESC4, C4['soubor'], 'fotky_sdileni/jak-se-oblect-na-vanocni-foceni.jpg', '2025-11-04')), T4)

# ---------- článek: rodinné focení jako vzpomínka ----------
C5 = next(c for c in CLANKY if c['soubor'] == 'rodinne-foceni-jako-vzpominka.html')
B5 = [('kazdy-rok', 'každý rok je jiný'), ('chvile-pro-vas', 'chvíle pro vás'), ('hodnota', 'fotky s nevyčíslitelnou hodnotou'),
      ('jak-casto', 'jak často se fotit'), ('co-si-odnest', 'co si z toho odnést')]
T5 = f"""{hero([(BL + 'rodina-u-potoka-rodinne-foceni.jpg', 'Rodiče pomáhají synovi přejít potok, rodinné focení v přírodě'), (P + 'rodinne-foceni-v-prirode-brno-2.jpg', 'Rodina s miminkem sedí v lese v protisvětle, černobílé rodinné focení'), (P + 'rodinne-foceni-bez-pozovani-brno.jpg', 'Rodiče se synem v rozkvetlé louce, rodinné focení bez pózování')], 'rady před focením · 3 min čtení', 'rodinné focení jako vzpomínka')}
<div class="uzky b-clanek"><p class="b-perex">Proč má smysl ho dělat pravidelně a proč ho tak miluju 🥰</p>
<blockquote class="b-citat">„Čas letí.“</blockquote>
<p>Všichni to říkáme, všichni to víme – ale naplno si to uvědomíme většinou až při pohledu na staré fotky nebo až když je pozdě.</p>
<p>Děti, které ještě před chvílí lezly po čtyřech, dnes běhají do školy. Naši rodiče, kteří se o nás celý život starali, dnes mají na tváři o pár vrásek navíc a možná teď potřebují, abychom se na oplátku postarali my o ně.</p>
<p>A my si přejeme, abychom mohli ty chvíle prožít znovu – i když jen na okamžik.</p>
<p>A přesně o tom rodinné focení je. Ne o dokonalých pózách nebo perfektních outfitech. Ale o zachycení okamžiků, které tvoří váš příběh.</p>
{obsah(B5)}
<h2 id="kazdy-rok" class="prvni">každý rok je jiný</h2><p>Každý rok se v rodině něco změní. Děti vyrostou, na nás jde vidět, jak vnitřně rosteme, máme jiné priority a třeba jsme změnili práci nebo bydlíme v jiném bytě. Rodinné fotky jsou krásný způsob, jak ten vývoj zachytit – a jak se po letech podívat zpátky a vidět, kolik lásky, smíchu i obyčejných dní za tím vším bylo.</p></div>
<figure class="foto-sirsi">{img(BL + 'cernobile-tehotenske-foceni-ve-studiu.jpg', 'Budoucí maminka v černých šatech drží bříško, černobílé těhotenské focení ve studiu')}</figure>
<div class="uzky b-clanek"><p>Fotím rodiny, které ke mně chodí každý rok. Vždycky se těší, až se na fotky podívají a zjistí, co všechno se změnilo, a až si aspoň na chvíli prožijí ty krásné momenty, kdy byli spolu.</p>
<h2 id="chvile-pro-vas">focení není povinnost, ale chvíle pro vás</h2><p>Vím, že pro spoustu lidí může být představa focení stresující.</p>
<blockquote class="b-citat">„Děti stejně neposedí.“<br>„Já nejsem fotogenická.“<br>„Nevím, co si obléct.“</blockquote>
<p>Tyhle věty slyším často. Ale pokaždé, když focení skončí, slyším jinou:</p>
<blockquote class="b-citat">„Bylo to vlastně hrozně příjemné a ani jsme si neuvědomili, že jsme na focení!“</blockquote>
<p>Rodinné focení není jen o fotkách. Je to čas, kdy se konečně zastavíte. Kdy se smějete, hrajete si, obejmete se – a ani si neuvědomíte, že vás u toho někdo fotí.</p></div>
<figure class="foto-vyska">{img(BL + 'holcicka-drzi-maminku-za-ruce-rodinne-foceni.jpg', 'Malá holčička v šedém svetříku drží maminku za ruce a učí se chodit')}</figure>
<div class="uzky b-clanek"><h2 id="hodnota">fotky, které budou mít jednou nevyčíslitelnou hodnotu</h2><p>Možná teď máte pocit, že fotky jsou jen „něco navíc“.</p>
<p>Ale za pár let – až budete listovat albem – se budete smát, dojímat a říkat si: „Tohle bylo to období, kdy…“</p>
<p>Fotky mají zvláštní sílu. Vrací vás zpátky do míst a chvil, které už dávno nejsou, ale pořád v nás žijí. Jednoho dne pro vás ty snímky budou nejcennějším mostem do minulosti. 🌿</p></div>
<figure class="foto-vyska">{img(P + 'rodinne-foceni-v-prirode-brno.jpg', 'Táta objímá dceru a vnučku v zahradě, rodinné focení tří generací')}</figure>
<div class="uzky b-clanek"><h2 id="jak-casto">jak často má smysl se fotit</h2><p>Rodinné focení dává největší smysl dělat pravidelně – třeba jednou ročně. Nemusí to být vždy stejné prostředí nebo stejné období. Naopak – právě ta pestrost dělá váš příběh autentickým.</p>
<p>Pro někoho je to letní focení v přírodě, pro jiné zase koulování se na zasněžené louce nebo třeba klidné dny strávené <a href="univerzalni-lokace-na-foceni.html">u vás doma</a>. Přemýšlejte o focení tak, že chcete zachovat, jací doopravdy jste, co vás vystihuje.</p></div>
{kolaz((P + 'hrave-rodinne-foceni-venku.jpg', 'Hravé rodinné focení venku v létě'), (P + 'rodice-drzi-dcery-vanocni-foceni.jpg', 'Rodiče drží dcery v náručí, vánoční rodinné focení ve studiu'), (P + 'rodina-s-miminkem-v-kuchyni.jpg', 'Rodiče s miminkem v objetí ve své kuchyni, rodinné focení doma'))}
<div class="uzky b-clanek"><h2 id="co-si-odnest">co si z toho mám teda odnést?</h2><p>Vzpomínky sice žijí v našich hlavách, ale časem se nám chtě nechtě promění nebo vytratí úplně. Fotky jim ale dávají tvar a díky nim se můžeme znovu přenést do chvil, které jsou pro nás cenné.</p>
<p>Umožňují nám dotknout se času, který už odešel – a připomenout si, co je opravdu důležité.</p></div>
<section class="zelena"><div class="uzky"><p>Pokud máte pocit, že letos chcete něco uchovat, něco pro sebe – pojďme zachytit vaši rodinu takovou, jaká je právě teď.</p>
<p>Protože za pár let vám ty fotky řeknou víc, než by kdy dokázala slova. 🤍</p>
<p>Rodinné focení fotím v Brně i v Bratislavě – venku v přírodě, ve studiu nebo klidně u vás doma. Jak takové focení u mě probíhá, si můžete přečíst <a href="jak-u-me-probiha-rodinne-a-parove-foceni.html">tady</a>, ceny najdete v <a href="../cenik.html">ceníku</a> a ukázky rodinných fotek v <a href="../portrety.html">portfoliu</a>.</p>
<p>📩 Rezervujte si svůj termín přes <a href="../contact.html">kontaktní formulář</a>.</p>
{sdileni()}</div></section>
{konec(C5['soubor'])}
{SDILET_JS}"""
DESC5 = 'Rodinné focení jako vzpomínka: proč má smysl fotit rodinu pravidelně, třeba jednou ročně, a proč fotky jednou budou mít nevyčíslitelnou hodnotu. Fotografka Sofie Zbořilová, Brno.'
stranka(C5['soubor'], head('Rodinné focení jako vzpomínka: proč ho dělat pravidelně | Sofie Zbořilová', DESC5, 'blog/' + C5['soubor'], 'fotky_sdileni/rodinne-foceni-jako-vzpominka.jpg', 'pres-vlnu',
        ld('Rodinné focení jako vzpomínka: proč má smysl ho dělat pravidelně', DESC5, C5['soubor'], 'fotky_sdileni/rodinne-foceni-jako-vzpominka.jpg', '2026-11-26')), T5)

# ---------- článek: rodinné focení bez stresu ----------
C6 = next(c for c in CLANKY if c['soubor'] == 'rodinne-foceni-bez-stresu.html')
B6 = [('vyspete-se', 'vyspěte se'), ('obleceni', 'oblečení'), ('drobnosti', 'drobnosti, které děti milují'), ('jidlo', 'jídlo s rozmyslem'),
      ('priprava', 'nepřehánějte přípravy'), ('pohyb', 'nebojte se pohybu'), ('plynout', 'nechte to plynout')]
T6 = f"""{hero([(P + 'rodinne-foceni-v-prirode-hrave-brno.jpg', 'Hravé rodinné focení v přírodě u Brna'), (BL + 'cernobile-novorozenecke-foceni-miminko-na-rameni-tatinka.jpg', 'Miminko kouká tatínkovi přes rameno, černobílé rodinné focení'), (P + 'deti-bezi-za-rodici-vanocni-foceni.jpg', 'Holčičky běží rodičům do náruče, vánoční rodinné focení')], 'rady před focením · 4 min čtení', 'rodinné focení bez stresu: 7 tipů, jak se připravit')}
<div class="uzky b-clanek"><p class="b-perex">Rodinné focení by nemělo být o stresu, ale o pohodě. Nemusíte mít všechno dokonalé, děti nemusí stát na místě, a už vůbec nemusíte mít pocit, že musíte „umět pózovat“.</p>
<p>Cílem je zachytit vás takové, jací jste – přirozeně, autenticky a v pohodě. 🤍</p>
<p>Aby focení proběhlo co nejlépe, sepsala jsem pár jednoduchých tipů, které vám pomůžou se připravit – a zároveň si to celé opravdu užít.</p>
{obsah(B6)}
<h2 id="vyspete-se" class="prvni">1. vyspěte se (nebo ať jsou vyspané aspoň děti 😄)</h2><p>Kdybyste si z celého článku měli odnést jen jednu věc, bude to první a poslední bod tohoto článku. 🙏🏻</p>
<p>Vyspané děti = spokojené děti. Pokud fotíme odpoledne, zkuste, aby měly klidné dopoledne a dostatek jídla i pití. A když budete vyspaní i vy, bude to to nejlepší, co můžete udělat. Nezapomeňte totiž, že děti jsou jako zrcadlo a když z nás cítí, že nejsme v pohodě, nebudou ani ony. 🌿</p></div>
<figure class="foto-vyska">{img(BL + 'cernobile-novorozenecke-foceni-miminko-na-rameni-tatinka.jpg', 'Miminko kouká tatínkovi přes rameno, maminka se na něj usmívá, černobílé rodinné focení')}</figure>
<div class="uzky b-clanek"><h2 id="obleceni">2. oblečení – méně je více</h2><p>Držte se jednoduchosti a tónů, které k sobě ladí. Zemité barvy, béžová, krémová, tlumená zelená, světle hnědá – to nikdy nezklame. Vyhněte se křiklavým barvám, velkým logům a vzorům. Podrobněji jsem se rozepsala v článku <a href="co-si-vzit-na-sebe-na-foceni.html">co si vzít na sebe na focení</a> (a pokud se chystáte na Vánoce, tak i v článku <a href="jak-se-oblect-na-vanocni-foceni.html">jak se obléct na vánoční focení</a>).</p>
<p class="b-poznamka">🧺 Malý tip: připravte si oblečení dostatečně předem, abyste to neřešili pár minut před odjezdem na focení.</p>
<h2 id="drobnosti">3. přibalte drobnosti, které děti milují 🧸</h2><p>Hračku, plyšáka, oblíbený hrníček nebo sušenky – cokoli, co pomůže uvolnit atmosféru. Často právě tyhle malé rekvizity udělají fotky ještě osobnějšími.</p></div>
{dvojice_org((P + 'holcicky-polstarova-bitva-studio.jpg', 'Holčičky s polštáři běhají po studiu, hravé rodinné focení'), (P + 'sestry-se-tuli-vanocni-foceni.jpg', 'Sestry se tulí nosy k sobě, vánoční focení ve studiu'))}
<div class="uzky b-clanek"><h2 id="jidlo">4. jídlo ano, ale s rozmyslem</h2><p>Někdy je potřeba doplnit energii a je to úplně v pohodě. Pokud budete na focení brát nějaké jídlo, zkuste se vyhnout čokoládě. Jestli chcete opravdu realistické fotky a chcete, aby se vaše dítě patlalo ve svém prvním dortu – I’m all in! 😄 Ale pokud se jedná o „obyčejné“ rodinné focení, čokoláda vám může lehce zašpinit oblečení – a to nechceme.</p>
<h2 id="priprava">5. nepřehánějte to s přípravami 🫶🏻</h2><p>Není potřeba, aby bylo všechno dokonalé. Nejkrásnější fotky vznikají, když jste sami sebou. Když se smějete, běháte, děláte si legraci – prostě když žijete.</p>
<p class="b-poznamka">Focení není soutěž o nejhezčí rodinu, ale o zachycení vašeho vztahu a lásky. 🤍</p></div>
<figure class="foto-vyska">{img(BL + 'rodice-vyhazuji-smejici-se-miminko-vanocni-foceni.jpg', 'Rodiče se smějí a vyhazují miminko do vzduchu u vánočního stromku')}</figure>
<div class="uzky b-clanek"><h2 id="pohyb">6. nebojte se pohybu</h2><p>Nechci po vás, abyste stáli jako přikovaní a dívali se do objektivu – dobře, možná uděláme jednu takovou fotku pro babičku, ale u té to skončí. 😄</p>
<p>Budu vás navádět tak, aby to bylo přirozené – procházka, hra s dětmi, tanec nebo klidné objetí. Když se budete hýbat, přirozeně zapomenete na foťák – a právě tehdy vznikají ty nejhezčí momenty.</p></div>
<figure class="foto-sirsi">{img(P + 'hrave-rodinne-foceni-venku.jpg', 'Hravé rodinné focení venku v pohybu')}</figure>
<div class="uzky b-clanek"><h2 id="plynout">7. všechno nechte trochu plynout ☀️</h2><p>Připravte se, ale netlačte na dokonalost. Když dítě nechce spolupracovat, nic se neděje a hlavně, je to úplně normální. Děti nejsou stroj, aby hodinu v kuse poslouchaly naše pokyny. Nemusí mít neustále úsměv od ucha k uchu.</p>
<p>Nechme děti, aby byly dětmi a klidně i tím, kdo bude určovat průběh focení. Chtějí jít k vodě a hrát si s kamínky? Super! Pojďme všichni! Chtějí dělat závody v běhu? Můžeme!</p></div>
<figure class="foto-sirsi">{img(BL + 'rodina-u-potoka-rodinne-foceni.jpg', 'Rodiče pomáhají synovi přejít potok po kamenech, rodinné focení v přírodě')}</figure>
<div class="uzky b-clanek"><p>Děti nás svými nápady dokážou nádherně uvolnit – a je krásné, když se i dospělí nechají strhnout a na chvíli se znovu stanou dětmi.</p>
<p>A navíc, někdy z toho, co se zdá jako „nepovedená chvilka“, vznikne ta nejhezčí fotka z celého focení.</p></div>
<section class="zelena"><div class="uzky"><p>Rodinné focení není o perfektnosti. Je o vás – o tom, že jste spolu, že se smějete, že máte mezi sebou něco, co stojí za zachycení. A pokud si z toho kromě krásných fotek odnesete i hezký společný zážitek, splnilo to přesně svůj účel. 🌿</p>
<p>📩 Chcete si domluvit rodinné focení v Brně nebo okolí? <a href="../contact.html">Napište mi</a> – společně to vymyslíme tak, aby to bylo přesně „vaše“. Ceny najdete v <a href="../cenik.html">ceníku</a> a ukázky rodinných fotek v <a href="../portrety.html">portfoliu</a>.</p>
{sdileni()}</div></section>
{konec(C6['soubor'])}
{SDILET_JS}"""
DESC6 = 'Rodinné focení bez stresu: 7 tipů, jak se připravit a užít si to naplno. Spánek, oblečení, hračky, jídlo, pohyb a děti, které nemusí stát na místě. Fotografka Sofie Zbořilová, Brno.'
stranka(C6['soubor'], head('Rodinné focení bez stresu: 7 tipů, jak se připravit | Sofie Zbořilová', DESC6, 'blog/' + C6['soubor'], 'fotky_sdileni/rodinne-foceni-bez-stresu.jpg', 'pres-vlnu',
        ld('Rodinné focení bez stresu: 7 tipů, jak se připravit a užít si to naplno', DESC6, C6['soubor'], 'fotky_sdileni/rodinne-foceni-bez-stresu.jpg', '2026-11-26')), T6)

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
