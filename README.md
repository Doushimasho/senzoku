# 法人向けサイト（専属キャリアコンサルタント契約）

## GitHubで公開する手順
1. GitHubにログインし、右上の「+」から「New repository」を選ぶ。
2. Repository name に好きな名前（例：senzoku）を入れ、Public を選んで「Create repository」を押す。
3. 作成後の画面で「uploading an existing file」を押す。
4. このフォルダの中身（index.html などのファイルと img フォルダ）をすべてドラッグして入れ、「Commit changes」を押す。
5. リポジトリの「Settings」→「Pages」を開く。
6. 「Branch」で main と /(root) を選び、「Save」を押す。
7. 数分待つと、同じ画面に公開URL（https://アカウント名.github.io/リポジトリ名/）が表示される。

## ページの直し方
- 文章やページ構成は build.py の中にある。直したら `python3 build.py 出力フォルダ` で全ページを作り直す。
- フォームや予約ページのURLが決まったら、build.py の FORMS を書き換える。
- 写真は img フォルダに入れる。

## ファイル
- index.html：トップ
- keieisha.html / jinji.html / saiyo.html / kanrishoku.html / hataraku.html：相手別ページ
- annai.html：社員向け案内チラシ（会社名と予約URLを入れるとQRコード付きのA4になる）
- teian.html：上司に見せる提案資料（A4）
