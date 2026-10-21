# -*- coding: utf-8 -*-
# the calm site: one ordinary scroll, the comic frames as pictures, quiet motion only
import re, json
NAV = open('/home/claude/site/frag_nav.html').read()
LOGO = re.search(r'<svg.*?</svg>', NAV, re.S).group(0).replace('#F0EEFF','#0A061B').replace('#7C3AED','#8526FD').replace('#8C87A3','#6A6480')
LOGO_CREAM = re.search(r'<svg.*?</svg>', NAV, re.S).group(0).replace('#F0EEFF','#F3EADA').replace('#7C3AED','#8526FD').replace('#8C87A3','#B9B0D6')
PHONE_INTL='972525649801'; PHONE_LOCAL='052-5649801'; WA=f'https://wa.me/{PHONE_INTL}'; MAIL='guy@zigzagmedia.co.il'
PLATFORMS=['מטא','גוגל','יוטיוב','טיקטוק','צ׳אט ג׳י־פי־טי','טאבולה','אאוטבריין']
PLATFORMS_LONG=['מטא (פייסבוק ואינסטגרם)','גוגל','יוטיוב','טיקטוק',"צ'אט ג'י־פי־טי",'טאבולה','אאוטבריין']

LD_ORG = {"@context":"https://schema.org","@type":"ProfessionalService","name":"Z.G Digital (זיגזג מדיה)","alternateName":"ז.ג דיגיטל בע\"מ",
 "url":"https://zigzagmedia.co.il","email":MAIL,"telephone":"+"+PHONE_INTL,"areaServed":"IL",
 "address":{"@type":"PostalAddress","addressLocality":"תל אביב","addressCountry":"IL"},
 "founder":{"@type":"Person","name":"גיא שושני"},
 "knowsAbout":["Performance marketing","Meta Ads","Google Ads","YouTube Ads","TikTok Ads","ChatGPT Ads","Taboola","Outbrain","Creative team management","Generative AI","Business automation","Landing pages"],
 "makesOffer":[
  {"@type":"Offer","itemOffered":{"@type":"Service","name":"פרפורמנס בכל הפלטפורמות","description":"ניהול תקציבי פרסום בכל הגדלים ולכל המטרות: לידים, מכירות וניהול מוניטין. "+", ".join(PLATFORMS_LONG)}},
  {"@type":"Offer","itemOffered":{"@type":"Service","name":"ניהול והפעלת צוותי קריאייטיב","description":"הכוונה ועבודה בפועל מול צוות יצירת התוכן של הלקוח, מהבריף ועד המודעה שעולה לאוויר"}},
  {"@type":"Offer","itemOffered":{"@type":"Service","name":"פתרונות בינה מלאכותית","description":"דפי נחיתה ואתרים, אוטומציות עסקיות ותוכן גנרטיבי"}}]}

html = r'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Z.G Digital · זיגזג מדיה · גיבורי־על דיגיטליים</title>
<meta name="description" content="סוכנות פרסום ובינה מלאכותית מתל אביב: פרפורמנס בכל הפלטפורמות, ניהול והפעלת צוותי קריאייטיב ופתרונות בינה מלאכותית. כמעט 15 שנה של תקציבים גדולים ותוצאות גדולות.">
<meta property="og:title" content="Z.G Digital · גיבורי־על דיגיטליים">
<meta property="og:description" content="פרפורמנס בכל הפלטפורמות, צוותי קריאייטיב ופתרונות בינה מלאכותית. תל אביב.">
<meta property="og:image" content="https://zigzagmedia.co.il/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:type" content="website"><meta property="og:locale" content="he_IL"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://zigzagmedia.co.il/">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="theme-color" content="#F3EADA">
<link rel="alternate" type="text/plain" href="llms.txt" title="LLM summary">
<link rel="alternate" type="text/html" href="agents.html" title="מידע מסודר לסוכני AI">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap">
<style>
:root{__VARS__--ink:#0A061B;--moon:#8526FD;--moonD:#5B14C4;--font:'Heebo',system-ui,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--bg)}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--fg);font:400 17px/1.6 var(--font);direction:rtl;overflow-x:hidden}
img{display:block;max-width:100%}
picture{display:contents}
a{color:inherit}
.wrap{width:min(1180px,calc(100% - 40px));margin:0 auto}
/* nav */
.nav{position:fixed;top:0;right:0;left:0;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:64px;padding:calc(6px + env(safe-area-inset-top,0px)) 20px 6px;background:var(--navbg);box-shadow:0 1px 0 rgba(10,6,27,.1);transition:transform .3s cubic-bezier(.23,1,.32,1)}
.nav.away{transform:translateY(-100%)}
@media (prefers-reduced-motion:reduce){.nav{transition:none}}
.skip{position:absolute;top:8px;right:8px;z-index:60;background:var(--fg);color:var(--bg);padding:10px 14px;font-weight:700;text-decoration:none;transform:translateY(-200%)}.skip:focus{transform:none}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--moon);outline-offset:3px}
section,header,footer{scroll-margin-top:80px}
.nav .logo{display:flex;align-items:center;height:44px;min-height:0;padding:0}.nav .logo svg{height:36px;width:auto;display:block}
.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:4px;align-items:center;min-width:0}
.nav a{text-decoration:none;font-weight:500;font-size:15px;display:inline-flex;align-items:center;min-height:44px;padding:0 10px;white-space:nowrap}
.nav a.btn{background:var(--moon);color:#fff;font-weight:700;padding:0 16px;min-height:44px;margin-inline-start:6px}
@media (max-width:640px){.nav{padding-left:12px;padding-right:12px}.nav ul{gap:0}.nav a{font-size:14px;padding:0 8px}.nav .logo svg{height:28px}.nav a.btn{padding:0 11px;margin-inline-start:2px}}
@media (max-width:379px){.nav a{font-size:13px;padding:0 6px}.nav .logo svg{height:24px}.nav a.btn{padding:0 9px}.nav li.hide-xs,.nav li.hide-xs2{display:none}}
/* type */
.eyebrow{display:inline-block;font-size:13px;letter-spacing:.05em;font-weight:700;color:var(--bg);background:var(--fg);padding:6px 12px;margin:0 0 14px;position:relative;z-index:2}
h1,h2{margin:0 0 16px;font-weight:900;line-height:1.02;letter-spacing:-.01em;text-wrap:balance}
h1{font-size:clamp(44px,8.5vw,88px)}
h2{font-size:clamp(34px,5.4vw,64px)}
h3{margin:0 0 6px;font-weight:900;font-size:21px;line-height:1.2}
.k{color:var(--moon)}
.svc .nw{white-space:nowrap;display:inline-block}
.svc{font-weight:700;font-size:clamp(17px,1.5vw,21px);color:var(--dim);margin:-4px 0 14px}
h2.long{font-size:clamp(26px,3.2vw,42px);line-height:1.12;max-width:24ch}
.lead{font-size:clamp(17px,1.5vw,20px);line-height:1.6;max-width:34ch;margin:0 0 20px}
p{margin:0 0 12px}
.small{font-size:14px;color:var(--dim)}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 24px;background:var(--moon);color:#fff;text-decoration:none;font-weight:700;font-size:17px;transition:transform .18s cubic-bezier(.23,1,.32,1),box-shadow .18s}
@media (hover:hover){.btn:hover{transform:translateY(-1px);box-shadow:0 10px 24px -12px var(--moon)}}
.btn:active{transform:scale(.97)}
.link{display:inline-flex;align-items:center;min-height:50px;padding:0 10px;text-decoration:none;font-weight:700;color:var(--fg)}
.ctas{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
/* frames */
.frame{position:relative;margin:0;background:var(--bg2);border:5px solid var(--line);box-shadow:12px 12px 0 var(--moon);overflow:hidden}
.frame img{width:100%;height:100%;object-fit:cover}
.frame .pic{position:absolute;inset:-6%;width:112%;height:112%}
.frame .pic img{width:100%;height:100%;object-fit:cover}
.frame .ov{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
/* sections */
.sec{padding:72px 0}
@media (max-width:899px){.sec{padding:52px 0}}
.grid{display:grid;gap:48px;align-items:center}
@media (min-width:900px){.grid{grid-template-columns:1fr 1fr}.grid.rev>.copy{order:2}}
.copy{max-width:52ch}
/* hero */
.hero{position:relative;min-height:92svh;display:flex;align-items:center;padding:100px 0 40px;overflow:hidden}
.hero canvas.full{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}
.art-wrap{position:relative;justify-self:center;width:min(100%,calc(72svh*970/1300))}
.art-wrap canvas.ink{position:absolute;inset:-22% -30%;width:160%;height:144%;display:block;pointer-events:none;z-index:0}
.art-wrap .frame{position:relative;z-index:1;width:100%}
.hero .copy,.hero .ctas{position:relative;z-index:2}
.hero .wrap{position:relative;z-index:1}
.hero-grid{display:grid;gap:28px 40px;align-items:center;grid-template-areas:"copy" "art" "ctas"}
.hero-grid>.copy{grid-area:copy}.hero-grid>.art-wrap{grid-area:art}.hero-grid>.ctas{grid-area:ctas}
@media (min-width:900px){.hero{min-height:0;padding:100px 0 24px}.hero-grid{grid-template-columns:.95fr 1.05fr;grid-template-areas:"art copy" "art ctas";row-gap:0}.hero-grid>.copy{align-self:end}.hero-grid>.ctas{align-self:start;margin-top:4px}}
.hero-art{aspect-ratio:970/1300;max-height:72svh}
.hero-art .pic{inset:0;width:100%;height:100%}
@media (max-width:899px){.hero{padding:84px 0 8px;min-height:0}.about{padding-top:28px}.art-wrap{width:100%}.hero-art{max-height:none;width:100%;aspect-ratio:1/1}.hero-art .pic img{object-position:50% 35%}}
/* about: the roof frame with the silhouette standing beside it on the paper */
.about .frame.roof{aspect-ratio:1047/1300;width:min(100%,520px);justify-self:center}
.about .man{position:absolute;left:50%;bottom:3.5%;height:44%;transform:translateX(-50%);z-index:2;transform-origin:50% 100%}
.about .man img{height:100%;width:auto;display:block}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.facts div{border-inline-start:4px solid var(--moon);padding:2px 14px 2px 0}
@media (max-width:599px){.facts{grid-template-columns:1fr;gap:12px}.facts div{display:flex;align-items:baseline;gap:10px}.facts b{min-width:6.5ch}}
.facts b{display:block;font-size:clamp(19px,2vw,26px);font-weight:900;line-height:1.1;white-space:nowrap}
.facts span{font-size:15px;color:var(--dim);line-height:1.4}
/* clients: real logos, quiet in grey, their own colour on hover; every logo links to the client */
.clients{padding-top:40px}
.clients h2{font-size:clamp(28px,3.6vw,46px);margin-bottom:28px}
.logos{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:26px 44px}
.logos li{display:flex;align-items:center;justify-content:center;height:72px}
.logos a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:6px 4px}
.logos img{display:block;width:auto;max-width:168px;filter:grayscale(1);opacity:.78;transition:filter .25s,opacity .25s}
.logos .h1 img{height:30px}.logos .h2 img{height:46px}.logos .h3 img{height:58px}
@media (hover:hover){.logos a:hover img{filter:none;opacity:1}}
.logos a:focus-visible img{filter:none;opacity:1}
.logos .lt img{opacity:1;filter:grayscale(1) contrast(1.6)}
@media (max-width:899px){.clients{padding-top:28px}.logos{gap:18px 26px}.logos li{height:56px}.logos img{max-width:130px}.logos .h1 img{height:22px}.logos .h2 img{height:36px}.logos .h3 img{height:46px}}
/* services */
/* the three services: three ordinary sections on a wide screen, one horizontal slider on the phone */
.only-m{display:none}
@media (min-width:900px){.only-m{display:none !important}}
.services .frame{width:100%}
.svc-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;margin-bottom:18px}
@media (min-width:900px){.svc-head{margin-bottom:0}}
.svc-head .eyebrow{margin:0}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tabs button{appearance:none;border:2px solid var(--line);background:transparent;color:var(--fg);font:700 14px var(--font);padding:0 12px;min-height:44px;cursor:pointer;transition:background .2s,color .2s}
.tabs button.on{background:var(--fg);color:var(--bg)}
.arrows{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:18px}
.arr{appearance:none;border:2px solid var(--line);background:transparent;color:var(--fg);width:46px;height:46px;font:900 22px var(--font);cursor:pointer;display:inline-flex;align-items:center;justify-content:center}
.count{font-weight:700;font-size:15px;min-width:7ch;text-align:center;font-variant-numeric:tabular-nums}
.go{font-weight:700;display:inline-block;padding:10px 0;margin:-10px 0}
@media (min-width:900px){
  .services{padding:24px 0 0}
  .slide{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:36px 0}
  .slide.rev>.copy{order:2}
  .slide>.copy{justify-self:center}
  .services .frame{aspect-ratio:1300/872;justify-self:center;align-self:center;width:min(100%,560px)}
  .services .frame.tall{aspect-ratio:970/1300;max-height:76svh;width:min(100%,calc(76svh*970/1300))}
  .services .frame.sq{aspect-ratio:1/1;width:min(100%,72svh)}
  .pstack{justify-self:center;width:min(100%,560px)}
}
@media (max-width:899px){
  .only-m{display:flex}.only-d{display:none}
  .slide p.morph{font-size:clamp(28px,7.6vw,34px);text-align:right}
  .slide p.morph+h2.svc{text-align:right}
  .services{padding:40px 0 44px}
  .track{display:flex;align-items:flex-start;gap:20px;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}
  .track::-webkit-scrollbar{display:none}
  .slide{flex:0 0 90%;scroll-snap-align:start;transition:opacity .3s;display:grid;gap:14px;min-width:0;align-content:start}
  .slide .copy{order:2}
  .track .slide:not(.on){opacity:.45}
  .track .slide:not(.on) .copy{opacity:0;transition:opacity .3s}
  .track .slide .copy{transition:opacity .3s}
  .services .frame{aspect-ratio:16/10}
  .slide h2{font-size:clamp(28px,7.6vw,34px);margin-bottom:6px}
  .slide .svc{margin:-2px 0 10px;font-size:16px}
  .slide .lead{font-size:16px;margin-bottom:12px}
  .pstack{gap:8px}
  .goals,.cards{gap:8px;margin:8px 0 0}
  .goal,.card{padding:10px 12px}
  .goal b,.card h3{font-size:17px}
  .goal p,.card p{font-size:14px;line-height:1.45}
}
.goals{display:grid;gap:12px;margin:22px 0 10px}
.goal{background:var(--bg2);border:3px solid var(--line);padding:14px 18px;display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;position:relative}
.goal::before{content:'';position:absolute;top:0;right:0;width:46px;height:5px;background:var(--moon)}
.goal b{display:block;font-size:20px;font-weight:900}
.goal p{margin:0;font-size:16px;line-height:1.55}
@media (max-width:480px){.goal{grid-template-columns:1fr;gap:4px}}
.pstack{display:grid;gap:14px;align-self:center}
.ticker{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.ticker>div{display:flex;gap:0;width:max-content;animation:tick 28s linear infinite}.ticker .set{display:flex}
.ticker:hover>div,.ticker:focus-within>div,.ticker.paused>div,html.still .ticker>div{animation-play-state:paused}
.still-btn{min-height:44px;padding:0 12px;border:2px solid var(--line);background:transparent;color:var(--fg);font:700 13px var(--font);display:inline-flex;align-items:center;gap:8px;cursor:pointer;margin-inline-start:auto}
.svc-head .eyebrow{margin-bottom:0}
@media (prefers-reduced-motion:reduce),(max-width:899px){.still-btn{display:none}}
.ticker span{font-weight:900;font-size:clamp(20px,2.2vw,30px);white-space:nowrap;padding:0 18px}
.ticker span::after{content:'·';color:var(--moon);margin-inline-start:36px}
@keyframes tick{from{transform:translateX(0)}to{transform:translateX(50%)}}
@media (prefers-reduced-motion:reduce){.ticker>div{animation:none}}
.morph span{position:absolute;right:0;left:0;top:0;display:block;white-space:nowrap}
p.morph{position:relative;height:1.06em;filter:blur(0.5px) url(#threshold);text-align:center;margin:0 0 4px 0;font-weight:900;line-height:1.02;letter-spacing:-.01em;font-size:clamp(34px,5.4vw,64px)}
p.morph+h2.svc{text-align:center;margin:0 0 10px;font-weight:700;font-size:clamp(17px,1.5vw,21px);line-height:1.3;color:var(--dim);letter-spacing:0}
.creative .frame{aspect-ratio:970/1300;max-height:84svh;width:min(100%,calc(84svh*970/1300));justify-self:center}
.ai .frame{aspect-ratio:1/1}
.cards{display:grid;gap:12px;margin-top:24px}
.card{background:var(--bg2);border:3px solid var(--line);padding:16px 18px;position:relative;display:grid;grid-template-columns:150px 1fr;gap:14px;align-items:center}
.card::before{content:'';position:absolute;top:0;right:0;width:46px;height:5px;background:var(--moon)}
.card h3{margin:0;font-size:19px}
.card p{margin:0;font-size:16px;line-height:1.55}
@media (max-width:480px){.card{grid-template-columns:1fr;gap:4px}}
/* contact */
.contact .grid{grid-template-columns:1fr;justify-items:center}
.contact .copy{width:100%;max-width:620px}
.contact .form{max-width:none}
.price{margin:0 0 28px;padding:16px 18px;border-inline-start:4px solid var(--moon);background:var(--bg2)}
.price p{margin:0;font-size:16px;line-height:1.6}
.price .eyebrow{margin-bottom:8px}
.price b{font-weight:900}
.form{display:grid;gap:10px;background:var(--bg2);border:4px solid var(--line);padding:16px;box-shadow:10px 10px 0 var(--moon);max-width:520px}
.form .fields{display:grid;gap:14px}
.form{position:relative}
.form .hp{position:absolute;inset-inline-start:0;top:0;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);opacity:0;pointer-events:none}
.form .field{display:grid;gap:5px}
.form label{font-weight:700;font-size:15px}
.form .req{font-weight:400;color:var(--dim);font-size:14px}
.form .hint{margin:0;font-size:13px;color:var(--dim);line-height:1.4}
.form .err{display:none;margin:0;font-size:14px;font-weight:700;color:var(--err)}
.form .field.bad .err{display:block}.form .field.bad input{border-color:var(--err)}
.form input{width:100%;text-align:start;background:var(--inputbg);border:2px solid var(--line);border-radius:0;color:var(--fg);font:400 16px var(--font);padding:11px 12px;min-height:48px}
.form input::placeholder{color:#8A849C}
.form input:focus{border-color:var(--moon);outline:none;box-shadow:0 0 0 3px rgba(133,38,253,.25)}
.form button{min-height:50px;border:0;background:var(--moon);color:#fff;font:900 18px var(--font);cursor:pointer}
.form .wa{display:flex;align-items:center;justify-content:center;gap:6px;min-height:48px;border:2px solid var(--line);text-decoration:none;font-weight:700;font-size:15px}
.form .alt{margin:4px 0 0;font-size:14px;color:var(--dim)}
.form .ok{padding:8px 4px;font-size:18px}.form .ok:focus{outline:none}.form .ok b{display:block;font-size:24px;font-weight:900;margin-bottom:6px}.form .ok p{margin:0;font-size:16px;line-height:1.6}.form .ok a{color:var(--moon);font-weight:700}
.form.sent .fields{display:none}.form.sent .ok{display:block}.form .ok[hidden]{display:none}
footer{position:relative;overflow:hidden;color:#F3EADA;background:#0A061B;padding:72px 0 calc(28px + env(safe-area-inset-bottom,0px));font-size:15px}
footer::before{content:'';position:absolute;left:-140px;bottom:-220px;width:480px;height:480px;border-radius:50%;background:var(--moon);pointer-events:none}
footer .wrap{position:relative;z-index:1}
footer .top{display:grid;gap:28px 48px;align-items:start;margin-bottom:44px}
@media (min-width:900px){footer .top{grid-template-columns:1.2fr 1fr 1fr 1fr}}
footer .brand .logo{height:30px;margin-bottom:18px}footer .brand .logo svg{height:100%;width:auto;display:block}
footer .motto{font-weight:900;font-size:clamp(22px,2.4vw,30px);line-height:1.15;margin:0;max-width:22ch;letter-spacing:-.01em}
footer h3{margin:0 0 10px;font-size:13px;font-weight:700;letter-spacing:.08em;color:#B9B0D6}
footer ul{list-style:none;margin:0;padding:0;display:grid;gap:2px}
footer a{color:#F3EADA;text-decoration:none;display:inline-flex;align-items:center;min-height:44px;font-weight:500}
@media (hover:hover){footer a:hover{color:#C9A9FF}}
footer .wa{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 18px;border:2px solid #F3EADA;font-weight:700;margin-top:6px}
footer .bottom{display:flex;flex-wrap:wrap;gap:6px 28px;align-items:center;justify-content:flex-start;border-top:1px solid rgba(243,234,218,.18);padding-top:18px;font-size:13px;color:#B9B0D6}
footer .bottom a{min-height:44px;color:#B9B0D6;font-weight:400}
@media (max-width:899px){footer{padding-top:52px;font-size:15px}footer::before{width:260px;height:260px;left:-100px;bottom:-130px}footer .top{grid-template-columns:1fr 1fr;gap:22px 18px;margin-bottom:26px}footer .brand,footer .contact{grid-column:1/-1}footer .brand .logo{height:26px;margin-bottom:12px}footer .motto{font-size:22px;max-width:none}footer h3{margin-bottom:4px}footer a{min-height:44px}footer .contact ul{display:flex;flex-wrap:wrap;gap:2px 20px}footer .contact .wa{width:100%;justify-content:center;margin-top:12px}footer .bottom{flex-direction:column;align-items:flex-start;gap:0}}
.form .alt a{display:inline-flex;align-items:center;min-height:44px;color:var(--moon);font-weight:700}
/* reveal */
html.gsap .rv{opacity:0;transform:translateY(22px)}
@media (prefers-reduced-motion:reduce){html.gsap .rv{opacity:1;transform:none}}
</style>
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','386396115213106');fbq('track','PageView');
</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=386396115213106&ev=PageView&noscript=1" alt=""></noscript>
<!-- GA4: יתווסף כשיהיה מזהה -->
</head>
<body>
<svg style="position:absolute;width:0;height:0" aria-hidden="true"><defs><filter id="threshold"><feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 255 -140"/></filter></defs></svg>
<a class="skip" href="#main">דלג לתוכן</a>
<nav class="nav" aria-label="ראשי">
  <a class="logo" href="#top" aria-label="דף הבית, Z.G Digital">__LOGO__</a>
  <ul>
    <li><a href="#perf">שירותים</a></li>
    <li class="hide-xs"><a href="#about">עלינו</a></li>
    <li class="hide-xs2"><a href="knowledge.html">ידע</a></li>
    <li><a class="btn" href="#contact">דברו איתנו</a></li>
  </ul>
</nav>

<header class="hero" id="top">
  __CANVAS_HERO__
  <div class="wrap hero-grid">
    <div class="copy">
      <p class="eyebrow">סוכנות פרסום בוטיק. תל אביב</p>
      <h1>גיבורי־על<br><span class="k">דיגיטליים.</span></h1>
      <p class="lead">סוכנות פרסום ממומן לעסקים עם תקציב ויעד ברור: לידים, מכירות באיקומרס או מוניטין. כמעט 15 שנה, מאות לקוחות, כל הפלטפורמות, ומדידה שאומרת את האמת.</p>
    </div>
    <div class="art-wrap">__CANVAS_ART__<figure class="frame hero-art"><div class="pic" data-par="6"><picture><source type="image/webp" srcset="art/w/azrieli-480.webp 480w, art/w/azrieli-800.webp 800w, art/w/azrieli-970.webp 970w" sizes="(max-width:899px) calc(100vw - 40px), min(45vw, 520px)"><img src="art/azrieli.jpg" alt="איור דיו של מגדלי עזריאלי וירח סגול" fetchpriority="high" width="970" height="1300"></picture></div></figure></div>
    <div class="ctas"><a class="btn" href="#contact">דברו איתנו</a><a class="link" href="#perf">מה אנחנו עושים ↓</a></div>
  </div>
</header>

<main id="main">
<section class="sec about" id="about">
  <div class="wrap grid">
    <div class="copy">
      <p class="eyebrow rv">מי אנחנו</p>
      <h2 class="rv long">מהבסטות בשוק מחנה יהודה בירושלים לגורדי השחקים של <span class="k" style="white-space:nowrap">תל אביב.</span></h2>
      <p class="lead rv">ז.ג דיגיטל (שהתחילה כ"זיגזג מדיה") נולדה בירושלים עוד לפני שידעו מה זה לעשות לייק, כשכל הפרסום הדיגיטלי התרכז סביב גוגל. מאז ניהלנו מאות לקוחות, מכל התחומים ובכל סוגי התקציבים, בארץ ובעולם.</p>
      <p class="rv">מה שלא השתנה: אנחנו מודדים הכול, אומרים את האמת על המספרים, ומתייחסים לכל שקל בתקציב כאילו הוא שלנו.</p>
      <div class="facts rv">
        <div><b>15 שנה</b><span>ניסיון שלא הולך ברגל</span></div>
        <div><b>כל תקציב</b><span>מנהלים תקציבים קטנים וגדולים</span></div>
        <div><b>תל אביב</b><span>מספקים שירותים בכל העולם</span></div>
      </div>
    </div>
    <figure class="frame roof rv"><div class="pic" data-par="4"><picture><source type="image/webp" srcset="art/w/roof-480.webp 480w, art/w/roof-800.webp 800w, art/w/roof-1047.webp 1047w" sizes="(max-width:899px) calc(100vw - 40px), 520px"><img src="art/roof.jpg" alt="איור דיו של גג תל אביבי עם דודי שמש וירח סגול" loading="lazy" width="1047" height="1300"></picture></div></figure>
  </div>
</section>

<section class="sec clients" id="clients">
  <div class="wrap">
    <p class="eyebrow rv">לקוחות</p>
    <h2 class="rv">עבדנו עם הגדולים. וגם עם הקטנים.</h2>
    <ul class="logos rv" aria-label="לקוחות שעבדנו איתם">
      <li class="h3"><a href="https://telaviv.intercontinental.com/" target="_blank" rel="noopener" title="InterContinental David Tel Aviv"><img src="art/clients/intercontinental.svg" alt="InterContinental David Tel Aviv" loading="lazy"></a></li>
      <li class="h2"><a href="https://clover.security/" target="_blank" rel="noopener" title="Clover Security"><img src="art/clients/clover.svg" alt="Clover Security" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.yes.co.il/" target="_blank" rel="noopener" title="yes"><img src="art/clients/yes.svg" alt="yes" loading="lazy"></a></li>
      <li class="h2"><a href="https://soglowek.co.il/" target="_blank" rel="noopener" title="זוגלובק"><img src="art/clients/soglowek.png" alt="זוגלובק" loading="lazy"></a></li>
      <li class="h3"><a href="https://www.ariel.ac.il/" target="_blank" rel="noopener" title="אוניברסיטת אריאל"><img src="art/clients/ariel.svg" alt="אוניברסיטת אריאל" loading="lazy"></a></li>
      <li class="h3"><a href="https://www.sixsenses.com/en/hotels-resorts/middle-east-africa/israel/shaharut/" target="_blank" rel="noopener" title="Six Senses שחרות"><img src="art/clients/sixsenses.svg" alt="Six Senses שחרות" loading="lazy"></a></li>
      <li class="h2"><a href="https://jvpvc.com/" target="_blank" rel="noopener" title="JVP"><img src="art/clients/jvp.svg" alt="JVP" loading="lazy"></a></li>
      <li class="h3"><a href="https://schechter.ac.il/" target="_blank" rel="noopener" title="מכון שכטר למדעי היהדות"><img src="art/clients/schechter.svg" alt="מכון שכטר למדעי היהדות" loading="lazy"></a></li>
      <li class="h2"><a href="https://feuerstein-institute.org/" target="_blank" rel="noopener" title="מכון פוירשטיין"><img src="art/clients/feuerstein.svg" alt="מכון פוירשטיין" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.inbalhotel.com/" target="_blank" rel="noopener" title="מלון ענבל ירושלים"><img src="art/clients/inbal.svg" alt="מלון ענבל ירושלים" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.madatech.org.il/" target="_blank" rel="noopener" title="מדעטק"><img src="art/clients/madatech.png" alt="מדעטק" loading="lazy"></a></li>
      <li class="h1"><a href="https://comme-il-faut.com/" target="_blank" rel="noopener" title="Comme il faut"><img src="art/clients/commeilfaut.png" alt="Comme il faut" loading="lazy"></a></li>
      <li class="h2"><a href="https://auraisrael.co.il/" target="_blank" rel="noopener" title="אאורה ישראל"><img src="art/clients/aura.svg" alt="אאורה ישראל" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.rlaw.co.il/" target="_blank" rel="noopener" title="רפאל אלמוג ושות' עורכי דין"><img src="art/clients/rlaw.svg" alt="רפאל אלמוג ושות' עורכי דין" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.waterrower-il.com/" target="_blank" rel="noopener" title="WaterRower ישראל"><img src="art/clients/waterrower.png" alt="WaterRower ישראל" loading="lazy"></a></li>
      <li class="h2"><a href="https://www.butchers.co.il/" target="_blank" rel="noopener" title="The Butchers Furniture"><img src="art/clients/butchers.png" alt="The Butchers Furniture" loading="lazy"></a></li>
    </ul>
  </div>
</section>

<section class="sec services" id="perf">
  <div class="wrap">
    <div class="svc-head rv">
      <p class="eyebrow">השירותים שלנו</p>
      <button type="button" class="still-btn" id="still" aria-pressed="false"><span aria-hidden="true">❚❚</span><span class="still-txt">עצור תנועה</span></button>
      <div class="tabs only-m" aria-label="בחירת שירות">
        <button type="button" class="on" data-i="0" aria-controls="perf-slide" aria-current="true">פרפורמנס</button>
        <button type="button" data-i="1" aria-controls="creative">צוותי קריאייטיב</button>
        <button type="button" data-i="2" aria-controls="ai">בינה מלאכותית</button>
      </div>
    </div>
    <div class="track" id="track" aria-label="השירותים שלנו">
      <article class="slide rev on" id="perf-slide">
        <div class="copy">
          <p class="morph rv" id="morph" aria-hidden="true"><span class="m1">כל תקציב.</span><span class="m2"></span></p>
          <h2 class="svc rv"><span class="nw">פרפורמנס (קידום ממומן)</span> <span class="nw">בכל הפלטפורמות</span></h2>
          <p class="lead rv">ניהול תקציבי פרסום בכל הגדלים ולכל המטרות. לא "מריצים קמפיין", בונים מערך: מדידה נכונה מהיום הראשון, מבנה חשבון שמאפשר לגדול, בדיקות קריאייטיב כל שבוע, ואופטימיזציה יומית על מה שבאמת מזיז את המספרים.</p>
          <div class="goals rv">
            <div class="goal"><b>לידים</b><p>טפסים, שיחות והודעות וואטסאפ מאנשים שבאמת רוצים לשמוע מכם, במחיר לליד שאפשר לחיות איתו.</p></div>
            <div class="goal"><b>מכירות</b><p>חנויות ומוצרים: קטלוגים, רימרקטינג וחשבון שיודע כמה רווח יש על כל מכירה.</p></div>
            <div class="goal"><b>מוניטין</b><p>כשצריך שהשם שלכם יופיע נכון, במקום הנכון, לאנשים הנכונים, גם כשלא קל.</p></div>
          </div>
        </div>
        <div class="pstack">
          <figure class="frame rv"><div class="pic" data-par="5"><picture><source type="image/webp" srcset="art/w/ayalon-480.webp 480w, art/w/ayalon-800.webp 800w, art/w/ayalon-1300.webp 1300w" sizes="(max-width:899px) calc(100vw - 40px), 560px"><img src="art/ayalon.jpg" alt="איור דיו של נתיבי איילון בלילה" loading="lazy" width="1300" height="872"></picture></div></figure>
          <div class="ticker rv" role="marquee" aria-label="הפלטפורמות: מטא, גוגל, יוטיוב, טיקטוק, צ׳אט ג׳י־פי־טי, טאבולה, אאוטבריין"><div><div class="set" aria-hidden="true">__TICK__</div><div class="set" aria-hidden="true">__TICK__</div></div></div>
        </div>
      </article>
      <article class="slide" id="creative">
        <div class="copy">
          <h2 class="rv">יודעים לעבוד<br><span class="k">בשיתוף פעולה.</span></h2>
          <p class="svc rv">ניהול והפעלת צוותי קריאייטיב</p>
          <p class="lead rv">הקמפיין הכי טוב בעולם לא יציל מודעה משעממת. אנחנו מכווינים את צוות התוכן שלכם ועובדים איתו בפועל: מהבריף, דרך הצילום והעריכה, ועד המודעה שעולה לאוויר.</p>
          <p class="rv">יש לכם צוות? נהפוך אותו למכונה שמייצרת קריאייטיב שעובד, עם בריפים שמבוססים על נתונים, לוח הפקות קבוע ובדיקות א/ב כל שבוע. אין לכם צוות? בשביל זה יש <a href="#ai" class="go" data-i="2">פתרונות AI</a>.</p>
        </div>
        <figure class="frame tall rv"><div class="pic" data-par="6"><picture><source type="image/webp" srcset="art/w/blvd-480.webp 480w, art/w/blvd-800.webp 800w, art/w/blvd-970.webp 970w" sizes="(max-width:899px) calc(100vw - 40px), 520px"><img src="art/blvd.jpg" alt="איור דיו של שדרות רוטשילד בלילה עם שביל סגול" loading="lazy" width="970" height="1300"></picture></div></figure>
      </article>
      <article class="slide rev" id="ai">
        <div class="copy">
          <h2 class="rv">שימוש ב־AI כדי לחסוך לכם<br><span class="k">זמן וכסף.</span></h2>
          <p class="svc rv">פתרונות בינה מלאכותית</p>
          <p class="lead rv">בינה מלאכותית היא לא טריק, היא עובד נוסף שלא ישן. אנחנו בונים לעסקים פתרונות שעובדים ביום־יום, לא מצגות על העתיד.</p>
          <div class="cards rv">
            <div class="card"><h3>דפי נחיתה ואתרים</h3><p>מהירים, מדויקים לקמפיין, ונבנים בימים במקום בחודשים. כולל מדידה מובנית מהיום הראשון.</p></div>
            <div class="card"><h3>אוטומציות עסקיות</h3><p>לידים שמגיעים למקום הנכון, מענה ראשוני מיידי, דוחות שנכתבים לבד. מה שחוזר על עצמו, עובד לבד.</p></div>
            <div class="card"><h3>תוכן גנרטיבי</h3><p>תמונות, סרטונים וטקסטים בשפת המותג שלכם, בכמויות שקמפיין צריך, ובמחיר שאפשר לעמוד בו.</p></div>
          </div>
        </div>
        <figure class="frame sq rv"><div class="pic" data-par="5"><picture><source type="image/webp" srcset="art/w/cat-480.webp 480w, art/w/cat-800.webp 800w, art/w/cat-1047.webp 1047w" sizes="(max-width:899px) calc(100vw - 40px), 560px"><img src="art/cat.jpg" alt="איור דיו של חתול על מעקה מול ירח סגול" loading="lazy" width="1300" height="1300"></picture></div></figure>
      </article>
    </div>
    <div class="arrows only-m"><button type="button" class="arr prev" aria-label="השירות הקודם">→</button><span class="count" id="count" aria-live="polite">1 מתוך 3</span><button type="button" class="arr next" aria-label="השירות הבא">←</button></div>
  </div>
</section>

<section class="sec contact" id="contact">
  <div class="wrap grid">
    <div class="copy">
      <p class="eyebrow rv">דברו איתנו</p>
      <h2 class="rv">צריכים עזרה?<br><span class="k">דברו איתנו עכשיו.</span></h2>
      <p class="lead rv">שיחה אחת, בלי התחייבות. נספר לכם מה היינו עושים עם התקציב שלכם, ואיפה לדעתנו יש כסף על הרצפה.</p>
      <div class="price rv"><p class="eyebrow">כמה זה עולה</p><p>הריטיינר החודשי נקבע לפי מספר הפלטפורמות שאנחנו מפעילים, תקציב המדיה והשירותים המשלימים, ומתחיל מ־<b>3,500 ₪ לחודש</b>. בתקציבים גדולים עובדים גם במודל של ריטיינר בסיסי בתוספת אחוז מתקציב הפרסום, מההכנסות או מהרווח שנוסף, בהסכמה ובהסכם חתום.</p></div>
      <form class="form rv" id="form" novalidate>
        <div class="fields">
          <div class="field"><label for="f-name">שם מלא <span class="req">(חובה)</span></label><input id="f-name" name="name" autocomplete="name" dir="auto" required aria-describedby="e-name"><p class="err" id="e-name"></p></div>
          <div class="field"><label for="f-phone">טלפון <span class="req">(חובה)</span></label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="052-1234567" required aria-describedby="h-phone e-phone"><p class="hint" id="h-phone">כדי שנחזור אליכם בוואטסאפ או בשיחה. כל פורמט מתקבל.</p><p class="err" id="e-phone"></p></div>
          <div class="hp" aria-hidden="true"><label for="f-web">אתר</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
          <div class="field"><label for="f-biz">מה העסק ומה המטרה? <span class="req">(לא חובה)</span></label><input id="f-biz" name="biz" dir="auto" autocomplete="organization"></div>
          <button type="submit" id="send">שלחו ונחזור אליכם עד מחר</button>
          <a class="wa" href="__WA__" target="_blank" rel="noopener">וואטסאפ <bdi>__PL__</bdi></a>
          <p class="alt">או במייל: <a href="mailto:__MAIL__"><bdi>__MAIL__</bdi></a></p>
        </div>
        <div class="ok" id="ok" role="status" tabindex="-1" hidden><b>קיבלנו, תודה.</b><p>נחזור אליכם עד מחר בבוקר. דחוף? <a href="__WA__" target="_blank" rel="noopener">כתבו לנו בוואטסאפ</a>.</p></div>
      </form>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="top">
      <div class="brand">
        <div class="logo">__LOGO_CREAM__</div>
        <p class="motto">עם כוח גדול מגיעה אחריות גדולה, ועם תקציב גדול עוד יותר.</p>
      </div>
      <nav aria-label="ניווט בפוטר"><h3>באתר</h3><ul><li><a href="#perf">השירותים שלנו</a></li><li><a href="#about">מי אנחנו</a></li><li><a href="#clients">לקוחות</a></li><li><a href="knowledge.html">ידע</a></li><li><a href="#contact">דברו איתנו</a></li></ul></nav>
      <div><h3>השירותים</h3><ul><li><a href="#perf">פרפורמנס בכל הפלטפורמות</a></li><li><a href="#creative">ניהול צוותי קריאייטיב</a></li><li><a href="#ai">פתרונות בינה מלאכותית</a></li></ul></div>
      <div class="contact"><h3>דברו איתנו</h3><ul><li><a href="mailto:__MAIL__"><bdi>__MAIL__</bdi></a></li><li><a href="tel:+__PHONE_INTL__"><bdi>__PL__</bdi></a></li><li><span>תל אביב, ישראל</span></li></ul><a class="wa" href="__WA__" target="_blank" rel="noopener">וואטסאפ</a></div>
    </div>
    <div class="bottom"><span>© 2026 Z.G Digital Ltd · ז.ג דיגיטל בע"מ</span><a href="accessibility.html">הצהרת נגישות</a><a href="agents.html">מידע מסודר לסוכני AI</a></div>
  </div>
</footer>
__LD__
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>if(window.gsap&&window.ScrollTrigger&&!matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('gsap');</script>
<script>
(function(){
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const INK='__FG__', MOON='#8526FD';
// כתובת ה־Web app של Apps Script (lead-script.gs). ריק = הטופס נפתח בוואטסאפ עם הפרטים.
const LEAD_ENDPOINT='https://script.google.com/macros/s/AKfycbwAmHE-dSD9xdDrPztPh54oS75LD30-8bzfmKs3MRZzqpVeSvJFCEJxMcZx0mwUy-SFpQ/exec';
const WA_URL='__WA__';
// ---------- violet mist behind the opener: the Magic UI mist shader, recoloured to paper and violet ----------
(function mist(){ const c=document.getElementById('mist'); if(reduce) { c.remove(); return; }
  const gl=c.getContext('webgl',{antialias:false,alpha:false,preserveDrawingBuffer:false}); if(!gl){ c.remove(); return; }
  const VS=`attribute vec2 a_position; varying vec2 v_uv; void main(){ v_uv=a_position*0.5+0.5; gl_Position=vec4(a_position,0.0,1.0); }`;
  const FS=__FS__;
  const mk=(t,s)=>{ const sh=gl.createShader(t); gl.shaderSource(sh,s); gl.compileShader(sh); if(!gl.getShaderParameter(sh,gl.COMPILE_STATUS)){ console.error(gl.getShaderInfoLog(sh)); return null; } return sh; };
  const vs=mk(gl.VERTEX_SHADER,VS), fs=mk(gl.FRAGMENT_SHADER,FS); if(!vs||!fs){ c.remove(); return; }
  const pr=gl.createProgram(); gl.attachShader(pr,vs); gl.attachShader(pr,fs); gl.linkProgram(pr); gl.useProgram(pr);
  const buf=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,buf); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'a_position'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const uT=gl.getUniformLocation(pr,'u_time'), uR=gl.getUniformLocation(pr,'u_resolution');
  let visible=true; const resize=()=>{ const s=0.6; c.width=Math.round(c.clientWidth*s); c.height=Math.round(c.clientHeight*s); gl.viewport(0,0,c.width,c.height); }; resize(); addEventListener('resize',resize);
  new IntersectionObserver(e=>{ visible=e[0].isIntersecting; },{threshold:0}).observe(c);
  const t0=performance.now(); let last=0;
  (function frame(now){ requestAnimationFrame(frame); if(!visible||document.hidden||window.ZG_STILL||now-last<33) return; last=now; gl.uniform1f(uT,(now-t0)/1000); gl.uniform2f(uR,c.width,c.height); gl.drawArrays(gl.TRIANGLE_STRIP,0,4); })(t0);
})();
if(!window.gsap) return; gsap.registerPlugin(ScrollTrigger);
// ---------- quiet entrances ----------
if(!reduce){ ScrollTrigger.batch('.rv',{start:'top 100%',once:true,onEnter:els=>gsap.to(els,{opacity:1,y:0,duration:0.8,ease:'power3.out',stagger:0.08})}); gsap.set('.rv',{opacity:0,y:22}); }
else gsap.set('.rv',{opacity:1,y:0});
// ---------- the pictures drift a little slower than the page ----------
if(!reduce) document.querySelectorAll('.pic[data-par]').forEach(p=>{ const a=+p.dataset.par; gsap.fromTo(p,{yPercent:-a},{yPercent:a,ease:'none',scrollTrigger:{trigger:p.parentElement,start:'top bottom',end:'bottom top',scrub:0.4}}); });
// ---------- the silhouette breathes ----------

// ---------- melting words: budget, goal, platform; and the platform names ----------
function morpher(el,texts,colors,morph,hold){ const a=el.querySelector('.m1'), b=el.querySelector('.m2'), n=texts.length, per=morph+hold;
  const st=(sp,txt,col,f)=>{ sp.textContent=txt; sp.style.color=col||''; if(f<=0){ sp.style.filter='none'; sp.style.opacity=0; } else if(f>=1){ sp.style.filter='none'; sp.style.opacity=1; } else { sp.style.filter=`blur(${Math.min(8/f-8,100).toFixed(1)}px)`; sp.style.opacity=Math.pow(f,0.4).toFixed(3); } };
  return { at(t){ const i=Math.floor(Math.max(0,t)/per), u=t-i*per, f=u<hold? 0 : Math.min(1,(u-hold)/morph); st(a,texts[i%n],colors&&colors[i%n],1-f); st(b,texts[(i+1)%n],colors&&colors[(i+1)%n],f); } }; }
{ const mh=morpher(document.getElementById('morph'),['כל תקציב.','כל מטרה.','כל פלטפורמה.'],[INK,INK,MOON],0.7,1.7); mh.at(0);
  if(!reduce){ const o={t:0}; const tw=gsap.to(o,{t:3600,duration:3600,ease:'none',onUpdate(){ mh.at(o.t); },paused:true});
    ScrollTrigger.create({trigger:'#perf-slide',start:'top 85%',end:'bottom 15%',onToggle:s=>s.isActive? tw.resume() : tw.pause()}); } }
// ---------- the services slider ----------
(function slider(){ const track=document.getElementById('track'), slides=[...track.children], tabs=[...document.querySelectorAll('.tabs button')]; let cur=0;
  const go=i=>{ i=Math.max(0,Math.min(slides.length-1,i)); slides[i].scrollIntoView({behavior:'smooth',inline:'start',block:'nearest'}); };
  const fit=()=>{ if(matchMedia('(max-width:899px)').matches) track.style.height=slides[cur].offsetHeight+'px'; else track.style.height=''; };
  const count=document.getElementById('count');
  const roles=()=>{ const m=matchMedia('(max-width:899px)').matches; if(m){ track.setAttribute('role','region'); track.setAttribute('aria-roledescription','קרוסלה'); track.setAttribute('tabindex','0'); slides.forEach((sl,k)=>{ sl.setAttribute('role','group'); sl.setAttribute('aria-roledescription','שקופית'); sl.setAttribute('aria-label',(k+1)+' מתוך '+slides.length); }); } else { ['role','aria-roledescription','tabindex'].forEach(a=>track.removeAttribute(a)); slides.forEach(sl=>['role','aria-roledescription','aria-label'].forEach(a=>sl.removeAttribute(a))); } };
  roles(); addEventListener('resize',roles);
  const mark=i=>{ cur=i; slides.forEach((sl,k)=>sl.classList.toggle('on',k===i)); tabs.forEach((b,k)=>{ b.classList.toggle('on',k===i); if(k===i) b.setAttribute('aria-current','true'); else b.removeAttribute('aria-current'); }); if(count) count.textContent=(i+1)+' מתוך '+slides.length; fit(); };
  if(window.ResizeObserver){ const ro=new ResizeObserver(fit); slides.forEach(sl=>ro.observe(sl)); } addEventListener('resize',fit); addEventListener('load',fit); fit();
  tabs.forEach(b=>b.addEventListener('click',()=>go(+b.dataset.i))); document.querySelectorAll('.go').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); go(+a.dataset.i); }));
  document.querySelector('.arr.prev').addEventListener('click',()=>go(cur-1)); document.querySelector('.arr.next').addEventListener('click',()=>go(cur+1));
  const io=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting&&e.intersectionRatio>=0.6) mark(slides.indexOf(e.target)); }); },{root:track,threshold:[0.6]}); slides.forEach(sl=>io.observe(sl));
})();
// ---------- the top bar steps aside while reading on the phone, and comes back on the way up ----------
(function navHide(){ const nav=document.querySelector('.nav'); let last=scrollY; addEventListener('scroll',()=>{ const y=scrollY; if(!matchMedia('(max-width:899px)').matches){ nav.classList.remove('away'); last=y; return; } if(y>last+8&&y>140) nav.classList.add('away'); else if(y<last-8||y<80) nav.classList.remove('away'); last=y; },{passive:true}); nav.addEventListener('click',()=>nav.classList.remove('away')); })();
// ---------- one button stops everything that moves on its own ----------
(function still(){ const b=document.getElementById('still'); if(!b) return; b.addEventListener('click',()=>{ const on=document.documentElement.classList.toggle('still'); b.setAttribute('aria-pressed',on); b.querySelector('.still-txt').textContent=on?'הפעל תנועה':'עצור תנועה'; b.firstElementChild.textContent=on?'▶':'❚❚'; window.ZG_STILL=on; if(window.gsap){ on? gsap.globalTimeline.pause() : gsap.globalTimeline.resume(); } }); })();
// ---------- the ticker stops on a tap (phones have no pause button) ----------
(function tick(){ const t=document.querySelector('.ticker'); if(!t) return; t.addEventListener('click',()=>t.classList.toggle('paused')); })();
// ---------- the form ----------
(function form(){ const f=document.getElementById('form'); const F={name:document.getElementById('f-name'),phone:document.getElementById('f-phone')};
  const msg=(k,v)=>{ if(k==='name') return v?'' : 'כתבו את השם שלכם, כדי שנדע למי לחזור.'; const d=v.replace(/\D/g,''); if(!v) return 'צריך טלפון כדי שנוכל לחזור אליכם.'; if(d.length<9||d.length>13) return 'המספר צריך 9–13 ספרות, למשל 052-1234567 או +972.'; return ''; };
  const check=k=>{ const el=F[k], m=msg(k,el.value.trim()), box=el.closest('.field'); box.classList.toggle('bad',!!m); box.querySelector('.err').textContent=m; el.setAttribute('aria-invalid',m?'true':'false'); return !m; };
  Object.keys(F).forEach(k=>{ F[k].addEventListener('blur',()=>check(k)); F[k].addEventListener('input',()=>{ if(F[k].closest('.field').classList.contains('bad')) check(k); }); });
  const btn=f.querySelector('button[type=submit]'), ok=document.getElementById('ok');
  if(!LEAD_ENDPOINT) btn.textContent='שלחו לנו בוואטסאפ';
  const done=(viaWa)=>{ f.classList.add('sent'); if(viaWa) ok.querySelector('p').innerHTML='פתחנו לכם וואטסאפ עם הפרטים, נשאר רק ללחוץ "שלח". דחוף? <a href="'+WA_URL+'" target="_blank" rel="noopener">כתבו לנו ישירות</a>.'; ok.hidden=false; ok.focus(); try{ if(window.fbq) fbq('track','Lead'); if(window.gtag) gtag('event','generate_lead'); }catch(_){} };
  const payload=()=>({name:F.name.value.trim(),phone:F.phone.value.trim(),biz:document.getElementById('f-biz').value.trim(),website:document.getElementById('f-web').value,page:location.href});
  const viaWhatsApp=p=>{ const t=`היי, אני ${p.name}. טלפון: ${p.phone}.${p.biz?' '+p.biz:''} (מהאתר)`; window.open(WA_URL+'?text='+encodeURIComponent(t),'_blank','noopener'); done(true); };
  f.addEventListener('submit',async e=>{ e.preventDefault(); const bad=Object.keys(F).filter(k=>!check(k)); if(bad.length){ F[bad[0]].focus(); return; }
    const p=payload(); if(p.website) { done(false); return; }
    if(!LEAD_ENDPOINT){ viaWhatsApp(p); return; }
    btn.disabled=true; const t0=btn.textContent; btn.textContent='שולחים…';
    try{ const r=await fetch(LEAD_ENDPOINT,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(p),redirect:'follow'}); const j=await r.json(); if(!j.ok) throw new Error(j.error||'bad'); done(false); }
    catch(err){ btn.disabled=false; btn.textContent=t0; viaWhatsApp(p); } });
})();
})();
</script>
</body></html>
'''
import sys
THEME = sys.argv[1] if len(sys.argv)>1 else 'light'
if THEME=='dark':
    VARS="--bg:#0A061B;--bg2:#140D2E;--fg:#F3EADA;--line:#F3EADA;--dim:#B9B0D6;--navbg:#0A061B;--err:#FF8A80;--inputbg:#0A061B;--footbg:#05030E;color-scheme:dark;"
    MAN='hero_big_cream.png'; FG='#F3EADA'; SH_BG='vec3 bg=vec3(0.039,0.024,0.106);'; MIX='1.0'; HI='1.15'
    PART='float grain=fract(sin(dot(gl_FragCoord.xy*0.15+t*0.05, vec2(12.9898,78.233)))*43758.5453123); float particles=step(0.988,grain)*smoothstep(0.2,0.9,combinedDensity); col+=violet*particles*0.32; col=pow(col,vec3(0.92));'
    LOGO_NAV=LOGO_CREAM
else:
    VARS="--bg:#F3EADA;--bg2:#FBF6EC;--fg:#0A061B;--line:#0A061B;--dim:#5E5873;--navbg:#F3EADA;--err:#B3261E;--inputbg:#fff;--footbg:#0A061B;color-scheme:light;"
    MAN='hero_big.png'; FG='#0A061B'; SH_BG=''; MIX=''; HI=''; PART=''
    LOGO_NAV=LOGO
FS_MIST = '''`precision mediump float; varying vec2 v_uv; uniform float u_time; uniform vec2 u_resolution;
  #define TWO_PI 6.28318530718
  #define PI 3.14159265358979323846
  float random(vec2 st){ return fract(sin(dot(st.xy, vec2(12.9898,78.233)))*43758.5453123); }
  float noise(vec2 st){ vec2 i=floor(st); vec2 f=fract(st); float a=random(i); float b=random(i+vec2(1.0,0.0)); float c=random(i+vec2(0.0,1.0)); float d=random(i+vec2(1.0,1.0)); vec2 u=f*f*(3.0-2.0*f); return mix(mix(a,b,u.x),mix(c,d,u.x),u.y); }
  void main(){ vec2 uv=v_uv; float t=u_time*0.55-1.175; float noise_scale=0.00338;
    uv-=0.5; uv*=(noise_scale*u_resolution); uv/=1.5; uv+=0.5;
    float n1=noise(uv*1.0+t); float n2=noise(uv*2.0-t); float angle=n1*TWO_PI; uv.x+=0.32*n2*cos(angle); uv.y+=0.32*n2*sin(angle);
    for(int i=1;i<=5;i++){ float fi=float(i); uv.x+=0.65/fi*cos(t+fi*1.5*uv.y); uv.y+=0.65/fi*cos(t+fi*1.0*uv.x); }
    float sh=1.0-uv.y; sh-=0.5; sh/=(noise_scale*u_resolution.y); sh+=0.5;
    float shape=smoothstep(0.45-0.104,0.55+0.104,sh+0.3*(0.33-0.5)); float mixer=shape;
    vec3 bg=vec3(0.039,0.024,0.106); vec3 violet=vec3(0.522,0.149,0.992);
    float mistFocus=pow(sin(mixer*PI),4.2);
    float fineMist=noise(uv*3.5-t*1.3)*0.4+noise(uv*1.5+t*0.85)*0.6;
    float combinedDensity=mix(mixer,fineMist,0.28)*mistFocus;
    vec3 col=mix(bg,violet,smoothstep(0.0,0.85,combinedDensity));
    float highlight=smoothstep(0.42,0.88,fineMist)*smoothstep(0.12,0.9,mixer)*mistFocus;
    col=mix(col,violet*1.15,highlight*0.35);
    vec2 raySource=vec2(0.2,1.25); vec2 rayDir=normalize(v_uv-raySource); float rayAngle=atan(rayDir.y,rayDir.x);
    float rays=sin(rayAngle*6.5+t*0.35)*0.35+sin(rayAngle*12.0-t*0.22)*0.25+sin(rayAngle*24.0+t*0.15)*0.15; rays=smoothstep(0.15,0.82,rays*0.5+0.5);
    float rayGlow=rays*smoothstep(0.15,0.9,combinedDensity)*(1.1-v_uv.y)*mistFocus*0.7; col+=violet*rayGlow*0.38;
    float grain=random(gl_FragCoord.xy*0.15+t*0.05); float particles=step(0.988,grain)*smoothstep(0.2,0.9,combinedDensity); col+=violet*particles*0.32;
    col=pow(col,vec3(0.92));
    gl_FragColor=vec4(col,1.0); }`'''
# wet violet ink on paper: three soft blots that drift slowly behind the frame, edges warped by noise, fading out well before the canvas edge
FS_INK = '''`precision mediump float; varying vec2 v_uv; uniform float u_time; uniform vec2 u_resolution;
  float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453123); }
  float noise(vec2 p){ vec2 i=floor(p); vec2 f=fract(p); vec2 u=f*f*(3.0-2.0*f); return mix(mix(hash(i),hash(i+vec2(1.0,0.0)),u.x),mix(hash(i+vec2(0.0,1.0)),hash(i+vec2(1.0,1.0)),u.x),u.y); }
  float fbm(vec2 p){ float v=0.0; float a=0.5; for(int i=0;i<3;i++){ v+=a*noise(p); p=p*2.1+vec2(37.0,11.0); a*=0.5; } return v; }
  void main(){ vec2 uv=v_uv; float asp=u_resolution.x/u_resolution.y; vec2 p=vec2(uv.x*asp,uv.y); float t=u_time*0.11;
    vec3 cream=vec3(0.953,0.918,0.855); vec3 violet=vec3(0.522,0.149,0.992);
    float d=0.0;
    for(int i=0;i<3;i++){ float fi=float(i);
      vec2 c=vec2(0.5*asp+0.24*asp*cos(t*0.7+fi*2.1), 0.5+0.22*sin(t*0.9+fi*1.7));
      float r=0.30+0.05*sin(t*1.3+fi*2.0);
      float n=fbm(p*2.4+fi*5.0+vec2(t*0.6,-t*0.4));
      float dist=length(p-c)+(n-0.5)*0.26;
      d+=1.0-smoothstep(r*0.25,r,dist); }
    d=clamp(d,0.0,1.0);
    float edge=smoothstep(0.0,0.22,uv.x)*smoothstep(0.0,0.22,1.0-uv.x)*smoothstep(0.0,0.2,uv.y)*smoothstep(0.0,0.2,1.0-uv.y);
    float a=(smoothstep(0.0,1.0,d)*0.42 + smoothstep(0.05,0.3,d)*(1.0-smoothstep(0.3,0.7,d))*0.12)*edge;
    vec3 col=mix(cream,violet,a);
    gl_FragColor=vec4(col,1.0); }`'''
if THEME=='dark':
    html = html.replace('__CANVAS_HERO__','<canvas id="mist" class="full" aria-hidden="true"></canvas>').replace('__CANVAS_ART__','').replace('__FS__',FS_MIST)
else:
    html = html.replace('__CANVAS_HERO__','').replace('__CANVAS_ART__','<canvas id="mist" class="ink" aria-hidden="true"></canvas>').replace('__FS__',FS_INK)
html = html.replace('__VARS__',VARS).replace('__MAN__',MAN).replace('__FG__',FG).replace('__SHADER_BG__',SH_BG).replace('__MIX__',MIX).replace('__HI__',HI).replace('__PARTICLES__',PART)
OUT = '/home/claude/site/calm/dark.html' if THEME=='dark' else '/home/claude/site/calm/index.html'
if THEME=='dark': html = html.replace('<link rel="canonical" href="https://zigzagmedia.co.il/">','<meta name="robots" content="noindex">')
out = (html.replace('__LOGO_CREAM__',LOGO_CREAM).replace('__LOGO__',LOGO_NAV).replace('__WA__',WA).replace('__PL__',PHONE_LOCAL).replace('__MAIL__',MAIL).replace('__PHONE_INTL__',PHONE_INTL)
        .replace('__LD__','<script type="application/ld+json">'+json.dumps(LD_ORG,ensure_ascii=False)+'</script>')
        .replace('__TICK__',''.join(f'<span>{p}</span>' for p in PLATFORMS)))
open(OUT,'w').write(out); print('written',THEME,len(out))
