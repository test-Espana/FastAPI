function changeBackgroundColor() {
    const hour = new Date().getHours();
    const body = document.body;
    console.log(new Date().getHours());

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