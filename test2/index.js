function redraw() {
    let bbox = document.querySelector(".grid").getBoundingClientRect();
    const min_size = 50;
    let amount_x = Math.ceil(bbox.width / min_size);
    let amount_y = Math.ceil(bbox.height / min_size);
    let size_x = 60;
    let size_y = 60;

    const box_anims = [];

    document.querySelector(".grid").style.setProperty("--sizeX", size_x + "px");
    document.querySelector(".grid").style.setProperty("--sizeY", size_y + "px");
    for (let i = 0; i < amount_x; i++) {
        box_anims.push([]);
        for (let j = 0; j < amount_y; j++) {
            let box = document.createElement("div");
            box.style.setProperty("--col", i);
            box.style.setProperty("--row", j);
            box.classList.add("box");

            document.querySelector(".grid").appendChild(box);
            box_anims[i].push(null);


            box.addEventListener("mouseover", () => {
                /*box.animate([
                    {},
                    {backgroundColor: "transparent"}
                ], {
                    duration: 200,
                    fill: "forwards"
                });*/
            });
            box.addEventListener("mouseout", () => {
                /*box.animate([
                    {},
                    {backgroundColor: "black"}
                ], {
                    duration: 200,
                    fill: "forwards"
                });*/
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