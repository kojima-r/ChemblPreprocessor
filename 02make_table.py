import joblib
from multiprocessing import Pool
import numpy as np

path="data_29"
fp=open(path+"/data.tsv")
ofp=open(path+"/dataset.tsv","w")
compound_feature=joblib.load(path+'/compound_features.pkl')
target_feature=joblib.load(path+ '/target_features.pkl')
target_feature_items=None
new_target_feature={}
for tid,v in target_feature:
    d={key:val for key,val in v}
    if target_feature_items is None:
        target_feature_items=list(d.keys())
    f=[d[i] for i in target_feature_items]
    new_target_feature[tid]=np.array(f)

    
c_feat_len=None
new_compound_feature={}
for cid,v in compound_feature:
    new_compound_feature[cid]=v 
    c_feat_len=len(v)
    
h=next(fp)
mapping={v:i for i,v in enumerate(h.strip().split("\t"))}
data=[]
new_compound_feature_tbl={cid: "\t".join(map(str,c_feat)) for cid,c_feat in new_compound_feature.items()}
new_target_feature_tbl={tid: "\t".join(map(str,t_feat)) for tid,t_feat in new_target_feature.items()}
for line in fp:
    arr=line.strip().split()
    rid=arr[mapping["id"]]
    cid=arr[mapping["compound_chembl_id"]]
    tid=arr[mapping["target_chembl_id"]]
    label_val=arr[mapping["pchembl_value"]]
    t_feat=new_target_feature_tbl[tid]
    c_feat=new_compound_feature_tbl[cid]
    data.append([rid,cid,tid,label_val,c_feat,t_feat])


###
ofp.write("\t".join(["id","c_id","p_id","label_val","label_5","label_6","label_7"]))
ofp.write("\t")
ofp.write("\t".join(["c_{:04d}".format(i) for i in range(c_feat_len)] ))
ofp.write("\t")
ofp.write("\t".join(["p_{}".format(i) for i in target_feature_items ]))
ofp.write("\n")
for el in data:
    rid,cid,tid,label_val,c_feat,t_feat=el
    ofp.write("\t".join([rid,cid,tid]))
    ofp.write("\t")
    ofp.write(str(label_val))
    ofp.write("\t")
    val=float(label_val)
    if val<=5:
        ofp.write("1\t")
    else:
        ofp.write("0\t")
    if val<=6:
        ofp.write("1\t")
    else:
        ofp.write("0\t")
    if val<=7:
        ofp.write("1\t")
    else:
        ofp.write("0\t")
    ofp.write(c_feat)
    ofp.write("\t")
    ofp.write(t_feat)
    ofp.write("\n")
