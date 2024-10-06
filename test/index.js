function redraw() {
    let bbox = document.querySelector(".grid").getBoundingClientRect();
    const min_size = 80;
    let amount_x = Math.ceil(bbox.width / min_size);
    let amount_y = Math.ceil(bbox.height / min_size);
    let size_x = 80;
    let size_y = 80;

    const box_anims = [];

    for (let i = 0; i < amount_x; i++) {
        box_anims.push([]);
        for (let j = 0; j < amount_y; j++) {
            let box = document.createElement("div");
            box.style.left = i * size_x + "px";
            box.style.top = j * size_y + "px";
            box.style.width = size_x + "px";
            box.style.height = size_y + "px";
            box.classList.add("box");

            document.querySelector(".grid").appendChild(box);
            box_anims[i].push(null);


            box.addEventListener("mouseover", () => {
                box.animate([
                    {},
                    {backgroundColor: "transparent"}
                ], {
                    duration: 200,
                    fill: "forwards"
                });
            });
            box.addEventListener("mouseout", () => {
                box.animate([
                    {},
                    {backgroundColor: "black"}
                ], {
                    duration: 200,
                    fill: "forwards"
                });
            });

        }
    }
}

window.onload = () => {
    redraw();
};

window.onresize = () => {
    document.querySelectorAll(".box").forEach((box) => box.remove());
    redraw();
};