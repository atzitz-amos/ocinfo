const pos = [
    {x: 20, y: 50},
    {x: 270, y: 220},
    {x: 600, y: 70},
    {x: 750, y: 350},
]

const data = {
    modules: [
        {
            id: "1",
            name: "HTML",
            exercises: [
                {
                    id: "1",
                    name: "Exercice"
                }
            ]
        },
        {
            id: "2",
            name: "CSS",
            exercises: []
        },
        {
            id: "3",
            name: "JavaScript I",
            exercises: []
        },
        {
            id: "4",
            name: "JavaScript II",
            exercises: []
        },
        {
            id: "5",
            name: "React",
            exercises: []
        }
    ],
}

let sceneTranslate = 0;

const scene = {
    currentScene: "main",

    mainTransitions: {
        toModule: (module) => {
            let bbox = module.getBoundingClientRect();
            let left = -bbox.left - bbox.width / 2;
            let top = -bbox.top - bbox.height / 2;
            document.body.style.perspectiveOrigin = (bbox.left + bbox.width / 2 - 10) + "px " + (bbox.top + bbox.height / 2 + 20) + "px";
            document.querySelector(".content").style.transformOrigin = `${left}px ${top}px`;
            document.body.classList.add("transition");
            document.querySelector(".content").animate([
                {transform: "translateZ(0)"},
                {transform: "translateZ(1000px)"}
            ], {
                duration: 1000,
                easing: "cubic-bezier(0.455, 0.030, 0.515, 0.955)"
            }).onfinish = () => {
                let id = module.getAttribute("module-id");
                document.querySelectorAll("[active]").forEach(x => x.removeAttribute("active"));

                try {
                    document.querySelector(".content-exercise-" + id).setAttribute("active", "");
                } catch (e) {
                    console.log(e);
                }

                document.body.classList.remove("transition");
            };
        }
    },


    toModule: (module) => {
        switch (scene.currentScene) {
            case "main":
                scene.mainTransitions.toModule(module);
                break;
        }

    },
    toExercise: (exercise) => {

    },
    toMain: () => {
        document.querySelector("[active]").removeAttribute("active");
        document.querySelector(".content-main").setAttribute("active", "");
    },

    buildScene: () => {
        let main = document.querySelector(".content-main");
        main.setAttribute("active", "");

        data.modules.forEach((module, i) => {
            let moduleEl = document.createElement("div");
            moduleEl.classList.add("module");
            moduleEl.setAttribute("module-id", module.id);
            main.appendChild(moduleEl);

            // TODO: Add support for two digits numbers
            for (let c of "Module") {
                let letter = document.createElement("div");
                letter.classList.add("letter");
                letter.textContent = c;
                moduleEl.appendChild(letter);
            }

            let lastLetter = document.createElement("div");
            lastLetter.classList.add("letter");
            lastLetter.textContent = module.id;
            moduleEl.appendChild(lastLetter);

            drawModule(moduleEl);
            moduleEl.style.translate = `${pos[i % pos.length].x + document.body.clientWidth * Math.floor(i / pos.length)}px ${pos[i % pos.length].y + document.body.clientHeight * Math.floor(i / pos.length)}px`;

            scene.buildExercises(module);
        });
    },
    buildExercises: (module) => {
        let content = document.createElement("div");
        content.classList.add("content-panel");
        content.classList.add("content-exercise-" + module.id);
        document.querySelector(".content").appendChild(content);

        module.exercises.forEach((exercise, i) => {
            let exerciseEl = document.createElement("div");
            exerciseEl.classList.add("exercise");
            for (let c of "Exercice") {
                let letter = document.createElement("div");
                letter.classList.add("letter");
                letter.textContent = c;
                exerciseEl.appendChild(letter);
            }

            let lastLetter = document.createElement("div");
            lastLetter.classList.add("letter");
            lastLetter.textContent = exercise.id;
            exerciseEl.appendChild(lastLetter);
            content.appendChild(exerciseEl);
            exerciseEl.style.translate = `${pos[i % pos.length].x + document.body.clientWidth * Math.floor(i / pos.length)}px ${pos[i % pos.length].y + document.body.clientHeight * Math.floor(i / pos.length)}px`;

            drawModule(exerciseEl, true);
        });
    }
}

function drawModule(module, is_exercise = false) {
    let children = module.children;
    let radius = 100;
    let angle = Math.PI * (is_exercise ? 1.05 : 1.1);
    let total = Math.PI;
    let step = total / (children.length - 1);

    module.style.setProperty("--radius", radius);
    for (let i = 0; i < children.length - 1; i++) {
        let child = children[i];
        child.style.setProperty("--angle", angle);

        angle += step;
    }
    // Put last child in the middle
    let child = children[children.length - 1];
    child.style.left = 0 + "px";
    child.style.top = 0 + "px";


    module.addEventListener("click", (e) => {
        is_exercise ? scene.toExercise(module) : scene.toModule(module);
    });
}

function redraw() {
    let bbox = document.querySelector(".content").getBoundingClientRect();
    const min_size = 10;
    let amount_x = Math.ceil(bbox.width / min_size);
    let amount_y = Math.ceil(bbox.height / min_size);
    let size_x = 60;
    let size_y = 60;

    document.querySelector(".grid").style.setProperty("--sizeX", size_x + "px");
    document.querySelector(".grid").style.setProperty("--sizeY", size_y + "px");
    for (let i = 0; i < amount_x; i++) {
        for (let j = 0; j < amount_y; j++) {
            let box = document.createElement("div");
            box.style.setProperty("--col", i);
            box.style.setProperty("--row", j);
            box.classList.add("box");

            document.querySelector(".grid").appendChild(box);
        }
    }
}

window.onload = () => {
    redraw();
    scene.buildScene();

    document.querySelector(".arrow").addEventListener("click", () => {
        document.querySelector(".content-main").style.transform = `translate(${(++sceneTranslate) * -100}%, ${sceneTranslate * -100}%)`;
        document.querySelector(".arrow").style.translate = `${sceneTranslate * 100}vw ${sceneTranslate * 100}vh`;
    });
};

window.onresize = () => {
    document.querySelectorAll(".box").forEach((box) => box.remove());
    redraw();
};


/*
    let selected = null;
document.querySelectorAll(".letter").forEach((letter) => {
        letter.addEventListener("mousedown", (e) => {
            console.log(1);
            let letter = e.target;

            if (selected) {
                selected.style.outline = "none";
            }
            letter.style.outline = "2px solid lightblue";
            selected = letter;

        });

        letter.addEventListener("mouseup", (e) => {
            console.log(2);
            let letter = e.target;

            if (selected) {
                selected.style.outline = "none";
            }
            selected = null;
        });
    });

    document.body.addEventListener("mousemove", ev => {
        // move selected letter
        if (selected) {
            let bbox = selected.getBoundingClientRect();
            let parentBBox = selected.parentElement.getBoundingClientRect();
            selected.style.position = "absolute";
            selected.style.left = -parentBBox.left + ev.clientX - bbox.width / 2 + "px";
            selected.style.top = -parentBBox.top + ev.clientY - bbox.height / 2 + "px";
        }

    });*/