document.getElementById("anasayfabaslikbtn").addEventListener("click", function() {
    // Başlık div'ini göster
    document.getElementById("anasayfabaslik").style.display = "block";
    // Hizmetler div'ini gizle
    document.getElementById("anasayfahizmetler").style.display = "none";
});

document.getElementById("anasayfahizmetlerbtn").addEventListener("click", function() {
    // Hizmetler div'ini göster
    document.getElementById("anasayfahizmetler").style.display = "block";
    // Başlık div'ini gizle
    document.getElementById("anasayfabaslik").style.display = "none";
});