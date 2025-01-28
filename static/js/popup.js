var popup = document.getElementById("popup");
var closePopup = document.getElementById("closePopup");
let formData = new FormData();
var dataId;
function showPopup(imgElement) {
    dataId = imgElement.getAttribute('data-id');
    formData.append('dataid', dataId);
    console.log(dataId);
    popup.style.display = "flex";
}
function offPopup() {
    popup.style.display = "none";
}
closePopup.addEventListener("click", offPopup);