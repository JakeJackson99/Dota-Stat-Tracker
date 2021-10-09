var recent_matches = document.querySelector("#recent_matches");
var entry = document.querySelector("#entry");
var sentinel = document.querySelector("#sentinel");

const limit = 20;
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

        new_entry.querySelector("#hero").innerHTML = data[i]['hero_name'];
        new_entry.querySelector("#result").innerHTML = "N/A";
        new_entry.querySelector("#duration").innerHTML = data[i]['duration'];
        new_entry.querySelector("#kda").innerHTML = "N/A";

        recent_matches.appendChild(new_entry);
      }


      offset += limit;
    });
}

var intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  loadRecentMatches();
});

intersectionObserver.observe(sentinel);
