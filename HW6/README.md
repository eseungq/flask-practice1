# HW6

23013438 이승규

## 실행 방법

Python 3.12 이상 (3.14.5에서 동작 확인).

1. 패키지를 설치한다: `pip install -r ../requirements.txt jupyter`
2. 이 폴더(`HW6/`)에서 jupyter로 `hw6.ipynb`를 Run All 한다. 같은 폴더의 `sales_clean.csv`를 읽고, 단계 6.에서 `sales_model.pkl`을 만든다.
3. 같은 폴더에서 서버를 켠다: `flask --app app run`
4. http://127.0.0.1:5000/api/docs 를 열고 `POST /api/sales/predict`에서 Try it out → Execute.
   - 요청: `{"quantity": 40, "unit_price": 200000}`
   - 응답: `{"total_sales": 8000000}` (`docs.png`)

## 단계 3. 답

총액은 `수량 × 단가`, 즉 곱셈으로 정해진다. linear regression은 `a×수량 + b×단가 + c`처럼 각 값에 계수를 곱해 더하는 형태만 만들 수 있어 곱셈을 표현하지 못하므로, test R²가 0.862에 그쳤다.
qp(= 수량 × 단가) 열을 더하면 총액 = `1 × qp`인 선형 관계가 되므로 linear regression으로 정확히 맞출 수 있어 R²가 1.0이 된다.

## 단계 5. 결정과 이유

**max_depth 8**을 골랐다. cross-validation 평균은 depth 8이 0.992, 12와 None이 0.995로 거의 같은데, depth 8은 잎 수가 250개로 depth 12(781개)·None(800개)보다 훨씬 적은 단순한 model이기 때문이다.
제한 없는 tree의 training R² 1.000과 test R² 0.994의 차이가 작은 것은 데이터에 `총액 = 수량 × 단가`라는 실제 규칙이 있어서, training에서 익힌 것이 test에도 그대로 통하기 때문이다.

cross-validation의 max_depth 12 · None 줄은 강의 슬라이드와 소수 셋째 자리가 다르다 (12: 0.9946 → 0.995, None: 0.9947 → 0.995). 코드는 슬라이드와 같으므로, 라이브러리 버전 등 실행 환경 차이로 값이 조금 달라진 것으로 보인다.

## 단계 7. 답

**linear regression + qp**를 골라 API로 내보냈다. 수량 40 · 단가 200,000일 때 linear + qp는 8,000,000, tree (depth 8)는 7,362,301을 예측했고, 실제 곱은 8,000,000이다.
linear + qp는 실제 곱과 정확히 같지만, tree는 training 데이터의 구간별 평균으로 계단처럼 근사할 뿐이라 637,699원 차이가 난다.
총액이 공식으로 정해지는 문제이므로 그 공식을 그대로 담을 수 있는 linear + qp가 적합하다. (공식을 아는 이상 model 없이 `수량 × 단가`로 계산해도 된다.)