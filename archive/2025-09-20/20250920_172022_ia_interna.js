document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("textarea").forEach(caixa => {
    caixa.addEventListener("keydown", e => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        alert("🧠 Interpretação simbólica: " + caixa.value);
      }
    });
  });
});