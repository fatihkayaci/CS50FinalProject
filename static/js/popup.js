var popup = document.getElementById("popup");
var closePopup = document.getElementById("closePopup");

function showPopup() {
    popup.style.display = "flex";
}
function offPopup() {
    popup.style.display = "none";
}
closePopup.addEventListener("click", offPopup);