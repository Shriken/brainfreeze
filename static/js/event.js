BRAIN.Event = (function() {
	var newEvent = function(type, id, timestamp, props) {
		return {
			type : type,
			id : id,
			timestamp : timestamp,
			props : props
		};
	};

	var runEvent = function(e) {
		b = e;
		if (e.type == "ActorSpawned") {
			var unit = BRAIN.Unit.newUnit(e.data.id, e.data.x, e.data.y, e.data.team);
			BRAIN.units.push(unit);
		} else if (e.type == "ActorVelocityChange") {
			var unit = BRAIN.Unit.getUnit(e.data.id);
			if (e.data.x != undefined) {
				unit.x = e.data.x;
			}
			if (e.data.y != undefined) {
				unit.y = e.data.y;
			}
			unit.vx = e.data.vx;
			unit.vy = e.data.vy;
			// Only update the heading if we didn't stop entirely.
			if (unit.vx != 0 || unit.vy != 0) {
				unit.direction = Math.atan2(unit.vy, unit.vx);
			}
		} else if (e.type == "ActorSeen") {
			var unit = BRAIN.Unit.newUnit(e.data.id, e.data.x, e.data.y, 1,
			                                 e.data.vx, e.data.vy);
			BRAIN.units.push(unit);
		} else if (e.type == "ActorHidden") {
			var unit = BRAIN.Unit.getUnit(e.data.id);
			unit.hidden = true;
			unit.vx = 0;
			unit.vy = 0;
		} else if (e.type == "ActorPositionUpdate") {
			var unit = BRAIN.Unit.getUnit(e.data.id);
			unit.x = e.data.x;
			unit.y = e.data.y;
		} else if (e.type == "ActorDied") {
			var unit = BRAIN.Unit.getUnit(e.data.id);
			unit.dead = true;
			unit.vx = 0;
			unit.vy = 0;
			BRAIN.particles.push(BRAIN.Particle.newExplosion(unit.x, unit.y));
		} else {
            console.warn("Unknown Event encountered: " + e.type);
        }
	};

	return {
		newEvent : newEvent,
		runEvent : runEvent,
	};
})();
