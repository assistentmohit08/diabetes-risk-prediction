import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from app import app

client = app.test_client()

valid = {
    "Pregnancies": 6, "Glucose": 148, "BloodPressure": 72,
    "SkinThickness": 35, "Insulin": "", "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627, "Age": 50,
}


def test_valid_prediction():
    r = client.post("/predict", json=valid)
    assert r.status_code == 200
    body = r.get_json()
    assert 0 <= body["probability"] <= 1
    assert body["risk_level"] in {"Low", "Moderate", "High"}


def test_missing_required_field():
    bad = {k: v for k, v in valid.items() if k != "Glucose"}
    r = client.post("/predict", json=bad)
    assert r.status_code == 400


def test_out_of_range():
    r = client.post("/predict", json={**valid, "Age": -5})
    assert r.status_code == 400


if __name__ == "__main__":
    test_valid_prediction()
    test_missing_required_field()
    test_out_of_range()
    print("All tests passed")