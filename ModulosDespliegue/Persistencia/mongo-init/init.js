db = db.getSiblingDB('metabolite-separation-api');

db.createCollection('evaluates');
db.createCollection('experiments');
db.createCollection('families');
db.createCollection('feedbacks');
db.createCollection('predicts');
db.createCollection('recommendfamilies');

db.families.insertMany([
    { "class": "Azoles", "CHEMONTID": "0000436", "API_version": "1" },
    { "class": "Lactones", "CHEMONTID": "0000050", "API_version": "1" },
    { "class": "Organooxygen compounds", "CHEMONTID": "0000323", "API_version": "1" },
    { "class": "Phenylpropanoic acids", "CHEMONTID": "0002551", "API_version": "1" },
    { "class": "Purine nucleotides", "CHEMONTID": "0001506", "API_version": "1" },
    { "class": "Cinnamic acids and derivatives", "CHEMONTID": "0000476", "API_version": "1" },
    { "class": "Pyridines and derivatives", "CHEMONTID": "0000089", "API_version": "1" },
    { "class": "Imidazopyrimidines", "CHEMONTID": "0001797", "API_version": "1" },
    { "class": "Prenol lipids", "CHEMONTID": "0000259", "API_version": "1" },
    { "class": "Triazines", "CHEMONTID": "0000098", "API_version": "1" },
    { "class": "Phenols", "CHEMONTID": "0000134", "API_version": "1" },
    { "class": "Hydroxy acids and derivatives", "CHEMONTID": "0000472", "API_version": "1" },
    { "class": "Coumarins and derivatives", "CHEMONTID": "0000145", "API_version": "1" },
    { "class": "Indoles and derivatives", "CHEMONTID": "0000211", "API_version": "1" },
    { "class": "Pyrimidine nucleotides", "CHEMONTID": "0001509", "API_version": "1" },
    { "class": "Fatty Acyls", "CHEMONTID": "0003909", "API_version": "1" },
    { "class": "Benzene and substituted derivatives", "CHEMONTID": "0002279", "API_version": "1" },
    { "class": "Steroids and steroid derivatives", "CHEMONTID": "0000258", "API_version": "1" },
    { "class": "Organonitrogen compounds", "CHEMONTID": "0000278", "API_version": "1" },
    { "class": "Phenol ethers", "CHEMONTID": "0002341", "API_version": "1" },
    { "class": "Keto acids and derivatives", "CHEMONTID": "0000389", "API_version": "1" },
    { "class": "Diazines", "CHEMONTID": "0001346", "API_version": "1" },
    { "class": "Coumarans", "CHEMONTID": "0004189", "API_version": "1" },
    { "class": "Organic thiophosphoric acids and derivatives", "CHEMONTID": "0001303", "API_version": "1" },
    { "class": "Pyrimidine nucleosides", "CHEMONTID": "0000480", "API_version": "1" },
    { "class": "Quinolines and derivatives", "CHEMONTID": "0001253", "API_version": "1" },
    { "class": "Organic dithiophosphoric acids and derivatives", "CHEMONTID": "0003385", "API_version": "1" },
    { "class": "Purine nucleosides", "CHEMONTID": "0000479", "API_version": "1" },
    { "class": "Pteridines and derivatives", "CHEMONTID": "0000109", "API_version": "1" },
    { "class": "Carboxylic acids and derivatives", "CHEMONTID": "0000265", "API_version": "1" }
  ]);