db = db.getSiblingDB('metabolite-separation-api');

db.createCollection('evaluates');
db.createCollection('experiments');
db.createCollection('families');
db.createCollection('feedbacks');
db.createCollection('predicts');
db.createCollection('recommendfamilies');