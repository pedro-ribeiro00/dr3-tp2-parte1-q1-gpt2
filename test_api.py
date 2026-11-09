from fastapi.testclient import TestClient
from unittest.mock import Mock
from threading import Lock
from main import app

def test_generation():
    generator = Mock(return_value=[{"generated_text":"Hello world"}])
    generator.tokenizer.encode.return_value = [1,2]
    generator.tokenizer.eos_token_id = 50256
    generator.model.config.n_positions = 1024
    app.state.generator = generator
    app.state.lock = Lock()
    client = TestClient(app)
    response = client.post("/generate", json={"text":"Hello"})
    assert response.status_code == 200
    assert response.json()["generated_text"] == "Hello world"
    assert client.post("/generate", json={"text":" "}).status_code == 422
    generator.tokenizer.encode.return_value = [1]*1024
    assert client.post("/generate", json={"text":"Hello"}).status_code == 422
