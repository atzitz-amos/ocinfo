let canvas, ctx;


window.onload = () => {
    canvas = document.getElementById('c');
    ctx = canvas.getContext('2d');

    draw(`
        mt 340 340
        rpoly -20 -40 40 0 -20 40 $ > yellow + orange
        dup
        rot 90° at bottom $
        dup
        rot 90° at bottom $
        dup
        rot 90° at bottom $
        
        group $0 4
        anim 5 {
            translate 1 1            
        }
    `);
}


/**
 * Commands
 *
 * ------------  DRAW COMMANDS  ------------
 * mt x y                // move to x y
 * lt x y                // line to x y
 * circle r at x y       // circle at x y with radius r
 * rect x y w h          // rectangle at x y with width w and height h
 * arc x y x2 y2 r     // arc from x y to x2 y2 with radius r
 * poly x1 y1 x2 y2 ...  // polygon with vertices x1 y1, x2 y2, ...
 * rpoly x1 y1 x2 y2 ... // polygon with vertices x1 y1, x2 y2, ... given as relative positions to the last point
 * clear x y w h         // clear a rectangle at x y with width w and height h
 * reset                 // clear all
 * ------------  STACK BASED COMMANDS  ------------
 * dup                   // duplicate the top of the stack
 * pop                   // pop the top of the stack
 * swap i                // swap the top of the stack with the ith element
 * ------------ TRANSFORM COMMANDS ------------
 * translate x y         // translate the top of the stack by x and y
 * rot a                 // rotate the top of the stack by a degrees
 * scale x y             // scale the top of the stack by x and y
 * ------------  DIVERSE  ------------
 * rand a b              // push a random number between a and b inclusive
 * ----------------------------------------------------------------------
 *
 * Additional commands:
 *
 * $ > fill             // fill the top of the stack, pop the stack,        /!\ fails if the top of the stack is not a shape
 * $ + stroke           // stroke the top of the stack, pop the stack,      /!\ fails if the top of the stack is not a shape
 * $ > fill + stroke    // fill and stroke the current path
 * #                    // replaced by the top of the stack, pop the stack, /!\ fails if the top of the stack is not a number
 * #(a,b)               // replaced by a number between a and b inclusive
 */


function parseNumericParam(stack, n, isAngle = false) {
    if (n === "#") {
        return stack.pop();
    } else if (n.startsWith("#(")) {
        let parts = n.substring(2, n.length - 1).split(',');
        return Math.floor(Math.random() * (parseInt(parts[1]) - parseInt(parts[0]) + 1)) + parseInt(parts[0]);
    } else {
        if (isAngle && n.endsWith("°")) {
            n = n.substring(0, n.length - 1);
            return parseFloat(n) * Math.PI / 180;
        }
        return parseFloat(n);
    }
}

function isNumeric(n) {
    return !isNaN(parseFloat(n)) && !n.startsWith("#");
}


function recursiveCopy(arr) {
    let copy = [];
    for (let i = 0; i < arr.length; i++) {
        if (Array.isArray(arr[i])) {
            copy.push(recursiveCopy(arr[i]));
        } else {
            copy.push(arr[i]);
        }
    }
    return copy;
}

function executeCommand(command, ox, oy) {
    let cmd = command[0];
    switch (cmd) {
        case "mt":
            ctx.moveTo(command[1] - ox, command[2] - oy);
            break;
        case "lt":
            ctx.lineTo(command[1] - ox, command[2] - oy);
            break;
        case "circle":
            ctx.arc(command[1] - ox, command[2] - oy, command[3], command[4], command[5]);
            break;
        case "rect":
            ctx.rect(command[1] - ox, command[2] - oy, command[3] - ox, command[4] - oy);
            break;
        case "arc":
            ctx.arcTo(command[1] - ox, command[2] - oy, command[3] - ox, command[4] - oy, command[5]);
            break;
    }
}

function parseRotateOrigin(commands, origin) {
    let x = origin[0], y = origin[1];
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

    for (let i = 0; i < commands.length; i++) {
        let cmd = commands[i];
        if (cmd[0] === "mt" || cmd[0] === "lt") {
            minX = Math.min(minX, cmd[1]);
            minY = Math.min(minY, cmd[2]);
            maxX = Math.max(maxX, cmd[1]);
            maxY = Math.max(maxY, cmd[2]);
        } else if (cmd[0] === "circle") {
            minX = Math.min(minX, cmd[1] - cmd[3]);
            minY = Math.min(minY, cmd[2] - cmd[3]);
            maxX = Math.max(maxX, cmd[1] + cmd[3]);
            maxY = Math.max(maxY, cmd[2] + cmd[3]);
        } else if (cmd[0] === "rect") {
            minX = Math.min(minX, cmd[1]);
            minY = Math.min(minY, cmd[2]);
            maxX = Math.max(maxX, cmd[1] + cmd[3]);
            maxY = Math.max(maxY, cmd[2] + cmd[4]);
        } else if (cmd[0] === "arc") {
            minX = Math.min(minX, cmd[1] - cmd[5]);
            minY = Math.min(minY, cmd[2] - cmd[5]);
            maxX = Math.max(maxX, cmd[1] + cmd[5]);
            maxY = Math.max(maxY, cmd[2] + cmd[5]);
        }
    }
    if (x === "left") x = minX;
    else if (x === "right") x = maxX;
    else if (x === "center") x = (minX + maxX) / 2;
    if (y === "top") y = minY;
    else if (y === "bottom") y = maxY;
    else if (y === "center") y = (minY + maxY) / 2;
    return [x, y];
}

function closePath(shape, add_transform = null) {
    let commands = shape[0];
    let transform = shape[1];

    let origin = [0, 0];

    if (add_transform) {
        transform[0] += add_transform[0];
        transform[1] += add_transform[1];
        transform[2] *= add_transform[2];
        transform[3] *= add_transform[3];
        transform[4] += add_transform[4];
    }

    let tlX = transform[0], tlY = transform[1];

    if (shape.length > 2 && shape[2] === "group") {
        for (let i = 0; i < commands.length; i++) {
            closePath(commands[i], transform);
        }
    } else {
        // We need to move the origin to the center of the shape
        // But first we need to find the center of the shape
        if (transform[4] !== 0) {
            origin = parseRotateOrigin(commands, transform[5]);
            tlX += origin[0];
            tlY += origin[1];
        }
        ctx.translate(tlX, tlY);
        ctx.scale(transform[2], transform[3]);
        ctx.rotate(transform[4]);

        for (let i = 0; i < commands.length; i++) {
            executeCommand(commands[i], origin[0], origin[1]);
        }
    }

    ctx.setTransform(1, 0, 0, 1, 0, 0);
}

function finishShape(currentShape, stack, parts) {
    closePath(currentShape);
    stack.push(currentShape);
    currentShape = [[], [0, 0, 1, 1, 0, "none"]];

    let fill = false, stroke = false;
    if (parts[0] === ">") {
        parts.shift();
        ctx.fillStyle = parts.shift();
        ctx.fill();
        fill = true;
    }
    if (parts[0] === "+") {
        parts.shift();
        ctx.strokeStyle = parts.shift();
        ctx.stroke();
        stroke = true;
    }
    if (!fill && !stroke) {
        ctx.fill();
        ctx.stroke();
    }
    ctx.closePath();
    ctx.beginPath();
    return currentShape;
}

function runAnim(duration, obj, from, to, isGroup) {
    let lastTime = 0;
    let totalTime = 0;
    let progress = 0;

    function frame(t) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        totalTime += t - lastTime;
        lastTime = t;
        console.log(duration, progress, totalTime / 1000)
        progress = ((totalTime / 1000) / duration);

        let newTranslate = [
            from[0] + (to[0] - from[0]) * progress,
            from[1] + (to[1] - from[1]) * progress,
            from[2],
            from[3],
            from[4] + to[4] * progress,
        ]

        finishShape([obj, newTranslate, isGroup ? "group" : "shape"], [], [])

        if (progress < 1) requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
}

function draw(s) {
    // ------------  INIT  ------------
    ctx.beginPath();

    let cX = 0, cY = 0;
    let stack = [];
    let currentShape = [[], [0, 0, 1, 1, 0, "none"]];  // [commands, transform], transform = [tx, ty, sx, sy, a, origin]
    let groups = {};

    let animDuration = null;
    let animContext = null;

    // ------------  PARSING  ------------
    let lines = s.split('\n');
    let x, y, r, w, h, a1, a2, tr;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (line.length !== 0) {
            let parts = line.split(' ');
            let cmd = parts.shift();
            switch (cmd) {
                case "mt":
                    cX = parseNumericParam(stack, parts.shift());
                    cY = parseNumericParam(stack, parts.shift());
                    currentShape[0].push(["mt", cX, cY]);
                    break;
                case "lt":
                    cX = parseNumericParam(stack, parts.shift());
                    cY = parseNumericParam(stack, parts.shift());
                    currentShape[0].push(["lt", cX, cY]);
                    break;
                case "circle":
                    r = parseNumericParam(stack, parts.shift());
                    parts.shift();  // We skip the "at" keyword
                    x = parseNumericParam(stack, parts.shift());
                    y = parseNumericParam(stack, parts.shift());
                    a1 = 0;
                    a2 = 2 * Math.PI;
                    if (parts.length > 0 && !isNumeric(parts[0])) {
                        a1 = parseNumericParam(stack, parts.shift(), true);
                    }
                    if (parts.length > 0 && !isNumeric(parts[6])) {
                        a2 = parseNumericParam(stack, parts.shift(), true);
                    }
                    currentShape[0].push(["circle", x, y, r, a1, a2]);
                    break;
                case "rect":
                    x = parseNumericParam(stack, parts.shift());
                    y = parseNumericParam(stack, parts.shift());
                    w = parseNumericParam(stack, parts.shift());
                    h = parseNumericParam(stack, parts.shift());
                    currentShape[0].push(["rect", x, y, w, h]);
                    break;
                case "arc":
                    x = parseNumericParam(stack, parts.shift());
                    y = parseNumericParam(stack, parts.shift());
                    let x2 = parseNumericParam(stack, parts.shift());
                    let y2 = parseNumericParam(stack, parts.shift());
                    r = parseNumericParam(stack, parts.shift());
                    currentShape[0].push(["arc", x, y, x2, y2, r]);
                    break;
                case "poly":
                    while (parts.length > 1 && isNumeric(parts[0]) && isNumeric(parts[1])) {
                        cX = parseNumericParam(stack, parts.shift());
                        cY = parseNumericParam(stack, parts.shift());
                        currentShape[0].push(["lt", cX, cY]);
                    }
                    break;
                case "rpoly":
                    while (parts.length > 1 && isNumeric(parts[0]) && isNumeric(parts[1])) {
                        cX += parseNumericParam(stack, parts.shift());
                        cY += parseNumericParam(stack, parts.shift());
                        currentShape[0].push(["lt", cX, cY]);
                    }
                    break;
                case "clear":
                    x = parseNumericParam(stack, parts.shift());
                    y = parseNumericParam(stack, parts.shift());
                    w = parseNumericParam(stack, parts.shift());
                    h = parseNumericParam(stack, parts.shift());
                    ctx.clearRect(x, y, w, h);
                    break;
                case "reset":
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    stack = [];
                    currentShape = [[], [0, 0, 1, 1, 0, "none"]];
                    break;
                case "dup":
                    if (!Array.isArray(stack[stack.length - 1])) {
                        stack.push(stack[stack.length - 1]);
                        break;
                    }
                    currentShape = recursiveCopy(stack[stack.length - 1]);
                    break;
                case "pop":
                    currentShape = stack.pop();
                    break;
                case "popgroup":
                    currentShape = groups[parts.shift()];
                    break;
                case "pushgroup":
                    stack.push(groups[parts.shift()]);
                    break;
                case "swap":
                    let i = parseNumericParam(stack, parts.shift());
                    let tmp = stack[stack.length - 1];
                    stack[stack.length - 1] = stack[stack.length - 1 - i];
                    stack[stack.length - 1 - i] = tmp;
                    break;
                case "translate":
                    let dx = parseNumericParam(stack, parts.shift());
                    let dy = parseNumericParam(stack, parts.shift());
                    if (animContext) {
                        tr = animContext;
                    } else {
                        tr = currentShape[1];
                    }

                    tr[0] += dx;
                    tr[1] += dy;
                    break;
                case "rot":
                    let da = parseNumericParam(stack, parts.shift(), true);
                    if (animContext) {
                        tr = animContext;
                    } else {
                        tr = currentShape[1];
                    }

                    tr[4] += da;
                    tr[5] = ["center", "center"];
                    if (parts[0] === "at") {
                        parts.shift();
                        let pos = parts.shift();
                        if (pos === "left") {
                            tr[5] = ["left", "center"];
                        } else if (pos === "right") {
                            tr[5] = ["right", "center"];
                        } else if (pos === "top") {
                            tr[5] = ["center", "top"];
                            if (parts.length > 0 && parts[0] === "left" || parts[0] === "right") {
                                tr[5] = [parts.shift(), "top"];
                            }
                        } else if (pos === "bottom") {
                            tr[5] = ["center", "bottom"];
                            if (parts.length > 0 && parts[0] === "left" || parts[0] === "right") {
                                tr[5] = [parts.shift(), "bottom"];
                            }
                        } else if (pos !== "center") {
                            let cx = parseNumericParam(stack, parts.shift());
                            let cy = parseNumericParam(stack, parts.shift());
                            tr[5] = [cx, cy];
                        }

                    }
                    break;
                case "scale":
                    let sx = parseNumericParam(stack, parts.shift());
                    let sy = parseNumericParam(stack, parts.shift());
                    if (animContext) {
                        tr = animContext;
                    } else {
                        tr = currentShape[1];
                    }
                    tr[2] *= sx;
                    tr[3] *= sy;
                    break;
                case "rand":
                    let a = parseNumericParam(stack, parts.shift());
                    let b = parseNumericParam(stack, parts.shift());
                    stack.push(Math.floor(Math.random() * (b - a + 1)) + a);
                    break;
                case "$":
                    currentShape = finishShape(currentShape, stack, parts);
                    break;
                case "group":
                    let name = parts.shift();
                    let count = parseNumericParam(stack, parts.shift());
                    let items = [stack.splice(stack.length - count, count), [0, 0, 1, 1, 0, "none"], "group"];
                    stack.push(items);
                    groups[name] = items;
                    break;
                case "anim":
                    animDuration = parseNumericParam(stack, parts.shift());
                    animContext = [0, 0, 1, 1, 0, "none"];
                    break;
                case "}":  // End of animation
                    const obj = stack.pop();
                    runAnim(animDuration, obj[0], obj[1], animContext, obj[2]);
                    break;
            }
            if (parts.length > 0) {
                if (parts[0] === "$") {
                    parts.shift();
                    currentShape = finishShape(currentShape, stack, parts);
                }
            }
        }
    }
}
