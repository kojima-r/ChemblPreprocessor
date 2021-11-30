import sqlite3
import collections

#dbname = 'data/exported.db'
dbname = 'chembl-exporter/data_29/exported-full.db'
out_path = 'data_29/'
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
c = conn.cursor()

items=["id",
    "assay_type", # 'F', 'B', 'A', 'P', 'T' and 'U'
    "assay_test_type",# 'In vitro' and 'In vivo'
    "assay_category", # 'confirmatory' and 'screening'
    "assay_organism", # 'Homo sapiens' and 'Musmusculus'
    "assay_tax_id",   
    "assay_strain",   # Sprague-Dawley' and 'Wistar'
    "assay_tissue",   # 'Plasma' and 'Liver'
    "assay_cell_type",# 'HEK293' and 'MCF7'
    "assay_subcellular_fraction", # 'Microsome' and 'Membrane'
    "target_type",            #'SINGLE PROTEIN' and 'ORGANISM'.
    "target_accession",       # Uniprot
    "target_sequence_length", # 
    "target_classification1", # 
    "target_classification2",
    "target_classification3",
    "target_classification4",
    "target_classification5",
    "target_classification6",
    #"standard_type",  #'Potency', 'GI50' and 'IC50'
    #"standard_relation",
    #"standard_value",
    #"standard_units",
    "pchembl_value",
    "compound_num_atoms",
    "compound_mol_weight",
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

with open(out_path+"meta.tsv","w") as fp:
    fp.write("\t".join(items))
    fp.write("\n")
    for x in c.fetchall():
        fp.write("\t".join(map(str,x)))
        fp.write("\n")
# DBとの接続を閉じる(必須)
conn.close()
cat_items=[
    "assay_type", # 'F', 'B', 'A', 'P', 'T' and 'U'
    "assay_test_type",# 'In vitro' and 'In vivo'
    "assay_category", # 'confirmatory' and 'screening'
    "assay_organism", # 'Homo sapiens' and 'Musmusculus'
    "assay_strain",   # Sprague-Dawley' and 'Wistar'
    "assay_tissue",   # 'Plasma' and 'Liver'
    "assay_cell_type",# 'HEK293' and 'MCF7'
    "assay_subcellular_fraction", # 'Microsome' and 'Membrane'
    "target_type",            #'SINGLE PROTEIN' and 'ORGANISM'.
    "target_classification1", # 
    "target_classification2",
    "target_classification3",
    "target_classification4",
    "target_classification5",
    "target_classification6",
    ]


fp=open(out_path+"meta.tsv")
h=next(fp)
mapping={k:i for i,k in enumerate(h.strip().split("\t"))}
data={k:[] for k in h.strip().split("\t")}
for line in fp:
    arr=line.strip().split("\t")
    for k in cat_items:
        data[k].append(arr[mapping[k]])


ofp=open(out_path+"meta_info.txt","w")
for k in cat_items:
    c = collections.Counter(data[k])
    print(k,len(c))
    ofp.write(k+"\t"+str(len(c)))
    ofp.write("\n")
    for key,val in c.items():
        ofp.write("\t"+str(key)+"\t"+str(val)+"\n")
    print(k,c)

