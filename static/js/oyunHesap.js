document.addEventListener('DOMContentLoaded', function () {
    // İlk işlev: .btnOyun butonları ve .data içerikleri için
    const buttonsOyun = document.querySelectorAll('.btnOyun');
    const dataItemsOyun = document.querySelectorAll('.data');

    buttonsOyun.forEach(button => {
        button.addEventListener('click', function () {
            // Aktif buton classını kaldır
            const activeButton = document.querySelector('.btnOyun.active');
            if (activeButton) {
                activeButton.classList.remove('active');
            }
            // Tıklanan butonu aktif yap
            this.classList.add('active');

            const targetGroup = this.getAttribute('data-target');
            showDataForButtonOyun(targetGroup);
        });
    });

    function showDataForButtonOyun(group) {
        // Tüm verileri gizle
        dataItemsOyun.forEach(data => data.classList.remove('active-data'));

        // İlgili gruptaki verileri göster
        dataItemsOyun.forEach(data => {
            const groups = data.getAttribute('data-groups').split(',');
            if (groups.includes(group)) {
                data.classList.add('active-data');
            }
        });
    }

    // İkinci işlev: .btnOyunOzel butonları ve .dataOzel içerikleri için
    const buttonsOzel = document.querySelectorAll('.btnOyunOzel');
    const dataItemsOzel = document.querySelectorAll('.dataOzel');

    buttonsOzel.forEach(button => {
        button.addEventListener('click', function () {
            // Aktif buton classını kaldır
            const activeButton = document.querySelector('.btnOyunOzel.active');
            if (activeButton) {
                activeButton.classList.remove('active');
            }
            // Tıklanan butonu aktif yap
            this.classList.add('active');

            const targetGroup = this.getAttribute('data-target');
            showDataForButtonOzel(targetGroup);
        });
    });

    function showDataForButtonOzel(group) {
        // Tüm verileri gizle
        dataItemsOzel.forEach(data => data.classList.remove('active-data'));

        // İlgili gruptaki verileri göster
        dataItemsOzel.forEach(data => {
            const groups = data.getAttribute('data-groups').split(',');
            if (groups.includes(group)) {
                data.classList.add('active-data');
            }
        });
    }
});
