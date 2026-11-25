import os,re
os.chdir('/home/user/site')
src=open('podminky.html',encoding='utf-8',newline='').read()
hdr=src[src.index('<button class="mobile-menu-btn"'):src.index('<main')]
hdr=hdr.replace('href="','href="../').replace("href=\"../#","href=\"#")
hdr=hdr.replace('<div class="Item-4"> <a href="../contact.html">kontakt</a></div>','<div class="Item-4"> <a href="blog.html">blog</a></div>\n            <div class="Item-4"> <a href="../contact.html">kontakt</a></div>')
hdr=hdr.replace('<a href="../contact.html">kontakt</a>\n        </div>\n    </div>','<a href="blog.html">blog</a>\n            <a href="../contact.html">kontakt</a>\n        </div>\n    </div>',1)
foot=src[src.index('<footer'):src.index('</footer>')+9]
LISTA='''<nav class="lista" aria-label="Menu"><a href="../index.html">hlavní stránka</a><a href="../svatby.html">portfolio</a><a href="../cenik.html">ceník</a><a href="blog.html">blog</a><a href="../contact.html">kontakt</a></nav>
<script>(function(){var l=document.querySelector('.lista'),h=document.querySelector('.black_background');function f(){l.classList.toggle('vidět',window.scrollY>(h.offsetHeight+60));}window.addEventListener('scroll',f,{passive:true});f();})();</script>'''
head='''<!DOCTYPE html><html lang="cs"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{t}</title>
<link rel="stylesheet" href="../contact.css?v=9"><link rel="stylesheet" href="../paticka.css?v=1"><link rel="stylesheet" href="blog.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100..900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet"></head><body class="{b}">'''
S='../fotky_svadby/';P='../fotky_portrety/';R='../fotky_produktove/';F='../fotky/'
def img(p,c='',alt=''):return f'<img class="{c}" src="{p}" alt="{alt}">'
K={'sv1':(S+'novomanzele-v-objeti-parove-foceni-vachuv-mlyn-trebejice.jpg','svatby','letní svatba ve Váchově mlýně'),
'sv2':(S+'novomanzele-na-pude-svatebni-portret-dohnaluv-mlyn.jpg','svatby','svatba v Dohnalově mlýně'),
'ra2':(P+'rodinna-laska-novorozenecke-foceni-brno.jpg','rady před focením','rodinné focení bez stresu: 7 tipů, jak se připravit'),
'ra3':(P+'portretni-foceni-se-psem-husky-les.jpg','rady před focením','univerzální lokace na focení, které máš na dosah'),
'sv3':(S+'zenich-objima-nevestu-smich-svatojakubsky-pivovar-hluboke.jpg','svatby','Klára a Michal: svatba na dvoře starého pivovaru')}
def karta(k):
    p,c,t=K[k];return f'<div class="karta">{img(p)}<span class="kategorie">{c}</span><h3>{t}</h3></div>'
def konec(nadpis,pod,karty,cta,odkazy):
    return f'''<section class="konec"><div class="medailon">{img(F+'sofie-zborilova-fotografka-portret.webp')}<div><h3>ahoj, jsem sofi</h3><p>Fotím svatby, rodiny a značky v Brně a Bratislavě. Mám ráda přirozené momenty, jemné barvy a lidi, kteří se nebojí být sami sebou.</p><a class="tlacitko" href="#">{cta}</a><span class="odkazy">{odkazy}</span></div></div>
<div class="dalsi"><h2>{nadpis}</h2><p class="podnadpis">{pod}</p><div class="karty">{''.join(karta(k) for k in karty)}</div></div></section>'''
def page(fn,t,body,b=''):
    open('nahled-blog/'+fn,'w',encoding='utf-8').write(head.format(t=t,b=b)+hdr+LISTA+'<main class="blog">'+body+'</main>'+foot+'</body></html>')
PAL={'jarní focení':[('vanilková','#F2DE9C'),('šalvějová','#A9B98F'),('korálová','#E3826B'),('prachově modrá','#9FB6CB'),('pudrově růžová','#EDC5C0'),('eukalyptová','#7F958C')],
'letní focení':[('bílá','#FFFFFF'),('lněná','#D8C7AA'),('starorůžová','#B07A74'),('levandulová','#B8A6CA'),('blankytná','#6CA0CF'),('námořnická','#1F3A5F')],
'podzimní focení':[('hořčicová','#A97C2E'),('karamelová','#C78F5E'),('rezavá','#9A4A2E'),('olivová','#9D9167'),('lesní zelená','#3E5A3F'),('čokoládová','#5C3B2A')],
'zimní focení':[('smetanová','#F2EBDD'),('šedohnědá','#9A8B7E'),('oříšková','#8C6A4E'),('vínová','#5C1F2E'),('švestková','#6E4F57'),('espresso','#2B211D')]}
def svetla(h):
    r,g,b=[int(h[i:i+2],16) for i in (1,3,5)];return 0.299*r+0.587*g+0.114*b>170
def palety():
    o='<div class="palety">'
    for s,cs in PAL.items():
        o+=f'<div class="paleta-sezona"><h4>{s}</h4><p class="pod">paleta barev</p><div class="barvy">'
        for n,h in cs: o+=f'<div class="barva{" svetla" if svetla(h) else ""}" style="background:{h}"><span>{n}</span></div>'
        o+='</div><p class="web">sofiezborilova.cz</p></div>'
    return o+'</div>'
PALHTML=palety()
B=f'''<section class="hero-pod-vlnou b-hero">{img(P+'hrave-rodinne-foceni-venku.jpg')}{img(P+'parove-foceni-tanec-na-louce.jpg')}{img(P+'rodinne-foceni-v-kvetouci-louce.jpg')}
<div class="b-hero-text"><span class="kategorie">rady před focením · 5 min čtení</span><h1>co si vzít na sebe na focení: 7 tipů, aby ti to slušelo</h1></div></section>
<div class="uzky b-clanek"><p class="b-perex">Oblečení hraje na fotkách obrovskou roli. Proto jsem sepsala pár rad a základních pravidel, kterých je fajn se při výběru outfitu držet. Platí pro portrétní, párové i rodinné focení.</p>
<div class="obsah-obal"><div class="obsah" style="clip-path:polygon(0% 0.4%,5% 1.2%,10% 0.2%,15% 1%,20% 0.3%,25% 1.4%,30% 0.6%,35% 0.1%,40% 1.1%,45% 0.5%,50% 1.3%,55% 0.2%,60% 0.9%,65% 0.4%,70% 1.5%,75% 0.3%,80% 1%,85% 0.2%,90% 1.2%,95% 0.5%,100% 0.8%,99.5% 20%,100% 40%,99.3% 60%,99.8% 80%,99.4% 99.3%,90% 99.8%,80% 98.6%,70% 99.6%,60% 98.9%,50% 99.7%,40% 98.5%,30% 99.4%,20% 98.8%,10% 99.6%,0.3% 98.9%,0.7% 80%,0.1% 60%,0.6% 40%,0.2% 20%)"><b>v článku najdeš</b><ol><li>neonové barvy, loga a nápisy</li><li>zemité barvy a palety</li><li>materiály a textury</li><li>rozevláté oblečení</li><li>doplňky</li><li>sladit, nebo nesladit?</li><li>tvoje srdcovka</li><li>bonus: výběr fotografa</li></ol></div></div>
<h2>1. nech doma neonové barvy, loga a nápisy</h2><p>Tohle je základ všeho, a pokud si máš zapamatovat jediné pravidlo, je to tohle. Na fotkách má jít hlavně o tebe a o chvíli, kterou se snažíme zachytit, takže nedopusť, aby tě oblečení překřikovalo. Výrazné a křiklavé barvy se navíc odrážejí do obličeje, a to fakt nechceme. A hlavně se vyhni velkým logům a nápisům. Malé nenápadné logo nevadí, ale když to jde úplně bez, je to určitě lepší.</p></div>
<div class="b-dvojice"><figure>{img(P+'parove-foceni-na-louce-v-objeti.jpg')}<figcaption>Jednoduché oblečení bez nápisů nechá vyniknout vás dva.</figcaption></figure><figure>{img(P+'rodinne-foceni-v-prirode-hrave-brno.jpg')}<figcaption>Světlé tóny, které ladí s přírodou.</figcaption></figure></div>
<div class="uzky b-clanek"><h2>2. zemité barvy tě nikdy nezklamou</h2><p>Když vůbec nevíš, co si vzít na sebe a jak zkombinovat barvy, sáhni po zemitých tónech. S nimi nikdy nešlápneš vedle. Fotím hlavně v přírodě a tam se hodí obzvlášť. Mám ráda i pastelové barvy, na fotkách vypadají skvěle.</p><p>Pro inspiraci přikládám paletu barev ke každému ročnímu období. Ber ji opravdu jen jako inspiraci, většina barev se hodí skoro vždycky. Mysli ale na místo, kde budeme fotit, aby se tvoje oblečení nebilo s pozadím.</p></div>
<div class="palety-obal">{PALHTML}</div>
<div class="uzky b-clanek"><h2>3. materiály a textury</h2><p>Neboj se kombinovat. Na fotkách vypadají skvěle různé textury, třeba kůže, koženka, džínovina, len nebo pletenina. Outfit tak jednoduše ozvláštníš.</p></div>
<figure class="foto-vyska">{img(P+'lifestylovy-portret-zeny-v-prirode.jpg')}<figcaption>Kárované šaty vyniknou i na černobílé fotce.</figcaption></figure>
<div class="uzky b-clanek"><h2>4. nech své oblečení rozevlát</h2><p>Co se nejvíc hodí pro uvolněné fotky? Uvolněné oblečení, ve kterém se budeš cítit dobře. Super jsou volné šaty, které doplníš třeba páskem. Pro pány lehká košile přehozená přes tričko. Pohodlné oblečení je mnohem lepší než se mačkat v něčem upnutém, co tě všude stahuje. A navíc krásně zachytí pohyb.</p>
<h2>5. neboj se doplňků ani „nevšedního“ outfitu</h2><p>Focení je skvělá příležitost obléct se podle svých představ a pořádně se vystrojit. Vezmi si to, v čem se cítíš dobře a přirozeně. Nezapomeň ani na doplňky, pokud je běžně nosíš: šálu, klobouk, sluneční brýle, čepici nebo zajímavé sponky do vlasů. Naopak se vyhni výrazným sportovním hodinkám a gumičkám zapomenutým na ruce (můj věčný problém vždy a všude).</p></div>
<div class="b-dvojice"><figure>{img(R+'brandove-foceni-pohyb-saty.jpg')}<figcaption>Volné šaty v pohybu.</figcaption></figure><figure>{img(R+'brandovy-portret-s-kloboukem.jpg')}<figcaption>Klobouk dodá fotce charakter.</figcaption></figure></div>
<div class="uzky b-clanek"><h2>6. sladit, nebo nesladit?</h2><p>Nemyslím kafe, to rozhodně nesladit, žejo? Ale možná řešíš, jak vymyslet oblečení, když se fotíte ve víc lidech. Rozhodně nemusíte mít stejně barevná trička a vypadat jak přes kopírák. Sladila bych se ale aspoň do jednoho stylu, aby nepřišla slečna v elegantních šatech a její partner ve sportovním. Buď jedno, nebo druhé.</p><p>Stejně tak u barev: zkuste se držet aspoň zemité palety. Černou, bílou, šedou, béžovou, tlumenou zelenou nebo hnědou doma určitě najdete. Dětem se neboj dopřát i výraznější barvy, jen ne křiklavé.</p></div>
<figure class="foto-sirsi">{img(P+'prirozene-rodinne-foceni-v-pohybu.jpg')}<figcaption>Sladění do jednoho stylu, ne do stejnokroje.</figcaption></figure>
<div class="uzky b-clanek"><h2>7. vezmi si na focení svou srdcovku</h2><p>Máš oblečení nebo doplněk, který vystihuje tvou osobnost a je pro tebe fakt důležitý? Tak ho nezapomeň doma. Mám ráda, když se do fotek dostanou i věci, na kterých ti opravdu záleží. Míša si třeba vzala košili s kočkama, kterou miluje a všichni si ji s ní spojují. Kačí zase přinesla šátek z cest po Indii. Pojďme do fotky vložit kousek tvého příběhu.</p></div>
<div class="b-dvojice"><figure>{img('misa-lokalni.jpg')}<figcaption>Míša a její košile s kočkama.</figcaption></figure><figure>{img('kaci-lokalni.jpg')}<figcaption>Kačí a šátek z Indie.</figcaption></figure></div>
<section class="zelena"><div class="uzky"><span class="kategorie" style="color:#cfc8bb">bonusový tip</span><h2>8. vyber si fotografa, který ti s tím pomůže</h2>
<p>Dobrý fotograf tě s oblečením nenechá v tom samotné a pomůže ti ho vybrat. U mě to funguje takhle: před focením ti pošlu základní pravidla, tedy v podstatě tenhle článek.</p><p>Když si pořád nevíš rady, třeba u rodinného focení, připravím vám moodboard s inspirací. Z každé fotky si vezmete něco málo a zkombinujete to s tím, co máte doma, takže nemusíte nic kupovat. Nebo mi oblečení doma vyfotíš a kombinaci vymyslíme spolu.</p><p>U párového nebo portrétního focení často vymýšlíme i celý koncept. Fotky můžeme lehce naladit do retro stylu, do kovbojského stylu nebo do čehokoli, co je ti blízké. Vyber si proto fotografa, který ví, co dělá, a se vším ti pomůže.</p></div></section>
<div class="uzky b-clanek"><h2>na závěr</h2><p>Tohle bylo mých 7 tipů a jeden bonusový, kterých se můžeš držet. Chtěla bych ale zdůraznit, že není až tak důležité, kde fotíme a jak vypadáš, ale hlavně jak se cítíš. Soustřeď se hlavně na to, ať tě focení baví. Jak budou fotky vypadat, nech na mně.</p><p>Když si s výběrem nebudeš vědět rady, napiš mi. Moc ráda ti s oblečením pomůžu. A jestli chceš vidět, jak to vypadá v praxi, sleduj mě na Instagramu <a href="https://www.instagram.com/sofiezbo/" style="color:#222">@sofiezbo</a>.</p>
<p class="sdilet"><button type="button" onclick="navigator.share?navigator.share({{url:location.href}}):navigator.clipboard.writeText(location.href)">sdílet článek</button></p></div>'''
B+=konec('mohlo by tě zajímat','Další rady, které se ti před focením hodí, a jedna svatba pro inspiraci.',['ra2','ra3','sv1'],'napiš mi','<a href="../portrety.html">portfolio</a><a href="../cenik.html">ceník</a>')
page('rady.html','Co si vzít na sebe na focení – návrh',B,'pres-vlnu')

# přehled blogu
C=[('sv3','Když mi Klára poprvé psala, měla jasno jen v jedné věci: nechtěla den, který by se odehrával podle harmonogramu.','6 min'),
(('misa-lokalni.jpg','rady před focením','co si vzít na sebe na focení: 7 tipů, aby ti to slušelo'),'Oblečení hraje na fotkách obrovskou roli. Proto jsem sepsala pár rad a základních pravidel, kterých je fajn se při výběru outfitu držet.','5 min'),
((R+'produktove-foceni-betonove-vazy-v-ruce.jpg','ze zákulisí','betonové vázy v obýváku místo ateliéru'),'Studio jsme neměli, jen obývák, jedno okno a pár bílých papírů. Ukážu ti, jak jsem nad focením přemýšlela.','4 min'),
('ra2','Rodinné focení by nemělo být o stresu, ale o pohodě. Nemusíte mít všechno dokonalé a děti nemusí stát na místě.','3 min'),
('ra3','Často mi lidé při domlouvání focení píšou, že kolem sebe nemají žádné hezké místo. Všude je jen pole, silnice nebo dětské hřiště.','2 min'),
((P+'prirozene-rodinne-foceni-v-pohybu.jpg','rady před focením','rodinné focení jako vzpomínka: proč má smysl ho dělat pravidelně'),'„Čas letí.“ Všichni to říkáme, všichni to víme, ale naplno si to uvědomíme většinou až při pohledu na staré fotky.','2 min')]
def prehled_karta(k,txt,cas):
    p,c,t=K[k] if isinstance(k,str) else k
    return f'<a class="p-karta" href="#">{img(p)}<span class="kategorie">{c} · {cas} čtení</span><h3>{t}</h3><p>{txt}</p><span class="cist">číst dál</span></a>'
O=f'''<section class="p-hero">
<div class="p-kolaz vlevo">{img(S+'nevesta-pripravy-zrcadlo-venecek-svatojakubsky-pivovar-hluboke.jpg','k1 ramecek')}{img(P+'parove-foceni-v-rozkvetlem-sadu.jpg','k2')}{img(P+'maminka-s-miminkem-u-okna.jpg','k3 stin')}</div>
<div class="p-titul"><h1>blog</h1><p>Příběhy ze svateb, rady před focením a pohled do zákulisí. Píšu o tom, jak fotím, co mě baví a co se vám může hodit.</p>
<div class="filtr"><button class="aktivni">vše</button><button>svatby</button><button>rady před focením</button><button>ze zákulisí</button></div></div>
<div class="p-kolaz vpravo">{img(R+'detail-betonove-vazy-s-eukalyptem.jpg','k4')}{img(S+'polibek-novomanzelu-po-obradu-cernobila-dohnaluv-mlyn.jpg','k5 ramecek stin')}{img(P+'cernobile-parove-foceni-v-sadu.jpg','k6')}</div></section>
<section class="p-mriz">{''.join(prehled_karta(*c) for c in C)}</section>
<section class="konec"><div class="medailon">{img(F+'sofie-zborilova-fotografka-portret.webp')}<div><h3>ahoj, jsem sofi</h3><p>Fotím svatby, rodiny a značky v Brně a Bratislavě. Mám ráda přirozené momenty, jemné barvy a lidi, kteří se nebojí být sami sebou.</p><a class="tlacitko" href="#">napiš mi</a><span class="odkazy"><a href="../svatby.html">portfolio</a><a href="../cenik.html">ceník</a></span></div></div></section>'''
page('blog.html','Blog – návrh',O)
