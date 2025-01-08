async function logout(){
    const response = await fetch("/user/logout", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" }
        })
    };
    