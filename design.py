"""サイトの新しいデザイン（2026-11-26〜）。ルールは claude.ai プロジェクトの「Webサイト制作の教科書」。
build.py から読み込んで、見た目・ヘッダー・フッター・トップ・立場別・お悩み別のページを作る。"""
import re, sys, html as _h
sys.path.insert(0, "/home/claude/slidekit")
import kit

CTA_TXT = "まずは話を聞いてみる（30分・無料）"

def I(name, size=24, color="currentColor", stroke=1.8):
    return kit.line(name, size, color, stroke)

# ---------------------------------------------------------------- CSS
CSS = """
:root{--bg:#fff;--alt:#f4f7f8;--ink:#1f2a37;--sub:#56616f;--main:#1d6f86;--main-dk:#155a6d;--main-soft:#e6f1f4;--accent:#ee6a35;--marker:#ffe58a;--line:#dfe6ea;
 --fh:'Zen Maru Gothic','Hiragino Maru Gothic ProN',sans-serif;--fb:'Noto Sans JP','Hiragino Sans','Noto Sans CJK JP','Yu Gothic',sans-serif}
*{box-sizing:border-box;min-width:0}html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--fb);font-size:17px;line-height:1.85;letter-spacing:.03em;
 word-break:auto-phrase;line-break:strict;font-feature-settings:"palt" 1;-webkit-text-size-adjust:100%;overflow-x:clip}
h1,h2,h3{font-family:var(--fh);font-weight:900;line-height:1.45;letter-spacing:.04em;text-wrap:balance;margin:0}
p{margin:0 0 .9em;text-wrap:pretty}
a{color:var(--main)}
b,strong{font-weight:700}
img{max-width:100%}
.mk{background:linear-gradient(transparent 62%,var(--marker) 62%);box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:0 .1em}
.nw{display:inline-block}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.narrow{max-width:760px}
section{padding:84px 0}
section.alt,section.band{background:var(--alt)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:var(--main);letter-spacing:.08em;margin:0 0 10px}
.eyebrow::before{content:"";width:18px;height:3px;background:var(--main);border-radius:2px}
h2{font-size:clamp(25px,3.3vw,35px);margin-bottom:16px}
h3{font-size:20px}
.lead,.sub{font-size:17px;color:var(--sub);max-width:700px}
.small{font-size:14px;color:var(--sub)}
.center{text-align:center}
/* ヘッダー */
.hd{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;gap:26px;height:68px}
.logo{display:flex;flex-direction:column;line-height:1.3;text-decoration:none;color:var(--ink);flex:none}
.logo small{font-size:11px;color:var(--sub);letter-spacing:.06em}.logo b{font-family:var(--fh);font-size:17px;font-weight:900}
.nav{display:flex;gap:22px;margin-left:auto}
.nav a{color:var(--ink);text-decoration:none;font-size:15px;font-weight:500;white-space:nowrap}
.nav a:hover,.nav a.on{color:var(--main)}
/* ボタン */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;
 border-radius:999px;padding:16px 30px;font-size:17px;line-height:1.4;box-shadow:0 4px 0 #c24f22;transition:transform .1s;text-align:center;border:0;cursor:pointer;font-family:inherit}
.btn:active{transform:translateY(2px);box-shadow:0 2px 0 #c24f22}
.btn.sm{padding:9px 18px;font-size:14px;box-shadow:none;flex:none}
.btn.ghost,.btn.sub{background:#fff;color:var(--main);border:2px solid var(--main);box-shadow:none}
.cta,.ctarow{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:24px}
.calm{font-size:14px;color:var(--sub);margin-top:10px;display:flex;gap:6px 16px;flex-wrap:wrap}
.calm span{display:inline-flex;align-items:center;gap:4px}
.textlink{font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.textlink:hover{text-decoration:underline}
/* 最初の画面 */
.hero{padding:52px 0 64px;background:linear-gradient(180deg,var(--main-soft),#fff)}
.hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.hero .wrap.one{display:block;max-width:860px}
.for{display:flex;align-items:center;gap:10px;font-family:var(--fh);font-weight:900;color:var(--main);font-size:clamp(20px,2.4vw,27px);line-height:1.45;margin:0 0 14px;letter-spacing:.04em}
.for .ln{flex:none}
.tag{display:inline-block;font-weight:700;color:var(--main);font-size:15px;margin:0 0 10px}
.hero h1{font-size:clamp(28px,4.1vw,46px);margin-bottom:20px}
.hero .lead{color:var(--ink);font-size:18px;margin-bottom:22px}
.reasons{display:grid;gap:10px;margin:0 0 4px;padding:0;list-style:none}
.reasons li{display:flex;align-items:center;gap:12px;font-size:16px;font-weight:700;line-height:1.5}
.reasons li .ico{width:38px;height:38px;border-radius:10px;flex:none}
.pricenote{font-size:14px;color:var(--sub);margin:16px 0 0}
.pricenote b{color:var(--ink)}
.person{position:relative}
.person img{width:100%;aspect-ratio:4/4.4;object-fit:cover;border-radius:28px;display:block}
.namecard{position:absolute;left:-28px;bottom:26px;background:#fff;border-radius:16px;padding:14px 18px;box-shadow:0 12px 30px rgba(20,40,60,.14);line-height:1.5}
.namecard small{display:block;font-size:12px;color:var(--sub)}.namecard b{font-family:var(--fh);font-size:20px}
.bubble{position:absolute;right:-14px;top:22px;background:#fff;border-radius:18px 18px 4px 18px;padding:12px 18px;font-size:15px;font-weight:700;box-shadow:0 12px 30px rgba(20,40,60,.14);line-height:1.6}
/* 信頼の帯 */
.trust{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:22px 0;background:#fff}
.trust ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.trust li{display:flex;align-items:center;gap:12px;font-size:14px;line-height:1.5;color:var(--sub)}
.trust li .ln{color:var(--main);flex:none}
.trust b{display:block;font-size:16px;color:var(--ink)}
/* 動画 */
.vidgrid{display:grid;grid-template-columns:.9fr 1.1fr;gap:44px;align-items:center}
.vid{position:relative;aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#000;box-shadow:0 18px 40px rgba(20,40,60,.15)}
.vid video,.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.checks{list-style:none;padding:0;margin:16px 0 0}
.checks li{display:flex;gap:10px;align-items:flex-start;margin-bottom:8px}
.checks li .ln{color:var(--main);flex:none;margin-top:5px}
/* カード */
.cards,.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}
.cards.c2,.grid.g2{grid-template-columns:repeat(2,1fr)}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px 24px}
.alt .card,.band .card{border-color:transparent}
.card h3{font-size:19px;margin:12px 0 8px}
.card h3:first-child{margin-top:0}
.card p{font-size:16px;color:var(--sub);margin:0 0 .6em}
.card p:last-child{margin-bottom:0}
.card .who{font-size:14px;font-weight:700;color:var(--main);margin-top:10px}
.ico{width:52px;height:52px;border-radius:14px;background:var(--main-soft);display:grid;place-items:center;color:var(--main)}
/* 関係図 */
.diagram{display:grid;grid-template-columns:1fr 190px 1fr;gap:18px;align-items:stretch;margin-top:30px}
.side{background:#fff;border-radius:18px;padding:26px;border:1px solid var(--line)}
.side .who{font-size:14px;font-weight:700;color:var(--main);display:flex;align-items:center;gap:8px;margin:0 0 6px}
.side h3{font-size:21px;margin-bottom:10px}
.side p{font-size:16px;color:var(--sub);margin:0 0 .6em}
.side ul{margin:10px 0 0;padding:0;list-style:none}
.side li{display:flex;gap:8px;font-size:15px;margin-bottom:6px;line-height:1.6}
.side li .ln{color:var(--main);flex:none;margin-top:4px}
.hub{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.hub img{width:120px;height:120px;border-radius:50%;object-fit:cover;border:6px solid #fff;box-shadow:0 8px 24px rgba(20,40,60,.15)}
.hub b{display:block;font-family:var(--fh);margin-top:8px}
.hub small{color:var(--sub);font-size:13px;line-height:1.5}
/* 手順 */
.flow{display:grid;grid-template-columns:300px 1fr;gap:52px;align-items:center;margin-top:30px}
.paper{background:#fff;border-radius:6px;box-shadow:0 18px 40px rgba(20,40,60,.16);padding:24px 22px;transform:rotate(-2deg)}
.paper .ph{display:inline-block;background:var(--main);color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:4px}
.paper .pt{font-family:var(--fh);font-weight:900;font-size:20px;line-height:1.45;margin:12px 0}
.paper .pl{height:8px;background:#e9eef0;border-radius:4px;margin:9px 0}
.paper .pq{display:flex;align-items:center;gap:12px;margin-top:16px;font-size:12px;color:var(--sub);line-height:1.5}
.steps{list-style:none;margin:20px 0 0;padding:0;counter-reset:s}
.steps li{position:relative;padding:0 0 24px 62px;min-height:44px}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:-2px;width:42px;height:42px;border-radius:50%;background:var(--main);color:#fff;font-weight:900;font-size:19px;display:grid;place-items:center;font-family:var(--fh)}
.steps li:not(:last-child)::after{content:"";position:absolute;left:20px;top:44px;bottom:4px;width:2px;background:var(--line)}
.steps b{font-size:18px;display:block;font-family:var(--fh);line-height:1.5;margin-bottom:2px}
.steps span{color:var(--sub);font-size:16px}
.steps .who{display:inline-block;font-size:12px;font-weight:700;color:var(--main);background:var(--main-soft);border-radius:6px;padding:1px 8px;margin-bottom:4px}
.note{display:inline-flex;align-items:center;gap:8px;background:var(--main-soft);border-radius:10px;padding:10px 16px;font-size:15px;font-weight:700}
/* 約束 */
.promises{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:30px}
.promise .n{font-family:var(--fh);font-weight:900;color:var(--main);font-size:14px;margin:12px 0 0}
.promise h3{font-size:18px;margin:4px 0 6px}
.limits{margin-top:22px;font-size:14px;color:var(--sub);background:#fff;border-radius:14px;padding:16px 20px;border:1px solid var(--line)}
.limits summary{cursor:pointer;font-weight:700;color:var(--ink)}
.limits p{margin:.6em 0 0}
/* 立場 */
.roles{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:28px}
.role{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px 20px;text-decoration:none;color:var(--ink)}
.role .who{font-size:13px;font-weight:700;color:var(--main)}
.role h3{font-size:18px;margin:6px 0 8px}
.role p{font-size:15px;color:var(--sub);margin:0 0 12px;flex:1}
.role .go{font-size:14px;font-weight:700;color:var(--main)}
.role:hover{border-color:var(--main)}
/* AI */
.aiways{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}
.aiway .tagline{display:inline-block;font-size:12px;font-weight:700;border-radius:6px;padding:2px 8px;background:var(--main-soft);color:var(--main);margin-top:12px}
.aiway ul{margin:10px 0 0;padding-left:1.1em;font-size:15px;color:var(--sub)}
.samples{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
.sample{background:#fff;border-radius:14px;box-shadow:0 10px 30px rgba(20,40,60,.10);overflow:hidden;display:flex;flex-direction:column}
.sample .top{padding:16px 20px;border-bottom:1px solid var(--line)}
.sample .top b{font-family:var(--fh);font-size:17px}
.sample .top small{display:block;color:var(--sub);font-size:13px;line-height:1.6}
.sample pre{margin:0;padding:16px 20px;font-family:var(--fb);font-size:14px;line-height:1.8;white-space:pre-wrap;max-height:220px;overflow:hidden;position:relative;flex:1}
.sample pre::after{content:"";position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(transparent,#fff)}
.sample .more{padding:12px 20px;font-size:14px;font-weight:700;border-top:1px solid var(--line);text-decoration:none}
.proof{display:flex;gap:14px;align-items:center;background:#fff;border:1px dashed var(--main);border-radius:14px;padding:14px 18px;margin-top:24px;font-size:15px}
.proof .ln{color:var(--main);flex:none}
/* 料金 */
.price{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px}
.pbox{background:#fff;border-radius:18px;padding:28px;border:1px solid var(--line)}
.pbox .k{font-size:15px;font-weight:700;color:var(--sub);margin:0}
.pbox .v{font-family:var(--fh);font-weight:900;font-size:44px;line-height:1.3;margin:0}
.pbox .v small{font-size:20px;margin-left:4px}
.pbox ul{margin:14px 0 0;padding-left:1.2em;color:var(--sub);font-size:15px}
.pbox.main{border:2px solid var(--main)}
.terms{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.terms span{display:inline-flex;align-items:center;gap:6px;background:#fff;border-radius:999px;padding:8px 16px;font-size:15px;font-weight:700}
.terms .ln{color:var(--main)}
.more-box{margin-top:22px;background:#fff;border-radius:14px;border:1px solid var(--line)}
.more-box>summary{cursor:pointer;padding:16px 20px;font-weight:700;list-style:none;color:var(--main)}
.more-box>summary::after{content:" ＋"}.more-box[open]>summary::after{content:" −"}
.more-box .in{padding:0 20px 20px}
/* 表 */
.tb{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:16px;background:#fff}
th,td{text-align:left;vertical-align:top;padding:14px 16px;border-bottom:1px solid var(--line);line-height:1.7}
th{width:28%;font-weight:700;color:var(--ink);background:#fafcfc}
/* 担当者 */
.me{display:grid;grid-template-columns:300px 1fr;gap:48px;align-items:start}
.me>img{width:100%;border-radius:22px;display:block}
.me h3.nm{font-size:28px}
.me .kana{font-size:15px;color:var(--sub);font-weight:700;margin-left:10px}
.me .role2{color:var(--sub);font-size:15px;margin:4px 0 16px}
.career{list-style:none;padding:0;margin:0 0 18px}
.career li{display:grid;grid-template-columns:28px 1fr;gap:10px;padding:10px 0;border-bottom:1px dashed var(--line);font-size:16px}
.career .ln{color:var(--main);margin-top:3px}
.minivid{margin-top:8px;max-width:520px}
/* よくある質問 */
details.q,.faq details{background:#fff;border-radius:14px;margin-bottom:10px;border:1px solid var(--line)}
.faq summary{cursor:pointer;padding:18px 52px 18px 22px;font-weight:700;list-style:none;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:22px;top:50%;transform:translateY(-50%);font-size:24px;color:var(--main);font-weight:400}
.faq details[open] summary::after{content:"−"}
.faq details p{padding:0 22px 18px;margin:0;color:var(--sub);font-size:16px}
/* 箇条書き（従来のページ用） */
.worry{list-style:none;padding:0;margin:20px 0 0;display:grid;gap:10px}
.worry li{background:#fff;border-radius:12px;padding:14px 18px 14px 48px;position:relative;font-weight:700}
.worry li::before{content:"";position:absolute;left:18px;top:22px;width:14px;height:14px;border-radius:50%;border:3px solid var(--main)}
.others{display:flex;flex-wrap:wrap;gap:10px}
.others a{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 16px;text-decoration:none;font-size:15px;font-weight:700;color:var(--ink)}
.others a:hover{border-color:var(--main);color:var(--main)}
.mihon{white-space:pre-wrap;background:#fafcfc;border:1px solid var(--line);border-radius:10px;padding:16px;font-size:14px;line-height:1.8;margin-top:12px}
/* 最後の申し込み */
.final{background:var(--main);color:#fff;border-radius:28px;padding:52px 48px;display:grid;grid-template-columns:1fr auto;gap:30px;align-items:center}
.final h2{color:#fff;margin-bottom:10px}
.final p{color:#e3f0f3;margin:0}
.final .calm{color:#d4e8ed}
.final .btn.sub{background:transparent;color:#fff;border-color:#fff}
.final .btns{display:flex;flex-direction:column;gap:12px}
/* フッター */
.ft{background:#16222c;color:#c9d3da;padding:56px 0 110px;font-size:14px}
.ft .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.ft h4{color:#fff;font-size:14px;margin:0 0 10px}
.ft a{color:#c9d3da;text-decoration:none;display:block;padding:4px 0;line-height:1.6}
.ft a:hover{color:#fff}
.ft .copy{margin-top:30px;border-top:1px solid #2c3a45;padding-top:18px}
.stick{display:none}
/* 道具のページ（チラシ・提案書・診断・試算） */
.q{border:1px solid var(--line);background:#fff;border-radius:12px;padding:12px 16px;margin:0 0 10px}.q legend{font-weight:700;padding:0 6px}.q label{margin-right:18px;display:inline-block;padding:4px 0}
.tool{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0;display:grid;gap:10px;max-width:640px}
.tool label{font-weight:700;font-size:14px}.tool input,.tool select{width:100%;font:inherit;font-size:16px;padding:10px 12px;border:1px solid #b8c2cc;border-radius:8px}
.sheet{background:#fff;border:1px solid var(--line);max-width:794px;margin:0 auto 32px;padding:40px 44px}
.sheet h1{font-size:30px}.sheet .co{font-family:var(--fh);font-size:18px;margin:0 0 4px}
.sheet .row{display:grid;grid-template-columns:1fr 190px;gap:24px;align-items:start;margin-top:18px}
.qr{border:3px solid var(--ink);border-radius:12px;padding:12px;text-align:center;font-size:13px}.qr #qr{display:grid;place-items:center;min-height:150px}
@media print{.hd,.tool,.ft,.stick,.noprint{display:none!important}body{background:#fff}.sheet{border:0;margin:0;padding:0;max-width:none}@page{size:A4;margin:16mm}}
/* スマホ */
@media (max-width:860px){
 body{font-size:16px}
 section{padding:58px 0}
 .wrap{padding:0 20px}
 .hd .wrap{height:auto;gap:0 12px;flex-wrap:wrap;padding-top:8px}
 .logo small{display:none}.logo b{font-size:15px}
 .nav{order:3;width:100%;margin:0;height:44px;align-items:center;gap:20px;overflow-x:auto;scrollbar-width:none}
 .nav::-webkit-scrollbar{display:none}
 .nav a{font-size:14px}
 .hd .btn.sm{margin-left:auto;padding:8px 12px;font-size:12px}
 .hero{padding:26px 0 44px}
 .hero .wrap{grid-template-columns:1fr;gap:28px}
 .person{max-width:420px;margin:0 auto;width:100%}
 .person img{aspect-ratio:4/3.3;object-position:50% 22%}
 .namecard{left:12px;bottom:12px}
 .bubble{right:10px;top:12px;font-size:14px}
 .hero .cta .btn,.hero .ctarow .btn{width:100%}
 .trust ul{grid-template-columns:1fr 1fr}
 .vidgrid,.flow,.me,.price,.final,.diagram{grid-template-columns:1fr}
 .vidgrid{gap:22px}
 .cards,.grid,.cards.c2,.grid.g2,.promises,.aiways{grid-template-columns:1fr}
 .roles,.samples{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin-left:-20px;margin-right:-20px;padding:0 20px 8px;grid-template-columns:none}
 .roles>*,.samples>*{flex:0 0 84%;scroll-snap-align:start}
 .hub{flex-direction:row;gap:14px;justify-content:flex-start;text-align:left}
 .hub img{width:72px;height:72px;border-width:3px}
 .flow{gap:32px}.paper{max-width:290px;margin:0 auto}
 .me{gap:22px}.me>img{max-width:240px}
 .final{padding:34px 22px;border-radius:22px}
 .final .btn{width:100%}
 th,td{display:block;width:100%;border:0;padding:4px 14px}
 th{padding-top:14px;background:none;color:var(--main)}
 tr{display:block;border-bottom:1px solid var(--line);padding-bottom:10px}
 .ft .cols{grid-template-columns:1fr 1fr}
 .sheet{padding:24px 18px}.sheet .row{grid-template-columns:1fr}
 .stick{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:30;background:rgba(255,255,255,.97);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));gap:10px;align-items:center;transform:translateY(110%);transition:transform .25s}
 .stick.on{transform:none}
 .stick .btn{flex:1;padding:13px 10px;font-size:15px}
 .stick small{font-size:11px;color:var(--sub);line-height:1.4;width:76px;flex:none}
}
"""

# ---------------------------------------------------------------- 共通の部品
NAV = [("service", "サービス"), ("ai", "AIでできること"), ("price", "料金"), ("me", "担当者"), ("faq", "よくある質問")]

def header(cur, form):
    pre = "" if cur == "index.html" else "index.html"
    links = "".join(f'<a href="{pre}#{k}">{t}</a>' for k, t in NAV)
    return (f'<header class="hd"><div class="wrap"><a class="logo" href="index.html"><small>竹村正太｜国家資格キャリアコンサルタント</small><b>社外の専属キャリアコンサルタント</b></a>'
            f'<nav class="nav" aria-label="メニュー">{links}</nav><a class="btn sm" href="{form}">無料で話を聞く</a></div></header>')

def footer(form, stick_label="まずは話を聞いてみる", stick_note="オンライン<br>30分・無料"):
    return (f'''<footer class="ft"><div class="wrap"><div class="cols">
 <div><h4>立場から探す</h4><a href="keieisha.html">経営者の方へ</a><a href="jinji.html">人事・総務の方へ</a><a href="saiyo.html">採用担当の方へ</a><a href="kanrishoku.html">管理職の方へ</a><a href="hataraku.html">会社で働く方へ</a><a href="sharoushi.html">社会保険労務士の方へ</a></div>
 <div><h4>お悩みから探す</h4><a href="wakate-rishoku.html">若手が本音を言わずに辞める</a><a href="kanrishoku-hihei.html">管理職が疲れている</a><a href="keieisha-sodan.html">経営者に相談相手がいない</a><a href="sodan-kawaranai.html">相談しても変わらない</a><a href="stress-check-junbi.html">ストレスチェックの準備</a><a href="coaching-kaisha-futan.html">コーチングを会社負担で</a></div>
 <div><h4>業種から探す</h4><a href="kaigo-fukushi.html">介護・福祉</a><a href="inshoku-shukuhaku.html">飲食・宿泊</a><a href="it-remote.html">IT・リモートワーク中心</a><a href="shien-kikan.html">支援機関・教育</a></div>
 <div><h4>道具と資料</h4><a href="mihon.html">AIで作った見本</a><a href="annai.html">社員向けの案内チラシ</a><a href="teian.html">上司に見せる1枚</a><a href="mitsumori.html">費用の試算</a><a href="shindan.html">3分診断</a><a href="unei.html">運営者情報・個人情報</a></div>
</div><p class="copy">社外の専属キャリアコンサルタント｜担当：竹村正太（国家資格キャリアコンサルタント）</p></div></footer>
<div class="stick" id="stick"><small>{stick_note}</small><a class="btn" href="{form}">{stick_label}</a></div>
<script>(function(){{var s=document.getElementById("stick");if(!s)return;function f(){{s.classList.toggle("on",window.scrollY>480)}}addEventListener("scroll",f,{{passive:true}});f()}})();</script>
</body></html>''')

def calm(items=("売り込みはしません", "オンラインで30分", "入力は1分ほど")):
    return '<p class="calm">' + "".join(f'<span>{I("check",16)}{t}</span>' for t in items) + '</p>'

def vid(src, title, poster=None):
    poster = poster or src[:-4] + ".jpg"
    return f'<div class="vid"><video controls preload="none" playsinline poster="{poster}" src="{src}" title="{title}"></video></div>'

def sec(inner, cls="", id_=""):
    return f'<section{" class=%s" % chr(34) + cls + chr(34) if cls else ""}{" id=%s" % chr(34) + id_ + chr(34) if id_ else ""}><div class="wrap">{inner}</div></section>'

def head2(eyebrow, h2, lead=""):
    return (f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else "") + f'<h2>{h2}</h2>' + (f'<p class="lead">{lead}</p>' if lead else "")

QR = kit.qr("https://doushimasho.github.io/senzoku/", 64)

def block_video():
    return sec(f'''<div class="vidgrid"><div>{head2("1分でわかる", "どんなサービスか、<br>動画でご覧ください")}
<ul class="checks"><li>{I("circle-check",20)}<span>誰が、誰の相談を受けるのか</span></li><li>{I("circle-check",20)}<span>社員が話した内容を、会社にどう扱うか</span></li><li>{I("circle-check",20)}<span>会社での導入の手間と、料金</span></li></ul>
<p class="small" style="margin-top:12px">音声つき・字幕あり（57秒）</p></div>{vid("shokai.mp4", "サービス紹介")}</div>''', id_="video")

def block_flow(cls="alt"):
    return sec(head2("会社での導入", "導入の手間は、<br>人事の方が<span class=\"mk\">社員にチラシを配るだけ</span>",
                     "説明会や、社内の仕組みづくりは要りません。契約から社員の相談が始まるまでの流れです。") +
f'''<div class="flow"><div class="paper"><span class="ph">社員のみなさんへ</span><div class="pt">社外の相談窓口が<br>できました</div><div class="pl" style="width:92%"></div><div class="pl" style="width:76%"></div><div class="pl" style="width:84%"></div>
<div class="pq">{QR}<span>QRコードから<br>予約できます</span></div></div>
<ol class="steps">
<li><span class="who">御社と担当者（竹村）</span><b>30分の説明のあと、契約します</b><span>申込フォームと電子契約で、書類のやりとりはありません。</span></li>
<li><span class="who">担当者（竹村）</span><b>御社用の案内チラシと案内文を用意します</b><span>会社名と予約用のQRコードを入れた、社員向けの案内です。</span></li>
<li><span class="who">人事・総務の方</span><b>社員の皆さんに、チラシを配ります</b><span>印刷して配っても、社内のチャットやメールで送っても構いません。</span></li>
<li><span class="who">社員の方</span><b>自分でQRコードから予約し、オンラインで30分話します</b><span>会社を通さずに予約するので、誰が相談したかは会社に分かりません。</span></li>
</ol></div>''', cls, "flow")

def block_promises(cls=""):
    return sec(head2("安心の約束", "社員が話したことは、<br><span class=\"mk\">会社に伝えません</span>",
                     "社員が安心して話せることが、このしくみの土台です。4つの約束を、会社との契約書にも書きます。") +
f'''<div class="promises">
<div class="card promise"><div class="ico">{I("lock",28)}</div><p class="n">約束 1</p><h3>話の内容は伝えない</h3><p>誰が何を話したかは、会社に伝えません。会社への報告は、月の件数だけです。</p></div>
<div class="card promise"><div class="ico">{I("microphone-off",28)}</div><p class="n">約束 2</p><h3>録音・録画をしない</h3><p>残すのは担当者の手書きのメモだけです。ほかの人は見られません。</p></div>
<div class="card promise"><div class="ico">{I("mail-forward",28)}</div><p class="n">約束 3</p><h3>望んだ声だけを届ける</h3><p>社員本人が会社に伝えたいことだけを、文面を一緒に確かめ、名前を出さずに届けます。</p></div>
<div class="card promise"><div class="ico">{I("scale",28)}</div><p class="n">約束 4</p><h3>どちらの味方もしない</h3><p>転職や退職の相談も受けます。引き止めも、転職の勧めもしません。</p></div>
</div>
<details class="limits"><summary>この窓口で扱わないこと</summary>
<p>この窓口は、会社が設けるハラスメントの相談窓口の代わりにはなりません。ハラスメントに関わる相談を受けたときは、会社の正式な窓口と社外の公的な相談先をご案内し、ご本人が望めば、会社に伝える手伝いをします。</p>
<p>この窓口は医療機関ではありません。体調や心の不調が続くときは、産業医や医療機関など適切な相談先につなぎます。命や安全に関わる差し迫った状況では、本人を守るために必要な相手へ連絡することがあります。</p></details>''', cls, "promise")

SAMPLES = [
 ("社員向けの案内", "社外の相談窓口ができたことを、全社員に知らせる文", "5分",
  "【社外の相談窓口ができました】\n\n仕事のこと、これからのこと、人間関係のこと。\n社内の人には少し話しにくいことを、社外のキャリアコンサルタントに相談できるようになりました。\n\n・1回30分、オンラインで話せます\n・誰が相談したかは、会社にはわかりません\n・予約は、下のQRコードから自分でできます\n\n「こんなことで相談していいのかな」と思うくらいのことで大丈夫です。"),
 ("管理職の、最初の1on1", "管理職になったばかりの人が、部下との最初の面談で使う言い方と質問", "10分",
  "【この時間の目的の伝え方】\n・「評価の時間ではなくて、困っていることを一緒に片づける時間にしたいと思っています」\n・「私もこの役割は初めてなので、どうしたら働きやすいか教えてほしいです」\n\n【話しやすくなる質問】\n・最近の仕事で、うまくいったことは何ですか\n・やりにくいと感じていることはありますか\n・私にしてほしいこと、やめてほしいことはありますか"),
 ("やさしい日本語への言い換え", "健康診断のお知らせを、外国籍の社員にも伝わる形に", "5分",
  "【元の文】\n定期健康診断を下記の日程で実施いたしますので、対象者は所定の問診票に記入の上、当日持参してください。\n\n【やさしい日本語】\nけんこうしんだん（体のチェック）があります。\n・日：12月3日（水）\n・時間：9時から\n・場所：2階の会議室\n・持って来るもの：問診票（紙に書いて持って来てください）"),
]
def sample_card(t, lead, mins, body):
    return (f'<div class="sample"><div class="top"><b>{t}</b><small>{lead}</small><small>一緒に作る時間の目安：{mins}</small></div>'
            f'<pre>{_h.escape(body)}</pre><a class="more" href="mihon.html">全文を見る →</a></div>')

def block_ai(cls="", full=True):
    ways = f'''<div class="aiways">
<div class="card aiway"><div class="ico">{I("device-desktop",28)}</div><h3>画面を見ながら、一緒に作る</h3><p>社内の案内、求人票、面談の準備、研修の資料。人事の方と画面を共有し、AIに質問しながら下書きを作ります。</p><span class="tagline">月2回の相談の中で</span></div>
<div class="card aiway"><div class="ico">{I("school",28)}</div><h3>AIの使い方を、仕事に合わせて伝える</h3><p>「何から始めればいいか分からない」ところから伺います。御社の仕事に合わせた指示書（AIに渡す文章）一式をお渡しし、ご自身で使えるようにします。</p><span class="tagline">月2回の相談の中で</span></div>
<div class="card aiway"><div class="ico">{I("presentation",28)}</div><h3>スライド・動画・Webページの制作</h3><p>研修のスライド、社内向けの説明動画、採用や案内のWebページを、AIを使って制作します。</p><span class="tagline">別途お見積もり</span></div>
</div>'''
    samples = ('<h3 style="margin-top:44px">AIで作った見本</h3><p class="small">架空の会社（食品の製造・35名）で作りました。実際には、御社の情報で作ります。</p>'
               f'<div class="samples">{"".join(sample_card(*s) for s in SAMPLES)}</div>'
               f'<p style="margin-top:18px"><a class="textlink" href="mihon.html">見本をすべて見る（8つ）→</a></p>') if full else \
              '<p style="margin-top:22px"><a class="textlink" href="mihon.html">AIで作った見本を見る →</a></p>'
    proof = f'<div class="proof">{I("sparkles",26)}<span>このサイト、紹介動画（ナレーションは担当者本人の声）、診断や試算の道具も、担当者がAIを使って作りました。</span></div>'
    return sec(head2("AIでできること", "AIが苦手でも大丈夫。<br><span class=\"mk\">一緒に作り、使えるように</span>します",
                     "一人で人事を担っていると、AIを使えば楽になると聞いても、何から始めればいいか分かりにくいものです。担当者は、キャリアコンサルタントとして相談を受けるだけでなく、AIで資料や道具を作ることも仕事にしています。")
               + ways + proof + samples, cls, "ai")

def block_price(form, cls="alt", detail=""):
    return sec(head2("料金", "料金は、この2つだけです", "金額は税別です。初期費用はかかりません。") +
f'''<div class="price">
<div class="pbox main"><p class="k">月額基本料（従業員100名まで一律）</p><p class="v">15,000<small>円</small></p>
<ul><li>窓口担当の方（人事・総務など、導入時に決めた方）の相談。チャットはいつでも、面談は月2回・各30分</li><li>社員向けの案内チラシ・案内文・予約ページ</li><li>社員の声を会社に届ける仕組みと、月の件数の報告</li></ul></div>
<div class="pbox"><p class="k">社員の相談　1回30分</p><p class="v">5,000<small>円</small></p>
<ul><li>使った分だけ。社員一人あたり月2回まで</li><li>会社ごとに、月の上限の件数を決められます</li><li>オンライン（Zoomなど）で行います</li></ul></div></div>
<div class="terms"><span>{I("calendar-check",18)}最初の3か月は、いつでも解約できます</span><span>{I("file-certificate",18)}守秘の取り決めを契約書に明記</span><span>{I("tag",18)}先着3社は、この価格を継続中ずっと据え置き</span></div>
{detail}
<div class="ctarow" style="margin-top:28px"><a class="btn" href="{form}">{CTA_TXT}</a><a class="textlink" href="mitsumori.html">{I("calculator",18)}御社の場合の費用を試算する</a></div>{calm()}''', cls, "price")

PRICE_DETAIL = '''<details class="more-box"><summary>料金と契約の詳細を見る</summary><div class="in"><div class="tb"><table>
<tr><th>月額基本料</th><td>15,000円（従業員100名まで一律）</td></tr>
<tr><th>基本料に含むもの</th><td>社員専用の予約ページ、社員向けの案内ページと配布用チラシ、会社へ声を届ける仕組み、窓口担当の方の相談（チャットはいつでも、面談は月2回・各30分。運用の確認もこの中で行います）、求人票や自社サイトでの表記</td></tr>
<tr><th>社員の相談</th><td>1回30分 5,000円。使った分だけ。どなたが使っても同額です</td></tr>
<tr><th>窓口担当の方の相談</th><td>チャットはいつでも（平日は原則、翌営業日までに返信）。面談は月2回（各30分）まで基本料に含みます。超えた分は1回30分5,000円です</td></tr>
<tr><th>研修や制度への組み込み</th><td>1回30分5,000円。対象者と回数を先に決めて、予約枠をまとめて確保します</td></tr>
<tr><th>利用の上限</th><td>社員一人あたり月2回まで。会社ごとに、月の上限の件数を決められます</td></tr>
<tr><th>契約</th><td>12か月の自動更新。最初の3か月はいつでも解約できます</td></tr>
<tr><th>いまの価格</th><td>月額15,000円は、先着3社までの価格です。この価格で契約した会社は、継続しているあいだ、更新後も据え置きます</td></tr>
<tr><th>紹介の特典</th><td>紹介で新しい契約が決まると、紹介した会社と紹介された会社の両方の基本料を1か月分無料にします。年払いの会社には、代わりに相談3回分を無料にします</td></tr>
<tr><th>担当者が不在のとき</th><td>病気や事故などで1か月を通じて実施できなかった場合、その月の基本料はいただきません。2か月以上続けて実施できない場合、会社はいつでも解約できます</td></tr>
</table></div></div></details>'''

CAREER = [("building-community", "<b>ハローワークで4年間、職業相談を担当</b>。年2,000件以上の相談を受けてきました。"),
          ("target-arrow", "<b>ビジネスコーチング</b>。大人の学び直し、個人で事業をする方の相談、目標づくりとやる気の立て直しを支えています。"),
          ("ball-basketball", "<b>バスケットボールの指導 10年以上</b>。小学生を中心に、一人ひとりの特性とやる気に合わせて指導しています。"),
          ("school", "<b>オンラインのフリースクール</b>で、不登校の子どもと家族の相談、運営の相談を受けています。"),
          ("world", "<b>JICAボランティア</b>として、大学卒業後に南アフリカで2年間、現地の農業省で農村の発展に取り組みました。")]

def block_me(cls="", full=True):
    car = "".join(f'<li>{I(i,20)}<span>{t}</span></li>' for i, t in CAREER)
    extra = (f'<div class="minivid">{vid("aisatsu.mp4", "竹村正太のごあいさつ")}</div><p class="small" style="margin-top:8px">ごあいさつの動画（43秒・字幕あり）</p>'
             f'<p style="margin-top:14px"><a class="textlink" href="unei.html">運営者情報を見る →</a></p>') if full else \
            '<p><a class="textlink" href="index.html#me">担当者のくわしい紹介を見る →</a></p>'
    return sec(f'''<div class="me"><img src="takemura.jpg" alt="担当の竹村正太の写真" width="300" height="330">
<div><p class="eyebrow">担当者</p><h3 class="nm">竹村 正太<span class="kana">たけむら しょうた</span></h3><p class="role2">国家資格キャリアコンサルタント</p>
<p>相談する人の話を、<b>否定せずに最後まで聴く</b>ことを大切にしています。個人で活動しているので、ご相談はすべて私が直接お受けします。御社の担当は毎回同じ私です（ほかの会社も担当しています）。</p>
<ul class="career">{car}</ul>{extra}</div></div>''', cls, "me")

def _faqs():
    src = open("/home/claude/sitebuild/build.py", encoding="utf-8").read()
    out, seen = [], set()
    for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", src):
        if q not in seen:
            seen.add(q); out.append((q, a))
    return out
FAQ = _faqs()

def block_faq(keys=None, cls="alt", all_=False):
    items = FAQ if keys is None else [f for f in FAQ if any(k in f[0] for k in keys)]
    first, rest = (items, []) if not all_ else (items[:6], items[6:])
    body = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in first)
    if rest:
        body += ('<details class="more-box" style="border:0;background:none"><summary style="padding:10px 0">ほかの質問も見る（' + str(len(rest)) + '個）</summary>'
                 + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in rest) + '</details>')
    if keys is not None:
        body += '<p style="margin-top:14px"><a class="textlink" href="index.html#faq">ほかの質問を見る →</a></p>'
    return f'<section class="{cls} faq" id="faq"><div class="wrap narrow">{head2("よくある質問", "よくある質問")}<div style="margin-top:20px">{body}</div></div></section>'

def block_final(form, h="まずは30分、<br>話を聞いてみませんか", p="御社の状況を伺い、合うかどうかを一緒に考えます。合わなければ、正直にそうお伝えします。", second=None, btn=CTA_TXT):
    sb = f'<a class="btn sub" href="{second[1]}">{second[0]}</a>' if second else ""
    return sec(f'''<div class="final"><div><h2>{h}</h2><p>{p}</p>{calm(("売り込みはしません","こちらから営業の電話はしません","お返事は翌営業日までに"))}</div>
<div class="btns"><a class="btn" href="{form}">{btn}</a>{sb}</div></div>''', "", "contact")

ROLES = [("keieisha.html", "経営者の方へ", "辞める前に、本音を知る", "社員の声を、名前を出さずに受け取れます。経営者ご自身の壁打ち相手にも。"),
         ("jinji.html", "人事・総務の方へ", "社員の相談を、一人で抱えない", "チャットでいつでも相談できます。研修や案内づくりも、AIを使って一緒に。"),
         ("kanrishoku.html", "管理職の方へ", "部下の相談に、迷ったら", "部下との面談の前に、考えを整理できます。ご自身のキャリアの相談にも。"),
         ("saiyo.html", "採用担当の方へ", "求人票に書ける制度に", "「入社後も社外の専門家に相談できる」を、応募する人への安心材料に。"),
         ("hataraku.html", "会社で働く方へ", "会社にこの制度を", "自己負担なしでコーチングを受けたい方へ。会社への伝え方を用意しています。")]

def block_roles(cur="", cls="alt"):
    rs = [r for r in ROLES if r[0] != cur][:4]
    cards = "".join(f'<a class="role" href="{f}"><span class="who">{w}</span><h3>{h}</h3><p>{p}</p><span class="go">くわしく見る →</span></a>' for f, w, h, p in rs)
    return sec(head2("立場ごとの使い方", "あなたの立場で、<br>使い方を見る" if not cur else "ほかの立場の方へ") + f'<div class="roles">{cards}</div>', cls, "roles")

def block_trust():
    return f'''<div class="trust"><div class="wrap"><ul>
<li>{I("certificate",30)}<span><b>国家資格</b>キャリアコンサルタント</span></li>
<li>{I("briefcase",30)}<span><b>職業相談 年2,000件以上</b>ハローワークで4年間</span></li>
<li>{I("user-check",30)}<span><b>毎回同じ担当者</b>個人で、すべて直接お受けします</span></li>
<li>{I("receipt",30)}<span><b>料金をすべて公開</b>月額15,000円から</span></li>
</ul></div></div>'''

def block_diagram(cls=""):
    return sec(head2("このサービスでできること", "社員と、相談を受ける人。<br><span class=\"mk\">同じ一人</span>が両方を支えます",
                     "社内の人には話しにくいことも、利害のない社外の相手になら話せます。御社の事情を知る同じ担当者が、社員の話も、相談を受ける人の話も聴きます。") +
f'''<div class="diagram">
<div class="side"><p class="who">{I("users",18)}社員の方には</p><h3>社外で、安心して話せる場所</h3>
<p>社内の人には言いにくいことを、会社の外の相手に話せます。予約は会社を通さず、オンラインで30分です。</p>
<ul><li>{I("check",16)}<span>仕事の進め方や、職場の人間関係の悩み</span></li><li>{I("check",16)}<span>異動・昇進・転職など、これからのキャリア</span></li><li>{I("check",16)}<span>困りごとがなくても、目標づくりやコーチングに</span></li></ul></div>
<div class="hub"><img src="takemura.jpg" alt=""><div><b>担当 竹村</b><small>毎回同じ担当者が<br>両方の話を聴きます</small></div></div>
<div class="side"><p class="who">{I("briefcase",18)}人事・管理職の方には</p><h3>相談を受ける側を、支える場所</h3>
<p>社員や部下の相談を受けて迷ったとき、考えを整理する相手になります。チャットでいつでも相談でき、月2回・各30分の面談も基本料に含みます。</p>
<ul><li>{I("check",16)}<span>部下への伝え方や、面談の準備</span></li><li>{I("check",16)}<span>研修や社内の取り組みの壁打ち</span></li><li>{I("check",16)}<span>ご自身のキャリアや、仕事の悩み</span></li></ul></div>
</div>''', cls, "service")

def block_worry(title, items, cls="alt"):
    cards = "".join(f'<div class="card"><div class="ico">{I(ic,28)}</div><h3>{h}</h3><p>{p}</p></div>' for ic, h, p in items)
    return sec(head2("こんなことはありませんか", title) + f'<div class="cards">{cards}</div>', cls)

# ---------------------------------------------------------------- トップページ
def top_page(head_html, form):
    hero = f'''<section class="hero"><div class="wrap">
<div>
<p class="for">{I("building",30)}<span>社員の相談窓口を、<span class="nw">社外に持ちたい会社の方へ</span></span></p>
<h1>社員の本音を、<br><span class="nw"><span class="mk">辞める前に</span></span><span class="nw">聞ける場所を。</span></h1>
<p class="lead">国家資格キャリアコンサルタントが御社の<b>専属</b>になり、<b>社員の相談</b>と、<b>相談を受ける人事・管理職の相談</b>の両方をお受けします。</p>
<ul class="reasons">
<li><span class="ico">{I("users",22)}</span>社員だけでなく、相談を受ける人事・管理職も支えます</li>
<li><span class="ico">{I("sparkles",22)}</span>社内の資料づくりも、AIを使って一緒に作ります</li>
<li><span class="ico">{I("user-check",22)}</span>職業相談の経験を持つ担当者が、毎回直接お話を伺います</li>
</ul>
<div class="ctarow"><a class="btn" href="{form}">{CTA_TXT}</a><a class="btn ghost" href="#video">{I("player-play",18)}1分の動画で見る</a></div>
<p class="pricenote">料金：<b>月額15,000円</b>＋社員の相談<b>1回30分5,000円</b>（税別）｜最初の3か月はいつでも解約できます</p>
</div>
<div class="person"><img src="takemura.jpg" alt="担当の竹村正太の写真" width="420" height="462">
<div class="bubble">はじめまして、竹村です。<br>どうぞよろしくお願いします！</div>
<div class="namecard"><small>担当</small><b>竹村 正太</b><small>国家資格キャリアコンサルタント</small></div></div>
</div></section>'''
    worry = block_worry("社員の本音は、<span class=\"mk\">辞めるとき</span>に初めて届く", [
        ("door-exit", "辞めると聞いて、<br>初めて理由を知った", "社内の人に言いにくいことほど、退職を決める直前まで表に出てきません。"),
        ("user-question", "相談を受ける人が、<br>一人で抱えている", "人事や管理職が部下の話を受け止めても、その人自身には相談する先がありません。"),
        ("message-off", "窓口はあるのに、<br>使われていない", "社内の窓口は「誰かに知られるかもしれない」と思うと、使いにくいものです。")])
    return (head_html + header("index.html", form) + "<main>" + hero + block_trust() + block_video() + worry + block_diagram()
            + block_ai("alt") + block_flow("") + block_promises("alt") + block_roles("", "")
            + block_price(form, "alt", PRICE_DETAIL) + block_me("") + block_faq(None, "alt", all_=True) + block_final(form) + "</main>" + footer(form))

# ---------------------------------------------------------------- 立場別のページ
AUD = {
 "keieisha.html": dict(
   title="経営者の方へ｜社員の相談窓口と、経営者の壁打ち相手を月15,000円から",
   desc="中小企業の経営者の方へ。社員が社外で話せる相談窓口と、経営者ご自身の壁打ち相手を、月額15,000円から。国家資格キャリアコンサルタントが担当します。",
   for_="経営者の方へ", icon="building",
   h1="社員の本音と、<br><span class=\"nw\">あなた自身の</span><span class=\"nw\">相談相手を。</span>",
   lead="社員が辞めると決めてから、初めて理由を知る。そうなる前に、社員が社外で話せる相手を置けます。経営者ご自身も、利害のない相手に考えを話せます。",
   worry=("経営者がひとりで<span class=\"mk\">抱えていること</span>", [
     ("door-exit", "辞めると決まってから、<br>初めて理由を知る", "社員は、社長に直接言いにくいことを、退職を決めるまで話しません。"),
     ("user-question", "幹部にも家族にも<br>言いにくい悩みがある", "会社の数字や人のことを、立場を気にせず話せる相手がなかなかいません。"),
     ("chart-bar", "社員が何を感じているか、<br>数字では分からない", "離職率や面談の記録だけでは、職場の空気までは見えません。")]),
   can=("経営者の方に<span class=\"mk\">できること</span>", [
     ("mail-forward", "社員の声を、名前を出さずに受け取れる", "社員が会社に伝えたいことだけを、担当者が文面に整えて届けます。誰の声かは伝わらないので、社員も本音を出しやすくなります。"),
     ("messages", "経営者ご自身の壁打ち相手に", "幹部にも家族にも言いにくいことを、社外の相手に話せます。経営者ご自身が窓口担当になれば、チャットでいつでも相談でき、月2回の面談も基本料に含まれます。"),
     ("calendar-check", "小さく始めて、続けるかを決められる", "初期費用はなく、社員の相談の費用は使った分だけです。最初の3か月はいつでも解約できます。")]),
   faq=["専属", "効果", "守秘", "不在", "産業医"]),
 "jinji.html": dict(
   title="人事・総務の方へ｜社員の相談を一人で抱えない。社外の相談窓口と、人事の相談相手",
   desc="一人で人事を担う方、兼務の人事担当の方へ。社員の相談窓口を社外に置き、人事の方ご自身もチャットでいつでも相談できます。研修や資料づくりもAIで一緒に。",
   for_="人事・総務の方へ（一人で人事を担う方にも）", icon="briefcase",
   h1="社員の相談を、<br><span class=\"nw\">一人で抱えなくていい。</span>",
   lead="人事を一人で、あるいはほかの仕事と兼務で担っている方へ。社員の相談窓口を社外に置けます。社員の相談を受けて迷ったときは、あなた自身も担当者に相談できます。",
   worry=("人事の方が<span class=\"mk\">抱えがちなこと</span>", [
     ("user-question", "社員の相談を受けても、<br>自分の相談先がない", "受け止めた話を、社内の誰にも話せないまま抱えてしまいます。"),
     ("clock", "相談窓口を作りたいが、<br>準備の手間をかけられない", "規程づくりや説明会まで手が回りません。"),
     ("sparkles", "AIを使えば楽になると<br>聞くけれど、始められない", "何から手をつければいいか、聞ける相手がいません。")]),
   can=("人事・総務の方に<span class=\"mk\">できること</span>", [
     ("messages", "チャットで、いつでも軽く相談", "「ちょっと聞きたい」は、御社が使っているチャット（Slack、Chatwork、LINE WORKSなど）かメールで送ってください。平日は原則、翌営業日までにお返事します。"),
     ("calendar-event", "月2回、担当の方の面談", "基本料に月2回・各30分の面談を含みます。社員対応の整理、施策の壁打ち、ご自身のキャリアの相談まで、考えを整理する時間に使えます。"),
     ("user-heart", "相談を受ける側の相談", "社員や部下の相談を受けて迷ったときに、どう受け止め、どう返すかを一緒に考えます。"),
     ("sparkles", "研修や資料づくりを、AIで一緒に", "研修の資料、社内の案内、求人票などを、画面を共有しながら一緒に作ります。使い方を覚えたい方には、手を動かしながらお伝えします。"),
     ("report-analytics", "取り組みを、社内で報告できる形に", "3か月ごとに3問だけのアンケートをとり、年に1度のふりかえりとあわせて、社内の報告に使える1枚にまとめます。"),
     ("user", "一人で人事を担う方に", "少人数の会社では、件数の報告を3か月ごとにまとめ、日付は書きません。その分、月2回の面談を担当の方の相談に厚く使います。")]),
   extra="kumikomi",
   cta2=("上司に見せる1枚を開く", "teian.html"),
   faq=["チャット", "研修", "もったいない", "誰が相談したか", "AI"]),
 "saiyo.html": dict(
   title="採用担当の方へ｜求人票に書ける、社外キャリア相談制度",
   desc="採用担当の方へ。「入社後も社外の専門家に相談できる」を求人票に書ける制度に。入社後の節目の面談にも使え、応募する人の安心材料になります。",
   for_="採用担当の方へ", icon="id-badge-2",
   h1="「入社後も相談できる」を、<br><span class=\"nw\">求人票に書ける制度に。</span>",
   lead="「人を大切にする会社です」を、具体的な制度で示せます。入社後の節目に社外の専門家と話せる機会は、応募する人にとっての安心材料になります。",
   worry=("採用で<span class=\"mk\">よくある悩み</span>", [
     ("file-text", "求人票で、ほかの会社との<br>違いを出しにくい", "給与や休日以外に、働きやすさを示す材料が少ない。"),
     ("door-exit", "入社して数か月で<br>辞めてしまう", "入社前の期待と、入社後の実際とのずれを、本人が誰にも話せません。"),
     ("user-question", "面接で「入社後のフォローは」と<br>聞かれても答えにくい", "具体的な仕組みがないと、言葉だけの約束になってしまいます。")]),
   can=("採用担当の方に<span class=\"mk\">できること</span>", [
     ("file-text", "求人票の文例（1）", "「社外の専属キャリアコンサルタント（国家資格）に、会社負担で相談できます。」"),
     ("file-text", "求人票の文例（2）", "「入社後の不安を一人で抱えないよう、社外のキャリアコンサルタントと契約しています。」"),
     ("calendar-event", "入社後の節目の面談に", "入社1か月、3か月、6か月、1年の節目に30分ずつ。辞めたくなりやすい時期に、社外の相手と話す時間をつくります。")]),
   extra="kumikomi",
   faq=["研修", "誰が相談したか", "外国籍"]),
 "kanrishoku.html": dict(
   title="管理職の方へ｜部下の相談を受けるあなたにも、社外の相談先を",
   desc="管理職の方へ。部下の相談を受ける人にも相談先を。面談の準備や振り返りを、社外のキャリアコンサルタントと30分で。話した内容は会社に伝えません。",
   for_="管理職の方へ", icon="users",
   h1="部下の相談を受けるあなたにも、<br><span class=\"nw\">相談先を。</span>",
   lead="部下の相談を受け、育成を任され、自分の仕事もある。その立場で弱音を言える相手は、社内にはなかなかいません。",
   worry=("管理職の方が<span class=\"mk\">抱えがちなこと</span>", [
     ("user-question", "部下の相談に、<br>どう答えればいいか迷う", "正解のない相談ほど、一人で考えると堂々めぐりになります。"),
     ("message-exclamation", "厳しいことを伝える面談が、<br>気が重い", "言い方ひとつで関係がこじれそうで、準備に時間がかかります。"),
     ("mood-sad", "自分の悩みを<br>話せる場がない", "上にも下にも、本音を言いにくい立場です。")]),
   can=("管理職の方に<span class=\"mk\">できること</span>", [
     ("clipboard-text", "面談の前に、30分で整理する", "部下との面談の前に、何を聞き、何を伝え、何を言わないかを一緒に整理します。終わったあとの振り返りにも使えます。"),
     ("ear", "聞き方を、一緒に考える", "キャリア相談とコーチングを仕事にしてきた立場から、部下の話の聞き方をお手伝いします。"),
     ("lock", "話した内容は、会社に伝えない", "あなたが話した内容は、会社に伝えません。ご自身のキャリアや働き方の相談にも使えます。")]),
   extra="kumikomi",
   cta2=("会社に提案する1枚を開く", "teian.html"),
   faq=["誰が相談したか", "研修", "チャット"]),
 "hataraku.html": dict(
   title="会社で働く方へ｜コーチングやキャリア相談を、会社の制度として受ける",
   desc="コーチングやキャリア相談を自己負担なしで受けたい方へ。会社に制度として導入してもらうための、上司に渡せる1枚と、代わりに案内する方法。",
   for_="会社で働く方へ", icon="user",
   h1="コーチングやキャリア相談を、<br><span class=\"nw\">会社の制度として</span><span class=\"nw\">受けませんか。</span>",
   lead="会社がこの制度を導入すると、あなたは自己負担なしで、社外のコーチングとキャリア相談を使えます。会社に取り入れてもらう方法を、2つ用意しています。",
   worry=("こんな<span class=\"mk\">思い</span>はありませんか", [
     ("message-off", "上司には<br>言いにくいことがある", "評価に関わる相手には、迷いや不満を話しにくいものです。"),
     ("route", "これからのキャリアを、<br>誰かと整理したい", "異動、昇進、転職。一人で考えていると、決めきれません。"),
     ("coin", "コーチングに興味はあるが、<br>自費では負担が大きい", "続けたいからこそ、費用が気になります。")]),
   can=("会社に<span class=\"mk\">取り入れてもらう方法</span>", [
     ("file-text", "自分で提案する", "上司や人事に渡せる1枚を用意しています。費用と手間が1枚にまとまっているので、そのまま見せられます。"),
     ("send", "担当者から会社に案内してもらう", "会社名を教えていただければ、担当者から会社に案内します。あなたが誰かは、会社に一切伝えません。"),
     ("lock", "名前の伝わり方は、あなたが選べる", "少人数の職場では、誰が頼んだか推測されることがあります。案内の仕方は、あなたと相談して決めます。")]),
   cta2=("上司に渡す1枚を開く", "teian.html"),
   main=("代わりに会社への案内を頼む", "suisen"),
   faq=["誰が相談したか", "どんな相談", "転職"]),
}

KUMIKOMI = '''<div class="tb" style="margin-top:26px"><table>
<tr><th>新入社員の最初の1年</th><td>入社1か月、3か月、6か月、1年の節目に30分ずつ。辞めたくなりやすい時期に、社外の相手と話す時間をつくります</td></tr>
<tr><th>3年目研修に</th><td>研修の前後に1回ずつ。研修で考えたことを、ご自身のキャリアの言葉に整えます</td></tr>
<tr><th>管理職の最初の半年</th><td>昇格後6か月のあいだ、月に1回。部下との面談の準備や、新しい役割の悩みを相談できます。いちばん孤立しやすい時期を支えます</td></tr>
<tr><th>会社の取り組みに</th><td>評価制度の見直し、異動や配置換え、組織の再編など、会社が進める取り組みに、対象者との面談を付けます</td></tr>
</table></div><p class="small" style="margin-top:12px">料金は通常と同じ1回30分5,000円です。対象者と回数を先に決めて、予約枠をまとめて確保します。助成金の対象になるかどうかは、社会保険労務士にご確認ください。</p>'''

def aud_page(file, head_html, forms):
    a = AUD[file]
    main_label, main_key = a.get("main", (CTA_TXT, "setsumei"))
    form = forms[main_key]
    cta2 = f'<a class="btn ghost" href="{a["cta2"][1]}">{a["cta2"][0]}</a>' if a.get("cta2") else f'<a class="btn ghost" href="#video">{I("player-play",18)}1分の動画で見る</a>'
    hero = f'''<section class="hero"><div class="wrap">
<div><p class="for">{I(a["icon"],30)}<span>{a["for_"]}</span></p><h1>{a["h1"]}</h1><p class="lead">{a["lead"]}</p>
<div class="ctarow"><a class="btn" href="{form}">{main_label}</a>{cta2}</div>
<p class="pricenote">料金：<b>月額15,000円</b>＋社員の相談<b>1回30分5,000円</b>（税別）｜最初の3か月はいつでも解約できます</p></div>
<div class="person"><img src="takemura.jpg" alt="担当の竹村正太の写真" width="420" height="462">
<div class="bubble">はじめまして、竹村です。<br>どうぞよろしくお願いします！</div>
<div class="namecard"><small>担当</small><b>竹村 正太</b><small>国家資格キャリアコンサルタント</small></div></div>
</div></section>'''
    wt, wi = a["worry"]
    ct, ci = a["can"]
    n = len(ci)
    cards = "".join(f'<div class="card"><div class="ico">{I(ic,28)}</div><h3>{h}</h3><p>{p}</p></div>' for ic, h, p in ci)
    can = sec(head2("この立場の方に", ct) + f'<div class="cards{" c2" if n == 4 else ""}">{cards}</div>'
              + (('<h3 style="margin-top:44px">会社の研修や制度に組み込む</h3><p class="small">相談は、待っているだけでは使われにくいものです。会社の取り組みの一部として面談を組み込むと、節目ごとに確実に話す機会ができます。</p>' + KUMIKOMI) if a.get("extra") == "kumikomi" else ""), "", "service")
    second = a.get("cta2")
    stick = ("代わりに案内を頼む", "会社への<br>案内を依頼") if main_key == "suisen" else ("まずは話を聞いてみる", "オンライン<br>30分・無料")
    return (head_html + header(file, form) + "<main>" + hero + block_trust() + block_worry(wt, wi) + can + block_video()
            + block_flow("alt") + block_promises("") + block_ai("alt", full=False) + block_price(forms["setsumei"], "", "")
            + block_me("alt", full=False) + block_faq(a["faq"], "") + block_roles(file, "alt")
            + block_final(form, second=second) + "</main>" + footer(form, *stick))

# ---------------------------------------------------------------- お悩み別・業種別のページ
NAYAMI_ICON = ["alert-circle", "bulb", "route"]
def nayami_page2(n, head_html, form):
    cards = "".join(f'<div class="card"><div class="ico">{I(NAYAMI_ICON[i % 3],28)}</div><h3>{h}</h3><p>{t}</p></div>' for i, (h, t) in enumerate(n["secs"]))
    tag = n.get("tag", "お悩みから探す")
    hero = f'''<section class="hero"><div class="wrap one">
<p class="tag">{tag}｜{n["nav"]}</p><h1>{n["h1"]}</h1><p class="lead">{n["lead"]}</p>
<div class="ctarow"><a class="btn" href="{form}">{CTA_TXT}</a><a class="btn ghost" href="{n["to"]}">{n["tolabel"]}の案内を見る</a></div>
<p class="pricenote">料金：<b>月額15,000円</b>＋社員の相談<b>1回30分5,000円</b>（税別）｜最初の3か月はいつでも解約できます</p>
</div></section>'''
    body = sec(f'<div class="cards">{cards}</div>', "", "service")
    return (head_html + header("", form) + "<main>" + hero + block_trust() + body + block_video() + block_diagram("alt")
            + block_flow("") + block_promises("alt") + block_price(form, "", "")
            + block_me("alt", full=False) + block_roles("", "") + block_final(form, second=("3分診断を試す", "shindan.html")) + "</main>" + footer(form))

# ---------------------------------------------------------------- AIで作った見本のページ
MIHON_CAT = {"01": "社員向け", "03": "社員向け", "08": "社員向け", "02": "採用", "10": "管理職", "09": "管理職", "07": "人事の仕事", "05": "人事の仕事"}
MIHON_EXTRA_CSS = """
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.chips button{font:inherit;font-size:14px;font-weight:700;border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 16px;cursor:pointer;color:var(--ink);min-height:40px}
.chips button.on{background:var(--main);border-color:var(--main);color:#fff}
.docs{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:22px}
.doc{background:#fff;border-radius:10px;box-shadow:0 10px 30px rgba(20,40,60,.10);display:flex;flex-direction:column;overflow:hidden}
.doc .dh{padding:18px 22px 14px;border-bottom:1px solid var(--line)}
.doc .cat{display:inline-block;font-size:12px;font-weight:700;color:var(--main);background:var(--main-soft);border-radius:6px;padding:1px 8px}
.doc h3{font-size:19px;margin:8px 0 4px}
.doc .dh p{font-size:14px;color:var(--sub);margin:0;line-height:1.7}
.doc .meta{display:flex;gap:14px;font-size:13px;color:var(--sub);margin-top:6px}
.doc .meta span{display:inline-flex;align-items:center;gap:4px}
.doc pre{margin:0;padding:18px 22px;font-family:var(--fb);font-size:14.5px;line-height:1.85;white-space:pre-wrap;max-height:250px;overflow:hidden;position:relative;flex:1}
.doc pre::after{content:"";position:absolute;left:0;right:0;bottom:0;height:80px;background:linear-gradient(transparent,#fff)}
.doc.open pre{max-height:none}.doc.open pre::after{display:none}
.doc .tg{font:inherit;font-size:14px;font-weight:700;color:var(--main);background:none;border:0;border-top:1px solid var(--line);padding:14px 22px;text-align:left;cursor:pointer}
.made{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:28px}
.made .card .vid{margin-top:14px}
.safe3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}
@media (max-width:860px){.docs,.made,.safe3{grid-template-columns:1fr}}
"""

def mihon_page(items, head_html, form):
    def doc(t, tool, mins, lead, body):
        no = tool.split("_", 1)[0]; cat = MIHON_CAT.get(no, "人事の仕事")
        return (f'<article class="doc" data-cat="{cat}"><div class="dh"><span class="cat">{cat}</span><h3>{t}</h3><p>{lead}</p>'
                f'<p class="meta"><span>{I("clock",14)}一緒に作る時間の目安：{mins}</span><span>{I("file-text",14)}指示書{no}番</span></p></div>'
                f'<pre>{_h.escape(body)}</pre><button class="tg" type="button">全文を読む ＋</button></article>')
    cats = ["すべて", "社員向け", "採用", "管理職", "人事の仕事"]
    chips = "".join(f'<button type="button"{" class=on" if i == 0 else ""} data-c="{c}">{c}</button>' for i, c in enumerate(cats))
    hero = f'''<section class="hero"><div class="wrap one">
<p class="for">{I("sparkles",30)}<span>人事・総務の方へ｜AIで作れるもの</span></p>
<h1>社内の文書づくりを、<br><span class="nw"><span class="mk">画面を見ながら</span></span><span class="nw">一緒に。</span></h1>
<p class="lead">AIが苦手でも大丈夫です。担当者（竹村）と人事の方が画面を共有し、人事の方は質問に答えるだけで、下書きができあがります。下は、架空の会社（食品の製造・35名）で、実際にAIを使って作った見本です。</p>
<div class="ctarow"><a class="btn" href="{form}">{CTA_TXT}</a><a class="btn ghost" href="#docs">見本を読む</a></div>
</div></section>'''
    steps = sec(head2("進め方", "作り方を覚えて、<br><span class=\"mk\">ご自身で使える</span>ようにします") + f'''
<ol class="steps" style="max-width:760px">
<li><span class="who">担当者と人事の方</span><b>一緒に作る</b><span>月2回の面談の中で画面を共有し、担当者がAIに指示を出します。人事の方は、AIや担当者の質問に答えるだけです。</span></li>
<li><span class="who">人事の方</span><b>使い方を覚える</b><span>次は、人事の方ご自身の手で動かしてみます。分からないことは、チャットでいつでも聞けます。</span></li>
<li><span class="who">人事の方</span><b>自分で回す</b><span>担当者が御社用に整えた「指示書」（AIに渡す文章）一式をお渡しします。次からは、AIに貼るだけで作れます。</span></li>
</ol>''', "", "flow")
    docs = sec(head2("見本", "架空の会社で作った、<br>8つの見本", "実際には、御社の情報で作ります。") + f'<div class="chips" role="group" aria-label="種類で絞り込む">{chips}</div><div class="docs">{"".join(doc(*x) for x in items)}</div>', "alt", "docs")
    made = sec(head2("制作もできます", "スライド・動画・Webページも、<br>AIを使って作ります", "研修のスライド、社内向けの説明動画、採用や案内のWebページなど。制作をまるごとご依頼いただく場合は、事前にお見積もりします。") + f'''
<div class="made">
<div class="card"><div class="ico">{I("movie",28)}</div><h3>説明動画（実例：このサービスの紹介動画）</h3><p>スライドと字幕を作り、ナレーションは担当者本人の声で入れました。社内の制度の説明や、新入社員向けの案内に使えます。</p>{vid("shokai.mp4", "サービス紹介（AIで制作）")}</div>
<div class="card"><div class="ico">{I("world-www",28)}</div><h3>Webページ（実例：このサイト）</h3><p>このサイトの全ページ、診断や費用の試算の道具も、AIを使って作りました。採用ページや、社員向けの案内ページを作れます。</p>
<p style="margin-top:12px"><a class="textlink" href="shindan.html">3分診断を試す →</a><br><a class="textlink" href="mitsumori.html">費用の試算を試す →</a><br><a class="textlink" href="annai.html">案内チラシを作ってみる →</a></p></div>
</div>''', "", "made")
    safe = sec(head2("安心して使うために", "AIを使うときの、3つの決まり") + f'''<div class="safe3">
<div class="card"><div class="ico">{I("user-off",28)}</div><h3>個人の情報は入れない</h3><p>社員の名前や、個人が分かる情報は、AIに入力しません。</p></div>
<div class="card"><div class="ico">{I("eye-check",28)}</div><h3>必ず人が確かめる</h3><p>AIの下書きは、人事の方と担当者が読んで確かめてから使います。</p></div>
<div class="card"><div class="ico">{I("scale",28)}</div><h3>法律や手続きは専門家へ</h3><p>就業規則や手続きに関わる内容は、社会保険労務士などの専門家に確認します。</p></div>
</div>''', "alt")
    js = '''<script>{const bs=document.querySelectorAll('.chips button'),ds=document.querySelectorAll('.doc');
bs.forEach(b=>b.addEventListener('click',()=>{bs.forEach(x=>x.classList.toggle('on',x===b));const c=b.dataset.c;ds.forEach(d=>{d.style.display=(c==='すべて'||d.dataset.cat===c)?'':'none'})}));
document.querySelectorAll('.doc .tg').forEach(t=>t.addEventListener('click',()=>{const d=t.closest('.doc');d.classList.toggle('open');t.textContent=d.classList.contains('open')?'閉じる −':'全文を読む ＋'}));}</script>'''
    head_html = head_html.replace("</head>", f"<style>{MIHON_EXTRA_CSS}</style></head>")
    return (head_html + header("mihon.html", form) + "<main>" + hero + steps + docs + made + safe
            + block_price(form, "", "") + block_final(form, h="御社の文書も、<br>一緒に作ってみませんか", p="30分の説明の中で、御社で作りたいものを伺います。その場で、AIで下書きを作ってお見せすることもできます。") + "</main>" + js + footer(form))

# ---------------------------------------------------------------- 社会保険労務士の方へ
def sharoushi_page(head_html, form):
    hero = f'''<section class="hero"><div class="wrap">
<div><p class="for">{I("scale",30)}<span>社会保険労務士の先生へ</span></p>
<h1>顧問先の社員の面談を、<br><span class="nw">お手伝いします。</span></h1>
<p class="lead">手続きと制度づくりは、先生に。社員一人ひとりとの面談は、社外のキャリアコンサルタント（竹村）に。先生のご紹介で、顧問先に「社外の相談窓口」を用意できます。</p>
<div class="ctarow"><a class="btn" href="{form}">まずは話を聞いてみる（15分・無料）</a><a class="btn ghost" href="#bunten">分担のかたちを見る</a></div>
<p class="pricenote">紹介料のやりとりはありません。ご紹介いただいた顧問先は、基本料が1か月分無料になります。</p></div>
<div class="person"><img src="takemura.jpg" alt="担当の竹村正太の写真" width="420" height="462"><div class="bubble">はじめまして、竹村です。<br>どうぞよろしくお願いします！</div>
<div class="namecard"><small>担当</small><b>竹村 正太</b><small>国家資格キャリアコンサルタント</small></div></div>
</div></section>'''
    worry = block_worry("顧問先から、<span class=\"mk\">こんな相談</span>はありませんか", [
        ("door-exit", "「若手がすぐ辞める」と<br>相談される", "制度は整えても、社員一人ひとりの話を聞く時間までは取れません。"),
        ("user-search", "キャリア面談の<br>担い手を探している", "キャリアコンサルティングを取り入れたい顧問先に、紹介できる相手がいない。"),
        ("alert-triangle", "不満が、労務の問題に<br>なる前に拾いたい", "揉めてからではなく、その前に声を拾える仕組みを勧めたい。")])
    bunten = sec(head2("分担のかたち", "それぞれの専門で、<br><span class=\"mk\">役割を分けます</span>") + f'''
<div class="cards">
<div class="card"><div class="ico">{I("scale",28)}</div><h3>社会保険労務士の先生</h3><p>就業規則、制度づくり、手続き、助成金の申請。これまでどおりです。</p></div>
<div class="card"><div class="ico">{I("building",28)}</div><h3>顧問先の会社</h3><p>人事・総務の方が、社員に案内チラシを配るだけ。説明会や社内の準備は要りません。</p></div>
<div class="card"><div class="ico">{I("messages",28)}</div><h3>担当者（竹村）</h3><p>社員との面談（オンライン・1回30分）、窓口担当の方の相談、社員本人が承認した声を名前を出さずに会社へ届けること。</p></div>
</div>
<p class="limits" style="margin-top:20px">面談の中で労務や制度の課題が見えたときは、社員本人の同意の範囲で顧問先に伝え、手続きや制度のことは先生に相談するよう顧問先に案内します。担当者が労務の相談や手続きを扱うことはありません。</p>''', "", "bunten")
    merit = sec(head2("先生にとっての利点", "顧問先への提案が、<br>ひとつ増えます") + f'''<div class="cards">
<div class="card"><div class="ico">{I("briefcase",28)}</div><h3>顧問サービスに厚みが出る</h3><p>「社外の相談窓口も紹介できる」ことを、先生の提案の一つにしていただけます。</p></div>
<div class="card"><div class="ico">{I("bell",28)}</div><h3>問題の芽に早く気づける</h3><p>辞める前、揉める前の社員の声が、名前を出さずに会社へ届きます。顧問先が制度を見直すきっかけになります。</p></div>
<div class="card"><div class="ico">{I("clock",28)}</div><h3>先生の手間は増えない</h3><p>契約と運営は、顧問先と担当者が直接行います。先生に事務の負担はかかりません。</p></div>
</div>''', "alt")
    flow = sec(head2("ご紹介の流れ", "ご紹介から、<br>顧問先で相談が始まるまで") + f'''
<ol class="steps" style="max-width:760px">
<li><span class="who">先生</span><b>顧問先に、このサービスを紹介する</b><span>このサイトのURLか、担当者が用意する案内資料をお渡しください。</span></li>
<li><span class="who">顧問先と担当者</span><b>30分のオンライン説明</b><span>顧問先の状況を伺い、合うかどうかを一緒に考えます。売り込みはしません。</span></li>
<li><span class="who">顧問先と担当者</span><b>契約</b><span>申込フォームと電子契約で、顧問先と担当者が直接契約します。</span></li>
<li><span class="who">顧問先の人事・総務の方</span><b>社員に案内チラシを配る</b><span>社員の方が自分で予約し、相談が始まります。</span></li>
</ol>''', "", "flow")
    price = sec(head2("料金（顧問先のご負担）", "料金は、この2つだけです") + '''<div class="tb" style="margin-top:22px"><table>
<tr><th>月額基本料</th><td>15,000円（税別。先着3社の価格。窓口担当の方の相談 月2回を含む）</td></tr><tr><th>社員の相談</th><td>1回30分 5,000円（税別）。使った分だけ</td></tr>
<tr><th>契約</th><td>12か月の自動更新。最初の3か月はいつでも解約できます</td></tr>
<tr><th>ご紹介の場合</th><td>ご紹介いただいた顧問先は、基本料が1か月分無料になります。先生との紹介料のやりとりはありません</td></tr></table></div>''', "alt")
    return (head_html + header("sharoushi.html", form) + "<main>" + hero + block_trust() + worry + bunten + merit + flow + price
            + block_me("", full=False) + block_final(form, h="まずは15分、<br>話を聞いてみませんか", p="顧問先の様子や、先生のお考えを伺います。提携のかたちも、ご相談しながら決めます。", btn="まずは話を聞いてみる（15分・無料）") + "</main>" + footer(form))

# ---------------------------------------------------------------- お悩み別ページの中身（数字・今日からできること・質問）
MHLW = "厚生労働省「新規学卒就職者の離職状況（2023年3月卒業者）」2026年10月"
HONNE = "働きがいのある会社研究所「退職にまつわる本音調査」2026年9月"
NX = {
 "wakate-rishoku.html": dict(
   stats=[("31.2%", "大学を卒業して就職した人のうち、3年以内に辞めた人", MHLW),
          ("50.6%", "同じく、従業員5〜29人の事業所に就職した人では", MHLW),
          ("70.9%", "20〜30代の転職者のうち、本当の退職理由を会社に「すべては伝えていない」人", HONNE)],
   today=[("評価と切り離した面談の時間をとる", "入社1か月、3か月、6か月の節目に、仕事の評価とは関係のない話をする時間を、会社が先に決めておきます。"),
          ("「辞めたくなった瞬間」も聞く", "続けている理由とあわせて、辞めたいと思ったことがあるかを聞きます。責めずに聞くと、改善の手がかりが見つかります。"),
          ("上司以外に話せる相手を決めておく", "先輩、ほかの部署の人、社外の相談先など、上司のほかに話せる相手がいることを、入社のときに伝えます。")],
   faq=[("入社後の面談は、誰が行うのですか。", "担当者（竹村）がオンラインで行います。会社は、対象の社員と時期を決めて、社員に案内するだけです。"),
        ("面談で話した内容は、上司に伝わりますか。", "伝わりません。社員本人が会社に伝えたいと望んだことだけを、名前を出さずに届けます。")]),
 "kanrishoku-hihei.html": dict(
   stats=[("68.0%", "中間管理職のうち、職務の負担が大きいと感じている人", "mento「ミドルマネージャー実態調査2024」"),
          ("24.0%", "中間管理職への支援を「特に行っていない」と答えた人事", "パーソル総合研究所「中間管理職の就業負担に関する定量調査」2019年")],
   today=[("一人で抱えないルールを決める", "部下の相談を受けて迷ったときに、誰に相談してよいかを、管理職の方に先に伝えておきます。"),
          ("面談の前に、3つを書き出す", "「聞くこと」「伝えること」「言わないこと」を書き出してから面談に臨むと、話がぶれにくくなります。"),
          ("管理職同士で話す場をつくる", "月に1回、管理職同士で困りごとを話す時間をとります。同じ立場の人と話すだけでも、負担は軽くなります。")],
   faq=[("管理職の相談にも、料金がかかりますか。", "窓口担当として決めた方は、月2回の面談まで基本料に含まれます。それ以外の管理職の方は、社員と同じ1回30分5,000円です。"),
        ("部下の相談を、そのまま担当者に任せてもいいですか。", "はい。社員の方が自分で予約すれば、担当者が直接お話を伺います。管理職の方が一人で受け止める量を減らせます。")]),
 "keieisha-sodan.html": dict(
   stats=[("85.0%", "従業員2〜100名の中小企業の経営者・幹部のうち、社外の相談相手が「十分にいない」人", "ラクスル「中小企業の経営課題に関する実態調査」"),
          ("68.8%<small> / </small>17.9%", "取り組みの成果が期待どおり以上だった割合（社外の相談相手が十分にいる層／全くいない層）", "同上")],
   today=[("決める前に、言葉にする時間をとる", "週に一度、迷っていることを書き出す時間をとります。言葉にすると、何に迷っているのかが見えてきます。"),
          ("相談先を、分野ごとに持つ", "お金は税理士、法律は弁護士や社会保険労務士、人と組織とご自身のことはキャリアコンサルタントやコーチ、と分けておきます。"),
          ("社員の声を聞く道を、社長以外にもつくる", "社長に直接は言いにくい声もあります。社外の窓口など、別の道を用意しておきます。")],
   faq=[("資金繰りなど、経営の相談もできますか。", "人と組織のこと、ご自身の働き方や考えの整理が中心です。資金や法律に関わることは、適切な専門家をご案内します。"),
        ("経営者が相談に使うと、社員の相談の枠は減りますか。", "減りません。経営者ご自身が窓口担当になれば、月2回の面談を使えます。社員の相談は、それとは別に1回ごとの料金です。")]),
 "sodan-kawaranai.html": dict(
   stats=[("54.3%", "職場のストレスを相談したくない人のうち、理由が「相談しても解決しないと思うから」の人", "メンタルヘルステクノロジーズ「職場のストレスに関する調査」2024年"),
          ("41.5%", "本当の退職理由を伝えなかった人のうち、理由が「本音を伝えても改善されないと思ったから」の人", HONNE)],
   today=[("相談の件数と、会社がしたことを知らせる", "窓口に何件の相談があり、受けて会社が何をしたかを、社内に知らせます。「話せば変わる」が見えると、相談は増えます。"),
          ("「誰が、どこまで知るか」を案内に書く", "相談した内容を誰が知るのかを、窓口の案内にはっきり書きます。分からないと、人は相談しません。"),
          ("すぐ対応できない声にも、返事をする", "「やる・やらない・保留」と、その理由を返します。見送る場合も、そう伝えることが信頼につながります。")],
   faq=[("社員の声を受け取ったあと、会社は何をすればいいですか。", "対応を決めるのは会社です。担当者は、次の面談の機会に、会社の受け止めを社員本人へお返しします。どう返すかは、月2回の面談で一緒に整理できます。")]),
 "stress-check-junbi.html": dict(
   stats=[("2025年5月", "改正労働安全衛生法が公布され、労働者50人未満の事業場にもストレスチェックが義務化", "厚生労働省"),
          ("3年以内", "施行の時期は「公布後3年以内に政令で定める日」", "厚生労働省"),
          ("2026年2月", "厚生労働省が「小規模事業場ストレスチェック制度実施マニュアル」を公表", "厚生労働省「こころの耳」")],
   today=[("厚生労働省のマニュアルを読む", "小規模事業場向けの実施マニュアルと概要版が「こころの耳」で公開されています。まず概要版で全体をつかみます。"),
          ("実施をどこに頼むかを考える", "ストレスチェックの実施者は、医師や保健師などです。外部の機関に頼む場合は、早めに探しておきます。"),
          ("ふだんの相談先を、社員に知らせておく", "検査は年に1度です。日々の気がかりを話せる先があることを、社員に伝えておきます。")],
   faq=[("この窓口で、ストレスチェックを実施できますか。", "できません。担当者はストレスチェックの実施者ではなく、医療機関でもありません。仕事とキャリアの相談を、ふだんから受ける役割です。"),
        ("いつから義務になりますか。", "施行の時期は「公布（2025年5月）後3年以内に政令で定める日」とされています。最新の情報は、厚生労働省の案内をご確認ください。")]),
 "coaching-kaisha-futan.html": dict(
   stats=[],
   today=[("会社にとっての利点を、一言で言う", "「社員が前向きに働き続けられる」「採用で打ち出せる」など、会社の得になる点から話します。"),
          ("試しやすさを伝える", "初期費用がなく、相談の費用は使った分だけ、最初の3か月はいつでも解約できることを伝えます。"),
          ("1枚の資料を見せる", "上司や人事に渡せる1枚を用意しています。口で説明するより、そのまま見せる方が伝わります。")],
   faq=[("自分が頼んだことは、会社に分かりますか。", "担当者から会社に案内する場合、あなたのお名前は一切伝えません。少人数の職場では推測されることがあるため、伝え方はあなたと相談して決めます。")]),
 "kaigo-fukushi.html": dict(
   stats=[("39.1%", "医療・福祉の仕事に就いた大学卒業者のうち、3年以内に辞めた人", MHLW),
          ("49.4%", "同じく、高校卒業者では", MHLW)],
   today=[("シフトの合間に話せる時間をつくる", "10分でも、職員がリーダーに話せる時間をシフトに組み込みます。"),
          ("「受け止める人」の相談先を決める", "利用者の気持ちを受け止める職員が、自分の気持ちを話せる先を決めておきます。"),
          ("小さなすれ違いを、早めに話す", "人間関係のすれ違いは、小さいうちに話す場があると、退職の理由になりにくくなります。")],
   faq=[("シフト勤務でも使えますか。", "使えます。オンラインで30分なので、勤務の前後や休憩時間に予約できます。")]),
 "inshoku-shukuhaku.html": dict(
   stats=[("49.9%", "宿泊業・飲食サービス業に就いた大学卒業者のうち、3年以内に辞めた人（産業別で最も高い）", MHLW),
          ("61.6%", "同じく、高校卒業者では", MHLW)],
   today=[("店長が話を聞く時間を、仕事として決める", "月に1回、スタッフ一人ひとりと10分話す時間を、店長の仕事として予定に入れます。"),
          ("来なくなる前のサインに気づく", "遅刻が増える、シフトの希望が減るなどの変化に気づいたら、責めずに声をかけます。"),
          ("店の外に、話せる先を用意する", "店の人に言いにくいことを話せる先があることを、スタッフに伝えておきます。")],
   faq=[("店舗が複数あっても、基本料は同じですか。", "同じです。従業員100名までは一律で月額15,000円です。")]),
 "it-remote.html": dict(
   stats=[("4割以上", "会社員300人のうち、リモートワークで孤独感を経験した人", "オトバンク「リモートワークの実態調査」2026年4月")],
   today=[("1on1に、雑談の時間を入れる", "進捗の確認だけで終わらせず、最初の5分を雑談にあてます。"),
          ("「困っていること」を聞く質問を決める", "「何か困っていることは？」ではなく、「最近やりにくかった作業は？」のように、答えやすい聞き方をします。"),
          ("チームの外に、話せる相手をつくる", "上司やチームの外に、気軽に話せる相手がいることを伝えます。")],
   faq=[("相談はすべてオンラインですか。", "はい。Zoomなどで行います。いつもの働き方のまま使えます。")]),
 "shien-kikan.html": dict(
   stats=[("42.3%", "教育・学習支援業に就いた大学卒業者のうち、3年以内に辞めた人", MHLW)],
   today=[("ケースを振り返る時間を決める", "月に1回でも、対応に迷ったケースを落ち着いて振り返る時間をとります。"),
          ("一人で抱えない仕組みをつくる", "難しいケースは、必ず誰かと共有するルールを決めます。"),
          ("職員自身の働き方を話す場をつくる", "利用者や生徒の話だけでなく、職員自身のこれからを話す機会をつくります。")],
   faq=[("ケースの相談もできますか。", "月2回の担当者の面談を、対応の振り返りに使えます。個人が分かる情報は伏せてお話しください。")]),
}

NX_CSS = """
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px}
.stat{background:#fff;border-radius:18px;padding:24px;border:1px solid var(--line)}
.stat b{display:block;font-family:var(--fh);font-weight:900;font-size:40px;line-height:1.2;color:var(--main)}
.stat b small{font-size:22px}
.stat p{font-size:16px;margin:8px 0 10px;color:var(--ink);font-weight:700;line-height:1.6}
.stat cite{display:block;font-style:normal;font-size:12px;color:var(--sub);line-height:1.6}
.todo{list-style:none;padding:0;margin:26px 0 0;display:grid;gap:14px;counter-reset:t}
.todo li{background:#fff;border-radius:16px;padding:20px 22px 20px 74px;position:relative;border:1px solid var(--line)}
.todo li::before{counter-increment:t;content:counter(t);position:absolute;left:22px;top:20px;width:36px;height:36px;border-radius:10px;background:var(--marker);font-family:var(--fh);font-weight:900;display:grid;place-items:center}
.todo b{display:block;font-size:18px;font-family:var(--fh)}
.todo span{color:var(--sub);font-size:16px}
@media (max-width:860px){.stats{grid-template-columns:1fr}}
"""

def nayami_page3(n, head_html, form):
    x = NX.get(n["file"], {})
    cards = "".join(f'<div class="card"><div class="ico">{I(NAYAMI_ICON[i % 3],28)}</div><h3>{h}</h3><p>{t}</p></div>' for i, (h, t) in enumerate(n["secs"]))
    tag = n.get("tag", "お悩みから探す")
    hero = f'''<section class="hero"><div class="wrap one">
<p class="tag">{tag}｜{n["nav"]}</p><h1>{n["h1"]}</h1><p class="lead">{n["lead"]}</p>
<div class="ctarow"><a class="btn" href="{form}">{CTA_TXT}</a><a class="btn ghost" href="{n["to"]}">{n["tolabel"]}の案内を見る</a></div>
<p class="pricenote">料金：<b>月額15,000円</b>＋社員の相談<b>1回30分5,000円</b>（税別）｜最初の3か月はいつでも解約できます</p>
</div></section>'''
    stats = ""
    if x.get("stats"):
        tiles = "".join(f'<div class="stat"><b>{v}</b><p>{l}</p><cite>出典：{s}</cite></div>' for v, l, s in x["stats"])
        stats = sec(head2("数字で見る", "調査から分かっていること") + f'<div class="stats">{tiles}</div>', "", "data")
    body = sec(head2("原因と、できること", "なぜ起きるのか、<br>社外の相手に何ができるか") + f'<div class="cards">{cards}</div>', "alt" if stats else "", "service")
    today = ""
    if x.get("today"):
        items = "".join(f'<li><b>{h}</b><span>{t}</span></li>' for h, t in x["today"])
        today = sec(head2("今日からできること", "まずは、<span class=\"mk\">自社でできる3つのこと</span>", "この窓口を使うかどうかに関わらず、取り組めることです。") + f'<ol class="todo" style="max-width:820px">{items}</ol>', "" if stats else "alt")
    faq = ""
    if x.get("faq"):
        faq = ('<section class="alt faq"><div class="wrap narrow">' + head2("よくある質問", "この悩みについての質問") + '<div style="margin-top:20px">'
               + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in x["faq"])
               + '<p style="margin-top:14px"><a class="textlink" href="index.html#faq">ほかの質問を見る →</a></p></div></div></section>')
    head_html = head_html.replace("</head>", f"<style>{NX_CSS}</style></head>")
    return (head_html + header("", form) + "<main>" + hero + block_trust() + stats + body + today + block_video() + block_diagram("alt")
            + block_flow("") + block_promises("alt") + block_price(form, "", "") + faq
            + block_me("", full=False) + block_roles("", "alt") + block_final(form, second=("3分診断を試す", "shindan.html")) + "</main>" + footer(form))
