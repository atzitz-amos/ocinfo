window.onload = () => {
    let canvas = document.getElementById('c');

    w = document.body.clientWidth;
    h = document.body.clientHeight
    canvas.width = w;
    canvas.height = h;

    ctx = canvas.getContext('2d');

    mx = w / 2;
    my = 10;

    requestAnimationFrame(draw);
};


let ctx;
let w, h, mx, my;
let lastTime = 0;

let path = [];

// Constants
let L0 = 0;
let deltaL = 3;

let B = 1;
let q = 2;

let K = 7;
let g = 9.81;

let slowingFactor = 0.1;


let obj = {
    pos: [0, deltaL + L0], vel: [0, 1], acc: [0, 0], mass: 1
}


function drawForce(x, y, fx, fy, color = "black", text = "", scale = 1) {
    x = x * 100 + mx;
    y = y * 100 + my;
    fx *= 10 * scale;
    fy *= 10 * scale;

    let oldSStyle = ctx.strokeStyle;
    let oldFStyle = ctx.fillStyle;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;

    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + fx, y + fy);
    ctx.stroke()


    let _x, _y, angle;
    let radius = 6;

    ctx.beginPath();

    angle = Math.atan2(fy, fx);
    _x = radius * Math.cos(angle) + x + fx;
    _y = radius * Math.sin(angle) + y + fy;

    ctx.moveTo(_x, _y);

    angle += (1.0 / 3.0) * (2 * Math.PI);
    _x = radius * Math.cos(angle) + x + fx;
    _y = radius * Math.sin(angle) + y + fy;

    ctx.lineTo(_x, _y);

    angle += (1.0 / 3.0) * (2 * Math.PI);
    _x = radius * Math.cos(angle) + x + fx;
    _y = radius * Math.sin(angle) + y + fy;

    ctx.lineTo(_x, _y);

    ctx.fill();

    if (text) {
        ctx.font = "15px monospace";
        ctx.fillText(text, x + fx - 10 * text.length, y + fy - 10);
    }

    ctx.strokeStyle = oldSStyle;
    ctx.fillStyle = oldFStyle;
}


function update(t) {
    let x = obj.pos[0];
    let y = obj.pos[1];
    let vx = obj.vel[0];
    let vy = obj.vel[1];

    path.push([x, y]);

    let alpha = Math.atan2(y, x);

    let forceGy = obj.mass * g;
    let forceKx = -K * (Math.sqrt(x ** 2 + y ** 2) - L0) * Math.cos(alpha);
    let forceKy = -K * (Math.sqrt(x ** 2 + y ** 2) - L0) * Math.sin(alpha);

    let perpendicular = [-vy, vx];
    let norm = Math.sqrt(perpendicular[0] ** 2 + perpendicular[1] ** 2);
    if (norm === 0) {
        perpendicular = [0, 0];
    } else {
        perpendicular[0] /= norm;
        perpendicular[1] /= norm;

    }


    let forceBx = B * Math.sqrt(vx ** 2 + vy ** 2) * q * perpendicular[0];
    let forceBy = B * Math.sqrt(vx ** 2 + vy ** 2) * q * perpendicular[1];

    let forceX = forceKx + forceBx;
    let forceY = forceGy + forceKy + forceBy;


    let ax = forceX / obj.mass;
    let ay = forceY / obj.mass;


    console.log("angle = ", Math.acos((vx * forceX + vy * forceY) / (Math.sqrt(vx ** 2 + vy ** 2) * Math.sqrt(forceX ** 2 + forceY ** 2))) * 180 / Math.PI);

    obj.acc = [ax, ay];
    obj.vel[0] += ax * t;
    obj.vel[1] += ay * t;
    obj.pos[0] += obj.vel[0] * t;
    obj.pos[1] += obj.vel[1] * t;

    drawForce(obj.pos[0], obj.pos[1], obj.vel[0], obj.vel[1], "red", "v", 2);
    drawForce(obj.pos[0], obj.pos[1], 0, forceGy, "green", "Fp");
    drawForce(obj.pos[0], obj.pos[1], forceKx, forceKy, "green", "Fr");
    drawForce(obj.pos[0], obj.pos[1], forceBx, forceBy, "green", "Fb");

    drawForce(obj.pos[0], obj.pos[1], forceX, forceY, "blue", "ΣF");
}

function draw(t) {
    ctx.clearRect(0, 0, w, h)

    ctx.fillRect(mx - 200, my, 400, 10);

    ctx.beginPath();
    ctx.arc(obj.pos[0] * 100 + mx, obj.pos[1] * 100 + 10, 10, 0, Math.PI * 2);
    ctx.fill();

    if (path.length) {
        ctx.beginPath();
        ctx.moveTo(path[0][0] * 100 + mx, path[0][1] * 100 + 10);
        for (let i = 1; i < path.length; i++) {
            ctx.lineTo(path[i][0] * 100 + mx, path[i][1] * 100 + 10);
        }
        ctx.stroke();
    }

    ctx.beginPath();
    ctx.moveTo(mx, my);
    ctx.lineTo(obj.pos[0] * 100 + mx, obj.pos[1] * 100 + my + 10);
    ctx.stroke();


    let dt = t - lastTime;
    lastTime = t;

    update(dt / 1000 * slowingFactor);
    requestAnimationFrame(draw);
}