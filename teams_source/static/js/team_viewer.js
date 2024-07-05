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

function favouriteTeam(e, user, id) {
    var data = JSON.stringify({"username":user,"team":id})
    fetch('http://localhost:8000/api/manage/?method=favourite', {
        method:"POST",
        body:data,
    })
    .then(()=>{
        location.reload()
    })
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

function showLeaveTeamModal(button, token) {
    
    window.currentLeaveButton = button;
    window.leaveToken = token;

    const modal = document.getElementById('leaveTeamModal');
    modal.classList.add('is-active');

    document.getElementById('confirmLeaveButton').onclick = function() {
        sendData(window.currentLeaveButton, 'remove', window.leaveToken);

        modal.classList.remove('is-active');
    };

    document.getElementById('cancelLeaveButton').onclick = function() {
        modal.classList.remove('is-active');
    };

    modal.querySelector('.modal-background').onclick = function() {
        modal.classList.remove('is-active');
    };
    modal.querySelector('.modal-close').onclick = function() {
        modal.classList.remove('is-active');
    };
}