// Get the modal, the modal image, and the close button
const modal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImg');
const closeBtn = document.querySelector('.modal .close');

// Function to open the modal with the clicked image
document.querySelectorAll('.imgArsiv img').forEach(img => {
    img.addEventListener('click', () => {
        modal.style.display = 'flex';
        modalImg.src = img.src;
    });
});

// Function to close the modal when the close button is clicked
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Function to close the modal when clicking outside the image
modal.addEventListener('click', (e) => {
    if (e.target !== modalImg) {
        modal.style.display = 'none';
    }
});
