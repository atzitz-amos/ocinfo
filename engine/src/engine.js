!function ($, $$, assign, make_callable, thrower) {
    let ENGINE = {}

    Object.assign(ENGINE, {
        Vector: function (x, y, z = 0) {
            this.x = x;
            this.y = y;
            this.z = z;
        },
        Force: function (name, props, calculator) {
            this.obj = null;
            this.name = name;
            let vector;
            this.vector = vector = new ENGINE.Vector(props.x || 0, props.y || 0, props.z || 0);
            this.position = props.position ? new ENGINE.Vector(props.position.x || 0, props.position.y || 0, props.position.z || 0) : null;
            this.calculate = calculator ? obj => calculator(vector, obj) : obj => vector;
        },
        PhysicalObject: function (visual_converter, properties = null) {
            this.mass = properties.mass || thrower("Mass is required");
            this.inertia_momentum = properties.inertia_momentum;
            this.nogravity = properties.nogravity || false;

            this.position = new ENGINE.Vector(
                properties.x || 0,
                properties.y || 0,
                0
            );

            this.center_of_mass = properties.center_of_mass || this.position.scaled(1); // Copy of the position
            this.forces_sum = new ENGINE.Vector(0, 0, 0);

            this.velocity = new ENGINE.Vector(
                properties.vx || 0,
                properties.vy || 0,
                0
            );
            this.a_velocity = new ENGINE.Vector(
                0,
                0,
                properties.angular_velocity || 0
            );
            this.acceleration = new ENGINE.Vector(
                properties.ax || 0,
                properties.ay || 0,
                0
            );
            this.a_acceleration = new ENGINE.Vector(
                0,
                0,
                properties.angular_acceleration || 0
            );
            this.rot = properties.rot || 0;

            this.id = ENGINE._object_id = (ENGINE._object_id === undefined ? 0 : ENGINE._object_id + 1);
            this._visual_converter = visual_converter;
            this.rendered_obj = null;

            this.world = null;
            this.quadrants = [];

            this.forces = [];
            this.last_updated = 0;

            this.properties = properties;
        },
        SvgObject: function (renderer, id, obj) {
            this.renderer = renderer;
            this.object = obj;
            this.id = id;

            this.children = [];
        },
        SvgObjectChild: function (child, pos) {
            this.element = child;
            this.pos = pos;

            child.style.translate = `${pos[0]}px ${pos[1]}px`;
        },
        World: function (options) {
            this.options = options || {};

            this.objects = {};
            this.objects_list = [];
            this.forces = [];

            this.quadrant_x_size = 1;
            this.quadrant_y_size = 1;
        },
        Renderer: function (options) {
            this.options = options || {};

            this.objects = {};

            this.mode = this.options.mode || "svg";
        },
        Collider: function (world) {
            this.world = world;

            this.maybe_colliding = [];
            this.marked = [];

            this.collisions = [];
        },
        Engine: function (world, options) {
            this.options = options || {};

            this.world = world || new ENGINE.World();
            this.collider = this.options.collider || new ENGINE.Collider(this.world);
            this.renderer = this.options.renderer || new ENGINE.Renderer(options);

            this.world.init(this.renderer);

            this.time = null;
            this.startTimestamp = null;
            this.lastTimestamp = null;

            return this;
        }
    });

    Object.assign(ENGINE, {
        createSquareObject: function (properties) {
            return new ENGINE.PhysicalObject.Square(properties);
        },
        create: function (world, options) {
            if (typeof world === "string") {
                return {
                    "square": ENGINE.createSquareObject
                }[world](options);
            }
            if (!(world instanceof ENGINE.World)) {
                options = world;
                world = new ENGINE.World(options);
            }
            return new ENGINE.Engine(world, options);
        }
    });

    assign(ENGINE.Vector, {
        add: function (other, y = null, z = null) {
            if (y == null) {
                return new ENGINE.Vector(this.x + other.x, this.y + other.y, this.z + other.z);
            }
            return new ENGINE.Vector(this.x + other, this.y + y, this.z + z);
        },
        sub: function (other, y = null, z = null) {
            if (y == null) {
                return new ENGINE.Vector(this.x - other.x, this.y - other.y, this.z - other.z);
            }
            return new ENGINE.Vector(this.x - other, this.y - y, this.z - z);
        },
        scalarmult: function (other) {
            return this.x * other.x + this.y * other.y + this.z + other.z;
        }, crossproduct: function (other) {
            return new ENGINE.Vector(
                (this.y * other.z - this.z * other.y),
                (this.x * other.z - this.z * other.x),
                (this.x * other.y - this.y * other.x)
            );
        }, scale: function (lambda) {
            this.x *= lambda;
            this.y *= lambda;
            this.z *= lambda;
        }, scaled: function (lambda) {
            return new ENGINE.Vector(this.x * lambda, this.y * lambda, this.z * lambda);
        }, norm: function () {
            return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2) + Math.pow(this.z, 2));
        }, normalize: function () {
            let norm = this.norm();
            return new ENGINE.Vector(this.x / norm, this.y / norm, this.z / norm);
        }
    });
    assign(ENGINE.PhysicalObject, {
        attach_to: function (renderer, props) {
            this.rendered_obj = this._visual_converter(this, renderer);
            renderer.add_obj(this.id, this.rendered_obj, props);

            this.update_quadrants();
        },
        update: function (time, world_forces) {
            let elapsed = time - this.last_updated;

            let forces = this.forces.concat(world_forces);
            let sum_force = new ENGINE.Vector(0, 0, 0);

            let normal_force_index = null;
            let i = -1;
            for (let f of forces) {
                i++;
                if (f.name === "gravity" && this.nogravity)
                    continue;
                else if (f.name === "normal") {
                    normal_force_index = i;
                }
                sum_force = sum_force.add(f.calculate(this));
            }

            this.sum_force = sum_force;

            this.acceleration = sum_force.scaled(1 / this.mass);
            this.velocity = this.velocity.add(this.acceleration.scaled(elapsed));
            this.position = this.position.add(this.velocity.scaled(elapsed));

            let torque = new ENGINE.Vector(0, 0, 0);
            for (let f of forces) {
                if (f.obj !== this) {
                    continue;
                }
                let r = f.position ? f.position.scaled(-1) : this.center_of_mass.scaled(-1);  // f.position and this.center_of_mass are relative to the object's position, which simplifies
                torque = torque.add(r.crossproduct(f.vector));
            }

            this.a_acceleration = torque.scaled(1 / this.inertia_momentum);
            this.a_velocity = this.a_velocity.add(this.a_acceleration.scaled(elapsed));
            this.rot += this.a_velocity.z * elapsed;
            this.last_updated = time;


            this.update_quadrants();

            if(normal_force_index) this.forces.splice(normal_force_index);
        },
        update_quadrants: function () {
            let bbox = this.rendered_obj.getBBox();
            this.quadrants = [];
            let q1x = Math.floor(bbox.x / this.world.quadrant_x_size);
            let q1y = Math.floor(bbox.y / this.world.quadrant_y_size);
            let q2x = Math.floor((bbox.x + bbox.width) / this.world.quadrant_x_size);
            let q2y = Math.floor((bbox.y + bbox.width) / this.world.quadrant_y_size);
            this.quadrants.push([q1x, q1y]);
            if (q1x !== q2x && q1y !== q2y) {
                this.quadrants.push([q2x, q2y]);
            }
            if (q1x !== q2x) {
                this.quadrants.push([q2x, q1y]);
            }
            if (q1y !== q2y) {
                this.quadrants.push([q1x, q2y]);
            }
        },
        add_force: function (force) {
            this.forces.push(force);
            force.obj = this;
        },

        set_position: function (vector) {
            if (vector instanceof ENGINE.Vector) {
                this.position = vector;
            } else {
                this.position = new ENGINE.Vector(vector.x || 0, vector.y || 0, vector.z || 0);
            }
        },
        set_velocity: function (vector) {
            if (vector instanceof ENGINE.Vector) {
                this.velocity = vector;
            } else {
                this.velocity = new ENGINE.Vector(vector.x || 0, vector.y || 0, vector.z || 0);
            }
        },
        set_acceleration: function (vector) {
            if (vector instanceof ENGINE.Vector) {
                this.acceleration = vector;
            } else {
                this.acceleration = new ENGINE.Vector(vector.x || 0, vector.y || 0, vector.z || 0);
            }
        },
        set_rot: function (rot) {
            this.rot = rot;
        },
        set_angular_velocity: function (vector) {
            if (vector instanceof ENGINE.Vector) {
                this.a_velocity = vector;
            } else {
                this.a_velocity = new ENGINE.Vector(vector.x || 0, vector.y || 0, vector.z || 0);
            }
        },
        set_angular_acceleration: function (vector) {
            if (vector instanceof ENGINE.Vector) {
                this.a_acceleration = vector;
            } else {
                this.a_acceleration = new ENGINE.Vector(vector.x || 0, vector.y || 0, vector.z || 0);
            }
        },
    });
    assign(ENGINE.SvgObject, {
        init: function (props) {
            let w = props.box_width || "100";
            let h = props.box_height || "100";

            this._svg = $$(`svg.obj#obj-${this.id}`, this.renderer.scene, true);
            this._svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
            this._svg.setAttribute("width", w);
            this._svg.setAttribute("height", h);

            this.props = props;

        },
        add_rect: function (x, y, w, h) {
            let rect = $$("rect", this._svg, true);
            rect.setAttribute("x", "0");
            rect.setAttribute("y", "0");
            rect.setAttribute("width", w);
            rect.setAttribute("height", h);


            rect.setAttribute("fill", this.props.fill || "black");
            rect.setAttribute("stroke", this.props.stroke || "none");
            rect.setAttribute("stroke-width", this.props.stroke_width || "2");

            let bbox = this._svg.getBoundingClientRect();
            let pos = [(bbox.width - w) / 2 + x, (bbox.height - h) / 2 + y];
            this.children.push(new ENGINE.SvgObjectChild(rect, pos));
        },
        clear: function () {
            this._svg.innerHTML = "";
        },
        setPositionAndRot: function (x, y, rot) {
            this._svg.style.transform = `translate(${x}px, ${y}px) rotate(${rot}rad)`;
        },
        get_svg_bbox: function () {
            let bbox = this._svg.getBoundingClientRect();
            return {
                x: bbox.x / 100,
                y: bbox.y / 100,
                width: bbox.width / 100,
                height: bbox.height / 100
            };
        },
        graphical_bbox: function () {
            return this._svg.getBoundingClientRect();
        },
        normal_at: function (length) {
            let dx = 1;
            let after = this.children[0].element.getPointAtLength(length + dx)

            let j = length - dx;
            let before = this.children[0].element.getPointAtLength(j < 0 ? this.children[0].element.getTotalLength() + j : j)
            return new ENGINE.Vector(-1, 0, 0)
            return new ENGINE.Vector(-after.y + before.y, after.x - before.x);
        }
    });
    assign(ENGINE.World, {
        init: function (renderer) {
            this.renderer = renderer;
        },
        add: function (obj, props) {
            if (obj instanceof ENGINE.Force) {
                return this.add_force(obj);
            }

            this.objects[obj.id] = obj;
            this.objects_list.push(obj);
            obj.world = this;
            obj.attach_to(this.renderer, props);
        },
        add_force: function (force) {
            this.forces.push(force);
            force.obj = this;
        },
        gravity: function (opt) {
            this.add_force(ENGINE.Force.Gravity(opt));
        },
        update: function (time) {
            for (let id in this.objects) {
                this.objects[id].update(time / 1000, this.forces);
                this.renderer.update_object(this.objects[id]);
            }
        },
        resolve_collision(a, b, inter, all) {
            // First find relative inter based on the position of the scene
            // if (document.querySelector(".dot")) return;
            // for (let int of all) {
            //     int[0] = this.renderer.from_screen_coords(int[0]);
            //     this.plot(int[0].x, int[0].y, int == inter ? "green" : "red", 1);
            // }
            // this.plot(inter[0].x, inter[0].y, "green", 1);
            // console.log(inter[0].x*100, inter[0].x*100, inter[1].before.x, inter[1].before.y, inter[1].after.x, inter[1].after.y);
            // a.velocity = new ENGINE.Vector(0, 0);
            // b.velocity = new ENGINE.Vector(0, 0);
            // return;

            let [rCO, length] = inter;
            rCO = this.renderer.from_screen_coords(rCO);
            nBA = a.rendered_obj.svg_obj.normal_at(length).normalize().scaled(-1);


            let e = 1; // TODO

            let rAO = a.position.add(a.center_of_mass);
            let rAC = rAO.sub(rCO);
            let rBO = b.position.add(b.center_of_mass);
            let rBC = rBO.sub(rCO);

            // if (document.querySelector(".dot")) return;
            //
            // this.plot(rCO.x, rCO.y);
            // this.plot(rBO.x, rBO.y, "red");
            // this.plot(rAO.x, rAO.y, "blue");
            // this.plotVector(rCO.x, rCO.y, nBA, "red");
            // a.velocity = new ENGINE.Vector(0, 0);
            // b.velocity = new ENGINE.Vector(0, 0);
            // return;

            let J = -(1 + e) * (a.velocity.add(a.a_velocity.crossproduct(rAC)).scalarmult(nBA) - b.velocity.add(b.a_velocity.crossproduct(rBC)).scalarmult(nBA))
                / (1 / a.mass + 1 / b.mass + rAC.crossproduct(nBA).crossproduct(rAC).scaled(a.inertia_momentum ** -1).scalarmult(nBA) + rBC.crossproduct(nBA).crossproduct(rBC).scaled(a.inertia_momentum ** -1).scalarmult(nBA))

            a.velocity = a.velocity.add(nBA.scaled(J / a.mass));
            b.velocity = b.velocity.sub(nBA.scaled(J / b.mass));

            a.a_velocity = a.a_velocity.add(rAC.crossproduct(nBA).scaled(J * a.inertia_momentum ** -1));
            b.a_velocity = b.a_velocity.sub(rBC.crossproduct(nBA).scaled(J * b.inertia_momentum ** -1));

            // normal force
            let fA = a.sum_force.crossproduct(nBA.scaled(-1));
            let fB = b.sum_force.crossproduct(nBA);

            a.add_force(ENGINE.Force.NormalForce(fA));
            a.add_force(ENGINE.Force.NormalForce(fB));
        },
        plot: function (x, y, color = "green", size = 5) {
            let d = document.createElement("div")
            d.style.background = color;
            d.style.width = size + "px";
            d.style.height = size + "px";
            d.style.borderRadius = "50%";
            d.style.position = "absolute";
            d.className = "dot";
            document.querySelector(".main").appendChild(d);

            d.style.left = x * 100 - size / 2 + "px";
            d.style.top = y * 100 - size / 2 + "px";
        }, plotVector: function (x, y, v, color = "green") {
            let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("width", "100%");
            svg.setAttribute("height", "100%");
            svg.style.position = "absolute";

            let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", x * 100);
            line.setAttribute("y1", y * 100);
            line.setAttribute("x2", (x + v.x) * 100);
            line.setAttribute("y2", (y + v.y) * 100);
            line.setAttribute("stroke", color);
            line.setAttribute("stroke-width", "2");

            svg.appendChild(line);
            document.querySelector(".main").appendChild(svg);

        }
    });
    assign(ENGINE.Renderer, {
        init: function (parent, options) {
            this.scene = $$("div.physical-world", parent);
            this.scene.style.width = (options.width + "px") || "100%";
            this.scene.style.height = (options.height + "px") || "100%";
        },
        add_obj: function (id, obj, props) {
            obj.init(this, id, props);
            this.objects[id] = obj;
        },
        render_object: function (obj) {
            this._render(obj, this.objects[obj.id]);
        },
        update_object: function (obj) {
            this.objects[obj.id].setPositionAndRot(obj.position.x, obj.position.y, obj.rot);
        },
        _render: function (p_obj, r_obj) {
            r_obj.render();
            r_obj.setPositionAndRot(p_obj.position.x, p_obj.position.y, p_obj.rot);
        },
        make_obj: function (type) {
            if (this.mode === "svg") {
                if (!(type in ENGINE.SvgObject))
                    thrower("Unsupported object type");
                return new ENGINE.SvgObject[type](...Array.prototype.slice.call(arguments, 1));
            } else {
                thrower("Unsupported mode");
            }
        },
        from_screen_coords: function (coords) {
            let rect = this.scene.getBoundingClientRect();
            return new ENGINE.Vector(coords.x - rect.x, coords.y - rect.y).scaled(1 / 100);
        }
    });
    assign(ENGINE.Engine, {
        reattach: function (parent) {
            this.renderer.init(parent, this.world.options);
        },
        render: function () {
            for (let id in this.world.objects)
                this.renderer.render_object(this.world.objects[id]);
        },
        create: function (t, p) {
            return ENGINE.create(t, p);
        },
        run: function () {
            setTimeout(this._run.bind(this, 0), 0);  // Wait for the next frame, to prevent starting before the objects actually appear
        },
        _run: function (timestamp) {
            if (!this.startTimestamp) {
                this.startTimestamp = timestamp;
            }
            this.time = timestamp - this.startTimestamp;
            this.world.update(this.time);
            this.collider.collide();

            this.fps = Math.round(1000 / (timestamp - this.lastTimestamp));
            this.lastTimestamp = timestamp;

            requestAnimationFrame(this._run.bind(this));
        }
    });

    /**
     * Objects */
    Object.assign(ENGINE.PhysicalObject, {
        Square: function (properties) {
            properties["inertia_momentum"] = properties["inertia_momentum"] || properties.mass * Math.pow(properties.size, 2) / 6000;
            properties["center_of_mass"] = new ENGINE.Vector(0.5, 0.5); // Center of viewBox
            this.size = properties.size || thrower("Size is required");
            return new ENGINE.PhysicalObject(function (obj, renderer) {
                return renderer.make_obj("square", properties.size);
            }, properties);
        }
    });
    Object.assign(ENGINE.SvgObject, {
        square: function (size) {
            this.size = size;

            this.collider = new ENGINE.SvgObject.SVGCollider();
        },
        circle: function (radius) {
            this.radius = radius;
        },
    });
    assign(ENGINE.SvgObject.square, {
        init: function (renderer, id, props) {
            this.svg_obj = new ENGINE.SvgObject(renderer, id, this);
            this.svg_obj.init(props);
        },
        render: function () {
            this.svg_obj.clear();
            this.svg_obj.add_rect(0, 0, this.size, this.size);
        },
        setPositionAndRot: function (x, y, rot) {
            this.svg_obj.setPositionAndRot(x * 100, y * 100, rot); // 1px = 1cm
        },
        getBBox: function () {
            return this.svg_obj.get_svg_bbox();
        }
    });

    /**
     * Forces */
    Object.assign(ENGINE.Force, {
        Gravity: function (intensity) {
            return new ENGINE.Force("gravity", intensity, (vector, obj) => vector.scaled(obj.mass));
        }, Dummy: function (value) {
            return new ENGINE.Force("dummy", value);
        }, NormalForce: function (vec) {
            return new ENGINE.Force("normal", vec);
        }
    });

    /**
     * Colliders
     */
    assign(ENGINE.Collider, {
        init: function () {
            this.collide();
        },
        is_rect_colliding: function (A, B) {
            return A.left < B.right && A.right > B.left && A.top < B.bottom && A.bottom > B.top;
        },
        collide: function () {
            let inter;

            this.update_maybe_colliding();
            if (this.world.options["debug.show_potential_collisions"]) {
                this.world.objects[0].rendered_obj.svg_obj._svg.style.outline = "1px solid black";
                this.world.objects[1].rendered_obj.svg_obj._svg.style.outline = "1px solid black";
            }

            for (let [a, b] of this.maybe_colliding) {
                if (this.world.options["debug.show_potential_collisions"]) {
                    a.rendered_obj.svg_obj._svg.style.outline = "1px solid blue";
                    b.rendered_obj.svg_obj._svg.style.outline = "1px solid red";
                }

                [a, b] = a.velocity.norm() > b.velocity.norm() ? [a, b] : [b, a];

                let c1 = a.rendered_obj.collider;
                let c2 = b.rendered_obj.collider;

                if (c1 && c2) {
                    if ((inter = (c1.priority > c2.priority ? c1 : c2).collide_between(a, b)).length !== 0) {
                        this.world.resolve_collision(a, b, this.find_inter(a, b, inter), inter);
                    }
                } else if (c1) {
                    if ((inter = c1.collide_between(a, b)).length !== 0) {
                        this.world.resolve_collision(a, b, this.find_inter(a, b, inter));
                    }
                } else if (c2) {
                    if ((inter = c2.collide_between(a, b)).length !== 0) {
                        this.world.resolve_collision(a, b, this.find_inter(a, b, inter));
                    }
                }
            }
        },
        find_inter: function (a, b, inter) {
            let rel_P = b.position.add(b.center_of_mass).sub(a.position).sub(a.center_of_mass);

            let TL = inter[0];
            let TR = inter[0];
            let BL = inter[0];
            let BR = inter[0];

            let MLR = inter[0];  // Middle of points
            let MBT = inter[0];

            for (let int of inter) {  // Find the TL, TR, BL, BR points
                if (int[0].x <= TL[0].x && int[0].y <= TL[0].y) {  // FIXME
                    TL = int;
                }
                if (int[0].x >= TR[0].x && int[0].y <= TR[0].y) {
                    TR = int;
                }
                if (int[0].x <= BL[0].x && int[0].y >= BL[0].y) {
                    BL = int;
                }
                if (int[0].x >= BR[0].x && int[0].y >= BR[0].y) {
                    BR = int;
                }
            }

            let mX = (TL[0].x + BR[0].x) / 2;
            let mY = (TL[0].y + BR[0].y) / 2;

            for (let int of inter) {
                if (Math.abs(int[0].x - mX) < Math.abs(MLR[0].x - mX)) {
                    MLR = int;
                }
                if (Math.abs(int[0].y - mY) < Math.abs(MBT[0].y - mY)) {
                    MBT = int;
                }
            }

            if (rel_P.x < 0 && rel_P.y < 0) {
                return TL;
            } else if (rel_P.x > 0 && rel_P.y < 0) {
                return TR;
            } else if (rel_P.x < 0 && rel_P.y > 0) {
                return BL;
            } else if (rel_P.x > 0 && rel_P.y > 0) {
                return BR;
            } else if (rel_P.x === 0) {
                return MLR;
            } else if (rel_P.y === 0) {
                return MBT;
            }

        },
        update_maybe_colliding: function () {
            this.maybe_colliding = [];
            let quadrant_seen_x = {};
            let quadrant_seen_y = {};

            let x;
            for (let obj of this.world.objects_list) {
                for (let [qx, qy] of obj.quadrants) {
                    if (qx in quadrant_seen_x && (x = quadrant_seen_y[qy]) != null) {
                        this.maybe_colliding.push([obj, x]);
                        break;
                    }
                }
                for (let [qx, qy] of obj.quadrants) {
                    quadrant_seen_x[qx] = obj;
                    quadrant_seen_y[qy] = obj;
                }
            }
        }
    });

    Object.assign(ENGINE.SvgObject, {
        SVGCollider: function () {
            this.priority = 0; // Lowest priority
        }
    });
    assign(ENGINE.SvgObject.SVGCollider, {
        collide_parts: function (a, b) {
            const t = 0.1;
            const dx = 1;

            let arr = [];

            for (let i = 0; i < a.getTotalLength(); i++) {
                let x = a.getPointAtLength(i)
                x = x.matrixTransform(a.getScreenCTM());

                let y = x.matrixTransform(b.getScreenCTM().inverse())

                let s = window.getComputedStyle(b).strokeWidth;
                b.style.strokeWidth = t + "px!important";

                if (b.isPointInStroke(y)) {
                    // let after = a.getPointAtLength(i + dx)
                    //
                    // let j = i - dx;
                    // let before = a.getPointAtLength(j < 0 ? a.getTotalLength() + j : j)

                    arr.push([x, i]);  // Push normal vector
                }
                b.style.strokeWidth = s;
            }

            return arr;
        },
        collide_between: function (a, b) {
            let arr = [];
            for (let x of a.rendered_obj.svg_obj.children) {
                for (let y of b.rendered_obj.svg_obj.children) {
                    arr = arr.concat(this.collide_parts(x.element, y.element));
                }
            }
            return arr;
        }
    });


    /**
     * END */
    window.ENGINE = make_callable(ENGINE);

}(document.querySelector, (x, s, m) => {
    function _(e, t, v) {
        switch (t) {
            case '.':
                e.classList.add(v);
                break;
            case '#':
                e.id = v;
                break;
        }
    }

    let n = "",
        l = null,
        t = null;
    for (let i of x) {
        if ([".", "#"].includes(i)) {
            if (!l) {
                l = m ? document.createElementNS("http://www.w3.org/2000/svg", n) : document.createElement(n);
            } else {
                _(l, t, n);
            }
            t = i;
            n = "";
        } else n += i;
    }
    if (!l) {
        l = m ? document.createElementNS("http://www.w3.org/2000/svg", n) : document.createElement(n);
    }
    _(l, t, n);

    if (s) {
        s.appendChild(l);
    }
    return l;
}, (p, v) => {
    Object.assign(p.prototype, v)
}, o => {
    function F(cmd) {
        let path = cmd.split(".");
        if (path[0] in o) {
            let x = o;
            let this_ = o;
            for (let i = 0; i < path.length; i++) {
                if (path[i] in x) {
                    x = x[path[i]];
                    if (i < path.length - 1)
                        this_ = x;
                } else {
                    throw "error: " + path[i] + " is not a function";
                }
            }
            return x.call(this_, ...Array.prototype.slice.call(arguments, 1));
        }
        throw "error: " + path[i] + " is not a function";
    }

    for (let k in o) {
        F[k] = o[k];
    }
    return F;
}, msg => {
    throw "error: " + msg;
});
