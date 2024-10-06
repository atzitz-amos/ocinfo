window.onload = function () {
    document.addEventListener("mousemove", function (e) {
        const x = e.pageX;
        const y = e.pageY;
        const cursor = document.querySelector(".cursor");
        const bbox = cursor.getBoundingClientRect();
        setTimeout(() => {
            cursor.style.left = x - bbox.width / 2 + "px";
            cursor.style.top = y - bbox.height / 2 + "px";
        }, 100);
    });
}