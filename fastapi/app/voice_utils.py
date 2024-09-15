import requests
from fastapi.responses import FileResponse

async def create_voice_from_text(text: str):
    speaker = 1
    audio_query_url = f"http://voicevox_engine:50021/audio_query?speaker={speaker}&text={text}"

    # クエリデータの作成
    query_response = requests.post(audio_query_url)
    if query_response.status_code != 200:
        return {"error": "Failed to create audio query"}

    query_json = query_response.json()

    # 音声合成のリクエスト
    synthesis_url = f"http://voicevox_engine:50021/synthesis?speaker={speaker}"
    synthesis_response = requests.post(synthesis_url, json=query_json)
    if synthesis_response.status_code != 200:
        return {"error": "Failed to synthesize voice"}

    # 音声データを一時的にファイルに保存
    audio_filename = "wav_save/output.wav"
    with open(audio_filename, 'wb') as f:
        f.write(synthesis_response.content)

    # 音声ファイルを返す
    return FileResponse(audio_filename, media_type='audio/wav')
