from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import requests
import ezdxf
import io

app = FastAPI()

@app.post("/analyze_dxf/")
async def analyze_dxf(dxf_url: str = Form(...)):
    try:
        # Prenesi datoteko z URL-ja
        response = requests.get(dxf_url)
        if response.status_code != 200:
            return JSONResponse(status_code=400, content={"error": "Unable to download file"})

        doc = ezdxf.read(io.BytesIO(response.content))
        msp = doc.modelspace()

        total_area = 0.0

        for entity in msp:
            if entity.dxftype() == "LWPOLYLINE" and entity.closed:
                total_area += entity.area()

        return {"total_area_m2": round(total_area, 2)}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
