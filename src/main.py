import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from pydub import AudioSegment

# Import services
from src.services.brain import Brain
from src.services.transcriber import Transcriber
from src.services.synthesizer import Synthesizer
from src.utils.audio_utils import mulaw_to_pcm

load_dotenv()

# --- FFMPEG SETUP ---
# Ensure ffmpeg.exe and ffprobe.exe are in the ROOT folder
AudioSegment.converter = os.path.abspath("ffmpeg.exe")
AudioSegment.ffmpeg = os.path.abspath("ffmpeg.exe")
AudioSegment.ffprobe = os.path.abspath("ffprobe.exe") 

app = FastAPI()

brain = Brain()
transcriber = Transcriber()
synthesizer = Synthesizer()

@app.post("/start-call")
async def start_call(request: Request):
    host = request.headers.get("host")
    response_xml = f"""
    <Response>
        <Say>Hello! This is Omni from ATS Real Estate. How can I help you?</Say>
        <Connect>
            <Stream url="wss://{host}/media-stream" />
        </Connect>
    </Response>
    """
    return HTMLResponse(content=response_xml, media_type="application/xml")

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client Connected")
    
    # COMPETITION REQUIREMENT: Track the full chat for MoM
    full_conversation = []
    
    audio_buffer = bytearray()
    stream_sid = None
    
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data['event'] == 'start':
                stream_sid = data['start']['streamSid']
                print(f"Stream Started: {stream_sid}")

            elif data['event'] == 'media':
                chunk = base64.b64decode(data['media']['payload'])
                pcm_chunk = mulaw_to_pcm(chunk)
                audio_buffer.extend(pcm_chunk)
                
                # Process audio every ~1.5 seconds
                if len(audio_buffer) > 24000:
                    user_text = transcriber.transcribe_audio(audio_buffer)
                    audio_buffer = bytearray() # Clear buffer
                    
                    # --- GHOST FILTER ---
                    if len(user_text) < 4: continue
                    ghosts = ["Thank you.", "I don't know.", "Subtitle by", "Amara.org", "You're welcome."]
                    if any(g.lower() in user_text.lower() for g in ghosts):
                        print(f"👻 Ignored ghost: {user_text}")
                        continue
                    # --------------------

                    print(f"User said: {user_text}")
                    full_conversation.append(f"Customer: {user_text}") # Log for MoM
                    
                    # 1. THINK
                    ai_reply = await brain.think(user_text)
                    print(f"AI says: {ai_reply}")
                    full_conversation.append(f"AI: {ai_reply}")       # Log for MoM
                    
                    # 2. SPEAK
                    mp3_file = await synthesizer.speak(ai_reply)
                    
                    # 3. CONVERT
                    try:
                        audio = AudioSegment.from_mp3(mp3_file)
                        audio = audio.set_frame_rate(8000).set_channels(1)
                        mulaw_audio = audio.export(format="mulaw").read()
                        
                        # 4. SEND
                        chunk_size = 1000 
                        for i in range(0, len(mulaw_audio), chunk_size):
                            chunk = mulaw_audio[i:i+chunk_size]
                            payload = base64.b64encode(chunk).decode("utf-8")
                            await websocket.send_json({
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {"payload": payload}
                            })
                    except Exception as e:
                        print(f"Audio Error: {e}")

            elif data['event'] == 'stop':
                print("Call Ended.")
                break
                
    except Exception as e:
        print(f"Connection Error: {e}")
        
    finally:
        # --- COMPETITION REQUIREMENT: GENERATE MoM ON DISCONNECT ---
        if len(full_conversation) > 0:
            print("generating MoM...")
            mom_text = await brain.generate_mom(full_conversation)
            
            # Save to file
            filename = f"MoM_{stream_sid}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(mom_text)
            print(f"✅ SUCCESS! Minutes of Meeting saved to: {filename}")