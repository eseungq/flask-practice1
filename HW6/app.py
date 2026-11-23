from pathlib import Path

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
COLUMNS = ["quantity", "unit_price"]

app = Flask(__name__)
app.config["RESTX_JSON"] = {"ensure_ascii": False}

api = Api(
    app,
    version="1.0",
    title="Sales API",
    description="수량과 단가를 받아 총액을 예측한다",
    doc="/api/docs",
    prefix="/api",
)
ns = api.namespace("sales", description="총액 예측")

# 서버를 켤 때 한 번만 읽음. linear regression + qp (수량 × 단가)
model = joblib.load(BASE_DIR / "sales_model.pkl")

order = api.model("Order", {
    "quantity": fields.Integer(required=True, min=1, example=40, description="수량"),
    "unit_price": fields.Float(required=True, min=0, example=200000, description="단가 (원)"),
})


@ns.route("/predict")
class Predict(Resource):
    @ns.doc("총액 예측")
    @ns.expect(order, validate=True)
    def post(self) -> dict[str, int]:
        """수량과 단가를 받아 총액을 돌려준다"""
        data = api.payload
        x = pd.DataFrame([[data["quantity"], data["unit_price"]]], columns=COLUMNS)
        x = x.assign(qp=x["quantity"] * x["unit_price"])  # 학습 때 더한 feature 를 똑같이
        return {"total_sales": int(round(model.predict(x)[0]))}
