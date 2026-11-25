# Generuje stránky blogu (blog/index.html a články) z jednoho místa.
# Spuštění: python3 blog/gen_blog.py  (z kořene repozitáře)
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
CSSV = 1
src = open('podminky.html', encoding='utf-8', newline='').read()
hdr = src[src.index('<button class="mobile-menu-btn"'):src.index('<main')]
hdr = hdr.replace('\r\n', '\n').replace('href="', 'href="../')
hdr = hdr.replace('<!--<a href="../#">blog</a>\n            <a href="../#">o mně</a>-->', '<a href="./">blog</a>')
hdr = hdr.replace('<!--<div class="Item-4"> blog</div>\n            <div class="Item-4"> o mně</div>-->', '<div class="Item-4"> <a href="./">blog</a></div>')
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
    <link rel="icon" href="../favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="../favicon-192.png">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png">
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
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

C = CLANKY[0]
TITLE = 'Co si vzít na sebe na focení: 7 tipů, aby ti to slušelo | Sofie Zbořilová'
DESC = 'Nevíš, co si vzít na sebe na focení? 7 tipů od fotografky z Brna: jaké barvy a materiály volit, jak se sladit na rodinné či párové focení a palety barev pro každé roční období.'
LD = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Co si vzít na sebe na focení: 7 tipů, aby ti to slušelo",
      "description": DESC, "inLanguage": "cs", "datePublished": "2026-11-25", "dateModified": "2026-11-25",
      "image": WEB + "fotky_sdileni/co-si-vzit-na-sebe-na-foceni.jpg", "mainEntityOfPage": WEB + "blog/" + C['soubor'],
      "author": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB},
      "publisher": {"@type": "Person", "name": "Sofie Zbořilová", "url": WEB}}
EXTRA = '\n    <script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False) + '</script>'

P = 'fotky_portrety/'; R = 'fotky_produktove/'; BL = 'fotky_blog/'
T = f'''<section class="b-hero">{img(P + 'hrave-rodinne-foceni-venku.jpg', 'Hravé rodinné focení venku', lazy=False)}{img(P + 'parove-foceni-tanec-na-louce.jpg', 'Párové focení, tanec na louce', lazy=False)}{img(P + 'rodinne-foceni-v-kvetouci-louce.jpg', 'Rodinné focení v kvetoucí louce', lazy=False)}
<div class="b-hero-text"><span class="kategorie">rady před focením · 5 min čtení</span><h1>co si vzít na sebe na focení: 7 tipů, aby ti to slušelo</h1></div></section>
<div class="uzky b-clanek"><p class="b-perex">Oblečení hraje na fotkách obrovskou roli. Proto jsem sepsala pár rad a základních pravidel, kterých je fajn se při výběru outfitu držet. Platí pro portrétní, párové i rodinné focení.</p>
{OBSAH}
<h2 id="neonove-barvy" class="prvni">1. nech doma neonové barvy, loga a nápisy</h2><p>Tohle je základ všeho, a pokud si máš zapamatovat jediné pravidlo, je to tohle. Na fotkách má jít hlavně o tebe a o chvíli, kterou se snažíme zachytit, takže nedopusť, aby tě oblečení překřikovalo. Výrazné a křiklavé barvy se navíc odrážejí do obličeje, a to fakt nechceme. A hlavně se vyhni velkým logům a nápisům. Malé nenápadné logo nevadí, ale když to jde úplně bez, je to určitě lepší.</p></div>
{dvojice((P + 'parove-foceni-na-louce-v-objeti.jpg', 'Pár v objetí na louce v jednoduchém oblečení bez nápisů'), (P + 'rodinne-foceni-v-prirode-hrave-brno.jpg', 'Rodina ve světlém oblečení na focení v přírodě u Brna'))}
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
<section class="zelena"><div class="uzky"><h2>na závěr</h2><p>Tohle bylo mých 7 tipů a jeden bonusový, kterých se můžeš držet. Chtěla bych ale zdůraznit, že není až tak důležité, kde fotíme a jak vypadáš, ale hlavně jak se cítíš. Soustřeď se hlavně na to, ať tě focení baví. Jak budou fotky vypadat, nech na mně.</p><p>Když si s výběrem nebudeš vědět rady, napiš mi. Moc ráda ti s oblečením pomůžu. A jestli chceš vidět, jak to vypadá v praxi, sleduj mě na Instagramu <a href="https://www.instagram.com/sofiezbo/">@sofiezbo</a>.</p>
<p class="sdilet"><span>Znáš někoho, komu by tenhle článek pomohl? Klidně mu ho pošli.</span><button type="button" id="sdilet">sdílet článek</button></p></div></section>
{konec(C['soubor'])}
<script>document.getElementById('sdilet').addEventListener('click',function(){{var b=this,u=location.href.split('#')[0];if(navigator.share){{navigator.share({{title:document.title,url:u}}).catch(function(){{}});}}else if(navigator.clipboard){{navigator.clipboard.writeText(u).then(function(){{b.textContent='odkaz zkopírován';setTimeout(function(){{b.textContent='sdílet článek';}},2500);}});}}}});</script>'''
stranka(C['soubor'], head(TITLE, DESC, 'blog/' + C['soubor'], 'fotky_sdileni/co-si-vzit-na-sebe-na-foceni.jpg', 'pres-vlnu', EXTRA), T)

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
