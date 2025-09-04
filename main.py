from fastapi import FastAPI, Query
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Request model
class FileUpload(BaseModel):
    user_id: str
    run_id: str
    filename: str
    file_size: int
    data: list

@app.post("/upload-data")
async def upload_data(file: FileUpload):
    response = supabase.table("user_inputs").insert({
        "user_id": file.user_id,
        "run_id": file.run_id,
        "filename": file.filename,
        "file_size": file.file_size,
        "data": file.data
    }).execute()
    return {"status": "success", "supabase_response": response.data}

@app.get("/get-data")
async def get_data(user_id: str = Query(...), run_id: str = Query(...)):
    response = supabase.table("user_inputs").select("*") \
        .eq("user_id", user_id) \
        .eq("run_id", run_id) \
        .execute()
    return {"status": "success", "records": response.data}

