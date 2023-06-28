function leaveTeam(e, token) {
    console.log(e.id)
    console.log(window.location.href)
    var data = JSON.stringify({"team_id": e.id})
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