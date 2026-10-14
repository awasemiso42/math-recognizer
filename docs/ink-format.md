# 手書きストロークの収集形式

suminoteのデバッグ専用収集モード（`app/src/debug`、リリースビルドには含まれない）が書き出す形式。
1行1サンプルのJSONL（UTF-8）。ファイル名は`math-ink-<日時>-<セッション>.jsonl`。

## サンプル

```json
{"format":"sumi-math-ink","version":1,
 "id":"0f6c…","session":"9a1e…","writer":"w-3fa2c1",
 "prompt":{"set":"v1","id":"e012","kind":"expression","latex":"\\frac{1}{3}+\\frac{1}{6}"},
 "canvas":{"widthPx":2400,"heightPx":1100,"density":2.0},
 "device":{"manufacturer":"Xiaomi","model":"23043RP34C","sdk":34},
 "createdAt":"2026-10-14T09:30:00Z",
 "strokes":[{"tool":"stylus","points":[[412.5,300.25,0.41,0],[413.0,301.5,0.45,8]]}]}
```

| フィールド | 内容 |
|---|---|
| `format`・`version` | 固定値`sumi-math-ink`と形式の版。互換のない変更で版を上げる。 |
| `id` | サンプルのUUID。 |
| `session` | 収集画面を開いてから閉じるまでのUUID。 |
| `writer` | 書き手の匿名ID（端末ごとに生成、または収集画面で入力したラベル）。氏名は記録しない。 |
| `prompt` | 書いたお手本。`set`はお手本集の版、`id`・`kind`（`symbol`/`expression`）・`latex`はお手本集の値。 |
| `canvas` | 書く欄の大きさ（px）と画面密度（`DisplayMetrics.density`）。 |
| `device` | `Build.MANUFACTURER`・`Build.MODEL`・`Build.VERSION.SDK_INT`。 |
| `createdAt` | 保存時刻（UTC、ISO 8601）。 |
| `strokes` | 書いた順のストローク。各ストロークは`tool`（`stylus`/`finger`）と点列。 |

点は`[x, y, pressure, t]`。

- `x`・`y`は書く欄の左上を原点とするpx（右・下が正）。**手ぶれ補正前の生の座標**で、
  MotionEventの履歴点も含む。suminote本体の`StrokeSmoother`は学習時に同じ処理を適用して再現する
  （補正の強さを変えて水増しにも使う）。
- `pressure`はMotionEventの値（0〜1に丸める）。
- `t`はサンプルの最初の点からのミリ秒。suminote本体の`Stroke`は時刻を保存しないため、
  **認識モデルは`t`を入力に使わない**。合成時の書き順・速度の参考に限る。

消去した・取り消したストロークは含めない。スキップしたお手本は保存しない。

## 本番の入力との違い

本番ではsuminoteの`Stroke`（文書座標・手ぶれ補正後・時刻なし）を認識器へ渡す。前処理で
平行移動・拡大縮小を正規化するため、座標系の違い（画面px／文書座標）は問題にならない。
