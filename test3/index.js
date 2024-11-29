window.onload = () => {
    document.querySelectorAll(".window-bar").forEach(el => {
        el.addEventListener("mousedown", ev => {
            el.style.cursor = "pointer";
            el.parentElement.classList.add("dragging");

            let bbox = el.parentElement.getBoundingClientRect();

            el.setAttribute("data-dragging-x", -bbox.x + ev.clientX);
            el.setAttribute("data-dragging-y", -bbox.y + ev.clientY);
        });

        el.addEventListener("mouseup", ev => {
            el.style.cursor = "auto";
            el.parentElement.classList.remove("dragging");
        });
    });

    document.addEventListener("mousemove", ev => {
        let el = document.querySelector(".module.dragging");
        if (!el) return;

        let bar = el.querySelector(".window-bar");

        let x = -parseInt(bar.getAttribute("data-dragging-x")) + ev.clientX;
        let y = -parseInt(bar.getAttribute("data-dragging-y")) + ev.clientY;

        el.style.left = x + "px";
        el.style.top = y + "px";

        el.offsetX = el.offsetX;

        let bbox = el.getBoundingClientRect();
        let screenBbox = document.querySelector(".screen").getBoundingClientRect();

        if (bbox.right > screenBbox.width) {
            x -= (bbox.right - screenBbox.width);
        } else if (bbox.left < 0) {
            x += (bbox.left);
        }
        if (bbox.bottom > screenBbox.height) {
            y -= (bbox.bottom - screenBbox.height);
        } else if (bbox.top < 0) {
            y += (bbox.top);
        }

        el.style.left = x + "px";
        el.style.top = y + "px";
    });
};





