from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os

app = FastAPI(
    title="도서산간 판별 API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# CSV 불러오기
df = pd.read_csv("data/mi_service.csv", dtype={"zipcode": str})

@app.get("/")
def root():
    return {"message": "도서산간 지역 판별 API입니다. /docs 에서 문서를 확인하세요."}

@app.get("/check")
def check_zipcode(zipcode: str = Query(..., min_length=5, max_length=5)):
    match = df[df["zipcode"] == zipcode]
    if match.empty:
        return JSONResponse(status_code=404, content={"message": "해당 우편번호는 목록에 없습니다."})
    
    row = match.iloc[0]
    return {
        "zipcode": row["zipcode"],
        "region": row["region"],
        "is_island": bool(row["is_island"]),
        "is_mountain": bool(row["is_mountain"]),
        "surcharge": int(row["surcharge"])
    }

@app.get("/regions")
def get_all_regions():
    return df.to_dict(orient="records")

@app.get("/download")
def download_csv():
    return FileResponse("data/mi_service.csv", media_type="text/csv", filename="mi_service.csv")
