# import requests
# import simpleaudio
# import tempfile
# import json

# # VOICEVOX APIに接続し、テキストから音声合成を行う関数
# def synthesize_voice(text, speaker=3, host="127.0.0.1", port=50021):
#     # パラメータ設定
#     params = (
#         ("text", text),
#         ("speaker", speaker)  # 音声の種類を Int 型で指定
#     )

#     # Audio Query APIに POST リクエストを送信
#     response1 = requests.post(
#         f"http://{host}:{port}/audio_query",
#         params=params
#     )
#     response1.raise_for_status()  # エラーハンドリング

#     # Synthesis APIに POST リクエストを送信し、音声データを生成
#     response2 = requests.post(
#         f"http://{host}:{port}/synthesis",
#         headers={"Content-Type": "application/json"},
#         params=params,
#         data=json.dumps(response1.json())
#     )
#     response2.raise_for_status()  # エラーハンドリング

#     # 一時ファイルを作成し、音声データを保存して再生
#     with tempfile.TemporaryDirectory() as tmp:
#         with open(f"{tmp}/audio.wav", "wb") as f:
#             f.write(response2.content)
#             wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audio.wav")
#             play_obj = wav_obj.play()
#             play_obj.wait_done()

#     return "音声再生が完了しました"
