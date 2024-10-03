document.addEventListener('DOMContentLoaded', function () {
    const Toast = Swal.mixin({
        toast: true,
        position: "bottom-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });

    const toastElement = document.getElementById('toast-data');
    const icon = toastElement.getAttribute('data-icon');
    const title = toastElement.getAttribute('data-title');

    Toast.fire({
        icon: icon,
        title: title
    });
});