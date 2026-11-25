import os
os.chdir('/home/user/site')
src=open('podminky.html',encoding='utf-8',newline='').read()
hdr=src[src.index('<button class="mobile-menu-btn"'):src.index('<main')]
hdr=hdr.replace('href="','href="../').replace("href=\"../#","href=\"#")
foot=src[src.index('<footer'):src.index('</footer>')+9]
head='''<!DOCTYPE html><html lang="cs"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{t}</title>
<link rel="stylesheet" href="../contact.css?v=9"><link rel="stylesheet" href="../paticka.css?v=1"><link rel="stylesheet" href="blog.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100..900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,700;1,400&family=Great+Vibes&display=swap" rel="stylesheet"></head><body class="{b}">'''
S='../fotky_svadby/';P='../fotky_portrety/';R='../fotky_produktove/';F='../fotky/'
H='svatojakubsky-pivovar-hluboke.jpg'
def img(p,c=''):return f'<img class="{c}" src="{p}" alt="">'
K={'sv1':(S+'novomanzele-v-objeti-parove-foceni-vachuv-mlyn-trebejice.jpg','svatby','letní svatba ve Váchově mlýně'),
'sv2':(S+'novomanzele-na-pude-svatebni-portret-dohnaluv-mlyn.jpg','svatby','svatba v Dohnalově mlýně'),
'ra1':(P+'rodinne-foceni-v-kvetouci-louce.jpg','rady před focením','co si vzít na sebe na rodinné focení'),
'ra2':(P+'predsvatebni-foceni-ve-vinohradu.jpg','rady před focením','jak se připravit na předsvatební focení'),
'za1':(R+'produktove-foceni-betonove-vazy-v-ruce.jpg','ze zákulisí','betonové vázy v obýváku místo ateliéru'),
'za2':(R+'perlove-nausnice-z-hliny-kvet-detail-na-kameni.jpg','ze zákulisí','šperky z hlíny na kameni z potoka')}
def karta(k):
    p,c,t=K[k];return f'<div class="karta">{img(p)}<span class="kategorie">{c}</span><h3>{t}</h3></div>'
def konec(nadpis,pod,karty,cta,odkazy):
    return f'''<section class="konec"><div class="medailon">{img(F+'sofie-zborilova-fotografka-portret.webp')}<div><h3>ahoj, jsem sofi</h3><p>Fotím svatby, rodiny a značky v Brně a Bratislavě. Mám ráda přirozené momenty, jemné barvy a lidi, kteří se nebojí být sami sebou.</p><a class="tlacitko" href="#">{cta}</a><span class="odkazy">{odkazy}</span></div></div>
<div class="dalsi"><h2>{nadpis}</h2><p class="podnadpis">{pod}</p><div class="karty">{''.join(karta(k) for k in karty)}</div></div></section>'''
def page(fn,t,body,b=''):
    open('nahled-blog/'+fn,'w',encoding='utf-8').write(head.format(t=t,b=b)+hdr+'<main class="blog">'+body+'</main>'+foot+'</body></html>')
SCALLOP='''<script>
document.querySelectorAll('.obsah').forEach(function(el){
 var w=el.offsetWidth,h=el.offsetHeight,r=10;
 function strana(d,n0,dx,dy){var n=Math.max(1,Math.round(d/(2*r))),s=d/n,o='';for(var i=0;i<n;i++){var j=(Math.random()-.5)*2;o+=' a'+(s/2+j)+' '+(s/2+j)+' 0 0 1 '+(dx*s)+' '+(dy*s);}return o;}
 var p='M0 0'+strana(w,0,1,0)+strana(h,0,0,1)+strana(w,0,-1,0)+strana(h,0,0,-1);
 el.insertAdjacentHTML('afterbegin','<svg viewBox="0 0 '+w+' '+h+'"><path d="'+p+'" fill="none" stroke="#5e554b" stroke-width="1.3" stroke-linecap="round"/><path d="'+p+'" fill="none" stroke="#5e554b" stroke-width=".6" opacity=".5" transform="translate(1.2 .8)"/></svg>');
});
</script>'''
L='<a href="../svatby.html">jak to u mě probíhá</a><a href="../cenik.html">ceník</a>'
A=f'''<section class="hero-pod-vlnou a-hero">{img(S+'novomanzele-za-ruce-prochazka-v-prirode-'+H)}<div class="a-inicialy"><span>K</span><span class="a-spojka">a</span><span>M</span></div></section>
<p class="kategorie a-misto">svatby · Svatojakubský pivovar, Hluboké · červen 2026</p>
<div class="uzky a-pribeh"><h1 style="font-size:38px;margin-bottom:24px">Klára a Michal: svatba na dvoře starého pivovaru</h1>
<p class="prvni">Když mi Klára poprvé psala, měla jasno jen v jedné věci: nechtěla den, který by se odehrával podle harmonogramu. Chtěla, aby se lidi bavili, aby se jedlo u dlouhého stolu a aby se na konci tančilo bosky na dlažbě. Všechno ostatní se prý nějak vyřeší.</p>
<p>A taky se vyřešilo. Ráno v pokoji nad pivovarem vládl příjemný chaos. Družičky si půjčovaly sponky, maminka hledala nůžky na stuhu a Klára se smála tak, že ji kamarádka třikrát přemalovávala řasy. Kytice z lučních květin stála ve sklenici od okurek a nikomu to nevadilo.</p></div>
<section class="blok"><div class="mriz">{img(S+'nevesta-s-druzickami-pripravy-smich-'+H,'p-a1')}{img(S+'nevesta-vlasy-s-veneckem-zezadu-'+H,'p-a2 ramecek')}{img(S+'nevesta-s-druzickou-smich-cernobila-'+H,'p-a3 stin')}</div></section>
<div class="uzky text-mezi"><p>Michal čekal dole na dvoře a tvářil se, že vůbec není nervózní. Pak Klára vyšla ze dveří a bylo po statečnosti. Tenhle moment mám ráda nejvíc: ten krátký okamžik, kdy si dva lidi uvědomí, že je to opravdu dnes.</p></div>
<div class="dvojice">{img(S+'zenich-objima-nevestu-smich-'+H)}{img(S+'novomanzele-cela-k-sobe-cernobila-'+H)}</div>
<div class="uzky text-mezi"><p>Po obřadu se dvůr zaplnil lidmi. Klářin brácha, který se celé dopoledne tvářil drsně, se při gratulaci rozbrečel jako první. Kamarádky ji objímaly tak dlouho, že se fronta gratulantů táhla až k bráně.</p></div>
<div class="trojice">{img(S+'nevesta-s-bratrem-pusa-gratulace-'+H)}{img(S+'nevesta-pusa-od-kamaradky-gratulace-'+H,'ramecek')}{img(S+'svatebni-kytice-proti-nebi-'+H)}</div>
<div class="siroka">{img(S+'nevesta-s-kamaradkou-smich-'+H)}</div>
<p class="citat">„Nejvíc se mi líbilo, že jsme si Sofi celý den skoro nevšimli. A pak jsme brečeli nad každou fotkou.“<span>Klára a Michal</span></p>
<div class="uzky text-mezi"><p>Večer se nad dvorem rozsvítila světýlka a nikdo už se neposadil. Tancovalo se do tří do rána a já jsem odjížděla s pocitem, že jsem byla na svatbě kamarádů.</p></div>
<section class="blok"><div class="mriz">{img(S+'nevesta-tanci-na-svatebni-party-'+H,'p-a1')}{img(S+'nevesta-tanci-na-dvore-'+H,'p-a2 ramecek')}{img(S+'nevesta-s-kamaradkou-selfie-smich-cernobila-'+H,'p-a3 stin')}</div></section>
<div class="siroka">{img(S+'nevesta-s-kamaradkami-radost-cernobila-'+H)}</div>'''
A+=konec('chceš vidět víc?','Podívej se, jak vypadaly další svatby, které jsem fotila, nebo si přečti, jak se na focení připravit.',['sv1','sv2','ra2'],'zjistit volný termín',L)
page('svatba.html','Svatební příběh – návrh 2',A,'pres-vlnu')

B=f'''<section class="hero-pod-vlnou b-hero">{img(P+'hrave-rodinne-foceni-venku.jpg')}{img(P+'dokumentarni-rodinne-foceni-brno.jpg')}{img(P+'rodinne-foceni-v-prirode-brno-2.jpg')}
<div class="b-hero-text"><span class="kategorie">rady před focením</span><h1>co si vzít na sebe na rodinné focení</h1></div></section>
<div class="uzky b-clanek"><p class="b-perex">Oblečení umí fotky krásně podtrhnout, nebo z nich naopak udělat pestrobarevný chaos. Tady je, jak ho vybírám se svými rodinami, aby se vám v něm dobře hýbalo a fotky vypadaly nadčasově i za dvacet let.</p>
<div class="obsah-obal"><div class="obsah" style="clip-path:polygon(0.0% 0.4%,5.0% 0.2%,10.0% 0.6%,15.0% 0.2%,20.0% 0.1%,25.0% 0.6%,30.0% 1.5%,35.0% 1.3%,40.0% 1.2%,45.0% 0.4%,50.0% 0.9%,55.0% 0.4%,60.0% 0.3%,65.0% 0.2%,70.0% 0.3%,75.0% 1.5%,80.0% 1.3%,85.0% 1.3%,90.0% 1.3%,95.0% 0.3%,100.0% 0.5%,99.5% 10.0%,99.4% 20.0%,99.3% 30.0%,99.3% 40.0%,99.9% 50.0%,99.5% 60.0%,99.5% 70.0%,99.6% 80.0%,99.9% 90.0%,99.6% 100.0%,95.0% 99.8%,90.0% 98.3%,85.0% 98.4%,80.0% 99.0%,75.0% 99.5%,70.0% 98.4%,65.0% 99.0%,60.0% 98.4%,55.0% 98.5%,50.0% 99.1%,45.0% 99.3%,40.0% 98.9%,35.0% 99.2%,30.0% 99.7%,25.0% 99.5%,20.0% 98.5%,15.0% 99.9%,10.0% 99.9%,5.0% 98.9%,0.0% 99.5%,0.4% 90.0%,0.4% 80.0%,0.3% 70.0%,0.8% 60.0%,0.2% 50.0%,0.3% 40.0%,0.2% 30.0%,0.5% 20.0%,0.2% 10.0%)"><b>v článku najdeš</b><ol><li>barvy, které fungují</li><li>vzory a nápisy</li><li>sladit, ale nestejnokroj</li><li>děti a pohodlí</li><li>boty a doplňky</li><li>časté otázky</li></ol></div></div>
<h2>barvy, které fungují</h2><p>Nejlíp na fotkách vypadají tlumené, přírodní barvy: béžová, krémová, olivová, rezavá, prachově modrá. Ladí s přírodou i s interiérem a neodvádí pozornost od vašich tváří.</p><p>Čistě bílou a černou klidně použij, jen ať netvoří celou rodinu. Neonové barvy prosím vynech, odráží se na kůži a barví obličeje.</p>
<div class="tip"><b>tip</b>Vyber si jednu „hlavní“ barvu a k ní dvě tři doplňkové. Ostatní ať se jí jen drží v tónu.<div class="paleta"><span style="background:#e9dfcf"></span><span style="background:#c8b59a"></span><span style="background:#8b8f6e"></span><span style="background:#a7643f"></span><span style="background:#7d8b99"></span></div></div></div>
<figure class="foto-sirsi">{img(P+'rodinne-foceni-v-prirode-brno.jpg')}<figcaption>Tlumené barvy v létě na louce u Brna.</figcaption></figure>
<div class="uzky b-clanek"><h2>vzory a nápisy</h2><p>Drobný vzor je v pořádku, velká loga a nápisy ne. Na fotce přitáhnou oko dřív než úsměv.</p></div>
<figure class="foto-vyska">{img(P+'maminka-s-miminkem-u-okna.jpg')}<figcaption>Doma u okna: světlé a měkké materiály.</figcaption></figure>
<div class="uzky b-clanek"><h2>sladit, ale nestejnokroj</h2><p>Nemusíte mít všichni stejné tričko. Stačí, když si barvy povídají. Mamka v rezavých šatech, taťka v krémové košili a děti v olivové. Když si nebudeš jistá, <a href="#" style="color:#222">pošli mi fotky oblečení</a> a vybereme spolu.</p></div>
<div class="b-dvojice"><figure>{img(P+'rodinne-foceni-doma-na-gauci.jpg')}<figcaption>Doma: pohodlné oblečení v jemných tónech.</figcaption></figure><figure>{img(P+'prirozene-rodinne-foceni-v-pohybu.jpg')}<figcaption>Venku: barvy, které ladí s krajinou.</figcaption></figure></div>
<div class="uzky b-clanek"><h2>děti a pohodlí</h2><p>Děti musí v oblečení běhat, válet se v trávě a lézt tátovi na ramena. Když je něco škrábe, poznáš to na fotkách hned.</p></div>
<section class="zelena"><div class="uzky"><h2>časté otázky</h2>
<div class="otazka"><h3>Můžu si vzít víc outfitů?</h3><p>Jasně. U delšího focení se klidně převlečte, ideální jsou dva.</p></div><div class="otazka"><h3>Pomůžeš mi s výběrem?</h3><p>Ráda. Pošli mi fotky oblečení a vybereme spolu.</p></div><div class="otazka"><h3>Co když je zima?</h3><p>Vrstvy, svetry a kabáty jsou na fotkách krásné. Jen si vezmi něco teplého na přesuny.</p></div><div class="otazka"><h3>Musíme být všichni sladění?</h3><p>Nemusíte. Stačí, když se barvy nebijí. Klidně ať má každý trochu jiný odstín.</p></div><div class="otazka"><h3>Co obout dětem?</h3><p>Pohodlné boty, ve kterých zvládnou běhat. Na louce klidně i naboso.</p></div></div></section>'''
B+=konec('mohlo by tě zajímat','Další rady, které se ti před focením hodí, a jedna svatba pro inspiraci.',['ra2','ra1','sv1'],'napiš mi','<a href="../portrety.html">portfolio rodin</a><a href="../cenik.html">ceník</a>')
page('rady.html','Rady a tipy – návrh 2',B,'pres-vlnu')

C=f'''<section class="c-hero"><div><span class="kategorie">ze zákulisí · produktové focení</span><h1>betonové vázy v obýváku místo ateliéru</h1><p>Studio jsme neměli, jen obývák, jedno okno a pár bílých papírů. Ukážu ti, jak jsem nad focením přemýšlela, co jsem si postavila a proč fotky vypadají právě takhle.</p></div>
<div class="c-hero-fotky">{img(R+'minimalisticka-produktova-fotografie-vazy.jpg','velka ramecek')}{img(R+'produktove-foceni-aranzovani-vazy.jpg','mala')}</div></section>
<section class="c-krok"><div class="c-krok-text"><span class="kategorie">výchozí situace</span><h2>co jsem měla k dispozici</h2><p>Jedno okno na sever, stůl, dvě židle a látky z šuplíku. Klientka chtěla klidné, minimalistické fotky, které budou fungovat na e-shopu i na Instagramu.</p><p class="poznamka">Severní okno je pro produkty dar: dává měkké světlo bez ostrých stínů.</p></div>
<div class="pred-po"><figure>{img(R+'produktove-foceni-betonovych-vaz-na-stolku.jpg')}<figcaption>zákulisí</figcaption></figure><figure>{img(R+'detail-betonove-vazy-s-eukalyptem.jpg','ramecek')}<figcaption>výsledek</figcaption></figure></div></section>
<section class="c-krok obracene"><div class="c-krok-text"><span class="kategorie">světlo</span><h2>proč z boku a ne zepředu</h2><p>Beton má krásnou strukturu, ale jen když na něj světlo dopadá z boku. Zepředu by vázy vypadaly ploše jako z plastu.</p><p class="poznamka">Na druhou stranu jsem dala bílý papír, aby stíny nebyly úplně černé.</p></div>
<div class="pred-po"><figure>{img(R+'produktove-foceni-betonove-vazy-v-ruce-cernobila.jpg')}<figcaption>zákulisí</figcaption></figure><figure>{img(R+'produktove-foceni-betonove-vazy-v-ruce.jpg','ramecek')}<figcaption>výsledek</figcaption></figure></div></section>
<section class="zelena"><div class="uzky" style="max-width:1000px"><h2>s čím jsem pracovala</h2><div class="zadani"><div><b>zadání</b>Klidné fotky pro e-shop a Instagram, které ukážou strukturu betonu.</div><div><b>prostor</b>Obývák, severní okno, stůl a bílé papíry jako odrazné desky.</div><div><b>čas</b>Jedno odpoledne, 12 produktů a 40 hotových fotek.</div></div></div></section>
<section class="c-galerie">{img(R+'betonove-vazy-interier-lampa.jpg')}{img(R+'betonove-vazy-v-zrcadle-detail.jpg','ramecek')}{img(R+'produktove-foceni-vaz-s-pohybem.jpg')}{img(R+'produktove-foceni-keramickych-vaz-s-susenymi-kvetinami.jpg')}</section>'''
C+=konec('další ze zákulisí','Jak vznikaly další produktové fotky, a k tomu jeden příběh ze svatby.',['za2','za1','sv2'],'napiš mi','<a href="../produktove.html">produktové portfolio</a><a href="../cenik.html">ceník</a>')
page('zakulisi.html','Ze zákulisí – návrh 2',C)
