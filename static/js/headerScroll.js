window.onscroll = function() {
    var header = document.getElementById("myHeader");
    
    if (window.pageYOffset > 100) {
      header.style.backgroundColor = "#0a0a0a";
    } else {
      header.style.backgroundColor = "transparent";
    }
};