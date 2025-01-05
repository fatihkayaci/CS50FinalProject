var imageSelect = document.getElementById('imageSelect');
var imageInput = document.getElementById('imageInput');
let formData = new FormData();

function updateMedia(filename) {
    const previewImage = document.querySelector(".img-thumbnail"); // Önizleme resmi

    if (imageSelect.value) {
        formData.delete('image_name');
        formData.append('image_name', imageSelect.value);
        previewImage.src = "../../static/img/"+ filename +"/" + imageSelect.value;
    } else if (imageInput.files[0]) {
        formData.delete('image_file');

        formData.append('image_file', imageInput.files[0]);
        
        const fileReader = new FileReader();
        fileReader.onload = function(event) {
            previewImage.src = event.target.result;
        };
        fileReader.readAsDataURL(imageInput.files[0]);
    }
    offPopup();
}