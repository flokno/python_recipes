notebook=notebook_cmaps_cmocean.ipynb

cmocean.xlsx:
	jupyter nbconvert --inplace --execute $(notebook)
	clean_jupyter_notebook $(notebook)
	
clean:
	rm cmocean.xlsx

