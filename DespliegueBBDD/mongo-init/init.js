db = db.getSiblingDB('metabolite-separation-api');

db.createCollection('evaluates');
db.createCollection('experiments');
db.createCollection('families');
db.createCollection('feedbacks');
db.createCollection('predicts');
db.createCollection('recommendfamilies');

db.families.insertMany([
    { "family": "Azoles", "CHEMONTID": "0000436", "API_version": "1" },
    { "family": "Lactones", "CHEMONTID": "0000050", "API_version": "1" },
    { "family": "Organooxygen compounds", "CHEMONTID": "0000323", "API_version": "1" },
    { "family": "Phenylpropanoic acids", "CHEMONTID": "0002551", "API_version": "1" },
    { "family": "Purine nucleotides", "CHEMONTID": "0001506", "API_version": "1" },
    { "family": "Cinnamic acids and derivatives", "CHEMONTID": "0000476", "API_version": "1" },
    { "family": "Pyridines and derivatives", "CHEMONTID": "0000089", "API_version": "1" },
    { "family": "Imidazopyrimidines", "CHEMONTID": "0001797", "API_version": "1" },
    { "family": "Prenol lipids", "CHEMONTID": "0000259", "API_version": "1" },
    { "family": "Triazines", "CHEMONTID": "0000098", "API_version": "1" },
    { "family": "Phenols", "CHEMONTID": "0000134", "API_version": "1" },
    { "family": "Hydroxy acids and derivatives", "CHEMONTID": "0000472", "API_version": "1" },
    { "family": "Coumarins and derivatives", "CHEMONTID": "0000145", "API_version": "1" },
    { "family": "Indoles and derivatives", "CHEMONTID": "0000211", "API_version": "1" },
    { "family": "Pyrimidine nucleotides", "CHEMONTID": "0001509", "API_version": "1" },
    { "family": "Fatty Acyls", "CHEMONTID": "0003909", "API_version": "1" },
    { "family": "Benzene and substituted derivatives", "CHEMONTID": "0002279", "API_version": "1" },
    { "family": "Steroids and steroid derivatives", "CHEMONTID": "0000258", "API_version": "1" },
    { "family": "Organonitrogen compounds", "CHEMONTID": "0000278", "API_version": "1" },
    { "family": "Phenol ethers", "CHEMONTID": "0002341", "API_version": "1" },
    { "family": "Keto acids and derivatives", "CHEMONTID": "0000389", "API_version": "1" },
    { "family": "Diazines", "CHEMONTID": "0001346", "API_version": "1" },
    { "family": "Coumarans", "CHEMONTID": "0004189", "API_version": "1" },
    { "family": "Organic thiophosphoric acids and derivatives", "CHEMONTID": "0001303", "API_version": "1" },
    { "family": "Pyrimidine nucleosides", "CHEMONTID": "0000480", "API_version": "1" },
    { "family": "Quinolines and derivatives", "CHEMONTID": "0001253", "API_version": "1" },
    { "family": "Organic dithiophosphoric acids and derivatives", "CHEMONTID": "0003385", "API_version": "1" },
    { "family": "Purine nucleosides", "CHEMONTID": "0000479", "API_version": "1" },
    { "family": "Pteridines and derivatives", "CHEMONTID": "0000109", "API_version": "1" },
    { "family": "Carboxylic acids and derivatives", "CHEMONTID": "0000265", "API_version": "1" }
  ]);