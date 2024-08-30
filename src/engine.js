!function () {
    const assign = (p, v) => {Object.assign(p.prototype, v)}

    ENGINE = {}

    Object.assign(ENGINE, {
        Vector: function (x, y, z=0) {
            this.x = x;
            this.y = y;
            this.z = z;
        }, PhysicalObject: function(properties = null) {
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
        }
    });

    assign(ENGINE.Vector, {
        add: function(other, y=null, z=null) {
            if (y == null) {
                return new ENGINE.Vector(this.x+other.x, this.y+other.y, this.z + other.z);
            }
            return new ENGINE.Vector(this.x+other, this.y+y, this.z+z);
        }, scalarmult: function(other) {
            return this.x * other.x + this.y * other.y + this.z + other.z;
        }, crossproduct: function(other) {
            return new ENGINE.Vector(
                 this.x * (this.y * other.z - this.z * other.y),
                 -this.y * (this.x * other.z - this.z * other.x),
                 this.z * (this.x * other.y - this.y * other.x)
            );
        }, scale: function(lambda) {
            this.x *= lambda;
            this.y *= lambda;
            this.z *= lambda;
        }, scaled: function(lambda) {
            return new ENGINE.Vector(this.x * lambda, this.y * lambda, this.z * lambda);
        }, norm: function() {
            return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2) + Math.pow(this.z, 2));
        }
    });


}()