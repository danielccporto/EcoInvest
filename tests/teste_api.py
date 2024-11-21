from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

def test_processar_texto():
    response = client.post(
        "/processar_texto", 
        json={"texto": "Teste de API", "tipo_analise": "resumo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["text"] == "Teste de API"
    assert data["analysis_type"] == "resumo"
    assert "results" in data
