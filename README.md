
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


# 基本前処理済みsqliteファイルは以下
おおもとのファイルは様々なデータを含んでいるので、基本的な前処理によってデータベースを絞る
本プログラムはこちらを使うことを前提とする

# 必要前処理済みファイルは以下
上記のSqliteは使いにくい場合が多く、また、機械学習には不必要なデータも多く含んでいるため、
以下のtsvに変換する

- data.tsv：化合物タンパク質データ
- id.tsv: IDデータ
- meta.tsv: メタデータ

### スクリプト
`00_<....>.py`はsqliteからこれら３つのファイルを作成する

### 必要ライブラリ
- sqlite3


# データセット作成

データセット作成処理は基本的には、上記のdata.tsvさえあれば実行できる
```
python 01make_feature.py
python 02make_table.py
```
### スクリプト
data.tsvから特徴量を計算（`01_<....>.py`）しテーブルtsvとして保存する（`02_<....>.py`）

### 必要ライブラリ
- protlearn
- rdkit
- joblib



