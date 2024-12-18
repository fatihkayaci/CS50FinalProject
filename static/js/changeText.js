$(document).ready(function () {
    // Tüm input, textarea elementlerine change event'i bağlanır
    $("input, textarea").on("change", function () {
        let inputId = $(this).attr("id");
        let inputValue = $(this).val();

        // AJAX ile Flask sunucusuna veriyi gönder
        $.ajax({
            url: "/indexa",  // Flask endpointi
            type: "POST",
            contentType: "application/json", // JSON formatında veri gönderimi
            data: JSON.stringify({ id_name: inputId, value: inputValue }),
            success: function (response) {
                console.log("Başarıyla güncellendi: ", response.message);
            },
            error: function (error) {
                console.log("Hata: ", error);
            }
        });
    });
});
