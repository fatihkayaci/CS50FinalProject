document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.btnOyunOzel');
    const dataItems = document.querySelectorAll('.dataOzel');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            // Aktif buton classını kaldır
            const activeButton = document.querySelector('.btnOyunOzel.active');
            if (activeButton) {
                activeButton.classList.remove('active');
            }
            // Tıklanan butonu aktif yap
            this.classList.add('active');

            const targetGroup = this.getAttribute('data-target');
            showDataForButton(targetGroup);
        });
    });

    function showDataForButton(group) {
        // Tüm verileri gizle
        dataItems.forEach(data => data.classList.remove('active-data'));

        // İlgili gruptaki verileri göster
        dataItems.forEach(data => {
            const groups = data.getAttribute('data-groups').split(',');
            if (groups.includes(group)) {
                data.classList.add('active-data');
            }
        });
    }
});
