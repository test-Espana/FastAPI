const text      = document.querySelector('#text')
  const speakBtn  = document.querySelector('#speak-btn')
  const cancelBtn = document.querySelector('#cancel-btn')
  const pauseBtn  = document.querySelector('#pause-btn')
  const resumeBtn = document.querySelector('#resume-btn')

  speakBtn.addEventListener('click', function() {
    // 発言を作成
    const uttr = new SpeechSynthesisUtterance(text.value)
    // 発言を再生 (発言キュー発言に追加)
    speechSynthesis.speak(uttr)
  })
  cancelBtn.addEventListener('click', function() {
    // 再生停止 (発言キューをクリアして止まる)
    speechSynthesis.cancel()
  })
  pauseBtn.addEventListener('click', function() {
    // 一時停止 (発言キューを保持して止まる)
    speechSynthesis.pause()
  })
  resumeBtn.addEventListener('click', function() {
    // 再生再開 (一時停止を解除)
    speechSynthesis.resume()
  })