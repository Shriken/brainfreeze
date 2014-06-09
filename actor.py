import math

class Actor(object):
    def __init__(self, world, player, x, y):
        self.world = world
        self._x = x
        self._y = y
        self._fov = math.pi / 3
        self._heading = 0
        self._speed = 0
        self.actorID = len(world.actors)
        world.actors.append(self)
        self.max_speed = 10
        self.radius = 0
        self.player = player

    @property
    def typeID(self):
        return self.actorID

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x != self._x + self.vx:
            self._x = x
            self.world.history.actor_trajectory_update(self)
        else:
            self._x = x
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y != self._y + self.vy:
            self._y = y
            self.world.history.actor_trajectory_update(self)
        else:
            self._y = y

    @property
    def heading(self):
        return self._heading


    @heading.setter
    def heading(self, heading):
        """ Set the heading, and generate an event to inform the client of this change """
        if self._heading != heading:
            self._heading = heading
            self.world.history.actor_trajectory_update(self)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        """ Set the speed, clamped to max_speed, and generate an event to inform the client of this change """
        if self._speed != min(speed, self.max_speed):
            self._speed = min(speed, self.max_speed)
            self.world.history.actor_trajectory_update(self)

    @property
    def vx(self):
        return self.speed * math.cos(self.heading)

    @property
    def vy(self):
        return self.speed * math.sin(self.heading)

    def is_colliding_with(self, other):
        """ True if this unit is colliding with other, False otherwise"""
        quadrance = (self.x-other.x)**2 + (self.y-other.y)**2
        colliding_quadrance = (self.radius + other.radius)**2
        return quadrance <= colliding_quadrance

    def can_see(self, x, y):
        theta = math.atan2(x - self.x, y - self.y)

        # check fov
        max_angle = self._heading + self._fov
        min_angle = self._heading - self._fov
        if max_angle > math.pi:
            max_angle -= math.pi * 2
            min_angle -= math.pi * 2
        if max_angle < theta or theta > min_angle:
            return False

        # check walls
        for wall in self.world.walls:
            point_angles = [atan2(x, y) for x,y in wall.corners()]

            # cluster the angles if they are across the polar axis
            if max(point_angles) - min(point_angles) > math.pi:
                point_angles = [t if t > 0 else t + math.pi * 2
                                  for t in point_angles]

            maxa = max(point_angles)
            mina = min(point_angles)
            # TODO add distance logic
            if (maxa > theta and theta > mina):
                return False
            theta += math.pi * 2
            if (maxa > theta and theta > mina):
                return False

        return True
