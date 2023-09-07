document.addEventListener("DOMContentLoaded", function() {
  let correct = 0;
  let incorrect = 0;

  function getNewSentence() {
    fetch("/get_sentence")
      .then(response => response.json())
      .then(data => {
        if (data.end) {
          document.getElementById("game").style.display = "none";
          document.getElementById("end").style.display = "block";
          document.getElementById("score").innerText = `Correct: ${correct}, Incorrect: ${incorrect}`;
        } else {
          document.getElementById("sentence").innerText = data.sentence;
          document.getElementById("case").innerText = "Case: " + data.case;
          document.getElementById("declension").innerText = "Declension: " + data.declension;
          document.getElementById("correct_article").value = data.article;
          document.getElementById("correct_adj_ending").value = data.adj_ending;
        }
      });
  }

  getNewSentence();

  document.getElementById("answerForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const userArticle = document.getElementById("user_article").value;
    const userAdjEnding = document.getElementById("user_adj_ending").value;
    const correctArticle = document.getElementById("correct_article").value;
    const correctAdjEnding = document.getElementById("correct_adj_ending").value;

    fetch("/check_answer", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        "user_article": userArticle,
        "user_adj_ending": userAdjEnding,
        "correct_article": correctArticle,
        "correct_adj_ending": correctAdjEnding
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.article === "Correct" && data.adj_ending === "Correct") {
        correct++;
      } else {
        incorrect++;
      }
      getNewSentence();
    });
  });

  // Reset button event listener
  document.getElementById("reset").addEventListener("click", function() {
    location.reload();
  });
});
