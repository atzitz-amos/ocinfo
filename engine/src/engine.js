!function ($, $$, assign, make_callable, thrower) {
    let ENGINE = {}

    Object.assign(ENGINE, {
        Vector: function (x, y, z = 0) {
            this.x = x;
            this.y = y;
            this.z = z;
        },
        Force: function (name, props) {
            this.obj = null;
            this.name = name;
            this.vector = new ENGINE.Vector(props.x || 0, props.y || 0, props.z || 0);
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
            this.rot = 0;

            this.id = ENGINE._object_id = (ENGINE._object_id === undefined ? 0 : ENGINE._object_id + 1);
            this.visual_converter = visual_converter;

            this.world = properties.world || null;
            this.forces = [];
            this.last_updated = 0;

            this.properties = properties;
        },
        SvgObject: function (renderer, id, obj) {
            this.renderer = renderer;
            this.object = obj;
            this.id = id;
        },
        World: function (options) {
            this.options = options || {};

            this.objects = {};
            this.forces = [];
        },
        Renderer: function (options) {
            this.options = options || {};

            this.objects = {};
            this.mode = this.options.mode || "svg";
        },
        Engine: function (world, options) {
            this.options = options || {};

            this.world = world || new ENGINE.World();
            this.renderer = this.options.renderer || new ENGINE.Renderer(options);

            this.world.init(this.renderer);

            this.time = null;
            this.startTimestamp = null;

            return make_callable(this);
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
            return new ENGINE.Engine(world, options);
        }
    });

    assign(ENGINE.Vector, {
        add: function (other, y = null, z = null) {
            if (y == null) {
                return new ENGINE.Vector(this.x + other.x, this.y + other.y, this.z + other.z);
            }
            return new ENGINE.Vector(this.x + other, this.y + y, this.z + z);
        }, scalarmult: function (other) {
            return this.x * other.x + this.y * other.y + this.z + other.z;
        }, crossproduct: function (other) {
            return new ENGINE.Vector(
                this.x * (this.y * other.z - this.z * other.y),
                -this.y * (this.x * other.z - this.z * other.x),
                this.z * (this.x * other.y - this.y * other.x)
            );
        }, scale: function (lambda) {
            this.x *= lambda;
            this.y *= lambda;
            this.z *= lambda;
        }, scaled: function (lambda) {
            return new ENGINE.Vector(this.x * lambda, this.y * lambda, this.z * lambda);
        }, norm: function () {
            return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2) + Math.pow(this.z, 2));
        }
    });
    assign(ENGINE.PhysicalObject, {
        attach_to: function (renderer, props) {
            renderer.add_obj(this.id, this.visual_converter(this, renderer), props);
        },
        update: function (time, world_forces) {
            let elapsed = time - this.last_updated;

            let forces = this.forces.concat(world_forces);
            let sum_force = new ENGINE.Vector(0, 0, 0);
            for (let f of forces) {
                if (f.name === "gravity" && this.nogravity) {
                    continue;
                }
                sum_force = sum_force.add(f.vector);
            }

            this.acceleration = sum_force.scaled(1 / this.mass);
            this.velocity = this.velocity.add(this.acceleration.scaled(elapsed));
            this.position = this.position.add(this.velocity.scaled(elapsed));

            let torque = new ENGINE.Vector(0, 0, 0);
            for (let f of forces) {
                if (f.obj !== this) {
                    continue;
                }
                let r = f.obj.position.add(this.position.scaled(-1));
                torque = torque.add(r.crossproduct(f.vector));
            }

            this.a_acceleration = torque.scaled(1 / this.inertia_momentum);
            this.a_velocity = this.a_velocity.add(this.a_acceleration.scaled(elapsed));
            this.rot += this.a_velocity.z * elapsed;
            this.last_updated = time;
        },
        add_force: function (name, force) {
            if (name instanceof ENGINE.Force) {
            } else {
                name = new ENGINE.Force(name, force);
            }
            name.obj = this;
            this.forces.push(name);
        }
    });
    assign(ENGINE.SvgObject, {
        init: function (props) {
            this._svg = $$(`svg.obj#obj-${this.id}`, this.renderer.scene, true);
            this._svg.setAttribute("viewBox", "0 0 10 10");
            this._svg.setAttribute("width", props.box_width || "100");
            this._svg.setAttribute("height", props.box_height || "100");

            this.props = props;
        },
        add_rect: function (x, y, w, h) {
            let rect = $$("rect", this._svg, true);
            rect.setAttribute("x", x);
            rect.setAttribute("y", y);
            rect.setAttribute("width", w);
            rect.setAttribute("height", h);
            rect.style.translate = `calc(50% - ${w / 2}px) calc(50% - ${h / 2}px)`;

            rect.setAttribute("fill", this.props.fill || "black");
            rect.setAttribute("stroke", this.props.stroke || "none");
            rect.setAttribute("stroke-width", this.props.stroke_width || "0.2");
        },
        clear: function () {
            this._svg.innerHTML = "";
        },
        setPositionAndRot: function (x, y, rot) {
            this._svg.style.transform = `translate(${x}px, ${y}px) rotate(${rot}deg)`;
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
            obj.world = this;
            obj.attach_to(this.renderer, props);
        },
        add_force: function (force) {
            this.forces.push(force);
            force.obj = this;
        },
        update: function (time) {
            for (let id in this.objects) {
                this.objects[id].update(time / 1000, this.forces);
                this.renderer.update_object(this.objects[id]);
            }
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
            requestAnimationFrame(this._run.bind(this));
        },
        _run: function (timestamp) {
            if (!this.startTimestamp) {
                this.startTimestamp = timestamp;
            }
            this.time = timestamp - this.startTimestamp;
            this.world.update(this.time);

            requestAnimationFrame(this._run.bind(this));
        }
    });

    /* Objects */
    Object.assign(ENGINE.PhysicalObject, {
        Square: function (properties) {
            properties["inertia_momentum"] = properties["inertia_momentum"] || properties.mass * Math.pow(properties.size, 2) / 12;
            this.size = properties.size || thrower("Size is required");
            return new ENGINE.PhysicalObject(function (obj, renderer) {
                return renderer.make_obj("square", properties.size);
            }, properties);
        }
    });
    Object.assign(ENGINE.SvgObject, {
        square: function (size) {
            this.size = size;
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
            this.svg_obj.setPositionAndRot(x * 100, y * 100, rot); // x and y are in meters
        }
    });

    /* END */
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
