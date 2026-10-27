
document.addEventListener("DOMContentLoaded", () => {
    // Focus on the title input
    const titleInput = document.querySelector("#title");

    if (titleInput) {
        titleInput.focus();
    }

    // Hide notification messages after 3.5 seconds
    const notices = document.querySelectorAll(".notice");

    notices.forEach((notice) => {
        window.setTimeout(() => {
            notice.style.transition = "opacity 0.4s ease";
            notice.style.opacity = "0";

            window.setTimeout(() => {
                notice.remove();
            }, 400);
        }, 3500);
    });
});
