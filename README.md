# 法人向けサイト（専属キャリアコンサルタント契約）

## GitHubで公開する手順
1. GitHubにログインし、右上の「+」から「New repository」を選ぶ。
2. Repository name に好きな名前（例：senzoku）を入れ、Public を選んで「Create repository」を押す。
3. 作成後の画面で「uploading an existing file」を押す。
4. このフォルダの中身（index.html などのファイル）をすべてドラッグして入れ、「Commit changes」を押す。
5. リポジトリの「Settings」→「Pages」を開く。
6. 「Branch」で main と /(root) を選び、「Save」を押す。
7. 数分待つと、同じ画面に公開URL（https://アカウント名.github.io/リポジトリ名/）が表示される。

## ページの直し方
- 文章やページ構成は build.py の中にある。直したら `python3 build.py 出力フォルダ` で全ページを作り直す。
- GoogleフォームのURLは、build.py の上のほうにある FORM_MOSHIKOMI、FORM_SHIRYO、FORM_SUISEN の3か所に入れる。入れて作り直すと、全ページのボタンがフォームにつながる。
- 写真は sitebuild の img フォルダに入れておくと、作り直したときにページと同じ場所へコピーされる（公開側ではフォルダに分けない）。

## ファイル
- index.html：トップ
- keieisha.html / jinji.html / saiyo.html / kanrishoku.html / hataraku.html：相手別ページ
- annai.html：社員向け案内チラシ（会社名と予約URLを入れるとQRコード付きのA4になる）
- teian.html：上司に見せる提案資料（A4）

## 追加したページ
- wakate-rishoku.html / kanrishoku-hihei.html / keieisha-sodan.html / sodan-kawaranai.html / stress-check-junbi.html / coaching-kaisha-futan.html：悩み別ページ
- shindan.html：3分診断「相談が届く職場か」
- mitsumori.html：会社別の費用試算と提案ページ。URLの末尾に ?c=会社名&n=月の相談件数&h=入社予定人数 を付けると、入力済みの状態で開く

## 更新のしかた
新しいファイル一式を、リポジトリの「Add file」→「Upload files」に同じようにドラッグすると、同じ名前のファイルが上書きされる。

## 検索と共有の設定
- sitemap.xml：Google Search Console にこのサイトを登録し、「サイトマップ」に sitemap.xml を送信すると、全ページが検索に載りやすくなる。
- img/ogp.jpg：XやLINEでURLを共有したときに出る画像。
