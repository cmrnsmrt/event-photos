import os
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from fastapi.staticfiles import StaticFiles

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
AZURE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "eventphotos")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

blob_service_client = None
if AZURE_CONNECTION_STRING:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request, msg: str = None):
    image_urls = []
    if blob_service_client:
        try:
            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
            blobs = container_client.list_blobs()
            account_name = blob_service_client.account_name
            for blob in blobs:
                image_url = f"https://{account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob.name}"
                image_urls.append(image_url)
        except Exception:
            image_urls = []
    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "msg": msg, "image_urls": image_urls}
    )

@app.post("/upload", response_class=HTMLResponse)
def upload_photo(request: Request, file: list[UploadFile] = File(...)):
    if not blob_service_client:
        return HTMLResponse("Azure Storage not configured.", status_code=500)
    try:
        for f in file:
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{f.filename}"
            blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=filename)
            blob_client.upload_blob(f.file, overwrite=True)
        return RedirectResponse(url="/?msg=Photos uploaded successfully!", status_code=303)
    except Exception as e:
        return HTMLResponse(f"Upload failed: {e}", status_code=500)
