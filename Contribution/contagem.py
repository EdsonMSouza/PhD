import pandas as pd
df = pd.read_excel('annals_compilado.xlsx', encoding='utf-8')
print(df.shape)
unique_doi = df[['ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10']].groupby(df['doi'])
erro = []
count = 0
arq = 1
for index, row in unique_doi:
	ac1  = 0
	ac2  = 0
	ac3  = 0
	ac4  = 0
	ac5  = 0
	ac6  = 0
	ac7  = 0
	ac8  = 0
	ac9  = 0
	ac10 = 0
	print("Processando:", arq, index)
	arq += 1
	for i, r in df.iterrows():
		vet = []		
		if(index == r.doi):
			ac1  += r['ac1']
			ac2  += r['ac2']
			ac3  += r['ac3']
			ac4  += r['ac4']
			ac5  += r['ac5']
			ac6  += r['ac6']
			ac7  += r['ac7']
			ac8  += r['ac8']
			ac9  += r['ac9']
			ac10 += r['ac10']

			count += 1
	
	total = round(ac1,6) + round(ac2,6) + round(ac3,6) + round(ac4,6) + round(ac5,6) + round(ac6,6) + round(ac7,6) + round(ac8,6) + round(ac9,6) + round(ac10,6)
	if((total % 2) == 1 or (total % 2) == 0):
		pass
	else:
		if index not in erro:
			print('Erro em....:', index)
			erro.append([
				index, 
				round(ac1,6), 
				round(ac2,6), 
				round(ac3,6), 
				round(ac4,6), 
				round(ac5,6), 
				round(ac6,6), 
				round(ac7,6), 
				round(ac8,6), 
				round(ac9,6), 
				round(ac10,6)
				])
	
	count = 0

dfs = pd.DataFrame(erro, columns=['doi', 'ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10'])
dfs.to_excel("erros_contagem.xlsx", header=True, index=False, encoding='utf-8')
print('Done!!!')