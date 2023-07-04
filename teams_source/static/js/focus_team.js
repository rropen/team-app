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

function deleteTeam(token) {
    var data = JSON.stringify({"type": "delete_team"})
    fetch(window.location.href, {
        method: "post",
        headers: {
            "X-CSRFToken": token
        },
        body: data
    })
    .then(() => {
        location.assign("/team_viewer")
    })
}

function removeTeamButton() {
    document.getElementById("deleteTeamConfirmation").style.display = "block";
}
function closeDeletionMenu() {
    document.getElementById("deleteTeamConfirmation").style.display = "none";
}