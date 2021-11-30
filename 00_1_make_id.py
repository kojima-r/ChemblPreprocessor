import sqlite3

#dbname = 'data/exported.db'
dbname = 'chembl-exporter/data_29/exported-full.db'
out_path = 'data_29/'
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute('SELECT id,assay_chembl_id,target_chembl_id,compound_chembl_id  \
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

with open(out_path+"id.tsv","w") as fp:
    fp.write("\t".join(["id","assay_chembl_id","target_chembl_id","compound_chembl_id"]))
    fp.write("\n")
    for x in c.fetchall():
        fp.write("\t".join(map(str,x)))
        fp.write("\n")
for desc in c.description:
    print(desc[0])

# DBとの接続を閉じる(必須)
conn.close()

fp=open(out_path+"id.tsv")
h=next(fp)
mapping={i:k for i,k in enumerate(h.strip().split("\t"))}
data={k:[] for k in h.strip().split("\t")}
for line in fp:
    arr=line.strip().split("\t")
    for i in range(0,4):
        data[mapping[i]].append(arr[i])

for k,v in data.items():
    print(k,len(set(v)))


