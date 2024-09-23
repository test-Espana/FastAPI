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
