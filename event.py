import collections
import json

class History(object):
    def __init__(self):
        self.histories = {i : PlayerHistory() for i in xrange(2)}
        self.global_history = PlayerHistory()

    def wall_added(self, wall):
        self.throw_event({'timestamp' : wall.world.timestamp,
                          'type' : 'WallAdded',
                          'data' : {'id' : wall.wallID,
                                    'x' : wall.x,
                                    'y' : wall.y,
                                    'width' : wall.width,
                                    'height' : wall.height,
                                    }
                          })

    def actor_spawned(self, actor): #This should only be used on actors that are associated with a team
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorSpawned',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'team' : actor.player,
                                    'actorType' : actor.__class__.__name__,
                                    'typeID' : actor.typeID
                                }
                          })

    def actor_died(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorDied',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y
                                    }
                          })

    def actor_seen(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorSeen',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'type' : actor.___class___.___name__
                                }
                      })

    def actor_hidden(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorHidden',
                          'data' : {'id' : actor.actorID
                                }
                      })

    def actor_trajectory_update(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorTrajectoryUpdate',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'vx' : actor.vx,
                                    'vy' : actor.vy
                                }
                  })

    def throw_event(self, event):
        for player in self.histories:
            self.histories[player].throw_event(event)
        self.global_history.throw_event(event)
        


class PlayerHistory(object):
    def __init__(self):
        self.history = collections.deque()
        self.json_current = False
        self.json = None

    def throw_event(self, new_event):
        #Extend the deque to be large enough to contain the new event.
        while len(self.history) <= new_event['timestamp']:
            self.history.append([])
        #And then add the new event to that list.
        merge_event_into_list(new_event, self.history[new_event['timestamp']])
        self.json_current = False

    def get_event_json(self):
        if self.json_current:
            return self.json
        else:
            self.json = json.dumps([x for x in self.history])
            self.json_current = True


            #TEST CODE
            event_file = open('events.json', 'w')
            event_file.write(self.json)

            return self.json

def merge_event_into_list(new_event, event_list):
    for i in xrange(len(event_list)-1, -1, -1): #iterate backward through the indices
        merged_events = merge_events(new_event, event_list[i])
        if merge_events(new_event, event_list[i]):
            event_list[i] = merge_events(new_event, event_list[i])
            return
    event_list.append(new_event)
    
def merge_events(new_event, old_event):
    if new_event['data']['id'] == old_event['data']['id']:
        new_type = new_event['type']
        old_type = old_event['type']
        if new_type == old_type:
            return new_event
    return False
