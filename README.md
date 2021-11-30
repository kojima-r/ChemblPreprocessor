
# おおもとのファイルsqliteは以下
Original data
Chemblはバージョンがどんどん上がっているので、version 27 だと以下のようなコマンドでダウンロードできる

```
wget https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_27/chembl_27_sqlite.tar.gz
```

version 29 だと以下のようなコマンドでダウンロードできる
```
wget https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_29_sqlite.tar.gz
```

バージョンごとに、以下のようなディレクトリに中間ファイル含め出力することを想定する
```
data_29/
```
デフォルトで`data_29`に出力するようになっているので、以下では`data_29`として説明する。
version 27にするには、スクリプト中の`path=data_29/`となっている部分を`path=data_27/`にする必要がある。

# 基本前処理済みsqliteファイルは以下
おおもとのファイルは様々なデータを含んでいるので、基本的な前処理によってデータベースを絞る
本プログラムはこちらを使うことを前提とする

# 必要前処理済みファイルは以下
上記のSqliteは使いにくい場合が多く、また、機械学習には不必要なデータも多く含んでいるため、
以下のtsvに変換する

- `data_29/data.tsv`：化合物タンパク質データ
- `data_29/id.tsv`: IDデータ
- `data_29/meta.tsv`: メタデータ
- `data_29/meta_info.txt`: メタデータ

これらのデータは以下で共有している
https://drive.google.com/file/d/18YavlDiaGwY0DFqiiz0M6ME2yH2PxO22/view?usp=sharing


### スクリプト
`00_<....>.py`はsqliteからこれら３つのファイルを作成する

### 必要ライブラリ
- sqlite3


# データセット作成

データセット作成処理は基本的には、上記の`data.tsv`さえあれば実行できる。（これらのデータは以下で共有している
https://drive.google.com/file/d/18YavlDiaGwY0DFqiiz0M6ME2yH2PxO22/view?usp=sharing　）
最終的には、`dataset.tsv`が出力される。


```
python 01make_feature.py
python 02make_table.py
```

### スクリプト
`data.tsv` から特徴量を計算（`01_<....>.py`）しテーブルtsvとして保存する（`02_<....>.py`）

### 必要ライブラリ
- protlearn
- rdkit
- joblib



