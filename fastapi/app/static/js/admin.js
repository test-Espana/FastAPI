document.getElementById("dateFormMain").addEventListener("submit",async function(event) {
    event.preventDefault(); // フォームのデフォルトの動作を防ぐ

    const formData = new FormData(this);

    const response = await fetch("/dateForm", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    document.getElementById("result").textContent = '選択した期間: ${resut.start_date} から ${result.end_date}';
});

function submitForm(action) {
    const form = document.getElementById('dateForm');
    const startDate = form.startDate.value;
    const endDate = form.endDate.value;

    // 日付をクエリパラメータとして指定して遷移
    const url = `${action}?startDate=${startDate}&endDate=${endDate}`;
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    } else {
        console.error('Logout button not found');
    }
});

function logout() {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: token }), // トークンをJSON形式で送信
        })
        .then(response => {
            if (response.ok) {
                localStorage.removeItem('token');  // トークンを削除
                window.location.href = '/login';  // ログインページにリダイレクト
            } else {
                alert('Logout failed');
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
        });
    } else {
        console.error('No token found in localStorage');
    }
}