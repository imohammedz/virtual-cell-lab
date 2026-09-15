import unittest

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services import get_virtual_cell_service


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.service = get_virtual_cell_service()

    def test_health(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_local_frontend_cors_preflight(self) -> None:
        response = self.client.options(
            "/experiments",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            "http://localhost:3000",
        )

    def test_cell_metadata(self) -> None:
        response = self.client.get("/cell")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "cell_type": "RPE1",
                "gene_count": 8749,
                "data_type": "scRNA-seq",
            },
        )

    def test_perturbations_include_tfam(self) -> None:
        response = self.client.get("/perturbations")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["count"], 659)
        self.assertIn("TFAM", body["perturbations"])

    def test_tfam_experiment_matches_engine(self) -> None:
        response = self.client.post(
            "/experiments",
            json={"perturbation": "TFAM"},
        )
        body = response.json()
        engine_result = self.service.run_experiment("TFAM")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["cell_type"], "RPE1")
        self.assertEqual(body["perturbation"], "TFAM")
        self.assertEqual(
            body["top_increased_genes"][0]["gene"],
            engine_result.top_increased_genes()[0].gene,
        )
        self.assertEqual(
            body["top_decreased_genes"][0]["gene"],
            engine_result.top_decreased_genes()[0].gene,
        )
        self.assertEqual(body["metadata"]["training_perturbations"], 659)

    def test_unknown_perturbation_returns_not_found(self) -> None:
        response = self.client.post(
            "/experiments",
            json={"perturbation": "NOT_A_GENE"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("Unsupported perturbation", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
