window.onload = () => {
    document.querySelectorAll(".card").forEach(el => {
        el.addEventListener("mousemove", (e) => {
            el.animate([{}, {
                "--gx": e.offsetX + "px",
                "--gy": e.offsetY + "px"
            }], 300)
        });
        el.addEventListener("mouseleave", () => {

        })
    });
};