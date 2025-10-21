document.addEventListener("DOMContentLoaded", () => {
    const div = document.getElementById("resonancia");
    const cores = ["#3a3aee", "#aaaa22", "#ee3a3a", "#999999", "#4b0082", "#2e8b57"];
    let i = 0;
    setInterval(() => {
        div.style.backgroundColor = cores[i % cores.length];
        div.style.height = "100px";
        div.innerText = "Ressonância: " + cores[i % cores.length];
        i++;
    }, 3000);
});
