from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/figures';OUT.mkdir(parents=True,exist_ok=True)
for kind in ['department','product']:
 data=pd.read_excel(ROOT/f'{kind}_results.xlsx')
 totals=data.iloc[:,2:].sum().sort_values()
 totals.to_csv(ROOT/f'reports/{kind}-original-summary.csv')
 fig,ax=plt.subplots(figsize=(10,max(4,len(totals)*.35)))
 ax.barh(totals.index,totals.values,color='#2563eb');ax.set(title=f'Original survey: {kind} indicators',xlabel='Positive indicator count')
 fig.tight_layout();fig.savefig(OUT/f'{kind}-original.png',dpi=160);plt.close(fig)
