// /static/js/functions.js
export function readAloud() {
    // 登録された単語とそのカタカナ表記
    const wordMap = {
        "東山": "トウザン",
        "ありがとう": "アリガトウ",
        // その他の単語...
    };

    // テキストを取得
    let text = document.getElementById("text").value;

    // テキスト内の単語をカタカナに変換
    for (let word in wordMap) {
        let regex = new RegExp(word, 'g');
        text = text.replace(regex, wordMap[word]);
    }

    // ブラウザにWeb Speech API Speech Synthesis機能があるか判定
    if ('speechSynthesis' in window) {
        // 発言を設定
        const uttr = new SpeechSynthesisUtterance();
        // 文章を設定
        uttr.text = text;

        // 言語 (日本語:ja-JP)
        uttr.lang = 'ja-JP';

        // 音量 0-1
        uttr.volume = 1;

        // 発言を再生
        window.speechSynthesis.speak(uttr);
    } else {
        alert('大変申し訳ありません。このブラウザは音声合成に対応していません。');
    }
}
