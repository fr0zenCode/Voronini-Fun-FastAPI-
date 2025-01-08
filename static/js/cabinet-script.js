async function redirectToUserCabinet() {
    document.location.href = '/user/me';
}

async function redirectToFeedPage() {;
    document.location.href = '/feed'
}

async function logout() {
    alert( document.cookies );
    const response = await fetch("/user/logout", {
    method: "POST",
    headers: {"Accept": "application/json", "Content-Type": "application/json"}})
    document.location.href = '/user/login';
}
