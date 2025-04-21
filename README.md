# NeXov
**"NeXov Enables eXtensible Observation of Vertices"**

NeXovは、非常に高密度のマルコフ連鎖モデルの構築や生成、可視化、またそれをサポートするデータ処理をNetworkXで実現するツールです。

## Install
OSごとに一部操作が異なります。
### Windows
以下のサイトにあるインストーラーを実行します。

https://github.com/ikegami-yukino/mecab/releases/tag/v0.996.2  (MeCab)  
https://graphviz.org/download/#windows  (Graphviz)

### Linux
以下のコマンドを実行します。
```shell
$ sudo apt update
$ sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8 graphviz
$ sudo cp /etc/mecabrc /usr/local/etc/mecabrc
```

### NEologd (推奨)
`MeCab`に固有名詞などを認識させるためのユーザー辞書です。これを使うだけでも精度はかなり上がるのでインストールをお勧めします。

Windows: https://qiita.com/xi_guisheng/items/40ee7da516de05e5894f  
Linux: https://blog.forestberrypi.com/tools-services/linux/mecab-in-ubuntu/#toc7

### NeXovのインストール (共通)
`pip`でNeXovをインストールできます。
```shell
$ pip install nexov
```

## Usage
NeXovには以下のような機能があり、それぞれ対応するコマンドがあります。

| Command | Feature |
|---------|---------|
| `tokenize` | テキストのトークン化 |
| `generate` | モデルの構築・生成...etc |
| `visualize` | モデルの可視化 |

```
usage: nexov [-h] {tokenize,generate,visualize} ...

NeXov Enables eXtensible Observation of Vertices

positional arguments:
  {tokenize,generate,visualize}
    tokenize            テキストをトークンに分割
    generate            モデルまたはテキストを生成
    visualize           モデルを画像として可視化

options:
  -h, --help            show this help message and exit
```

### tokenize
`tokenize`は、自動でテキストをトークン化するコマンドです。
#### オプション
```
usage: nexov tokenize [-h] -i INPUT [-o OUTPUT] [--method {mecab,char}]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        入力ファイル
  -o OUTPUT, --output OUTPUT
                        出力ファイル
  --method {mecab,char}
                        分割方法
```
#### 例
```shell
$ cat input.txt
ぐっもーにん！
もにもに！
もーにん！！
もにもに！！！！
おはですー！！
おはですー！
おはようです！！！！！！
$ nexov tokenize -i input.txt -o tokens.txt
[+] Wrote tokenized data to tokens.txt
$ cat tokens.txt
ぐっも ー に ん ！
も に も に ！
も ー に ん ！ ！
も に も に ！ ！ ！ ！
お は です ー ！ ！
お は です ー ！
おはよう です ！ ！ ！ ！ ！ ！
```
### generate
`generate`は、モデルの構築と生成、またインポート・エクスポートも行うコマンドです。
#### オプション
```
usage: nexov generate [-h] -i INPUT [-s START] [-l LENGTH] [-e EXPORT] [-v VISUALIZE]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        モデルまたはトークン済みデータファイル
  -s START, --start START
                        開始トークン
  -l LENGTH, --length LENGTH
                        生成するトークン数
  -e EXPORT, --export EXPORT
                        生成後のモデルをファイルにエクスポート
  -v VISUALIZE, --visualize VISUALIZE
                        生成と同時に可視化を実行(拡張子を除く出力ファイル名を指定)
```
#### 例
```shell
$ cat tokens.txt
ぐっも ー に ん ！
も に も に ！
も ー に ん ！ ！
も に も に ！ ！ ！ ！
お は です ー ！ ！
お は です ー ！
おはよう です ！ ！ ！ ！ ！ ！
$ nexov generate -i tokens.txt -s も -l 100
もにもにもにもーにもにん！おはです！おはですー！！！！もに！もにん！！もにん！おはですー！！！おはですー！！もー！おはようです！！！おはようです！！おはですーにもにもー！もに！！！！もにもーにん！！！おは です！！おはようですー！もにん！！

$ nexov generate -i tokens.txt -e model.json
[+] The model was exported to model.json
$ nexov generate -i model.json -s も -l 100
もーにん！おはですーにもにん！！！！おはですー！！！もにん！もにもにもー！もにん！！！！！もにもにん！！もーにもにん！！！！おはようですー！おはです！！！！！！おはようですーに！おはですーに！！！！おはよ うですー！もにもにもにん！おは
```

### visualize
`visualize`は、モデルを画像で可視化するコマンドです。
#### オプション
```
usage: nexov visualize [-h] -i INPUT -o OUTPUT [--font FONT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        モデルファイル
  -o OUTPUT, --output OUTPUT
                        出力ファイル(拡張子を除くファイル名を指定)
  --font FONT           使用するフォント
```
#### 例
```shell
$ nexov visualize -i model.json -o output
[+] The model visualization was saved to output.png
```
![output.png](tests/output.png)

## LICENSE
NeXovはMITライセンスで配布されています。

ただし、以下の外部ソフト・ライブラリを利用しています。これらはNeXovに含まれていませんが、別途インストールが必要です。

- MeCab (形態素解析器) : BSD License
- NEologd (日本語辞書) : Apache License 2.0
- Graphviz (グラフ描画ツール) : Eclipse Public License 1.0
- mecab-python3 (Pythonバインディング) : MIT License
- networkx : BSD License
- graphviz (Pythonラッパー) : MIT License
- matplotlib : Matplotlib License (BSDスタイル)

それぞれのライセンス条件に従ってご利用ください。
