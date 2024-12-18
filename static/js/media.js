var photopath= '';
var popup = document.getElementById("popup");
var closePopup = document.getElementById("closePopup");
var imageInput = document.getElementById("imageInput");
var imageSelect = document.getElementById("imageSelect");
var changemediaElements = document.querySelectorAll(".changemedia");
var currentImageBox; // Tıklanan resmi belirlemek için değişken
var order = 0;
$(document).ready(function () {
    // Her resim kutusuna tıklama olayı ekle
    changemediaElements.forEach(function (element) {
        var imgElement = element.querySelector("img");
        imgElement.classList.add(order);
        order++;
        element.addEventListener('click', function () {
            currentImageBox = element.querySelector("img"); // Tıklanan resmin img etiketi
            var classList = currentImageBox.classList; // Tüm sınıfları al
            photopath = classList[0];
            popup.style.display = "flex";
            order = element.querySelector("img").className;
        });
    });

    console.log("Order: " + order);
    // Popup kapatma işlemi
    closePopup.addEventListener('click', function () {
        popup.style.display = "none";
    });
});
    function updateMedia() {
        let formData = new FormData(); // FormData oluştur
        
        let imageInput = $("#imageInput")[0]; // Resim input elementi
        let imageFile = imageInput.files[0]; // Seçilen dosya
        var selectedValue = imageSelect.value;

        console.log(imageInput);
        console.log(imageFile);
        console.log(selectedValue);
        console.log(photopath);


        if (imageFile) {
            formData.append("image", imageFile); // Dosya içeriğini ekle
            formData.append("imageName", imageFile.name); // Dosya adını ekle
            formData.append("order", order);
            formData.append("photopath", photopath);
        }else if(selectedValue){
            formData.append("imageName", selectedValue);
            formData.append("order", order);
            formData.append("photopath", photopath);
        }else {
            alert("Lütfen önce bir resim seçin.");
            return;
        }
        // AJAX ile Flask'e gönder
        $.ajax({
            url: "/uploadmedia", // Flask endpoint
            type: "POST",
            data: formData,
            contentType: false, // Otomatik olarak form-data ayarı yapılır
            processData: false, // FormData için gerekli
            success: function (response) {
                alert("Başarıyla yüklendi: " + response.message);
            },
            error: function (error) {
                console.error("Hata:", error);
            }
        });
    }