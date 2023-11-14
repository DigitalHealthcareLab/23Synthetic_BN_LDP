
#!/bin/bash

source ./bin/functions

#set_python_env
conda activate synthetic_data

echo "================ Post Processing DEAD_NFRM ================="
python3 src/3_postprocess/postprocess_dead_nfrm.py --epsilon 0.1
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_dead_nfrm.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_dead_nfrm.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_dead_nfrm.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_dead_nfrm.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing DG_RCNF ================="
python3 src/3_postprocess/postprocess_dg_rcnf.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_dg_rcnf.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_dg_rcnf.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_dg_rcnf.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_dg_rcnf.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing EX_DIAG ================="
python3 src/3_postprocess/postprocess_ex_diag.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_ex_diag.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_ex_diag.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_ex_diag.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_ex_diag.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing OPRT_NFRM ================="
python3 src/3_postprocess/postprocess_oprt_nfrm.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_oprt_nfrm.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_oprt_nfrm.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_oprt_nfrm.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_oprt_nfrm.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing PTH_BPSY ================="
python3 src/3_postprocess/postprocess_pth_bpsy.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_pth_bpsy.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_pth_bpsy.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_pth_bpsy.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_pth_bpsy.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing PTH_MLCR ================="
python3 src/3_postprocess/postprocess_pth_mlcr.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_pth_mlcr.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_pth_mlcr.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_pth_mlcr.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_pth_mlcr.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing PTH_MNTY ================="
python3 src/3_postprocess/postprocess_pth_mnty.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_pth_mnty.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_pth_mnty.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_pth_mnty.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_pth_mnty.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing PTH_SRGC ================="
python3 src/3_postprocess/postprocess_pth_srgc.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_pth_srgc.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_pth_srgc.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_pth_srgc.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_pth_srgc.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing TRTM_CASB ================="
python3 src/3_postprocess/postprocess_trtm_casb.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_trtm_casb.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_trtm_casb.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_trtm_casb.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_trtm_casb.py --epsilon 1000
echo "Epsilon 100 Done"

echo "================ Post Processing TRTM_RD ================="
python3 src/3_postprocess/postprocess_trtm_rd.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_trtm_rd.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_trtm_rd.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_trtm_rd.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_trtm_rd.py --epsilon 1000
echo "Epsilon 1000 Done"

echo "================ Post Processing PT_BSNF ================="
python3 src/3_postprocess/postprocess_pt_bsnf.py --epsilon 0.1 
echo "Epsilon 0.1 Done"
python3 src/3_postprocess/postprocess_pt_bsnf.py --epsilon 1
echo "Epsilon 1 Done"
python3 src/3_postprocess/postprocess_pt_bsnf.py --epsilon 10
echo "Epsilon 10 Done"
python3 src/3_postprocess/postprocess_pt_bsnf.py --epsilon 100
echo "Epsilon 100 Done"
python3 src/3_postprocess/postprocess_pt_bsnf.py --epsilon 1000
echo "Epsilon 1000 Done"


echo "finished "


