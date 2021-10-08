var recent_matches = document.querySelector("#recent_matches");
var entry = document.querySelector("#entry");
var sentinel = document.querySelector("#sentinel");

// function loadRecentMatches() {
//   fetch(
//     `https://api.opendota.com/api/players/${steam_id}/matches?limit=${results}&offset=${offset}&project=heroes`
//   )
//     .then((response) => response.json())
//     .then((data) => {
//       if (!data.length) {
//         sentinel.innerHTML = "No more matches";
//         return;
//       }

//       for (var i = 0; i < data.length; i++) {
//         let new_entry = entry.cloneNode(true);

//         var hero = getUserHero(data[i]["heroes"]);
//         var result = 0;
//         var duration = 0;
//         var kda = 0;

//         new_entry.querySelector("#hero").innerHTML = hero.hero_id;
//         new_entry.querySelector("#result").innerHTML = result;
//         new_entry.querySelector("#duration").innerHTML = duration;
//         new_entry.querySelector("#kda").innerHTML = kda;

//         recent_matches.appendChild(new_entry);
//       }
//       offset = offset + results_num;
//     });
//     offset = offset + results;
// }

// fetch from server using anon function

var intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  loadRecentMatches();
});

intersectionObserver.observe(sentinel);