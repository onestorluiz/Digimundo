
function abrirIA(evt, nomeIA) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(nomeIA).style.display = "block";
  evt.currentTarget.className += " active";
}
window.onload = function() {
  var primeiro = document.getElementsByClassName("tablink")[0];
  if (primeiro) primeiro.click();
};
