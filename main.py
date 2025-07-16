from fastapi import FastAPI, Form
import requests
import ezdxf
import tempfile
import os

app = FastAPI()

@app.post("/analyze_dxf/")
async def analyze_dxf(dxf_url: str = Form(...)):
    try:
        response = requests.get(dxf_url)
        if response.status_code != 200:
            return {"error": "Napaka pri prenosu DXF"}

        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        doc = ezdxf.readfile(tmp_path)
        msp = doc.modelspace()

        total_area = 0.0
        for entity in msp.query("LWPOLYLINE"):
            if entity.closed:
                try:
                    total_area += entity.area()
                except:
                    continue

        os.remove(tmp_path)

        return {
            "total_area_m2": round(total_area, 2),
            "message": "Analiza uspešna"
        }

    except Exception as e:
        return {"error": str(e)}