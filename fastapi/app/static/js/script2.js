// functions.js
export function readAloud() {
	// 登録された単語とそのカタカナ表記
	const wordMap = {
		"東山": "トウザン",
		"ありがとう": "アリガトウ",
		"さようなら": "サヨウナラ",
		"納場": "のうば",
		"時区": "じく",
		"現品票": "ゲンピンヒョウ",
		"先入先出": "サキイレサキダシ",
		"横持ち": "ヨコモチ",
		"積み荷": "ツミニ",
		"荷卸し": "ニオロシ",
		"かんばん": "カンバン",
		"入庫": "ニュウコ",
		"出庫": "シュッコ",
		"パレット": "パレット",
		"台車": "ダイシャ",
		"箱車": "ハコシャ",
		"長爪": "ナガヅメ",
		"構内": "コウナイ",
		"時産": "ジサン",
		"物管": "ブッカン",
		"KD": "ケーディー",
		"昼勤": "ヒルキン",
		"昼夜勤": "チュウヤキン",
		"昼専": "ヒルセン",
		"反対番": "ハンタイバン",
		"指差呼称": "シサコショウ",
		"名和": "ナワ",
		"船見": "フナミ",
		"酒倉": "サカクラ",
		"桐井": "キリイ",
		"福受": "フクジュ",
		"岡物": "オカブツ",
		"小針": "コバリ",
		"加茂": "カモ",
		"GKN": "ジーケーエヌ",
		"水菱": "スイリョウ",
		"久野金": "クノキン",
		"半谷": "ハンヤ"
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

