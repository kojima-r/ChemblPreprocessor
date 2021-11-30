import joblib
from protlearn.features import *
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdmolops import FastFindRings
import numpy as np
from multiprocessing import Pool
path="data_29"

feat_names =["ngram","aac","cksaap","aaindex1","ctd","ctdc","ctdt","ctdd","apaac"]
nondesc_feat_names=["moreau_broto","moran","geary"]
other_feat_names=["qso","socn","atc"]
def get_feat(x):
  feat_list=[]
  amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
  temp=""
  for aa in x:
    if aa in amino_acids:
      temp+=aa
    else:
      print("unnatual AA found:"+x)
  x=temp
  for name in feat_names:
    try:
      f=eval(name+"(x)")
      for v,k in zip(f[0][0],f[1]):
        kk=name+"-"+k
        feat_list.append((kk,v))
    except:
      print("skip:",name)

  for name in nondesc_feat_names:
    try:
      f=eval(name+"(x)")
      for i,v in enumerate(f[0]):
        kk=name+"-"+str(i)
        feat_list.append((kk,v))
    except:
      print("skip:",name)

  d0,d1,k=qso(x)
  for kk,v in zip(k,d0[0]):
    kkk="qso0-"+kk
    feat_list.append((kkk,v))
  for kk,v in zip(k,d1[0]):
    kkk="qso1-"+kk
    feat_list.append((kkk,v))

  s0,s1=socn(x)
  for i,v in enumerate(s0[0]):
    kkk="socn0-"+str(i)
    feat_list.append((kkk,v))
  for i,v in enumerate(s1[0]):
    kkk="socn1-"+str(i)
    feat_list.append((kkk,v))

  a0,a1=atc(x)
  for i,v in enumerate(a0[0]):
    kkk="atc0-"+str(i)
    feat_list.append((kkk,v))
  for i,v in enumerate(a1[0]):
    kkk="atc1-"+str(i)
    feat_list.append((kkk,v))

  return feat_list

def get_mol_feat(s):
    mol = Chem.MolFromSmiles(s)
    FastFindRings(mol)
    mfp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    mfp_vec = np.array([mfp.GetBit(i) for i in range(2048)], np.int32)
    return mfp_vec

def run_target(pair):
    tid,s=pair
    f=get_feat(s)
    if len(f)!=2261:
        print("feature error:",len(f),":",s)
    return tid,f

def run_compound(pair):
    cid,s=pair
    f=get_mol_feat(s)
    return cid,f


fp=open(path+"/data.tsv")
h=next(fp)
mapping={v:i for i,v in enumerate(h.strip().split("\t"))}
target_dict={}
compound_dict={}
data=[]
for line in fp:
    arr=line.strip().split()
    rid=arr[mapping["id"]]
    cid=arr[mapping["compound_chembl_id"]]
    tid=arr[mapping["target_chembl_id"]]
    if tid not in target_dict:
        s=arr[mapping["target_sequence"]]
        target_dict[tid]=s
    if cid not in compound_dict:
        s=arr[mapping["smiles"]]
        compound_dict[cid]=s
    data.append([rid,cid,tid])

with Pool(16) as p:
    compound_result=p.map(run_compound, compound_dict.items())
joblib.dump(compound_result,path+'/compound_features.pkl',compress=True)

with Pool(16) as p:
    target_result=p.map(run_target, target_dict.items())
joblib.dump(target_result,path+ '/target_features.pkl',compress=True)

