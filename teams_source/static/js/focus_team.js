function sendData(e, type, token) {
    var data = JSON.stringify({"type": type, "user_id": e.id})
    fetch(window.location.href, {
        method: "post",
        headers: {
            "X-CSRFToken": token
        },
        body: data
    })
    .then(() => {
        location.reload()
    })
}