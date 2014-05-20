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
		console.log("asdf");
		if (e.type == "ActorSpawned") {
			var unit = BRAIN.Unit.newUnit(e.data.id, e.data.x, e.data.y);
			BRAIN.units.push(unit);
		} else if (e.type == "ActorVelocityChange") {
			// TODO: update unit.x and unit.y based on event
			var unit = BRAIN.Unit.getUnit(e.data.id);
			unit.vx = e.data.vx;
			unit.vy = e.data.vy;
			// Only update the heading if we didn't stop entirely.
			if (unit.vx != 0 && unit.vy != 0) {
				unit.direction = Math.atan2(unit.vy, unit.vx);
			}
		} else if (e.type == "ActorSeen") {
			var unit = BRAIN.Unit.newUnit(e.data.id, e.data.x, e.data.y, 1,
			                                 e.data.vx, e.data.vy);
			BRAIN.units.push(unit);
		} else if (e.type == "ActorHidden") {
			BRAIN.Unit.removeUnit(e.data.id);
		} else if (e.type == "ActorPositionUpdate") {
			var unit = BRAIN.Unit.getUnit(e.data.id);
			unit.x = e.data.x;
			unit.y = e.data.y;
		}
	};

	return {
		newEvent : newEvent,
		runEvent : runEvent,
	};
})();