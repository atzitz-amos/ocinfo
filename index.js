window.onload = () => {
    document.querySelectorAll(".card-background").forEach(el => {
        let onElement = false;
        el.addEventListener("mousemove", (e) => {
            if (!onElement) return;
            console.log(1);
            let animation = el.animate([{}, {
                "--gx": e.offsetX + "px",
                "--gy": e.offsetY + "px"
            }], {
                duration: 2000,
                fill: "forwards"
            });
            animation.onfinish = () => {
                animation.cancel();
            };

        });

        el.addEventListener("mouseleave", () => {
            onElement = false;
            setTimeout(() => {
                el.style.setProperty("--gx", "0px");
                el.style.setProperty("--gy", "0px");
            }, 1200);
        });

        el.addEventListener("mouseenter", () => {
            onElement = true;
        });
    });
};