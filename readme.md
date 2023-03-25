# フェーズドアレイアンテナの電界合成シミュレータ

## 環境構築

### python をインストールする

バージョンは 3.10.8 を使用している

他のバージョンでは未検証

```
> python -V
Python 3.10.8
```

と出れば OK

### 必要なモジュールのインストールをする

pipenv を使用すると全て入る

```
pipenv sync
```

手動でインストールする場合は以下を入れる

- numpy
- matplotlib
- numba
- scipy

## 実行

0. config.csv にシミュレーションしたい条件を書く
1. シミュレータを実行
   - simulation.py を実行
   - result/simulation に実行結果のファイルが生成される
2. 描画を実行
   - show.py を実行
   - result/graph/x と result/graph/y にグラフの画像ファイルが生成される

## config.csv の書き方

### 関数で使用可能な変数

- x: アンテナ素子の x index
- y: アンテナ素子の y index

### 関数で使用可能な定数

- pi: 円周率

### 列の内容

- sim_theta
  - type: 符号なし整数
  - unit: none
  - 極角の解像度
- sim_phi
  - type: 符号なし整数
  - unit: none
  - 方位角の解像度()
- temp_func
  - type: 関数
  - unit: ℃
  - アンテナ素子の温度
- phase_func
  - type: 関数
  - unit: rad
  - アンテナ素子の位相
- power_func
  - type: 関数
  - unit: none(倍率)
  - アンテナ素子の利得
- x
  - type: 符号なし整数
  - unit: none
  - アンテナ素子の x 座標(アンテナ素子の間隔で正規化)
- y
  - type: 符号なし整数
  - unit: none
  - アンテナ素子の y 座標(アンテナ素子の間隔で正規化)
- z
  - type: 符号なし整数
  - unit: none
  - アンテナ素子の z 座標(アンテナ素子の間隔で正規化)
- array_num
  - type: 符号なし整数
  - unit: none
  - 一辺のアンテナ素子数
- reguler
  - type: Boolean(0 or 1)
  - unit: none
  - 最大値を 0dB として正規化するかどうか
- file_name
  - type: String
  - unit: none
  - シミュレーション結果につけるファイル名
