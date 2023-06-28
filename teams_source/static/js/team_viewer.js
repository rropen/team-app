function leaveTeam(e, token) {
    var data = JSON.stringify({"type": "remove", "team_id": e.id})
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

function joinTeam(e, token) {
    var data = JSON.stringify({"type": "add", "team_id": e.id})
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

function openTeamPage(e) {
    location.assign("/team/" + e.id)
}