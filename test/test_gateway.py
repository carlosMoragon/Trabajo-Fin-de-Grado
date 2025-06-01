import unittest
import requests
from config import GATEWAY_URL

class TestGateway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = GATEWAY_URL.rstrip("/")

    def atest_true(self):
        self.assertTrue(True)

    @staticmethod
    def get_configuration():
        return {
            "eluent_1": "h2o",
            "eluent_2": "acn",
            "eluent_1_ph": 8.683361183539699,
            "eluent_2_ph": 2.763763594101408,
            "column": {
                "column_usp_code": "L3",
                "column_length": 87.40525434151095,
                "particle_size": 55.74472569932265,
                "column_temperature": 41.92365706709454,
                "column_flowrate": 0.11539846293467673,
                "dead_time": 2.6075921691316535
            },
            "gradient": {
                "duration": 20.260231205112056,
                "x0": 6.120635223768948,
                "x1": 334.7865546759724,
                "x2": 886.6713034354549,
                "x3": 173.37581427312108,
                "x4": 180.8307820024546,
                "x5": 9.237550382186136,
                "x6": 1.7775394792474848,
                "x7": 0.2143937881473569,
                "x8": -0.00418896893113763,
                "x9": -0.00010676838274613766,
                "x10": 0.0000030303530621255794
            }
        }
    @staticmethod
    def get_configuration_2():
        return {
            "eluent_1": "h2o",
            "eluent_2": "acn",
            "eluent_1_ph": 8.683361183539699,
            "eluent_2_ph": 2.763763594101408,
            "column": {
                "column_usp_code": "L3",
                "column_length": 87.40525434151095,
                "particle_size": 55.74472569932265,
                "column_temperature": 41.92365706709454,
                "column_flowrate": 0.11539846293467673,
                "dead_time": 2.6075921691316535
            },
            "gradient": {
                "duration": 21.260231205112056,
                "x0": 6.120635223768948,
                "x1": 334.7865546759724,
                "x2": 886.6713034354549,
                "x3": 173.37581427312108,
                "x4": 180.8307820024546,
                "x5": 9.237550382186136,
                "x6": 1.7775394792474848,
                "x7": 0.2143937881473569,
                "x8": -0.00418896893113763,
                "x9": -0.00010676838274613766,
                "x10": 0.0000030303530621255794
            }
        }
    #OK
    def test_predict_success(self):
        
        payload = {"class": "Phenols"}
        resp = requests.post(f"{self.base}/predict", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("configuration", data)
        self.assertIn("score", data)

    #OK
    def test_predict_cache_success(self):
        
        payload = {"class": "Lactones"}

        resp1 = requests.post(f"{self.base}/predict", json=payload)

        resp2 = requests.post(f"{self.base}/predict", json=payload)

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

        self.assertEqual(resp1.json(), resp2.json(),"La respuesta cacheada difiere de la original")



    #Solucionado FALTA HACER PUSH
    def test_predict_bad_request(self):
        
        resp = requests.post(f"{self.base}/predict", json={})
        self.assertEqual(resp.status_code, 400)

    #OK
    def test_predict_not_found(self):
        
        resp = requests.post(f"{self.base}/predict", json={"class": "NoExiste"})
        self.assertEqual(resp.status_code, 404)
    #OK
    def test_evaluate_success(self):
        
        payload = {
            "class": "Phenols",
            "configuration": self.get_configuration()
        }
        resp = requests.post(f"{self.base}/evaluate", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("score", data)
    #OK
    def test_evaluate_bad_request(self):
        
        payload = { "class": "Phenols" }
        resp = requests.post(f"{self.base}/evaluate", json=payload)
        self.assertEqual(resp.status_code, 400)
    #OK
    def test_recommend_family_success(self):
        
        payload = { "configuration": self.get_configuration() }
        resp = requests.post(f"{self.base}/recommendFamily", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("class", data)
        self.assertIn("score", data)

    #OK SOLUCIONADO FALTA HACER PUSH
    def test_recommend_family_not_found(self):
        
        cfg = self.get_configuration()
        cfg["eluent_1"] = "imposible"
        resp = requests.post(f"{self.base}/recommendFamily", json={"configuration": cfg})
        self.assertEqual(resp.status_code, 422)
    
    #OK
    def test_evaluate_cache_success(self):
        
        payload = {
            "class": "Purine nucleosides",
            "configuration": self.get_configuration()
        }

        resp1 = requests.post(f"{self.base}/evaluate", json=payload)

        resp2 = requests.post(f"{self.base}/evaluate", json=payload)

        # Validaciones
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp1.json(), resp2.json(),"La respuesta cacheada en /evaluate difiere de la original")

    #OK
    def test_recommend_family_cache_success(self):
        
        payload = { "configuration": self.get_configuration() }

        resp1 = requests.post(f"{self.base}/recommendFamily", json=payload)

        resp2 = requests.post(f"{self.base}/recommendFamily", json=payload)

        # Validaciones
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp1.json(), resp2.json(),"La respuesta cacheada en /recommendFamily difiere de la original")
        
    #OK
    def test_families_list(self):
        
        resp = requests.get(f"{self.base}/families")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("families", data, "La respuesta no contiene la clave 'families'")

        self.assertIsInstance(data["families"], list, "'families' no es una lista")
    
    #OK
    def test_feedback_post_and_get(self):
        
        # POST
        fb = {
            "configuration": self.get_configuration(),
            "class": "Phenols",
            "score": 8.7,
            "feedback": 7
        }
        post = requests.post(f"{self.base}/feedback", json=fb)
        self.assertEqual(post.status_code, 200)
        self.assertIn("message", post.json())

        # GET filtered
        get = requests.get(f"{self.base}/feedback", params={"classname": "Phenols"})
        self.assertEqual(get.status_code, 200)
        items = get.json()
        self.assertIsInstance(items, list)
    #OK
    def test_experiments_submit(self):
        
        exp = [{
            "metabolite_name": "Caffeine",
            "formula": "C8H10N4O2",
            "rt": 5.23,
            "smiles_std": "Cn1cnc2c1c(=O)n(C)c(=O)n2C",
            "inchi_std": "InChI=1S/C8H10N4O2/c1-11-4-7-9-6(10-8(11)12(2)3)5(4)14(7)13/h4-5H,1-3H3",
            "inchikey_std": "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
            "classyfire": {
            "kingdom": "Organic compounds",
            "superclass": "Nucleosides, nucleotides, and analogues",
            "class": "Purine nucleosides",
            "subclass": "Purine nucleotides",
            "level5": "Xanthine",
            "level6": "Caffeine"
            },
            "comment": "Test experiment data for caffeine",
            "alternative_parents": "",
            "column": {
            "column_usp_code": "C18",
            "column_name": "Agilent ZORBAX Eclipse Plus C18",
            "column_length": 100,
            "particle_size": 3.5,
            "column_temperature": 30,
            "column_flowrate": 0.3,
            "dead_time": 1.8
            },
            "eluent_1": "water",
            "eluent_2": "acetonitrile",
            "eluent_1_ph": 2.5,
            "eluent_2_ph": 7.0,
            "gradient": {
            "duration": 15,
            "x0": 0,
            "x1": 5,
            "x2": 10,
            "x3": 20,
            "x4": 30,
            "x5": 50,
            "x6": 70,
            "x7": 85,
            "x8": 90,
            "x9": 95,
            "x10": 100
            }
        }
        ]
        resp = requests.post(f"{self.base}/experiments", json=exp)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("message", resp.json())