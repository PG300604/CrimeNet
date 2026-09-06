// Client-side UX improvement for CrimeNet Modals
document.addEventListener('DOMContentLoaded', function() {
    // Dismiss modal on pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' || e.keyCode === 27) {
            const closeBtn = document.getElementById('close-dialog');
            if (closeBtn) {
                closeBtn.click();
            }
        }
    });

    // Dismiss modal when clicking on the dark background overlay #modal or .modal-backdrop
    document.addEventListener('click', function(e) {
        if (e.target && (e.target.id === 'modal' || e.target.classList.contains('modal-backdrop'))) {
            const closeBtn = document.getElementById('close-dialog');
            if (closeBtn) {
                closeBtn.click();
            }
        }
    });
});
