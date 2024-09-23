var micButton = document.querySelector('.microphone');
var audioWaveCanvas = document.getElementById('AudioWave');
var audioWaveCtx = audioWaveCanvas.getContext('2d');

var audioCtx = null;
var analyser = null;
var dataArray = null;
var bufferLength = null;

function changeBackgroundColor() {
    const hour = new Date().getHours();
    const body = document.body;
    console.log(new Date().getHours());

    // 現在のクラスをクリア
    body.className = '';

    if (hour >= 6 && hour < 12) {
        // 朝（6時〜11時）
        body.className = 'morning';
    } else if (hour >= 12 && hour < 18) {
        // 昼（12時〜17時）
        body.className = 'afternoon';
    } else {
        // 夜（18時〜5時）
        body.className = 'evening';
    }
}

// ページ読み込み時に実行
window.onload = changeBackgroundColor;

function drawWaveform() {
    requestAnimationFrame(drawWaveform);

    // 周波数データを取得
    analyser.getByteTimeDomainData(dataArray);

    // canvasをクリア
    audioWaveCtx.clearRect(0, 0, audioWaveCanvas.width, audioWaveCanvas.height);

    // 波形の線のスタイル
    audioWaveCtx.lineWidth = 2;
    audioWaveCtx.strokeStyle = '#FFFFFF';

    // 描画開始
    audioWaveCtx.beginPath();

    var sliceWidth = audioWaveCanvas.width / bufferLength;
    var x = 0;

    // 波形データを描画
    for (var i = 0; i < bufferLength; i++) {
        var v = dataArray[i] / 128.0;
        var y = (v * audioWaveCanvas.height) / 2;

        if (i === 0) {
            audioWaveCtx.moveTo(x, y);
        } else {
            audioWaveCtx.lineTo(x, y);
        }

        x += sliceWidth;
    }

    audioWaveCtx.lineTo(audioWaveCanvas.width, audioWaveCanvas.height / 2);
    audioWaveCtx.stroke();
}

// マイクボタンをクリックしたときに音声を取得して波形を描画
micButton.addEventListener('click', function() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('マイクが利用できません');
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            if (!audioCtx) {
                // AudioContextを初期化
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioCtx.createAnalyser();
                analyser.fftSize = 2048;

                var source = audioCtx.createMediaStreamSource(stream);
                source.connect(analyser);

                bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);

                // 波形描画を開始
                drawWaveform();
            }
        })
        .catch(function(err) {
            console.log('マイクへのアクセスが拒否されました: ' + err);
        });
});

const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || webkitSpeechGrammarList;
const SpeechRecognitionEvent = window.SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

if (!SpeechRecognition) {
    alert("このブラウザは音声認識をサポートしていません。");
}

const recognition = new webkitSpeechRecognition();
recognition.lang = "ja";
recognition.continuous = true;

let isRecognizing = false;  // 音声認識が開始されているかを追跡
let recognitionTimeout = null; // タイマーIDを保存する変数
let lastRecognizedText = ""; // 最後に送信したテキストを記録する変数

recognition.onresult = ({ results }) => {
    const output = document.querySelector(".output");
    const recognizedText = results[0][0].transcript;
    output.textContent = recognizedText;

    // テキストデータをFastAPIに送信（前回と異なる場合のみ）
    if (recognizedText !== lastRecognizedText) {
        sendTextToFastAPI(recognizedText);
        lastRecognizedText = recognizedText; // 最新のテキストを記録
    }
};

// 音声認識が終了したときにフラグをリセット
recognition.onend = () => {
    isRecognizing = false;
    clearTimeout(recognitionTimeout); // タイマーをクリア
};

// 音声認識を開始
const startButton = document.querySelector(".start");
startButton.addEventListener("click", () => {
    if (!isRecognizing) {
        recognition.start();
        isRecognizing = true;

        // 10秒後に自動的に音声認識を停止
        recognitionTimeout = setTimeout(() => {
            if (isRecognizing) {
                recognition.stop();
                isRecognizing = false;
            }
        }, 10000); // 10000ミリ秒 = 10秒
    } else {
        console.log("音声認識はすでに開始されています。");
    }
});

// 音声認識を停止
const stopButton = document.querySelector(".stop");
stopButton.addEventListener("click", () => {
    if (isRecognizing) {
        recognition.stop();
        isRecognizing = false;
        clearTimeout(recognitionTimeout); // タイマーをクリア
    }
});

// FastAPIにテキストを送信する関数
function sendTextToFastAPI(text) {
    fetch('/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    })
    .then(response => {
        if (response.ok) {
            console.log('テキストが正常に送信されました');
        } else {
            console.log('テキスト送信に失敗しました');
        }
    })
    .catch(error => {
        console.log('エラーが発生しました:', error);
    });
}


// const recognition = new webkitSpeechRecognition();
// recognition.lang = "ja";
// recognition.continuous = true;

// let isRecognizing = false;  // 音声認識が開始されているかを追跡
// let recognitionTimeout = null; // タイマーIDを保存する変数

// recognition.onresult = ({ results }) => {
//     const output = document.querySelector(".output");
//     const recognizedText = results[0][0].transcript;
//     output.textContent = recognizedText;

//     // テキストデータをFastAPIに送信
//     sendTextToFastAPI(recognizedText);
// };

// // 音声認識が終了したときにフラグをリセット
// recognition.onend = () => {
//     isRecognizing = false;
//     clearTimeout(recognitionTimeout); // タイマーをクリア
// };

// // 音声認識を開始
// const startButton = document.querySelector(".start");
// startButton.addEventListener("click", () => {
//     if (!isRecognizing) {
//         recognition.start();
//         isRecognizing = true;

//         // 10秒後に自動的に音声認識を停止
//         recognitionTimeout = setTimeout(() => {
//             if (isRecognizing) {
//                 recognition.stop();
//                 isRecognizing = false;
//             }
//         }, 10000); // 10000ミリ秒 = 10秒
//     } else {
//         console.log("音声認識はすでに開始されています。");
//     }
// });

// // 音声認識を停止
// const stopButton = document.querySelector(".stop");
// stopButton.addEventListener("click", () => {
//     if (isRecognizing) {
//         recognition.stop();
//         isRecognizing = false;
//         clearTimeout(recognitionTimeout); // タイマーをクリア
//     }
// });

// // FastAPIにテキストを送信する関数
// function sendTextToFastAPI(text) {
//     fetch('/process_text', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ text: text }),
//     })
//     .then(response => {
//         if (response.ok) {
//             console.log('テキストが正常に送信されました');
//         } else {
//             console.log('テキスト送信に失敗しました');
//         }
//     })
//     .catch(error => {
//         console.log('エラーが発生しました:', error);
//     });
// }


function logout() {
    const token = localStorage.getItem('token');
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
    })
    .then(response => {
        if (response.ok) {
            localStorage.removeItem('token');  // トークンを削除
            window.location.href = '/login';  // ログインページにリダイレクト
        } else {
            alert('Logout failed');
        }
    });
}
