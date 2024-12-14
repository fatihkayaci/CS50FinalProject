const menuToggle = document.getElementById('menu-toggle');
const menuIcon = menuToggle.querySelector('i');
const navMobile = document.getElementById('nav-mobile');

// Başlangıçta navMobile'ı görünmez yap
navMobile.style.display = 'none';

menuIcon.addEventListener('click', function (e) {
    if (navMobile.classList.contains('active')) {
        // Menü kapanırken
        navMobile.classList.remove('active');

        // Animasyon tamamlandıktan sonra display: none
        navMobile.addEventListener('transitionend', function handler() {
            navMobile.style.display = 'none'; // Animasyon tamamlandıktan sonra display: none
            menuToggle.classList.remove('open'); // Menü kapandığında open sınıfını kaldır
            menuIcon.classList.remove('fa-times'); // İkonu fa-times'dan fa-bars'a döndür
            menuIcon.classList.add('fa-bars');
            navMobile.removeEventListener('transitionend', handler); // Olay dinleyicisini kaldır
        });
    } else {
        // Menü açılmadan önce display: flex
        navMobile.style.display = 'flex'; // Menüyü açmadan önce flex yap
        setTimeout(() => {
            navMobile.classList.add('active'); // Menü açılıyor
        }, 20); // Geçici bir süre bekleyerek animasyonu başlat
    }

    menuToggle.classList.toggle('open');

    if (menuToggle.classList.contains('open')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-times');
    } else {
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
    }

    e.stopPropagation();
});

window.addEventListener('click', function (e) {
    if (!navMobile.contains(e.target) && !menuToggle.contains(e.target)) {
        // Menü kapatılacak
        if (navMobile.classList.contains('active')) {
            navMobile.classList.remove('active');

            // Animasyon tamamlandıktan sonra display: none
            navMobile.addEventListener('transitionend', function handler() {
                navMobile.style.display = 'none'; // Animasyon tamamlandıktan sonra display: none
                menuToggle.classList.remove('open'); // Menü kapandığında open sınıfını kaldır
                menuIcon.classList.remove('fa-times'); // İkonu fa-times'dan fa-bars'a döndür
                menuIcon.classList.add('fa-bars');
                navMobile.removeEventListener('transitionend', handler); // Olay dinleyicisini kaldır
            });
        }
    } else {
        // Eğer navMobile 'none' ise 'flex' yap
        if (navMobile.style.display === 'none') {
            navMobile.style.display = 'flex'; // Menüyü aç
            setTimeout(() => {
                navMobile.classList.add('active'); // Menü açılıyor
            }, 20);
        }
    }
});
