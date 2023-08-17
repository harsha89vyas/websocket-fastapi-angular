import asyncio
import logging
from datetime import datetime
import os
from typing import Annotated

from fastapi import FastAPI, File, Form, WebSocket, WebSocketDisconnect, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import redis
from util.process import Processor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
#r = redis.from_url(os.environ.get("REDIS_URL"))
r = redis.from_url('redis://:password@localhost:6379')
#r = redis.from_url('rediss://:pd5dfa9bf22efd0213281d9afcc4ee18a7fc74ddaedaa738780c5f98db4212d1e@ec2-54-235-175-51.compute-1.amazonaws.com:26710', ssl=False)



@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    # Accept the connection from a client.
    await websocket.accept()
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(f'{session_id}_response',)
    while True:
        try:
            # Receive the JSON data sent by a client.
            #data = await websocket.receive_json()
            print('waiting for session')
            # Some (fake) heavey data processing logic.
            message = None
            while True:
                message = p.get_message()
                if message:
                    break
                print("waiting for message")
                await asyncio.sleep(1)
            message_processed = message['data'].decode('utf-8')
            # Send JSON data to the client.
            await websocket.send_json(
                {
                    "message": message_processed,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
            )
        except WebSocketDisconnect:
            logger.info("The connection is closed.")
            break

@app.websocket("/human/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    # Accept the connection from a client.
    await websocket.accept()
    prompt_p = r.pubsub(ignore_subscribe_messages=True)
    prompt_p.subscribe(f'human_prompt_{session_id}')
    while True:
        try:
            # Receive the JSON data sent by a client.
            #data = await websocket.receive_json()
            print('waiting for session')
            # Some (fake) heavey data processing logic.
            message = None
            while True:
                message = prompt_p.get_message()
                if message and message['type'] == 'message':
                    break
                print("waiting for prompt")
                await asyncio.sleep(1)
            message_processed = message['data'].decode('utf-8')
            # Send JSON data to the client.
            await websocket.send_json(
                {
                    "message": message_processed,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
            )
            data = await websocket.receive_json()
            r.publish(f'human_input_{session_id}', data["message"])
        except WebSocketDisconnect:
            logger.info("The connection is closed.")
            break

@app.post("/api/upload")
async def uploadTableFile(request: Request,type: Annotated[str, Form()], session:Annotated[str, Form()], file: UploadFile = File(...)):
    print(file.filename)
    print(type)
    print(session)
    print("after read")
    file_data = await file.read()
    print("after read")
    r.set(f"{type}_{session}", file_data)
    print("after set")
    print(r.get(f"{type}_{session}"))
    table_file = r.get(f"table_{session}")
    template_file = r.get(f"template_{session}")
    
    return {"filename": file.filename, "filetype": file.content_type, "filedata": file_data}

@app.post("/api/process")
async def processTableFile(request: Request, session:Annotated[str, Form()]):
    print("processing")
    table_file = r.get(f"table_{session}")
    template_file = r.get(f"template_{session}")
    print("got files")
    r.set(f"{session}_response", "processing")
    print("set response")
    processor= Processor(session=session)
    generated_csv = await processor.process_files(table_file, template_file)
    print("processed")
    return FileResponse(generated_csv, filename="generated_file.csv")