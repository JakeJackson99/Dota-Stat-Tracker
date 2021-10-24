var recent_matches = document.querySelector("#recent_matches");
var entry = document.querySelector("#entry");
var sentinel = document.querySelector("#sentinel");

const limit = 10;
var offset = 0; // try let instead of var

function loadRecentMatches() {
  fetch(`/recent_matches?limit=${limit}&offset=${offset}`)
    .then((res) => res.json())
    .then((data) => {
      if (!data.length) {
        sentinel.innerHTML = "No more matches";
        return;
      }

      for (var i = 0; i < data.length; i++) {
        let new_entry = entry.cloneNode(true);

        new_entry.querySelector("#hero").innerHTML = data[i]["hero_name"];
        new_entry.querySelector("#result").innerHTML = data[i]["radiant_score"] + " / " + data[i]["dire_score"];
        new_entry.querySelector("#duration").innerHTML = data[i]["duration"];
        new_entry.querySelector("#kda").innerHTML = "N/A";
        new_entry.querySelector("#view_game").innerHTML = `<a href="http://localhost:5000/match/${data[i]["match_id"]}">View</a>`

        recent_matches.appendChild(new_entry);
      }

      offset += limit;
    });
}

function alertM() {
  alert('Hello');
}

var intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  loadRecentMatches();
});

intersectionObserver.observe(sentinel);
