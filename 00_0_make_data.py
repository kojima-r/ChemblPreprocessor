import sqlite3
import collections

#dbname = 'data/exported.db'
dbname = 'chembl-exporter/data_29/exported-full.db'
out_path="data_29/"
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
c = conn.cursor()

items=["id",
    "target_chembl_id","compound_chembl_id",
    "smiles",   
    "target_sequence",
    "pchembl_value",
    ]

c.execute("select "+",".join(items)+' \
    FROM activities \
    WHERE standard_type IN ("IC50", "Ki", "EC50", "Kd") \
    AND valid = 1 \
    AND target_accession IN ( \
                SELECT target_accession FROM activities \
                WHERE valid = 1 \
                AND standard_type IN ("IC50", "Ki", "EC50", "Kd") \
                GROUP BY target_accession \
                HAVING COUNT(*) >= 100 \
    )')


with open(out_path+"data.tsv","w") as fp:
    fp.write("\t".join(items))
    fp.write("\n")
    for x in c.fetchall():
        fp.write("\t".join(map(str,x)))
        fp.write("\n")
# DBとの接続を閉じる(必須)
conn.close()

