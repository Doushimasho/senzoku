# -*- coding: utf-8 -*-
"""法人向けサイトの生成スクリプト。python3 build.py <出力フォルダ> で全ページを書き出す。"""
import os, sys, html

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
NAME = "竹村正太"
YAGO = ""        # 屋号（決まったら入れる。空なら表示しない）
REG_NO = ""      # キャリアコンサルタント登録番号（空なら表示しない）
VIDEO_WELCOME = "aisatsu.mp4"  # 挨拶動画。YouTubeの動画ID（例：dQw4w9WgXcQ）か、同じ場所に置いたmp4のファイル名。空なら表示しない
VIDEO_SAMPLE = ""   # 面談の雰囲気の動画（同上）
VIDEO_SHOKAI = "shokai.mp4"  # サービス紹介動画（同上）
CF_TOKEN = "f3ce115577a342c1b827ba55d74a7642"    # Cloudflare Web Analyticsのトークン。空なら計測タグを入れない
GC_CODE = ""     # GoatCounterを使う場合のコード（無料版は非商用向けのため、基本はCloudflareを使う）
SITE = "https://doushimasho.github.io/senzoku/"
# Googleフォームの公開URL（docs.google.com/forms/.../viewform）を入れる。空のままなら「準備中」の欄に飛ぶ
FORM_MOSHIKOMI = "https://docs.google.com/forms/d/e/1FAIpQLSdLWyaKJLw-DX6UcEgjtbLcXnZ2dcKj4_qNYGshUmNq85MQAQ/viewform"   # フォーム1：導入のお申込み
FORM_SHIRYO = "https://docs.google.com/forms/d/e/1FAIpQLSesxZUBfGm4NMgQSR6qnvHJkhl7DODfvgOXhJOcAZSlxScpYg/viewform"      # フォーム2：資料の受け取り・30分説明のご希望
FORM_SUISEN = "https://docs.google.com/forms/d/e/1FAIpQLSfFOu-RtAR-5cgqPioJ94SktrWd5nMysJgyRR93mLXmdw7o_w/viewform"      # フォーム3：会社に導入してほしい方へ
FORMS = {
    "setsumei": FORM_SHIRYO or "#junbi", "kyujin": FORM_SHIRYO or "#junbi",
    "suisen": FORM_SUISEN or "#junbi", "moshikomi": FORM_MOSHIKOMI or "#junbi",
    "shiryo": "teian.html", "kit": "teian.html",
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

USAGE = [("新入社員の最初の1年", "入社1か月、3か月、6か月、1年の節目に30分ずつ。社外にも話せる相手がいる安心感をつくります。", "新入社員、中途入社の方に"),
         ("辞める前に聞く面談", "退職が決まってからではなく、在職中に先回りして聞きます。", "年に1度、希望者または全員に"),
         ("前向きなコーチング", "目標づくり、昇進や異動の準備、やる気の立て直し。困りごとがなくても使えます。", "もっと力を出したい方に"),
         ("面談の準備", "部下との難しい面談の前に、何をどう伝えるかを整理します。", "管理職の方に"),
         ("いつでも話せる壁打ち相手", "チャットでいつでも軽く相談でき、月2回・各30分の面談も基本料に含まれます。利害のない相手との壁打ちに使えます。", "経営者、人事の方に"),
         ("研修や制度に組み込む", "新人研修、3年目研修、管理職への昇格など、会社の取り組みの一部として面談を付けます。", "研修担当の方に")]

PAGES = [
 dict(file="index.html", nav="トップ", name="社外の専属キャリアコンサルタント", c=("#8ec9e8", "#ffc56b"),
      desc="国家資格キャリアコンサルタントが御社の専属として社員の相談とコーチングを担当。月額15,000円、相談1回30分5,000円。",
      h1="社員にも、相談を受ける人にも、社外の相談相手を。",
      lead="国家資格キャリアコンサルタントが、御社の専属として社員の相談を受けます。悩みの相談にも、前向きなコーチングにも使えます。",
      points=[("社員が直接予約", "会社を通さずに予約できるので、担当の方の手間が増えません。"),
              ("声が会社に届く", "社員が望んだことだけを、匿名で会社にお伝えします。"),
              ("相談を受ける人も支える", "管理職、人事、経営者の方ご自身の相談相手にもなります。")],
      cta=[("まずは話を聞いてみる（30分・無料）", "setsumei")]),
 dict(file="keieisha.html", nav="経営者の方へ", name="社長と社員の、社外の相談役", c=("#ffc56b", "#7ccf9b"),
      desc="中小企業の経営者向け。社員の相談窓口と、経営者自身の相談相手を月額15,000円で。社外の国家資格キャリアコンサルタントが担当。",
      h1="社員の相談先と、あなた自身の相談相手を同時に。",
      lead="社員が辞めると決めてから、初めて本音を知る。そうなる前に、社外で話せる相手を用意できます。月2回の30分は、あなた自身の壁打ちに使えます。",
      points=[("費用は使った分だけ", "相談は1回30分5,000円。月の上限件数を決められます。"),
              ("小さく始められる", "初期費用はありません。最初の3か月はいつでも解約できます。"),
              ("利害のない聞き手", "社内の誰にも言いにくいことを、月に2回まで、社外の相手に話せます。")],
      cta=[("まずは話を聞いてみる（30分・無料）", "setsumei")]),
 dict(file="jinji.html", nav="人事・総務の方へ", name="人事のとなりの相談窓口", c=("#7ccf9b", "#8ec9e8"),
      desc="ひとり人事・兼務の人事担当者向け。社員の相談窓口を社外に置き、導入の手間はURLを共有するだけ。上司への提案資料つき。",
      h1="社員の相談を、一人で抱えなくていい。",
      lead="人事を一人で、あるいは兼務で担っている方へ。社員の相談窓口を社外に置けます。あなた自身にも、月に2回まで話せる相談相手ができます。",
      points=[("導入はURLを配るだけ", "説明会は不要です。配布用の案内チラシも、会社名を入れてすぐ印刷できます。"),
              ("上司に出せる資料あり", "費用と手間を1枚にまとめた提案資料を用意しています。"),
              ("報告は件数だけ", "誰が相談したかは伝わりません。毎月、件数だけを報告します。")],
      cta=[("上司に見せる資料を開く", "shiryo"), ("まずは話を聞いてみる（30分・無料）", "setsumei")]),
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
.career{margin:10px 0 12px;padding-left:1.2em;line-height:1.8}.career li{margin:4px 0}.yosu{margin:12px 0 0}.prof .yosu img{border-radius:12px;width:180px;height:auto;border:0;box-shadow:none}.yosu figcaption{font-size:13px;color:#667}
.grid.g2{grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr))}
.mihon{background:#fff;border:1px solid #e6e1d8;border-radius:12px;padding:14px 16px;white-space:pre-wrap;font-size:14px;line-height:1.85;margin-top:10px}.mcard .small{margin:4px 0 0}
.vid{position:relative;max-width:760px;aspect-ratio:16/9;margin-top:16px;border-radius:16px;overflow:hidden;background:#000}.vid iframe,.vid video{position:absolute;inset:0;width:100%;height:100%;border:0}
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
.q{border:1px solid var(--line);background:#fff;border-radius:12px;padding:12px 16px;margin:0 0 10px}.q legend{font-weight:700;padding:0 6px}.q label{margin-right:18px;display:inline-block;padding:4px 0}
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
            f'<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
            f'<meta property="og:image" content="{SITE}ogp.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="google-site-verification" content="2t_jYbV7BGn_y59pKTI4hIXxJJtO_QwigzLAIRFgzhE">'
            '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%2230%22 fill=%22%23ffd34d%22/%3E%3Cellipse cx=%2232%22 cy=%2230%22 rx=%2218%22 ry=%2213%22 fill=%22%23fff%22/%3E%3Ccircle cx=%2225%22 cy=%2230%22 r=%223%22 fill=%22%23ff7a59%22/%3E%3Ccircle cx=%2232%22 cy=%2230%22 r=%223%22 fill=%22%23ff7a59%22/%3E%3Ccircle cx=%2239%22 cy=%2230%22 r=%223%22 fill=%22%23ff7a59%22/%3E%3C/svg%3E">'
            '<link rel="stylesheet" href="style.css">' + (f'<script data-goatcounter="https://{GC_CODE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>' if GC_CODE else '') + (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{CF_TOKEN}"}}\'></script>' if CF_TOKEN else '') + '</head><body>')

def video(src, title):
    if not src:
        return ""
    if src.endswith(".mp4"):
        poster = src[:-4] + ".jpg"
        inner = f'<video controls preload="none" playsinline poster="{poster}" src="{src}" title="{title}"></video>'
    else:
        inner = f'<iframe src="https://www.youtube-nocookie.com/embed/{src}" title="{title}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>'
    return f'<div class="vid">{inner}</div>'
def welcome():
    if not VIDEO_WELCOME:
        return ""
    return ('<section><div class="wrap"><h2>はじめまして、竹村です</h2><p class="sub">40秒ほどの動画で、ごあいさつします（音声つき・字幕あり）。</p>'
            + video(VIDEO_WELCOME, "竹村正太のごあいさつ") + '</div></section>')
def shokai():
    if not VIDEO_SHOKAI:
        return ""
    return ('<section><div class="wrap"><h2>1分でわかる、このサービス</h2><p class="sub">仕組み、安心の約束、料金までを1分にまとめました（音声つき・字幕あり）。</p>'
            + video(VIDEO_SHOKAI, "サービス紹介") + '</div></section>')
def sample():
    if not VIDEO_SAMPLE:
        return shokai()
    return shokai() + ('<section class="band"><div class="wrap"><h2>30分の相談は、こんな雰囲気です</h2><p class="sub">再現した様子です。実際の相談の録画ではありません。</p>'
            + video(VIDEO_SAMPLE, "相談の雰囲気") + '</div></section>')

def bar(cur):
    links = "".join(f'<a class="n{" on" if p["file"] == cur else ""}" href="{p["file"]}">{p["nav"]}</a>' for p in PAGES)
    links += f'<a class="n{" on" if cur == "mihon.html" else ""}" href="mihon.html">AIで作れるもの</a>'
    return f'<div class="bar"><div class="wrap"><a class="brand" href="index.html">社外の専属キャリアコンサルタント</a>{links}</div></div>'

FOOT = f'<footer><div class="wrap">担当：{NAME}（国家資格キャリアコンサルタント）　<a href="unei.html">運営者情報・個人情報の取り扱い</a></div></footer></body></html>'

SHARED = f"""
<section><div class="wrap"><h2>使い方</h2><p class="sub">プランは1つです。使い方は会社ごとに決められます。</p>
<div class="grid">{''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p><p class="who">{w}</p></div>' for t, d, w in USAGE)}</div></div></section>
@@COMIC@@
@@SAMPLE@@<section><div class="wrap"><h2>仕組みと約束</h2><p class="sub">安心して話せることが、この制度の土台です。</p>
<div class="pr"><div><b>独立</b><span>会社の指揮命令の外にいます</span></div><div><b>中立</b><span>引き止めも、転職の勧めもしません。本人が納得して選ぶことを支えます</span></div><div><b>守秘</b><span>本人の同意なく内容を伝えません</span></div><div><b>非公式</b><span>人事評価や記録とは切り離します</span></div></div>
<h3>社員の声が、会社に届くまで</h3>
<ol class="steps"><li><span>30分の相談の最後の5分で、「会社に伝えておきたいことはありますか」と伺います。</span></li>
<li><span>伝えたい内容だけを選び、個人が特定されにくい表現に整えます。AIによる確認も併用します。録音や録画はしません。</span></li>
<li><span>整えた文面を一緒に読みます。本人が承認したものだけを、後から会社に届けます。</span></li>
<li><span>会社の受け止めや対応を、次の機会に本人へお返しします。</span></li></ol>
<p class="small" style="margin-top:16px">この窓口は、会社が設けるハラスメントの相談窓口の代わりにはなりません。ハラスメントに関わる相談を受けたときは、会社の正式な窓口と社外の公的な相談先をご案内し、ご本人が望めば、会社に伝える手伝いをします。<br>この窓口は医療機関ではありません。体調や心の不調が続くときは、産業医や医療機関など適切な相談先につなぎます。命や安全に関わる差し迫った状況では、本人を守るために必要な相手へ連絡することがあります。</p></div></section>
<section><div class="wrap"><h2>窓口担当の方も、支えます</h2><p class="sub">社員の相談を受ける人には、自分の相談先がないことが多いものです。困ったときに、いつでも話せる相手がいる。それだけで、仕事はずいぶん楽になります。コーチとして話を聴き、実務の手も貸します。</p>
<div class="grid"><div class="card"><h3>チャットで、いつでも軽く相談</h3><p>「ちょっと聞きたい」は、チャットで送ってください。御社が使っているチャット（Slack、Chatwork、LINE WORKSなど）か、メールに合わせます。平日は原則、翌営業日までにお返事します。じっくり話したくなったら、その場で面談の予定を入れます。</p></div>
<div class="card"><h3>月2回、担当の方の相談</h3><p>基本料に、月2回・各30分の相談を含みます。運用の確認は短く済ませ、残りは担当の方ご自身の相談に使えます。社員対応の整理、施策の壁打ち、ご自身のキャリアやモチベーションの相談まで扱います。</p></div>
<div class="card"><h3>相談を受ける側の相談</h3><p>人事、研修担当、管理職の方が、社員や部下の相談を受けて迷ったときの相談です。月2回の枠を使えます。それを超える分は、社員と同じ1回30分5,000円で予約できます。</p></div>
<div class="card"><h3>取り組みを形に残す</h3><p>3か月ごとに、社員と担当の方に3問だけの簡単なアンケートをとります（相談してよかったか、この窓口を続けてほしいか、など）。年に1度のふりかえりとあわせて、担当の方が社内で報告に使える1枚にまとめます。</p></div>
<div class="card"><h3>研修づくりとAIの活用</h3><p>研修のワークは、決まったものを売り込むのではなく、担当の方や管理職の方と一緒に作ります。AIが苦手な方には、資料や案内づくりにAIを使う方法を、月2回の相談の中でお伝えします。</p></div>
<div class="card"><h3>一人で人事を担う方に</h3><p>少人数の会社では、件数の報告は3か月ごとにまとめ、日付は書きません。その分、月2回の枠を担当の方の相談に厚く使います。</p></div></div>
<p class="small" style="margin-top:14px">担当者は国家資格キャリアコンサルタントです。ビジネスコーチングとスポーツのコーチングを、いまも仕事として行っています。</p></div></section>
<section class="band"><div class="wrap"><h2>会社の研修や制度に組み込む</h2><p class="sub">相談は、待っているだけでは使われにくいものです。会社の取り組みの一部として面談を組み込むと、節目ごとに確実に話す機会ができます。</p>
<div class="tb"><table><tr><th>新入社員の最初の1年</th><td>入社1か月、3か月、6か月、1年の節目に30分ずつ。辞めたくなりやすい時期に、社外の相手と話す時間をつくります</td></tr>
<tr><th>3年目研修に</th><td>研修の前後に1回ずつ。研修で考えたことを、ご自身のキャリアの言葉に整えます</td></tr>
<tr><th>管理職の最初の半年</th><td>昇格後6か月のあいだ、月に1回。部下との面談の準備や、新しい役割の悩みを相談できます。いちばん孤立しやすい時期を支えます</td></tr>
<tr><th>会社の取り組みに</th><td>評価制度の見直し、異動や配置換え、組織の再編など、会社が進める取り組みに、対象者との面談を付けます</td></tr></table></div>
<p class="small" style="margin-top:12px">料金は通常と同じ1回30分5,000円です。対象者と回数を先に決めて、予約枠をまとめて確保します。助成金の対象になるかどうかは、社会保険労務士にご確認ください。</p></div></section>
<section><div class="wrap"><h2>AIが苦手でも、大丈夫です</h2><p class="sub">一人で人事を担っていると、「AIを使えば楽になると聞くけれど、何から始めればいいか分からない」ということがよくあります。担当者はキャリアコンサルタントであり、AIで道具を作ることも仕事にしています。</p>
<div class="grid"><div class="card"><h3>このサイトの道具も、AIで作りました</h3><p><a href="annai.html">社員向けの案内チラシ</a>、<a href="teian.html">上司に見せる1枚</a>、<a href="mitsumori.html">費用の試算</a>、<a href="shindan.html">3分診断</a>。同じような道具を、御社に合わせて作れます。</p><p><a href="mihon.html">AIで作った見本を見る</a></p></div>
<div class="card"><h3>たとえば、こんなものが作れます</h3><p>求人票の下書き、新入社員向けの「最初の1か月ガイド」、1on1や面談の記録シート、社内アンケートの作成と集計、研修の資料。</p></div>
<div class="card"><h3>使い方から、お伝えします</h3><p>作り方を覚えたい方には、月2回の相談の中で一緒に手を動かします。作成までまるごと任せたい場合は、事前にお見積もりします。</p></div></div></div></section>
<section class="band"><div class="wrap"><h2>料金と流れ</h2><p class="sub">金額は税別です。</p>
<div class="tb"><table><tr><th>月額基本料</th><td>15,000円（従業員100名まで一律）</td></tr>
<tr><th>基本料に含むもの</th><td>社員専用の予約ページ、社員向けの案内ページと配布用チラシ、会社へ声を届ける仕組み、窓口担当の方の相談 月2回（各30分。運用の確認もこの中で行います）、求人や自社サイトでの表記</td></tr>
<tr><th>個別相談</th><td>1回30分 5,000円。使った分だけ。どなたが使っても同額</td></tr>
<tr><th>窓口担当の方の相談</th><td>チャットでの相談はいつでも（平日は原則、翌営業日までに返信）。面談は月2回（各30分）まで基本料に含みます。それを超える分は、社員と同じ1回30分5,000円です</td></tr>
<tr><th>研修や制度への組み込み</th><td>1回30分5,000円。対象者と回数を先に決めて予約枠を確保します</td></tr>
<tr><th>利用の上限</th><td>1人あたり月2回まで。会社ごとに月の上限件数を決められます</td></tr>
<tr><th>契約</th><td>12か月の自動更新。最初の3か月はいつでも解約できます</td></tr><tr><th>いまの価格</th><td>月額15,000円は、先着3社までの価格です。この価格でご契約いただいた会社は、継続しているあいだ、更新後も据え置きます</td></tr><tr><th>ご紹介の特典</th><td>ご紹介で新しい契約が決まると、紹介した会社とされた会社の両方の基本料を1か月分無料にします。年払いの会社には、代わりに相談3回分を無料にします</td></tr></table></div>
<h3 style="margin-top:26px">申込みから利用開始まで</h3>
<ol class="steps"><li><span>30分のオンライン説明。御社の状況を伺います。</span></li><li><span>申込フォームと電子契約。</span></li>
<li><span>案内ページのURLか、印刷した案内チラシを社員の方に配ります。説明会は不要です。</span></li><li><span>社員の方が直接予約し、相談が始まります。</span></li></ol></div></section>
<section><div class="wrap"><h2>よくある質問</h2><div style="margin-top:18px">
<details><summary>誰が相談したか、会社に分かりますか。</summary><p>分かりません。社員の方は会社を通さずに予約します。会社には月の件数だけを報告します。従業員20名未満の会社では、件数から推測されないよう、3か月ごとにまとめて日付なしで報告します。</p></details>
<details><summary>「専属」とは、御社だけを担当するという意味ですか。</summary><p>いいえ。御社の担当者が固定され、毎回同じ人が対応するという意味です。担当者はほかの会社も担当しています。御社の事情を知っている同じ人に、続けて相談できます。</p></details>
<details><summary>社員から転職や退職の相談があったら、どうしますか。</summary><p>そうした相談も受けます。引き止めも転職の勧めもせず、ご本人が納得して選べるよう整理を手伝います。相談の内容は、本人の同意なく会社に伝えません。</p></details>
<details><summary>ハラスメントの相談を受けたら、どうしますか。</summary><p>この窓口は、会社が設けるハラスメントの相談窓口の代わりにはなりません。会社の正式な窓口と社外の公的な相談先をご案内し、ご本人が望めば、会社に伝える手伝いをします。</p></details>
<details><summary>チャットでの相談は、誰が使えますか。</summary><p>窓口担当の方（人事・研修担当・管理職など、導入時に決めた方）です。社員の方の相談は、秘密を守るため、予約した面談で伺います。チャットに社員の名前や個人的な事情は書かないでください。</p></details>
<details><summary>外国籍の社員も相談できますか。</summary><p>できます。ハローワークでは外国籍の方の職業相談も担当してきました。やさしい日本語と、簡単な英語で対応します（英語は日常会話の水準です）。仕事のこと、日本での働き方や暮らしとの両立など、言葉にしにくいことも、ゆっくり伺います。</p></details>
<details><summary>新人研修などに組み込めますか。</summary><p>できます。新人研修、3年目研修、管理職への昇格、会社の取り組みなどに合わせて、対象者と回数を決めて面談を組み込みます。料金は通常と同じです。</p></details>
<details><summary>利用が少なかったら、もったいなくありませんか。</summary><p>相談の費用は使った分だけです。月2回の担当者相談は、窓口担当の方ご自身の相談に使えます。導入から1か月たったころと、利用が少ない月には、社員の方への再案内文をこちらで用意します。</p></details>
<details><summary>知り合いの会社を紹介すると、特典はありますか。</summary><p>あります。紹介した会社が契約に至ると、紹介した会社とされた会社の両方の基本料を1か月分無料にします。年払いの会社には、代わりに相談3回分（15,000円分）を無料にします。紹介は、窓口担当の方から一言お知らせいただくだけで結構です。</p></details>
<details><summary>どんな相談でも受けますか。</summary><p>仕事、職場の人間関係、これからのキャリア、働き方と生活の両立、目標づくりなどを扱います。診断や治療が必要な心身の不調、法律や労務の手続きは扱わず、適切な相談先をご案内します。</p></details>
<details><summary>個人で運営していて、守秘は大丈夫ですか。</summary><p>相談の内容を知っているのは担当者一人だけです。録音や録画はせず、手書きのメモはほかの人が見られない形で保管します。守秘の取り決めは、契約書にも明記します。</p></details>
<details><summary>相談にAIを使いますか。</summary><p>相談そのものは、担当者が直接お聴きします。会社に届ける文面を整えるときに、AIを補助として使うことがあります。その場合はご本人に先にお伝えし、お名前など個人が分かる情報は入力しません。</p></details>
<details><summary>費用に見合う効果はありますか。</summary><p>効果は会社ごとに異なるため、数字でお約束はしていません。その代わり、最初の3か月はいつでも解約できるようにしています。月2回の担当者相談の中で、利用の様子と届いた声を一緒に確かめながら、続けるかどうかを判断していただけます。</p></details>
<details><summary>担当が不在のときはどうなりますか。</summary><p>病気や事故などで1か月を通じて実施できなかった場合、その月の基本料はいただきません。2か月以上続けて実施できない場合は、会社はいつでも解約できます。</p></details>
<details><summary>産業医や既存の相談窓口と重なりませんか。</summary><p>こちらは仕事とキャリアの相談、前向きなコーチングを扱います。不調が疑われる場合は、産業医や医療機関につなぎます。</p></details>
</div></div></section>
<section><div class="wrap"><h2>担当者</h2><div class="prof"><img src="takemura.jpg" alt="{NAME}の写真" width="260" height="290"><div><p class="pn">{NAME}<span>たけむら しょうた</span></p><p>国家資格キャリアコンサルタント。ビジネスコーチングとスポーツのコーチングを、いまも仕事として続けています。</p><ul class="career"><li>ハローワークで4年間、職業相談を担当。高齢の方、障害のある方、外国籍の方を含め、年2,000件以上の相談を受けてきました。</li><li>ビジネスコーチング（2年目）。大人の学び直しや、個人で事業をする方の相談、モチベーションの支援。</li><li>小学生を中心としたバスケットボールの指導に10年以上。一人ひとりの特性とやる気に合わせた指導。</li><li>オンラインのフリースクールで、不登校の子どもと家族の相談、運営の相談。</li><li>JICAボランティアとして、大学卒業後に南アフリカで2年間活動。現地の農業省で農村の発展に取り組みました。</li></ul><p>相談する方の話を聴くことと、相談を受ける方を支えることの両方を仕事にしています。御社の専属として、毎回同じ担当者がお話を伺います（ほかの会社も担当しています）。</p><figure class="yosu"><img src="sodan-yosu.jpg" alt="オンライン相談のときの竹村正太" width="180" height="209"><figcaption>オンライン相談のときの様子</figcaption></figure><p><a href="unei.html">運営者情報を見る</a></p></div></div></div></section>
@@JUNBI@@
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
          ([(Y, K2), (G, K3)], "月2回の相談の時間。社員から届いた声を、匿名で受け取る。"), ([(Y, K2), (G, K3)], "打てる手が見えてくる。自分の悩みも、ここで話せる。")]),
 "jinji.html": dict(ctitle="たとえば、人事を一人で担っている方の場合",
   worry=["社員の相談を受けても、自分が相談できる人がいない。", "新しい制度を入れたいが、準備の時間がない。", "上司に提案したいが、説明の材料がない。"],
   comic=[([(G, K1)], "社員の相談、採用、労務。全部ひとりで受けている。"), ([(G, K1), (Y, K2)], "提案資料を1枚、上司に見せる。「月15,000円からです」"),
          ([(G, K1)], "案内チラシを印刷して配る。準備はそれだけ。"), ([(G, K1), (B, K3)], "相談は社外へ。自分にも、月2回話せる相談相手ができた。")]),
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

def junbi():
    if not (FORM_MOSHIKOMI or FORM_SHIRYO):
        return '<section class="band" id="junbi"><div class="wrap"><h2>お問い合わせ</h2><p class="sub">各フォームは準備中です。</p></div></section>'
    b = []
    if FORM_SHIRYO: b.append(f'<a class="btn" href="{FORM_SHIRYO}">まずは話を聞いてみる（30分・無料）</a>')
    if FORM_MOSHIKOMI: b.append(f'<a class="btn sub" href="{FORM_MOSHIKOMI}">導入を申し込む</a>')
    if FORM_SUISEN: b.append(f'<a class="btn sub" href="{FORM_SUISEN}">自分の会社に導入してほしい方</a>')
    return ('<section class="band" id="junbi"><div class="wrap"><h2>お問い合わせ</h2>'
            '<p class="sub">「少し話を聞いてみたい」くらいで大丈夫です。30分の説明と資料のお渡しは無料で、その場で担当の方ご自身のお悩みも伺います。こちらから営業のお電話をすることはありません。</p>'
            f'<div class="cta">{"".join(b)}</div></div></section>')
SHARED = SHARED.replace("@@JUNBI@@", junbi()).replace("@@SAMPLE@@", sample())

def page(p):
    pts = "".join(f'<div class="card p{i+1}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p["points"]))
    cta = "".join(f'<a class="btn{" sub" if i else ""}" href="{FORMS[k]}">{l}</a>' for i, (l, k) in enumerate(p["cta"]))
    others = "".join(f'<a href="{q["file"]}">{q["nav"]}</a>' for q in PAGES if q["file"] != p["file"])
    return (head(p["name"], p["desc"]) + bar(p["file"]) +
            f'<header class="hero"><div class="wrap"><div><p class="tag">{p["name"]}</p><h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p>'
            f'<div class="price"><span>月額基本料 <b>15,000円</b></span><span>相談1回30分 <b>5,000円</b></span><span>最初の3か月は解約自由</span></div>'
            f'<div class="cta">{cta}</div></div><div>{hero_svg(*p["c"])}</div></div></header>'
            + welcome() + worry(p) + f'<section><div class="wrap"><div class="grid">{pts}</div></div></section>' + SHARED.replace('@@COMIC@@', comic(p)) +
            f'<section><div class="wrap"><h2>ほかの立場の方へ</h2><div class="others" style="margin-top:18px">{others}</div></div></section>' + nayami_links() + FOOT)

TOOLJS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script>
(function(){var q=new URLSearchParams(location.search),c=document.getElementById('in-co'),u=document.getElementById('in-url');
if(c&&q.get('c'))c.value=q.get('c');if(u&&q.get('u'))u.value=q.get('u');
function draw(){document.querySelectorAll('.co-name').forEach(function(e){e.textContent=(c&&c.value)||'（会社名）';});
var box=document.getElementById('qr');if(!box)return;box.innerHTML='';
var t=document.getElementById('qr-url');t.textContent=(u&&u.value)||'';
if(u&&u.value&&window.QRCode){new QRCode(box,{text:u.value,width:150,height:150});}
else if(u&&u.value){box.textContent='QRコードを表示できませんでした。下のURLをお使いください';}
else{box.textContent='予約ページのURLを入力するとQRコードが出ます';}}
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
 '<h3>費用</h3><div class="tb"><table><tr><th>月額基本料</th><td>15,000円（年額18万円）。窓口担当者のチャット相談（随時）と面談 月2回（各30分）を含む</td></tr><tr><th>個別相談</th><td>1回30分5,000円。使った分だけ。月の上限件数を決められる</td></tr><tr><th>先着価格</th><td>月額15,000円は先着3社までの価格。契約を続けるあいだは更新後も据え置き</td></tr><tr><th>初期費用・解約</th><td>初期費用なし。最初の3か月はいつでも解約できる</td></tr></table></div>'
 '<h3 style="margin-top:16px">社内の手間</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>導入時は、案内ページのURLか印刷した案内チラシを社員に配るだけ。説明会は不要。</li><li>予約は社員が直接行う。窓口担当者の作業は月2回の相談（各30分）のみ。</li></ul>'
 '<h3>心配への答え</h3><ul style="margin:6px 0 14px;padding-left:1.2em"><li>相談内容は会社に伝わらない。会社に届くのは件数と、本人が望んだ声だけ。</li><li>不調が疑われる場合は、産業医や医療機関につなぐ。</li><li>使い方は会社で決められる（入社後フォロー面談、前向きなコーチング、管理職の面談準備など）。</li></ul>'
 f'<p class="small">金額は税別。担当：{NAME}（国家資格キャリアコンサルタント）</p></div>' + TOOLJS + FOOT)

# ---- 悩み別ページ、3分診断、会社別の提案ページ ----
NAYAMI = [
 dict(file="wakate-rishoku.html", nav="若手が本音を言わずに辞める", to="keieisha.html", tolabel="経営者の方へ",
      desc="若手社員が本音を言わないまま退職する職場で、辞める前に話を聞く方法。社外の専属キャリアコンサルタントによる相談と入社後フォロー面談。",
      h1="若手が、本音を言わないまま辞めていく。",
      lead="退職の話が出たときには、もう気持ちは決まっている。そうなる前に、社外で話せる相手を用意できます。",
      secs=[("なぜ本音が出ないのか", "上司に話すと評価に響くかもしれない。話しても変わらないかもしれない。そう感じると、人は黙ったまま転職先を探します。社内の面談を増やしても、同じ相手には同じことしか話せません。"),
            ("社外の相談相手にできること", "会社の評価と関係のない相手には、まだ整理できていない気持ちも話せます。話すうちに、辞めたい理由が仕事の内容なのか、人間関係なのか、将来への不安なのかが見えてきます。"),
            ("この制度での使い方", "入社1か月、3か月、6か月の節目に30分の面談を案内できます。年に1度、続けている理由と辞めたくなる瞬間を聞く面談も行えます。本人が望んだことだけを、匿名で会社にお伝えします。")]),
 dict(file="kanrishoku-hihei.html", nav="管理職が疲れている", to="kanrishoku.html", tolabel="管理職の方へ",
      desc="部下の相談と育成を抱える管理職の負担を軽くする方法。相談を受ける人を支える、社外のキャリアコンサルタントによる面談準備と壁打ち。",
      h1="相談を受ける管理職が、疲れている。",
      lead="部下の話を聞き、育て、自分の成果も出す。その負担を一人で抱えている管理職に、社外の相談先を用意できます。",
      secs=[("なぜ疲れるのか", "部下の相談には正解がありません。どう答えたか、あれでよかったのかを、あとから一人で考え続けることになります。立場上、弱音を言える相手も社内には多くありません。"),
            ("社外の相談相手にできること", "面談の前に、何を聞き、何を伝え、何を言わないかを一緒に整理できます。終わったあとには、うまくいった点と次に変える点をふりかえれます。"),
            ("この制度での使い方", "管理職の方も、社員と同じ30分の相談を使えます。部下の相談そのものを社外に任せることもできるので、管理職が一人で受け止める量が減ります。")]),
 dict(file="keieisha-sodan.html", nav="経営者に相談相手がいない", to="keieisha.html", tolabel="経営者の方へ",
      desc="社内にも家族にも話しにくい経営者の悩みを、利害のない社外の相手に話す月2回の30分。社員の相談窓口とあわせて月額15,000円。",
      h1="経営者には、相談相手がいない。",
      lead="社員には言えない。家族には心配をかけたくない。取引先には弱みを見せられない。月に2回まで、利害のない相手に話す時間を持てます。",
      secs=[("なぜ相談しにくいのか", "経営者の言葉は、社内では決定として受け取られます。迷っている段階の話を、迷っているまま話せる相手が必要です。"),
            ("社外の相談相手にできること", "答えを出すのは経営者ご自身です。こちらは、考えを言葉にする手伝いをします。人と組織の悩みは、キャリアコンサルティングとコーチングの専門領域です。"),
            ("この制度での使い方", "基本料に含まれる月2回・各30分の相談を、ご自身の壁打ちに使えます。同じ場で、社員から届いた声も匿名で受け取れます。")]),
 dict(file="sodan-kawaranai.html", nav="相談しても変わらないと思われている", to="jinji.html", tolabel="人事・総務の方へ",
      desc="相談窓口を置いても使われない、相談しても変わらないと思われている職場へ。社員の声が会社に届き、返事が戻る仕組み。",
      h1="「相談しても、どうせ変わらない」",
      lead="相談窓口を置いても使われない。その理由の多くは、話したことがどこにも届かないと思われているからです。",
      secs=[("置くだけの窓口が使われない理由", "相談した結果が見えないと、人は二度目の相談をしません。窓口があることを忘れてしまうこともあります。"),
            ("声が届き、返事が戻る仕組み", "30分の相談の最後に、会社に伝えたいことがあるかを伺います。伝える内容は本人が選び、個人が特定されにくい表現に整えて、一緒に確認してから会社に届けます。会社の受け止めは、次の機会に本人へお返しします。"),
            ("この制度での使い方", "届いた声と会社の対応を、社内に掲示できる1枚にまとめることもできます。「話せば変わる」が見えると、相談は増えていきます。")]),
 dict(file="stress-check-junbi.html", nav="50人未満のストレスチェック義務化に向けて", to="keieisha.html", tolabel="経営者の方へ",
      desc="労働者50人未満の事業場にもストレスチェックが義務化されます。検査の前後に、ふだんから話せる相手がいる体制づくりを。",
      h1="小さな会社にも、心の健康への備えが求められます。",
      lead="労働者50人未満の事業場にも、ストレスチェックの実施が義務づけられることが決まっています。検査だけでなく、ふだんから話せる相手がいる体制を整えておけます。",
      secs=[("何が変わるのか", "これまで努力義務だった50人未満の事業場でも、ストレスチェックの実施が必要になります。施行の時期や実施の方法は、厚生労働省の最新の案内をご確認ください。"),
            ("検査だけでは足りないこと", "検査は年に1度の確認です。日々の小さな気がかりを、不調になる前に話せる場所は、別に必要です。歯の治療と毎日の歯みがきが別であるのと同じです。"),
            ("この制度での使い方", "この窓口はストレスチェックの実施者ではなく、医療機関でもありません。仕事とキャリアの相談を、ふだんから受ける役割です。不調が疑われるときは、産業医や医療機関につなぎます。")]),
 dict(file="coaching-kaisha-futan.html", nav="コーチングを会社負担で受けたい", to="hataraku.html", tolabel="働くあなたへ",
      desc="コーチングやキャリア相談を、自己負担なしで受ける方法。会社に制度として導入してもらうための提案の進め方。",
      h1="コーチングを、会社の制度として受ける。",
      lead="もっと力を出したい。これからのキャリアを整理したい。その費用を自分で払い続けるのは大変です。会社の制度になれば、自己負担なしで使えます。",
      secs=[("会社にとっての利点", "社員が前向きに働き続けることは、会社にとっても得です。採用の場面でも、社外の専門家に相談できる制度は打ち出しになります。"),
            ("提案のしかた", "上司や人事に渡せる1枚の資料を用意しています。費用と手間がひと目で分かるので、そのまま見せられます。提案メールの文例もあります。"),
            ("名前を出さずに伝えたい場合", "会社名を教えていただければ、こちらから会社に案内します。あなたのお名前は一切伝えません。人数の少ない職場では推測されることがあるため、伝え方はあなたが選べます。")]),
]

GYOSHU = [
 dict(file="kaigo-fukushi.html", nav="介護・福祉の職場", to="jinji.html", tolabel="人事・総務の方へ", tag="業種から探す",
      desc="介護・福祉の職場で、利用者の相談を受ける職員が相談できる先を。社外の専属キャリアコンサルタントによる職員の相談と、管理者の支え。",
      h1="利用者の話を聴く職員にも、話を聴いてもらえる場所を。",
      lead="介護や福祉の仕事は、毎日誰かの気持ちを受け止める仕事です。受け止める側の職員が、自分の気持ちを話せる場所を、職場の外に置けます。",
      secs=[("この職場で起きやすいこと", "利用者やご家族への対応で、気持ちを張り続ける日が続きます。シフトがずれていて、同僚とゆっくり話す時間も取りにくい。小さなすれ違いが、そのまま退職の理由になることもあります。"),
            ("社外の相談相手にできること", "職場の人間関係、この先のキャリア、資格取得や働き方の迷いを、利害のない相手に話せます。施設長やリーダーの方も、職員対応の悩みを相談できます。"),
            ("この制度での使い方", "オンラインで30分なので、シフトの合間や勤務の前後に使えます。職員が望んだ声は、匿名で施設に届けます。職場の雰囲気づくりの手がかりになります。")]),
 dict(file="inshoku-shukuhaku.html", nav="飲食・宿泊の職場", to="keieisha.html", tolabel="経営者の方へ", tag="業種から探す",
      desc="飲食店・宿泊施設の店長やスタッフが、社外で仕事とキャリアを相談できる制度。人が定着しにくい職場の、辞める前の手当てに。",
      h1="忙しい現場ほど、話を聞く時間がない。",
      lead="お客様の対応で手一杯の日々の中で、スタッフ一人ひとりの気持ちまで聞く時間はなかなか取れません。その役割を、社外で引き受けます。",
      secs=[("この職場で起きやすいこと", "店長が売上もシフトも採用も抱え、スタッフの悩みを聞く余裕がない。若いスタッフが、何も言わずに来なくなる。店舗が分かれていると、本部からは現場の声が見えにくくなります。"),
            ("社外の相談相手にできること", "スタッフは、店の人に言いにくいことを話せます。店長は、スタッフとの関わり方や自分の働き方を相談できます。"),
            ("この制度での使い方", "スマートフォンから予約して、休憩時間や営業前後に30分。複数の店舗があっても、基本料は従業員100名まで一律です。")]),
 dict(file="it-remote.html", nav="IT・リモートワーク中心の職場", to="kanrishoku.html", tolabel="管理職の方へ", tag="業種から探す",
      desc="リモートワーク中心の会社で、雑談や相談の機会が減った社員に、社外で話せる相手を。オンライン30分のキャリア相談とコーチング。",
      h1="画面越しの職場では、小さな迷いが見えにくい。",
      lead="リモートワークでは、ちょっとした相談や雑談の機会が減ります。困っていることが、表に出る前に大きくなってしまう。オンラインで気軽に話せる社外の相手を置けます。",
      secs=[("この職場で起きやすいこと", "チャットでは用件しか話さない。1on1は進捗確認で終わってしまう。若手は、何が分からないのかを言葉にできないまま、一人で抱え込みがちです。"),
            ("社外の相談相手にできること", "技術や業務の話ではなく、働き方、キャリアの方向、チームでの居場所といった話を扱います。前向きなコーチングとして、目標の整理にも使えます。"),
            ("この制度での使い方", "すべてオンラインなので、いつもの働き方のまま使えます。管理職は、オンラインでの1on1の進め方を相談できます。")]),
 dict(file="shien-kikan.html", nav="支援機関・教育の職場", to="jinji.html", tolabel="人事・総務の方へ", tag="業種から探す",
      desc="就労支援、フリースクール、通信制高校などで、相談を受ける職員を支える社外の相談先。キャリアコンサルタントによるスーパーバイズ。",
      h1="支援する人を、支える人がいない。",
      lead="就労支援、フリースクール、学校。誰かの相談を受けることが仕事の職場では、職員自身の悩みは後回しになりがちです。相談を受ける人のための相談先を置けます。",
      secs=[("この職場で起きやすいこと", "利用者や生徒への対応に正解がなく、一人で抱え込む。職員の数が少なく、ケースについて落ち着いて振り返る時間が取れない。熱心な人ほど疲れてしまいます。"),
            ("社外の相談相手にできること", "キャリア相談、コーチング、不登校支援の現場で相談を受けてきた立場から、対応の振り返りと、職員自身の働き方の相談の両方を受けます。"),
            ("この制度での使い方", "職員の個別相談に加えて、月2回の担当者相談を、ケースの振り返りやチームの悩みの相談に使えます。")]),
]
NAYAMI = NAYAMI + GYOSHU

def nayami_links():
    a = "".join(f'<a href="{n["file"]}">{n["nav"]}</a>' for n in NAYAMI if n.get("tag") != "業種から探す")
    b = "".join(f'<a href="{n["file"]}">{n["nav"]}</a>' for n in GYOSHU)
    return (f'<section class="band"><div class="wrap"><h2>お悩みから探す</h2><div class="others" style="margin-top:18px">{a}'
            f'<a href="shindan.html">3分診断：相談が届く職場か</a><a href="mitsumori.html">費用の試算と提案ページ</a></div>'
            f'<h2 style="margin-top:32px">業種から探す</h2><div class="others" style="margin-top:18px">{b}</div></div></section>')


def nayami_page(n):
    secs = "".join(f'<div class="card"><h3>{h}</h3><p>{t}</p></div>' for h, t in n["secs"])
    return (head(n["nav"], n["desc"]) + bar("") +
            f'<header class="hero"><div class="wrap"><div><p class="tag">{n.get("tag", "お悩みから探す")}</p><h1>{n["h1"]}</h1><p class="lead">{n["lead"]}</p>'
            f'<div class="cta"><a class="btn" href="{n["to"]}">{n["tolabel"]}の案内を見る</a><a class="btn sub" href="shindan.html">3分診断を試す</a></div></div>'
            f'<div>{hero_svg("#8ec9e8", "#ffc56b")}</div></div></header>'
            f'<section><div class="wrap"><div class="grid">{secs}</div></div></section>'
            '<section class="band"><div class="wrap"><h2>料金</h2><p class="sub">月額基本料15,000円、相談1回30分5,000円（税別）。最初の3か月はいつでも解約できます。</p>'
            '<div class="cta"><a class="btn" href="index.html">サービスの全体を見る</a><a class="btn sub" href="mitsumori.html">費用を試算する</a></div></div></section>'
            + nayami_links() + FOOT)

SHINDAN_Q = ["社員が、上司以外に仕事の悩みを話せる相手がいる。", "直近1年で、退職する人から理由を率直に聞けた。", "管理職に、部下対応の悩みを相談できる相手がいる。",
             "社員の声を受けて会社が変えたことを、社員に伝えている。", "入社後3か月以内に、上司以外と話す機会を設けている。", "人事・総務の担当者に、相談相手がいる。",
             "経営者自身に、利害のない相談相手がいる。", "社員が匿名で意見を伝える方法がある。"]
SHINDAN = (head("3分診断：相談が届く職場か", "8つの質問に答えると、社員の声が会社に届きやすい職場かどうかの目安が分かります。") + bar("") +
 '<header class="hero"><div class="wrap" style="grid-template-columns:1fr"><div><p class="tag">3分診断</p><h1>相談が届く職場か</h1>'
 '<p class="lead">8つの質問に、いまの職場を思い浮かべて答えてください。簡易的な目安で、専門的な診断ではありません。</p></div></div></header>'
 '<section><div class="wrap"><form id="sf">' +
 "".join(f'<fieldset class="q"><legend>{i+1}. {q}</legend>'
         f'<label><input type="radio" name="q{i}" id="q{i}y" value="1"> はい</label>'
         f'<label><input type="radio" name="q{i}" id="q{i}n" value="0"> いいえ</label>'
         f'<label><input type="radio" name="q{i}" id="q{i}u" value="0"> 分からない</label></fieldset>' for i, q in enumerate(SHINDAN_Q)) +
 '<button class="btn" type="submit">結果を見る</button><p class="small" id="sf-msg" style="margin-top:10px"></p></form>'
 '<div id="res" class="card p1" hidden style="margin-top:24px"><h3 id="res-t"></h3><p id="res-b"></p>'
 '<div class="cta"><a class="btn" href="index.html">サービスの全体を見る</a><a class="btn sub" href="mitsumori.html">費用を試算する</a><a class="btn sub" href="' + FORMS["setsumei"] + '">資料を受け取る</a></div></div></div></section>'
 '<script>(function(){var f=document.getElementById("sf");f.addEventListener("submit",function(e){e.preventDefault();var n=' + str(len(SHINDAN_Q)) + ',s=0,a=0;'
 'for(var i=0;i<n;i++){var r=f.querySelector("input[name=q"+i+"]:checked");if(r){a++;s+=+r.value;}}'
 'var m=document.getElementById("sf-msg");if(a<n){m.textContent="まだ答えていない質問が"+(n-a)+"つあります。";return;}m.textContent="";'
 'var t,b;if(s>=6){t="声が届きやすい職場です（はい "+s+" / 8）";b="相談の経路がすでにいくつかあります。足りない経路がないか、「いいえ」と答えた項目を見直してみてください。社外の相談先は、いまある経路を補う役割になります。";}'
 'else if(s>=3){t="一部で声が止まっているかもしれません（はい "+s+" / 8）";b="届く経路と届かない経路が混ざっています。特に、相談を受ける側（管理職、人事、経営者）に相談先があるかを確かめてください。";}'
 'else{t="声が届きにくい状態かもしれません（はい "+s+" / 8）";b="社員が話せる相手と、話した結果が見える仕組みの両方が少ない状態です。最初の一歩として、社外に1つ相談先を置くことを検討できます。";}'
 'document.getElementById("res-t").textContent=t;document.getElementById("res-b").textContent=b;var r=document.getElementById("res");r.hidden=false;r.scrollIntoView({behavior:"smooth"});});})();</script>'
 + nayami_links() + FOOT)

MITSUMORI = (head("費用の試算と提案ページ", "会社名、従業員数、想定の相談件数を入れると、年間費用の目安と導入スケジュールを1枚で確認・印刷できます。") + bar("") +
 '<div class="wrap"><div class="tool"><b>会社に合わせた提案ページを作る</b>'
 '<div><label for="m-co">会社名</label><input id="m-co" placeholder="例：株式会社サンプル"></div>'
 '<div><label for="m-n">月の相談件数の見込み</label><input id="m-n" type="number" min="0" value="4"></div>'
 '<div><label for="m-h">年間の入社予定人数（入社後フォロー面談を行う場合。行わない場合は0）</label><input id="m-h" type="number" min="0" value="0"></div>'
 '<div><button class="btn" id="m-print" type="button">印刷する（PDF保存も可）</button></div>'
 '<p class="small" style="margin:0">ボタンが動かないときは、ブラウザの印刷（Ctrl+P または ⌘+P）を使ってください。</p></div></div>'
 '<div class="sheet"><p class="co"><span id="m-name"></span> 御中</p><h1>社外キャリア相談制度 ご提案と費用の目安</h1>'
 '<div class="tb"><table><tr><th>月額基本料</th><td>15,000円 × 12か月 ＝ <b>180,000円</b></td></tr>'
 '<tr><th>個別相談</th><td>月 <span id="m-n2"></span>件 × 5,000円 × 12か月 ＝ <b id="m-s"></b></td></tr>'
 '<tr><th>入社後フォロー面談</th><td><span id="m-h2"></span>人 × 3回 × 5,000円 ＝ <b id="m-f"></b></td></tr>'
 '<tr><th>年間の目安</th><td><b id="m-t" style="font-size:20px"></b>（税別。相談は使った分だけのご請求です）</td></tr></table></div>'
 '<h3 style="margin-top:18px">導入の流れ</h3><ol class="steps"><li><span>30分のオンライン説明。</span></li><li><span>申込フォームと電子契約。</span></li>'
 '<li><span>案内チラシを社員の方に配る。説明会は不要です。</span></li><li><span>社員の方が直接予約し、相談が始まる。</span></li></ol>'
 '<h3 style="margin-top:18px">お約束</h3><ul style="margin:6px 0 0;padding-left:1.2em"><li>相談内容は会社に伝えません。会社に届くのは件数と、本人が望んだ声だけです。</li>'
 '<li>月額15,000円は先着3社までの価格です。継続しているあいだは、更新後も据え置きます。</li><li>最初の3か月は、いつでも解約できます。</li><li>不調が疑われる場合は、産業医や医療機関につなぎます。</li></ul>'
 f'<p class="small" style="margin-top:16px">担当：{NAME}（国家資格キャリアコンサルタント）</p></div>'
 '<script>(function(){var q=new URLSearchParams(location.search),c=document.getElementById("m-co"),n=document.getElementById("m-n"),h=document.getElementById("m-h");'
 'if(q.get("c"))c.value=q.get("c");if(q.get("n"))n.value=q.get("n");if(q.get("h"))h.value=q.get("h");'
 'function yen(x){return x.toLocaleString("ja-JP")+"円";}function d(){var a=Math.max(0,+n.value||0),b=Math.max(0,+h.value||0),s=a*5000*12,f=b*3*5000;'
 'document.getElementById("m-name").textContent=c.value||"（会社名）";document.getElementById("m-n2").textContent=a;document.getElementById("m-h2").textContent=b;'
 'document.getElementById("m-s").textContent=yen(s);document.getElementById("m-f").textContent=yen(f);document.getElementById("m-t").textContent=yen(180000+s+f);}'
 '[c,n,h].forEach(function(e){e.addEventListener("input",d);});d();'
 'document.getElementById("m-print").addEventListener("click",function(){try{window.print();}catch(e){}});})();</script>' + FOOT)

UNEI = (head("運営者情報・個人情報の取り扱い", "社外の専属キャリアコンサルタントの運営者情報と、個人情報の取り扱いについて。") + bar("") +
 '<header class="hero"><div class="wrap" style="display:block"><p class="tag">運営者情報</p><h1>運営者情報・個人情報の取り扱い</h1></div></header>'
 '<section><div class="wrap"><h2>運営者</h2><div class="tb"><table>'
 + (f'<tr><th>屋号</th><td>{YAGO}</td></tr>' if YAGO else '') +
 f'<tr><th>運営・担当</th><td>{NAME}（たけむら しょうた）</td></tr><tr><th>資格</th><td>国家資格キャリアコンサルタント' + (f'（登録番号 {REG_NO}）' if REG_NO else '') + '</td></tr>'
 '<tr><th>拠点</th><td>東京都・三重県（ご相談はすべてオンラインです）</td></tr>'
 '<tr><th>提供するもの</th><td>会社と契約する社外のキャリア相談・コーチング</td></tr>'
 f'<tr><th>お問い合わせ</th><td><a href="{FORM_SHIRYO}">お問い合わせフォーム</a>からお送りください。2営業日以内にお返事します。</td></tr></table></div></div></section>'
 '<section class="band"><div class="wrap"><h2>個人情報の取り扱い</h2>'
 '<ol class="steps"><li><span>お預かりする情報は、お名前、会社名、連絡先、予約の日時、相談の際の手書きのメモです。</span></li>'
 '<li><span>使う目的は、相談の実施、予約や請求の連絡、ご本人が承認した声を会社に届けることに限ります。</span></li>'
 '<li><span>相談の内容は、ご本人の同意なく、会社を含む第三者に伝えません。ただし、命や安全に関わる差し迫った状況では、本人を守るために必要な相手へ連絡することがあります。</span></li>'
 '<li><span>録音や録画はしません。手書きのメモは、ほかの人が見られない形で保管し、契約の終了後に廃棄します。</span></li>'
 '<li><span>会社に届ける文面を整えるときにAIを補助として使うことがあります。その場合はお名前など個人が分かる情報を入力しません。</span></li>'
 '<li><span>予約にはTimeRex、ビデオ通話にはZoom、お問い合わせにはGoogleフォームを使います。</span></li>'
 + ('<li><span>サイトの改善のため、Cloudflare Web Analyticsで訪問数を計測しています。Cookieは使わず、個人を特定する情報は集めません。</span></li>' if CF_TOKEN else '') + '<li><span>ご自身の情報の確認や削除を希望される場合は、お問い合わせフォームからご連絡ください。</span></li></ol></div></section>' + FOOT)

SHAROUSHI = (head("社会保険労務士の先生へ｜顧問先の社員面談をお手伝いします", "顧問先の社員のキャリア相談・面談を、国家資格キャリアコンサルタントがオンラインで引き受けます。手続きと制度は先生に、面談は担当者に、という分担です。") + bar("") +
 '<header class="hero"><div class="wrap" style="display:block"><p class="tag">社会保険労務士の先生へ</p><h1>顧問先の社員面談を、お手伝いします</h1>'
 '<p class="lead">手続きと制度づくりは先生に。社員一人ひとりとの面談は、社外のキャリアコンサルタントに。顧問先に「社外の相談窓口」を、先生のご紹介で用意できます。</p></div></header>'
 '<section><div class="wrap"><h2>こんなときに</h2><ul class="worry">'
 '<li>顧問先から「社員の定着」や「若手の離職」の相談を受けるが、一人ひとりの面談までは手が回らない。</li>'
 '<li>キャリアコンサルティングが要件になる取り組みで、面談の担い手を探している。</li>'
 '<li>社員の不満が、労務の問題になる前に拾える仕組みを、顧問先に勧めたい。</li></ul></div></section>'
 '<section class="band"><div class="wrap"><h2>分担のかたち</h2><div class="tb"><table>'
 '<tr><th>先生</th><td>就業規則、制度づくり、手続き、助成金の申請</td></tr>'
 '<tr><th>担当者（竹村）</th><td>社員との個別面談（オンライン・1回30分）、窓口担当の方の相談、本人が承認した声の匿名での受け渡し</td></tr>'
 '<tr><th>顧問先</th><td>案内チラシを社員に配るだけ。説明会は不要です</td></tr></table></div>'
 '<p class="small" style="margin-top:12px">面談で労務や制度の課題が見えたときは、本人の同意の範囲で顧問先に伝え、手続きや制度のことは先生にご相談いただくよう案内します。労務の相談や手続きを、こちらで扱うことはありません。</p></div></section>'
 '<section><div class="wrap"><h2>先生にとっての利点</h2><div class="grid">'
 '<div class="card"><h3>顧問サービスの厚みが増す</h3><p>「社外の相談窓口も紹介できる」ことを、先生の提案の一つにしていただけます。</p></div>'
 '<div class="card"><h3>問題の芽を早く知れる</h3><p>辞める前、揉める前の声が、匿名で会社に届きます。制度の見直しのきっかけになります。</p></div>'
 '<div class="card"><h3>手間は増えません</h3><p>契約と運営は、顧問先とこちらで直接行います。先生に事務の負担はかかりません。</p></div></div>'
 '<p class="small" style="margin-top:14px">ご紹介への謝礼のやりとりは行いません。ご紹介いただいた顧問先には、基本料1か月分を無料にします。</p></div></section>'
 '<section class="band"><div class="wrap"><h2>料金（顧問先のご負担）</h2><div class="tb"><table>'
 '<tr><th>月額基本料</th><td>15,000円（先着3社の価格。窓口担当の方の相談 月2回を含む）</td></tr><tr><th>個別相談</th><td>1回30分 5,000円。使った分だけ</td></tr>'
 '<tr><th>契約</th><td>12か月の自動更新。最初の3か月はいつでも解約できます</td></tr></table></div>'
 '<div class="cta"><a class="btn" href="index.html">サービスの全体を見る</a>'
 f'<a class="btn sub" href="{FORM_SHIRYO}">15分、話を聞いてみる</a></div></div></section>' + FOOT)

MIHON_ITEMS = [
 ("社員向けの案内", "01_社員向け案内", "5分",
  "社外の相談窓口ができたことを、全社員に知らせる案内文。",
  """【社外の相談窓口ができました】

仕事のこと、これからのこと、人間関係のこと。
社内の人には少し話しにくいことを、社外のキャリアコンサルタントに相談できるようになりました。

・1回30分、オンラインで話せます
・誰が相談したかは、会社にはわかりません
・予約は、下のQRコードから自分でできます

「こんなことで相談していいのかな」と思うくらいのことで大丈夫です。
困ったとき、迷ったときの選択肢の一つとして、覚えておいてください。

問い合わせ：総務部　〇〇"""),
 ("求人票の、最初の一文", "02_求人票の下書き", "10分",
  "製造スタッフの求人票の冒頭に置く一文を3案。",
  """案1　「覚えるまで、何度聞いても大丈夫です。」
　　　未経験の方が最初に気にすることに、まっすぐ答える一文。

案2　「毎朝、できたての匂いの中で働けます。」
　　　仕事の手ざわりが伝わる一文。食品の製造ならでは。

案3　「35人の会社なので、全員の顔と名前がわかります。」
　　　小さな会社の良さを、そのまま強みにする一文。"""),
 ("やさしい日本語への言い換え", "08_やさしい日本語への言い換え", "5分",
  "健康診断のお知らせを、外国籍の社員にも伝わる形に。",
  """【元の文】
定期健康診断を下記の日程で実施いたしますので、対象者は所定の問診票に記入の上、当日持参してください。前日21時以降の飲食は控えてください。

【やさしい日本語】
けんこうしんだん（体（からだ）のチェック）があります。

・日（ひ）：12月3日（水）
・時間（じかん）：9時（じ）から
・場所（ばしょ）：2階（かい）の会議室（かいぎしつ）
・持（も）って来（く）るもの：問診票（もんしんひょう）※紙（かみ）に書（か）いて持って来てください

前（まえ）の日（ひ）の夜（よる）9時から、食（た）べたり飲（の）んだりしないでください。水（みず）は飲んでもいいです。

※「水は飲んでもいい」は、健診の実施機関に確認してから載せます。"""),
 ("新入社員の最初の1か月ガイド", "03_新入社員の最初の1か月ガイド", "10分",
  "入社した人に渡すガイドの目次と、一部の抜粋。",
  """【目次】
1. ようこそ、みどり台フーズへ
2. 最初の1週間の予定
3. 1か月でできるようになること
4. 困ったときは
5. よくある質問

【「4. 困ったときは」より】
分からないことを聞くのは、仕事の一部です。
同じことを2回聞いても、3回聞いても大丈夫です。

・仕事の手順のこと → 教育係の先輩（　　　　）
・体調や勤務時間のこと → 上司（　　　　）
・会社の人には話しにくいこと → 社外の相談窓口（予約はQRコードから）"""),
 ("管理職の、最初の1on1", "10_管理職の最初の1on1準備", "10分",
  "管理職になったばかりの人が、部下との最初の1on1で使う言い方と質問。",
  """【この時間の目的の伝え方（3案）】
・「評価の時間ではなくて、困っていることを一緒に片づける時間にしたいと思っています」
・「私もこの役割は初めてなので、どうしたら働きやすいか教えてほしいです」
・「月に1回、30分だけ。話したいことがない日は、早く終わってもいいです」

【話しやすくなる質問（一部）】
・最近の仕事で、うまくいったことは何ですか
・やりにくいと感じていることはありますか
・私にしてほしいこと、やめてほしいことはありますか"""),
 ("退職の申し出を受けたときの準備", "09_退職の申し出を受けたときの準備", "10分",
  "部下から「辞めたい」と言われた上司が、次の面談の前に読むメモ。",
  """【面談の目的】
本人の考えを正確に聴き、会社としてできることとできないことを整理する。

【聴くための質問（一部）】
・そう考えるようになったのは、いつごろからですか
・いちばん大きな理由を一つ挙げるとしたら、何ですか
・もし何かが変わるとしたら、考えは変わりそうですか

【言わないほうがよい言葉】
・「今辞めたら、どこに行っても通用しないよ」（脅しに聞こえる）
・「みんな我慢しているんだから」（本人の話を聴いていない、と受け取られる）

※手続きや法律に関わることは、社労士に確認します。"""),
 ("上司に見せる提案メモ", "07_上司への提案メモ", "10分",
  "社外の相談窓口を入れたい担当者が、社長に見せる1枚の骨子。",
  """【結論】社外の相談窓口を、3か月だけ試したいです。

【今の課題】この1年で、入社3年以内の社員が4人辞めた。辞める前に相談できる場がなかった。
【提案】月15,000円＋相談1回5,000円の社外窓口。担当者（総務）の相談も含む。
【手間】案内チラシを配るだけ。説明会は不要。
【心配への答え】最初の3か月はいつでもやめられる。3か月後に、社員アンケートで続けるか判断する。
【お願いしたい判断】12月からの試験導入の可否。

※数字は架空です。実際は御社の事実だけで作ります。"""),
 ("社内アンケート", "05_社内アンケート", "5分",
  "相談窓口を試した3か月後に、社員に聞く3問。",
  """Q1. 社外の相談窓口があって、よかったと思いますか
　□ とても思う　□ 思う　□ どちらでもない　□ 思わない

Q2. この窓口を、これからも残してほしいですか
　□ ぜひ残してほしい　□ あってもよい　□ なくてもよい

Q3. ひとことあれば、どうぞ（任意）

※匿名です。少人数のため、部署ごとの集計はしません。"""),
]

def _mihon_card(t, tool, mins, lead, body):
    b = body.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    return (f'<div class="card mcard"><h3>{t}</h3><p class="small">{lead}<br>使った指示書：{tool.split('_',1)[0]}番（{tool.split('_',1)[1]}）　かかった時間の目安：{mins}</p>'
            f'<div class="mihon">{b}</div></div>')

MIHON = (head("AIで作れるものの見本｜一人人事のための道具箱", "AIが苦手な人事・研修担当の方と、画面を共有しながら一緒に作ります。社員向けの案内、求人票、やさしい日本語、1on1の準備など、架空の会社で作った見本です。") + bar("mihon.html") +
 '<header class="hero"><div class="wrap" style="display:block"><p class="tag">AIで作れるもの</p><h1>こんなものが、30分で一緒に作れます</h1>'
 '<p class="lead">AIが苦手でも大丈夫です。画面を共有しながら、質問に答えていただくだけで、下書きができあがります。下は、架空の会社（食品の製造・35名）で実際にAIで作った見本です。</p></div></header>'
 '<section><div class="wrap"><h2>一緒に作る、3つの段階</h2><ol class="steps">'
 '<li><span><b>一緒に作る</b><br>画面を共有しながら、AIの質問に答えていただきます。その場で下書きができあがります。</span></li>'
 '<li><span><b>使い方を覚える</b><br>月2回の相談の中で、ご自身の手で動かしてみます。分からないことはチャットでいつでも。</span></li>'
 '<li><span><b>自分で回す</b><br>御社用に整えた「指示書」一式をお渡しします。次からは、AIに貼るだけで作れます。</span></li></ol></div></section>'
 '<section class="band"><div class="wrap"><h2>見本</h2><p class="sub">実際には、御社の情報で作ります。AIの下書きは、必ず人が読んで確かめてから使います。社員の名前など、個人が分かる情報はAIに入力しません。</p>'
 '<div class="grid g2">' + "".join(_mihon_card(*x) for x in MIHON_ITEMS) + '</div></div></section>'
 '<section><div class="wrap"><h2>ほかにも、作れるもの</h2><ul class="worry">'
 '<li>研修の進行表とスライドの骨子</li><li>面談の記録シート</li><li>社員向けのよくある質問集（就業規則をもとに）</li><li>月に1度の社内のお便り</li></ul>'
 '<p class="small" style="margin-top:12px">「こういうものがあったら」というご要望から、一緒に新しく作ることもできます。</p>'
 f'<div class="cta"><a class="btn" href="{FORM_SHIRYO}">まずは話を聞いてみる（30分・無料）</a><a class="btn sub" href="index.html">サービスの全体を見る</a></div></div></section>' + FOOT)

def more_pages():
    out = {n["file"]: nayami_page(n) for n in NAYAMI}
    out.update({"shindan.html": SHINDAN, "mitsumori.html": MITSUMORI, "unei.html": UNEI, "sharoushi.html": SHAROUSHI, "mihon.html": MIHON})
    return out


os.makedirs(OUT, exist_ok=True)
files = {p["file"]: page(p) for p in PAGES}
files.update({"annai.html": ANNAI, "teian.html": TEIAN, "style.css": CSS})
files.update(more_pages())
_pages = sorted(k for k in files if k.endswith(".html"))
files["sitemap.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"<url><loc>{SITE}{'' if k == 'index.html' else k}</loc></url>\n" for k in _pages) + "</urlset>\n")
files["robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n"
for name, body in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
import shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
if os.path.isdir(src):
    for f in os.listdir(src):  # 画像はフォルダに分けず、ページと同じ場所に置く（GitHubのアップロードでフォルダが崩れるため）
        shutil.copy(os.path.join(src, f), os.path.join(OUT, f))
print("\n".join(sorted(files)))
