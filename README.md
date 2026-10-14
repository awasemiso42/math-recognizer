# math-recognizer

suminoteで手書きした数式のストロークを認識し、[math-engine](https://github.com/awasemiso42/math-engine)で
計算できる式sourceへ変換する認識器です。対象は**関数電卓で打つ範囲**の式（四則・べき・根・初等関数・
対数・階乗・絶対値・積分・微分・極限・総和・関係式・小さな行列）で、入力は**ストロークのみ**です。
写真・画像からの認識は扱いません。

## 方針

- **オフライン・端末内で動作**します。対象端末はXiaomi Pad 6（Snapdragon 870）です。
- **商用利用できるデータだけ**で学習します。CROHME（研究目的のみ）・MathWriting（非営利）などの
  公開手書き数式データは使いません。学習データはsuminoteのデバッグ専用収集モードで集めた手書きと、
  それを組み合わせた合成データです。
- 認識器の出力はLaTeXの候補列です。各候補をmath-engineの`TeXInput.toSource`で式sourceへ変換し、
  解釈できる候補を優先します。LaTeXの解釈規則はmath-engineの
  [TeX入力の契約](https://github.com/awasemiso42/math-engine/blob/main/docs/specifications/tex-input.md)に従います。

```
suminoteの投げ縄選択 → ストローク列 → 前処理（正規化・間引き） → モデル → LaTeX候補（上位N件）
  → TeXInput.toSourceで検証・並べ替え → math-engine / sumicalcで評価
```

## 資料

- [手書きストロークの収集形式](docs/ink-format.md) — suminoteの収集モードが書き出すJSONLの形式。
- [認識する記号](docs/symbols.md) — 語彙と、収集する単独記号。
- [収集用のお手本](data/prompts/v1.json) — 単独記号と式のLaTeX。式は`tools/check_prompts.py`で
  math-engineが解釈できることを確認します。

## 予定

1. 収集形式・記号表・お手本（このリポジトリ）と、suminoteのデバッグ専用収集モード。
2. 収集データから式を合成するデータ生成（記号のストロークをTeXの配置規則で組み合わせる）。
3. ストローク列→LaTeXの小型モデル（数百万〜2千万パラメータ、量子化後5〜20MB）の学習とONNX書き出し。
4. Java 17の実行部（前処理・ONNX Runtime Android推論・候補検証）と、suminoteへの組み込み。

## お手本の検証

```sh
python3 tools/check_prompts.py path/to/math-engine.jar
```
