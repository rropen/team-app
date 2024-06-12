function openTeamPage(e) {
    location.assign("/team/" + e.id)
}

function starHover(e) {
    if (e.dataset.star == 'false'){
        e.innerHTML="<i class='fas fa-star'></i>"
        e.dataset.star = 'true'

    }
}

function removeHover(e) {
    if (e.dataset.star == 'true'){
        e.innerHTML="<i class='far fa-star'></i>"
        e.dataset.star = 'false'
    }
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
    for (var team in teams) {
        var teamID = teams[team].id.toString()
        if (!teamID.toUpperCase().includes(input.value.toString().toUpperCase())) {
            teams[team].style.display = "none";
        } else {
            teams[team].style.display = "";
        }
    }
}