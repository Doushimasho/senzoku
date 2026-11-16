# -*- coding: utf-8 -*-
"""法人向けサイトの生成スクリプト。python3 build.py <出力フォルダ> で全ページを書き出す。"""
import os, sys, html

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
NAME = "竹村正太"
FORMS = {                   # GoogleフォームやTimeRexのURLが決まったら差し替える
    "setsumei": "#junbi", "shiryo": "teian.html", "kyujin": "#junbi",
    "kit": "teian.html", "suisen": "#junbi",
}

def person(cx, cy, shirt, hair, skin="#ffd9b8"):
    return (f'<g><rect x="{cx-34}" y="{cy+26}" width="68" height="62" rx="26" fill="{shirt}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="28" fill="{skin}"/>'
            f'<path d="M{cx-28} {cy-4} a28 28 0 0 1 56 0 q-28 -22 -56 0z" fill="{hair}"/>'
            f'<circle cx="{cx-9}" cy="{cy+3}" r="3" fill="#3a3a3a"/><circle cx="{cx+9}" cy="{cy+3}" r="3" fill="#3a3a3a"/>'
            f'<path d="M{cx-9} {cy+13} q9 8 18 0" stroke="#3a3a3a" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>')

def hero_svg(c1, c2):
    return (f'<svg viewBox="0 0 420 300" role="img" aria-label="オンラインで話す二人のイラスト">'
            f'<circle cx="360" cy="52" r="34" fill="#ffd34d"/>'
            f'<rect x="20" y="70" width="180" height="170" rx="18" fill="#fff" stroke="#bfe3f2" stroke-width="5"/>'
            f'<rect x="220" y="100" width="180" height="170" rx="18" fill="#fff" stroke="#bfe3f2" stroke-width="5"/>'
            + person(110, 135, c1, "#5b4636") + person(310, 165, c2, "#2f3b52") +
            f'<ellipse cx="205" cy="48" rx="62" ry="30" fill="#fff" stroke="#ffb199" stroke-width="4"/>'
            f'<circle cx="185" cy="48" r="5" fill="#ff8a6b"/><circle cx="205" cy="48" r="5" fill="#ff8a6b"/><circle cx="225" cy="48" r="5" fill="#ff8a6b"/>'
            f'<path d="M30 285 q20 -30 40 0 M70 285 q20 -40 40 0" stroke="#7ccf9b" stroke-width="8" fill="none" stroke-linecap="round"/></svg>')

def koma(n, people, text):
    figs = "".join(person(60 + i * 110, 50, s, h) for i, (s, h) in enumerate(people))
    w = 120 + (len(people) - 1) * 110
    return (f'<div class="koma"><span class="kn">{n}</span>'
            f'<svg viewBox="0 0 {w} 140" style="max-width:{w}px" aria-hidden="true">{figs}</svg>'
            f'<p>{text}</p></div>')

COMIC = ('<div class="comic">'
         + koma(1, [("#8ec9e8", "#5b4636")], "入社して1か月。小さな疑問を、誰に聞けばいいか分からない。")
         + koma(2, [("#ffc56b", "#2f3b52")], "会社から案内が届く。「社外の相談、会社負担で使えます」")
         + koma(3, [("#8ec9e8", "#5b4636"), ("#7ccf9b", "#444")], "オンラインで30分。話すうちに、気がかりが整理されていく。")
         + koma(4, [("#8ec9e8", "#5b4636"), ("#ffc56b", "#2f3b52")], "伝えたいことだけを、匿名で会社へ。会社からの返事も戻ってくる。")
         + '</div><p class="small">使い方のイメージです。</p>')

USAGE = [("入社後フォロー面談", "入社1か月、3か月、6か月の節目に30分ずつ。社外にも話せる相手がいる安心感をつくります。", "新入社員、中途入社の方に"),
         ("辞める前に聞く面談", "退職が決まってからではなく、在職中に先回りして聞きます。", "年に1度、希望者または全員に"),
         ("前向きなコーチング", "目標づくり、昇進や異動の準備、やる気の立て直し。困りごとがなくても使えます。", "もっと力を出したい方に"),
         ("面談の準備", "部下との難しい面談の前に、何をどう伝えるかを整理します。", "管理職の方に"),
         ("月に1度の壁打ち", "基本料に含まれる30分の定例を、利害のない相手との相談に使えます。", "経営者、人事の方に")]

PAGES = [
 dict(file="index.html", nav="トップ", name="社外の専属キャリアコンサルタント", c=("#8ec9e8", "#ffc56b"),
      desc="国家資格キャリアコンサルタントが御社の専属として社員の相談とコーチングを担当。月額15,000円、相談1回30分5,000円。",
      h1="社員にも、相談を受ける人にも、社外の相談相手を。",
      lead="国家資格キャリアコンサルタントが、御社の専属として社員の相談を受けます。悩みの相談にも、前向きなコーチングにも使えます。",
      points=[("社員が直接予約", "会社を通さずに予約できるので、担当の方の手間が増えません。"),
              ("声が会社に届く", "社員が望んだことだけを、匿名で会社にお伝えします。"),
              ("相談を受ける人も支える", "管理職、人事、経営者の方ご自身の相談相手にもなります。")],
      cta=[("30分の説明を予約する", "setsumei")]),
 dict(file="keieisha.html", nav="経営者の方へ", name="社長と社員の、社外の相談役", c=("#ffc56b", "#7ccf9b"),
      desc="中小企業の経営者向け。社員の相談窓口と、経営者自身の相談相手を月額15,000円で。社外の国家資格キャリアコンサルタントが担当。",
      h1="社員の相談先と、あなた自身の相談相手を同時に。",
      lead="社員が辞めると決めてから、初めて本音を知る。そうなる前に、社外で話せる相手を用意できます。月に1度の30分は、あなた自身の壁打ちに使えます。",
      points=[("費用は使った分だけ", "相談は1回30分5,000円。月の上限件数を決められます。"),
              ("小さく始められる", "初期費用はありません。最初の3か月はいつでも解約できます。"),
              ("利害のない聞き手", "社内の誰にも言いにくいことを、月に1度、社外の相手に話せます。")],
      cta=[("30分の説明を予約する", "setsumei")]),
 dict(file="jinji.html", nav="人事・総務の方へ", name="人事のとなりの相談窓口", c=("#7ccf9b", "#8ec9e8"),
      desc="ひとり人事・兼務の人事担当者向け。社員の相談窓口を社外に置き、導入の手間はURLを共有するだけ。上司への提案資料つき。",
      h1="社員の相談を、一人で抱えなくていい。",
      lead="人事を一人で、あるいは兼務で担っている方へ。社員の相談窓口を社外に置けます。あなた自身にも、月に1度の相談相手ができます。",
      points=[("導入はURLを配るだけ", "説明会は不要です。配布用の案内チラシも、会社名を入れてすぐ印刷できます。"),
              ("上司に出せる資料あり", "費用と手間を1枚にまとめた提案資料を用意しています。"),
              ("報告は件数だけ", "誰が相談したかは伝わりません。毎月、件数だけを報告します。")],
      cta=[("上司に見せる資料を開く", "shiryo"), ("30分の説明を予約する", "setsumei")]),
 dict(file="saiyo.html", nav="採用担当の方へ", name="求人票に書けるキャリア相談制度", c=("#ffb199", "#8ec9e8"),
      desc="採用担当者向け。求人票に書ける社外キャリア相談制度。入社後フォロー面談にも使え、応募者の安心材料になります。",
      h1="求人票に書ける制度になります。",
      lead="「人を大切にする会社です」を、具体的な制度で示せます。入社後の節目に社外の専門家と話せる機会は、応募する側の安心材料になります。",
      points=[("文例1", "社外の専属キャリアコンサルタント（国家資格）に、会社負担で相談できます。"),
              ("文例2", "入社後の不安を一人で抱えないよう、社外のキャリアコンサルタントと契約しています。"),
              ("入社後フォローにも", "入社1か月、3か月、6か月の節目の面談として使えます。")],
      cta=[("求人票の文例を受け取る", "kyujin")]),
 dict(file="kanrishoku.html", nav="管理職の方へ", name="管理職のための壁打ち相談", c=("#8ec9e8", "#7ccf9b"),
      desc="管理職向け。部下の相談を受ける人にも相談先を。面談の準備やふりかえりを、社外のキャリアコンサルタントと30分で。",
      h1="相談を受ける人にも、相談先を。",
      lead="部下の相談を受け、育成を任され、自分の仕事もある。その立場で弱音を言える相手は、社内にはなかなかいません。",
      points=[("面談の前に30分", "何をどう伝えるかを、一緒に整理します。"),
              ("聞き方を一緒に考える", "相談とコーチングを長く仕事にしてきた立場からお手伝いします。"),
              ("会社には伝わらない", "あなたが話した内容は、会社に伝えません。")],
      cta=[("会社に提案する資料を開く", "kit")]),
 dict(file="hataraku.html", nav="働くあなたへ", name="会社負担で受けるコーチング", c=("#ffc56b", "#ffb199"),
      desc="働く個人向け。コーチングやキャリア相談を自己負担なしで受けたい方へ。会社に制度として導入してもらうための提案キット。",
      h1="コーチングを受けたい。でも自費は避けたい。",
      lead="会社がこの制度を導入すると、あなたは自己負担なしで、社外のコーチングとキャリア相談を使えます。会社に取り入れてもらう方法を2つ用意しています。",
      points=[("自分で提案する", "上司や人事に渡せる1枚を用意しています。そのまま見せられます。"),
              ("代わりに案内してもらう", "会社名を教えていただければ、こちらから会社に案内します。"),
              ("名前は伝えません", "あなたが誰かは、会社に一切伝えません。少人数の職場では推測されることがあるため、伝え方はあなたが選べます。")],
      cta=[("上司に渡す1枚を開く", "kit"), ("代わりに案内を依頼する", "suisen")]),
]

CSS = """
:root{--bg:#fffdf6;--sky:#e6f5fb;--sun:#ffd34d;--coral:#ff7a59;--leaf:#2f9e6b;--ink:#243342;--muted:#5d6b78;--line:#e3e8ee;--card:#ffffff;
--display:"Zen Maru Gothic","Hiragino Maru Gothic ProN","Yu Gothic",sans-serif;--body:"Zen Kaku Gothic New","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.85}
a{color:#1b6fa8}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--coral);outline-offset:2px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.bar{background:#fff;border-bottom:1px solid var(--line)}.bar .wrap{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;padding:10px 20px}
.brand{font-family:var(--display);font-weight:700;margin-right:auto;text-decoration:none;color:var(--ink)}
.bar a.n{font-size:14px;text-decoration:none;color:var(--ink);padding:4px 10px;border-radius:999px}.bar a.n.on{background:var(--sun)}
.hero{background:linear-gradient(180deg,var(--sky),var(--bg));padding:36px 0 28px}
.hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:28px;align-items:center}
@media(max-width:760px){.hero .wrap{grid-template-columns:1fr}}
.tag{display:inline-block;background:#fff;border:2px solid var(--sun);border-radius:999px;padding:2px 14px;font-size:14px;font-weight:700;margin:0 0 12px}
h1{font-family:var(--display);font-size:clamp(26px,4.6vw,40px);line-height:1.4;margin:0 0 14px;text-wrap:balance}
.lead{margin:0 0 18px;max-width:34em}.hero svg{width:100%;height:auto}
.price{display:flex;flex-wrap:wrap;gap:6px 20px;background:#fff;border-radius:14px;padding:12px 18px;border:1px solid var(--line)}
.price b{font-family:var(--display);font-size:20px;color:var(--coral)}
.btn{display:inline-block;background:var(--coral);color:#fff;font-weight:700;text-decoration:none;padding:12px 24px;border-radius:999px;border:0;font-size:16px;font-family:var(--body);cursor:pointer;box-shadow:0 4px 0 #d95f41}
.btn.sub{background:#fff;color:var(--ink);border:2px solid var(--ink);box-shadow:none}.cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px;align-items:center}
section{padding:40px 0}h2{font-family:var(--display);font-size:25px;margin:0 0 6px;text-wrap:balance}
h2::after{content:"";display:block;width:56px;height:6px;border-radius:3px;background:var(--sun);margin-top:8px}
.sub{color:var(--muted);margin:10px 0 20px}h3{font-family:var(--display);font-size:18px;margin:0 0 6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}
.card{background:var(--card);border-radius:16px;padding:18px;border:1px solid var(--line)}.card p{margin:0;font-size:15px}
.card.p1{background:#fff6d6;border-color:#ffe59a}.card.p2{background:#e6f5fb;border-color:#bfe3f2}.card.p3{background:#e8f7ee;border-color:#bfe6cf}
.who{color:var(--muted);font-size:13px;margin-top:8px!important}.band{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.comic{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}@media(max-width:820px){.comic{grid-template-columns:repeat(2,1fr)}}
.koma{position:relative;background:#fff;border:3px solid var(--ink);border-radius:10px;padding:14px 10px 10px;text-align:center}
.koma svg{width:100%;height:auto}.koma p{margin:6px 0 0;font-size:14px;line-height:1.6;text-align:left}
.kn{position:absolute;top:-12px;left:-10px;width:30px;height:30px;border-radius:50%;background:var(--sun);border:3px solid var(--ink);font-family:var(--display);font-weight:700;display:grid;place-items:center;font-size:14px}
.small{font-size:13px;color:var(--muted)}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s;display:grid;gap:10px}
ol.steps li{counter-increment:s;display:grid;grid-template-columns:38px 1fr;gap:12px}
ol.steps li::before{content:counter(s);width:34px;height:34px;border-radius:50%;background:var(--leaf);color:#fff;font-family:var(--display);font-weight:700;display:grid;place-items:center}
.pr{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:22px}
.pr div{background:#fff;border-radius:14px;border:1px solid var(--line);padding:12px 14px}.pr b{font-family:var(--display);font-size:18px;display:block;color:var(--leaf)}.pr span{font-size:14px;color:var(--muted)}
.tb{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:#fff}table{border-collapse:collapse;width:100%}
th,td{text-align:left;padding:12px 16px;border-bottom:1px solid var(--line);vertical-align:top;font-size:15px}th{width:10em;color:var(--muted);font-weight:500}tr:last-child th,tr:last-child td{border-bottom:0}
details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin-bottom:8px}summary{font-weight:700;cursor:pointer}details p{margin:8px 0 0}
.others{display:flex;flex-wrap:wrap;gap:10px}.others a{background:#fff;border:2px solid var(--sun);border-radius:999px;padding:6px 16px;text-decoration:none;color:var(--ink);font-weight:500}
footer{padding:28px 0 48px;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}
.prof{display:grid;grid-template-columns:260px 1fr;gap:28px;align-items:center;margin-top:20px}@media(max-width:700px){.prof{grid-template-columns:1fr}}
.prof img{width:100%;max-width:260px;height:auto;border-radius:24px;border:6px solid #fff;box-shadow:0 6px 0 var(--sun)}
.pn{font-family:var(--display);font-size:24px;font-weight:700;margin:0 0 8px}.pn span{font-size:14px;font-weight:500;color:var(--muted);margin-left:12px}
.worry{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:10px;max-width:42em}.worry li{background:#fff6d6;border-radius:12px;padding:10px 16px 10px 46px;position:relative}
.worry li::before{content:"";position:absolute;left:17px;top:18px;width:14px;height:7px;border-left:3px solid var(--coral);border-bottom:3px solid var(--coral);transform:rotate(-45deg)}
.tool{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0;display:grid;gap:10px;max-width:640px}
.tool label{font-weight:700;font-size:14px}.tool input{width:100%;font:inherit;padding:8px 10px;border:1px solid #b8c2cc;border-radius:8px}
.sheet{background:#fff;border:1px solid var(--line);max-width:794px;margin:0 auto 32px;padding:40px 44px}
.sheet h1{font-size:30px}.sheet .co{font-family:var(--display);font-size:18px;margin:0 0 4px}
.sheet .row{display:grid;grid-template-columns:1fr 190px;gap:24px;align-items:start;margin-top:18px}
.qr{border:3px solid var(--ink);border-radius:12px;padding:12px;text-align:center;font-size:13px}.qr #qr{display:grid;place-items:center;min-height:150px}
@media print{.bar,.tool,footer,.noprint{display:none!important}body{background:#fff}.sheet{border:0;margin:0;padding:0;max-width:none}@page{size:A4;margin:16mm}}
"""

def head(title, desc):
    return (f'<!DOCTYPE html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="style.css"></head><body>')

def bar(cur):
    links = "".join(f'<a class="n{" on" if p["file"] == cur else ""}" href="{p["file"]}">{p["nav"]}</a>' for p in PAGES)
    return f'<div class="bar"><div class="wrap"><a class="brand" href="index.html">社外の専属キャリアコンサルタント</a>{links}</div></div>'

FOOT = f'<footer><div class="wrap">担当：{NAME}（国家資格キャリアコンサルタント）</div></footer></body></html>'

SHARED = f"""
<section><div class="wrap"><h2>使い方</h2><p class="sub">プランは1つです。使い方は会社ごとに決められます。</p>
<div class="grid">{''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p><p class="who">{w}</p></div>' for t, d, w in USAGE)}</div></div></section>
@@COMIC@@
<section><div class="wrap"><h2>仕組みと約束</h2><p class="sub">安心して話せることが、この制度の土台です。</p>
<div class="pr"><div><b>独立</b><span>会社の指揮命令の外にいます</span></div><div><b>中立</b><span>会社と社員、どちらの側にも偏りません</span></div><div><b>守秘</b><span>本人の同意なく内容を伝えません</span></div><div><b>非公式</b><span>人事評価や記録とは切り離します</span></div></div>
<h3>社員の声が、会社に届くまで</h3>
<ol class="steps"><li><span>30分の相談の最後の5分で、「会社に伝えておきたいことはありますか」と伺います。</span></li>
<li><span>伝えたい内容だけを選び、個人が特定されにくい表現に整えます。AIによる確認も併用します。録音や録画はしません。</span></li>
<li><span>整えた文面を一緒に読みます。本人が承認したものだけを、後から会社に届けます。</span></li>
<li><span>会社の受け止めや対応を、次の機会に本人へお返しします。</span></li></ol>
<p class="small" style="margin-top:16px">この窓口は医療機関ではありません。体調や心の不調が続くときは、産業医や医療機関など適切な相談先につなぎます。命や安全に関わる差し迫った状況では、本人を守るために必要な相手へ連絡することがあります。</p></div></section>
<section class="band"><div class="wrap"><h2>料金と流れ</h2><p class="sub">金額は税別です。</p>
<div class="tb"><table><tr><th>月額基本料</th><td>15,000円（従業員100名まで一律）</td></tr>
<tr><th>基本料に含むもの</th><td>社員専用の予約ページ、社員向けの案内ページと配布用チラシ、会社へ声を届ける仕組み、窓口担当の方との月に1度の定例（30分）、求人や自社サイトでの表記</td></tr>
<tr><th>個別相談</th><td>1回30分 5,000円。使った分だけ。どなたが使っても同額</td></tr>
<tr><th>利用の上限</th><td>1人あたり月2回まで。会社ごとに月の上限件数を決められます</td></tr>
<tr><th>契約</th><td>12か月の自動更新。最初の3か月はいつでも解約できます</td></tr></table></div>
<h3 style="margin-top:26px">申込みから利用開始まで</h3>
<ol class="steps"><li><span>30分のオンライン説明。御社の状況を伺います。</span></li><li><span>申込フォームと電子契約。</span></li>
<li><span>案内ページのURLか、印刷した案内チラシを社員の方に配ります。説明会は不要です。</span></li><li><span>社員の方が直接予約し、相談が始まります。</span></li></ol></div></section>
<section><div class="wrap"><h2>よくある質問</h2><div style="margin-top:18px">
<details><summary>誰が相談したか、会社に分かりますか。</summary><p>分かりません。社員の方は会社を通さずに予約します。会社には月の件数だけを報告します。</p></details>
<details><summary>利用が少なかったら、もったいなくありませんか。</summary><p>相談の費用は使った分だけです。月に1度の定例は、窓口担当の方ご自身の相談に使えます。利用が少ない月は、社員の方への再案内文をこちらで用意します。</p></details>
<details><summary>担当が不在のときはどうなりますか。</summary><p>病気や事故などで1か月を通じて実施できなかった場合、その月の基本料はいただきません。</p></details>
<details><summary>産業医や既存の相談窓口と重なりませんか。</summary><p>こちらは仕事とキャリアの相談、前向きなコーチングを扱います。不調が疑われる場合は、産業医や医療機関につなぎます。</p></details>
</div></div></section>
<section><div class="wrap"><h2>担当者</h2><div class="prof"><img src="img/takemura.jpg" alt="{NAME}の写真" width="260" height="290"><div><p class="pn">{NAME}<span>たけむら しょうた</span></p><p>国家資格キャリアコンサルタント。キャリア相談、コーチング、不登校の若者支援に携わってきました。</p><p>相談する方の話を聴くことと、相談を受ける方を支えることの両方を仕事にしています。御社の専属として、毎回同じ担当者がお話を伺います。</p></div></div></div></section>
<section class="band" id="junbi"><div class="wrap"><h2>お問い合わせ</h2><p class="sub">説明の予約と各フォームは準備中です。公開時にここへつなぎます。</p></div></section>
"""

B, Y, G, R = "#8ec9e8", "#ffc56b", "#7ccf9b", "#ffb199"
K1, K2, K3 = "#5b4636", "#2f3b52", "#444444"
EXTRA = {
 "index.html": dict(ctitle="たとえば、入社したばかりの方の場合",
   worry=["社員が何を考えているのか、辞めると言われるまで分からない。", "相談を受ける管理職や人事が、疲れている。", "相談窓口を置きたいが、準備に手間をかけられない。"],
   comic=[([(B, K1)], "入社して1か月。小さな疑問を、誰に聞けばいいか分からない。"), ([(Y, K2)], "会社から案内が届く。「社外の相談、会社負担で使えます」"),
          ([(B, K1), (G, K3)], "オンラインで30分。話すうちに、気がかりが整理されていく。"), ([(B, K1), (Y, K2)], "伝えたいことだけを、匿名で会社へ。会社からの返事も戻ってくる。")]),
 "keieisha.html": dict(ctitle="たとえば、社員の退職が続いた会社の場合",
   worry=["辞めると決まってから、初めて理由を知る。", "幹部にも家族にも言いにくい悩みがある。", "社員が何を感じているか、数字だけでは分からない。"],
   comic=[([(Y, K2)], "また一人、辞めると言われた。理由は最後まで分からなかった。"), ([(Y, K2)], "社外の相談窓口を置いてみる。やることは案内を配るだけ。"),
          ([(Y, K2), (G, K3)], "月に1度の定例。社員から届いた声を、匿名で受け取る。"), ([(Y, K2), (G, K3)], "打てる手が見えてくる。自分の悩みも、ここで話せる。")]),
 "jinji.html": dict(ctitle="たとえば、人事を一人で担っている方の場合",
   worry=["社員の相談を受けても、自分が相談できる人がいない。", "新しい制度を入れたいが、準備の時間がない。", "上司に提案したいが、説明の材料がない。"],
   comic=[([(G, K1)], "社員の相談、採用、労務。全部ひとりで受けている。"), ([(G, K1), (Y, K2)], "提案資料を1枚、上司に見せる。「月15,000円からです」"),
          ([(G, K1)], "案内チラシを印刷して配る。準備はそれだけ。"), ([(G, K1), (B, K3)], "相談は社外へ。自分にも、月に1度の相談相手ができた。")]),
 "saiyo.html": dict(ctitle="たとえば、求人で違いを出したい会社の場合",
   worry=["求人票で、他社との違いを出しにくい。", "内定者から、入社後の不安を聞かれる。", "入社後のフォローまで、手が回らない。"],
   comic=[([(R, K1)], "求人票。どの会社も、似たことを書いている。"), ([(R, K1)], "「社外のキャリアコンサルタントに相談できます」と書き足す。"),
          ([(R, K1), (B, K2)], "面接で聞かれる。「入社後も相談できるんですか」"), ([(B, K2), (G, K3)], "入社後の節目に30分。安心して働き始められる。")]),
 "kanrishoku.html": dict(ctitle="たとえば、部下との面談を控えた方の場合",
   worry=["部下の相談に、どう答えるのがよいか迷う。", "厳しいことを伝える面談が、気が重い。", "自分の悩みを話せる場がない。"],
   comic=[([(B, K2), (R, K1)], "部下から「少し相談が」。どう答えるのがいいだろう。"), ([(B, K2), (G, K3)], "面談の前に30分、社外で整理する。"),
          ([(B, K2)], "聞くこと、伝えること、言わないことを決める。"), ([(B, K2), (R, K1)], "落ち着いて面談に臨める。終わったら、ふりかえりも。")]),
 "hataraku.html": dict(ctitle="たとえば、コーチングを受けてみたい方の場合",
   worry=["上司には言いにくいことがある。", "これからのキャリアを、誰かと整理したい。", "コーチングに興味はあるが、自費では負担が大きい。"],
   comic=[([(Y, K1)], "もっと力を出したい。でもコーチングは、自費だと続けにくい。"), ([(Y, K1), (B, K2)], "上司に1枚、見せてみる。「こういう制度があるそうです」"),
          ([(Y, K1)], "会社が導入。自己負担なしで予約できる。"), ([(Y, K1), (G, K3)], "目標が言葉になる。次の一歩が決まる。")]),
}
def worry(p):
    e = EXTRA[p["file"]]
    return ('<section class="band"><div class="wrap"><h2>こんなことはありませんか</h2><ul class="worry">'
            + "".join(f"<li>{w}</li>" for w in e["worry"]) + '</ul></div></section>')
def comic(p):
    e = EXTRA[p["file"]]
    ks = "".join(koma(i + 1, ppl, t) for i, (ppl, t) in enumerate(e["comic"]))
    return (f'<section class="band"><div class="wrap"><h2>{e["ctitle"]}</h2><p class="sub">4コマでご紹介します。</p>'
            f'<div class="comic">{ks}</div><p class="small">使い方のイメージです。</p></div></section>')

def page(p):
    pts = "".join(f'<div class="card p{i+1}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p["points"]))
    cta = "".join(f'<a class="btn{" sub" if i else ""}" href="{FORMS[k]}">{l}</a>' for i, (l, k) in enumerate(p["cta"]))
    others = "".join(f'<a href="{q["file"]}">{q["nav"]}</a>' for q in PAGES if q["file"] != p["file"])
    return (head(p["name"], p["desc"]) + bar(p["file"]) +
            f'<header class="hero"><div class="wrap"><div><p class="tag">{p["name"]}</p><h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p>'
            f'<div class="price"><span>月額基本料 <b>15,000円</b></span><span>相談1回30分 <b>5,000円</b></span><span>最初の3か月は解約自由</span></div>'
            f'<div class="cta">{cta}</div></div><div>{hero_svg(*p["c"])}</div></div></header>'
            + worry(p) + f'<section><div class="wrap"><div class="grid">{pts}</div></div></section>' + SHARED.replace('@@COMIC@@', comic(p)) +
            f'<section><div class="wrap"><h2>ほかの立場の方へ</h2><div class="others" style="margin-top:18px">{others}</div></div></section>' + FOOT)

TOOLJS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script>
(function(){var q=new URLSearchParams(location.search),c=document.getElementById('in-co'),u=document.getElementById('in-url');
if(c&&q.get('c'))c.value=q.get('c');if(u&&q.get('u'))u.value=q.get('u');
function draw(){document.querySelectorAll('.co-name').forEach(function(e){e.textContent=(c&&c.value)||'（会社名）';});
var box=document.getElementById('qr');if(!box)return;box.innerHTML='';
if(u&&u.value&&window.QRCode){new QRCode(box,{text:u.value,width:150,height:150});document.getElementById('qr-url').textContent=u.value;}
else{box.textContent='予約ページのURLを入力するとQRコードが出ます';document.getElementById('qr-url').textContent='';}}
[c,u].forEach(function(e){if(e)e.addEventListener('input',draw);});draw();
var b=document.getElementById('print');if(b)b.addEventListener('click',function(){try{window.print();}catch(e){}});})();</script>"""

ANNAI = (head("社員向け案内チラシ", "会社名と予約ページのURLを入れると、社員に配れるA4の案内チラシができます。") + bar("") +
 '<div class="wrap"><div class="tool"><b>案内チラシを作る</b><div><label for="in-co">会社名</label><input id="in-co" placeholder="例：株式会社サンプル"></div>'
 '<div><label for="in-url">社員用の予約ページのURL</label><input id="in-url" placeholder="https://"></div>'
 '<div><button class="btn" id="print" type="button">印刷する（PDF保存も可）</button></div>'
 '<p class="small" style="margin:0">ボタンが動かないときは、ブラウザの印刷（Ctrl+P または ⌘+P）を使ってください。A4縦1枚に収まります。</p></div></div>'
 f'<div class="sheet"><p class="co"><span class="co-name"></span>で働くみなさんへ</p><h1>社外の相談窓口ができました</h1>'
 '<p>仕事のこと、これからのこと、誰に言えばいいか分からないこと。社外のキャリアコンサルタント（国家資格）に、オンラインで30分、話せます。悩みがなくても、目標づくりなど前向きな相談にも使えます。</p>'
 '<div class="row"><div><h3>安心して使っていただくために</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>誰が相談したか、何を話したかは、会社に伝わりません。</li><li>費用は会社が負担します（月2回まで）。</li><li>会社に伝えてほしいことがある場合だけ、あなたが確認した内容を匿名で届けられます。</li><li>録音や録画はしません。</li></ul>'
 '<h3>使い方</h3><ol class="steps"><li><span>右のQRコードを読み取り、都合のよい日時を選ぶ。</span></li><li><span>話したいテーマを選び、一言メモを書く。</span></li><li><span>届いたURLから、時間になったら参加する。</span></li></ol></div>'
 '<div class="qr"><div id="qr"></div><p style="margin:8px 0 0;font-weight:700">予約はこちら</p><p id="qr-url" style="margin:4px 0 0;word-break:break-all"></p></div></div>'
 f'<p class="small" style="margin-top:20px">担当：{NAME}（国家資格キャリアコンサルタント）。この窓口は医療機関ではありません。体調や心の不調が続くときは、適切な相談先を一緒に探します。命や安全に関わる差し迫った状況では、あなたを守るために必要な相手へ連絡することがあります。</p></div>'
 + TOOLJS + FOOT)

TEIAN = (head("社外キャリア相談制度 導入のご提案", "上司や経営者にそのまま見せられる、社外キャリア相談制度の提案資料（A4 1枚）。") + bar("") +
 '<div class="wrap"><div class="tool"><b>提案資料を作る</b><div><label for="in-co">会社名（入れなくても使えます）</label><input id="in-co" placeholder="例：株式会社サンプル"></div>'
 '<div><button class="btn" id="print" type="button">印刷する（PDF保存も可）</button></div>'
 '<p class="small" style="margin:0">ボタンが動かないときは、ブラウザの印刷（Ctrl+P または ⌘+P）を使ってください。</p></div></div>'
 '<div class="sheet"><p class="co"><span class="co-name"></span> 御中</p><h1>社外キャリア相談制度 導入のご提案</h1>'
 '<p><b>提案の要点：</b>月額15,000円で、社員が社外の国家資格キャリアコンサルタントに相談できる制度を導入します。</p>'
 '<h3>なぜ必要か</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>辞めると決める前に、社員が本音を話せる相手が社内にいない。</li><li>管理職が部下の相談を一人で抱えている。</li><li>求人で「人を大切にする会社」だと具体的に示せる材料が少ない。</li></ul>'
 '<h3>費用</h3><div class="tb"><table><tr><th>月額基本料</th><td>15,000円（年額18万円）。窓口担当者との月に1度の定例30分を含む</td></tr><tr><th>個別相談</th><td>1回30分5,000円。使った分だけ。月の上限件数を決められる</td></tr><tr><th>初期費用・解約</th><td>初期費用なし。最初の3か月はいつでも解約できる</td></tr></table></div>'
 '<h3 style="margin-top:16px">社内の手間</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>導入時は、案内ページのURLか印刷した案内チラシを社員に配るだけ。説明会は不要。</li><li>予約は社員が直接行う。窓口担当者の作業は月に1度の定例30分のみ。</li></ul>'
 '<h3>心配への答え</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>相談内容は会社に伝わらない。会社に届くのは件数と、本人が望んだ声だけ。</li><li>不調が疑われる場合は、産業医や医療機関につなぐ。</li><li>使い方は会社で決められる（入社後フォロー面談、前向きなコーチング、管理職の面談準備など）。</li></ul>'
 f'<p class="small">金額は税別。担当：{NAME}（国家資格キャリアコンサルタント）</p></div>' + TOOLJS + FOOT)

os.makedirs(OUT, exist_ok=True)
files = {p["file"]: page(p) for p in PAGES}
files.update({"annai.html": ANNAI, "teian.html": TEIAN, "style.css": CSS})
for name, body in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
import shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
if os.path.isdir(src):
    shutil.copytree(src, os.path.join(OUT, "img"), dirs_exist_ok=True)
print("\n".join(sorted(files)))
