function openTeamPage(e) {
    location.assign("/team/" + e.id)
}

function sendData(e, type, token) {
    var data = JSON.stringify({"type": type, "team_id": e.id})
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

function filterTeams(input) {
    var teams = Array.from(document.getElementById("usersTeams").children)
    for (team in teams) {
        var teamID = teams[team].id.toString()
        if (!teamID.toUpperCase().includes(input.value.toString().toUpperCase())) {
            teams[team].style.display = "none";
        } else {
            teams[team].style.display = "";
        }
    }
}