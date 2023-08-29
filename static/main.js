document.addEventListener("DOMContentLoaded", function () {
    let correct = 0;
    let incorrect = 0;
  
    async function fetchSentence() {
      const res = await fetch("/get_sentence");
      const data = await res.json();
      if (data.end) {
        document.getElementById("game").style.display = "none";
        document.getElementById("end").style.display = "block";
        document.getElementById("score").textContent = `Correct: ${correct}, Incorrect: ${incorrect}`;
        return;
      }
      document.getElementById("sentence").textContent = data.sentence.replace(/{}/g, "______");
      document.getElementById("case").textContent = `Case: ${data.case}`;
      document.getElementById("declension").textContent = `Declension: ${data.declension}`;
      document.getElementById("correct_article").value = data.article;
      document.getElementById("correct_adj_ending").value = data.adj_ending;
    }
  
    document.getElementById("submit").addEventListener("click", async function (event) {
      event.preventDefault();
      const userArticle = document.getElementById("user_article").value;
      const userAdjEnding = document.getElementById("user_adj_ending").value;
      const correctArticle = document.getElementById("correct_article").value;
      const correctAdjEnding = document.getElementById("correct_adj_ending").value;
  
      const res = await fetch("/check_answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `user_article=${userArticle}&user_adj_ending=${userAdjEnding}&correct_article=${correctArticle}&correct_adj_ending=${correctAdjEnding}`,
      });
  
      const data = await res.json();
      correct = data.correct;
      incorrect = data.incorrect;
  
      fetchSentence();
    });
  
    fetchSentence();
  });
  