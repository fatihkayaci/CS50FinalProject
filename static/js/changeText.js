function updateText() {
    let formData = {};
    
    // form-data sınıfındaki tüm inputları topluyoruz
    $(".form-data").each(function () {
        formData[$(this).attr("id")] = $(this).val();
    });
    console.log(formData);

    // AJAX ile Flask sunucusuna veriyi gönderme
    $.ajax({
        url: "/indexa", // Flask endpointi
        type: "POST",
        data: formData, // Veri URL encoded formatında gönderilecek
        success: function (response) {
            alert("Başarıyla güncellendi: " + response.message);
        },
        error: function (error) {
            console.log(error);
        }
    });
}