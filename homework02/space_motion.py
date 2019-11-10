r"""
Simulate the stars/planets/satellites motion in 2D space. Every two objects in the universe are attracted by the gravitational force

$$\vec{F_{ij}} = \frac{G m_i m_j}{r_{ij}^2} \frac{\vec{r_{ij}}}{\|r_{ij}\|}.$$ 

The force that acts on the object $i$ is the vectorial sum of the forces induced by all other (massive) objects

$$\vec{F_i} = \sum_{j \neq i} \vec{F_{ij}}$$

Use SI units, don't be concerned with the speed of the code - do not optimize!!!

Write function that takes any number of space objects (named tuples) as arguments (may not be a list of named tuples for any function!!!) plus the size of the time step and number of time steps. For each object it calculates the force caused by other objects (vector sum of attractive forces). It returns the dictionary with name of the object as a key and tuple of lists of coordinates (one list of x, one of y, every time step one item in list). 

Write a decorator that measures number of calling of each function and their runtime of the functions. The information should be printed to standard output in a form "function_name - number_of_calls - time units\n". The decorator takes optional parameter units which allows to specify time units for printing (default is ms). You can implement the unit measurement only for ns, ms, s, min, h and days.

Below is description of all steps for calculating the update. If you are unsure of precise interface see test script for examples of calling the function.
"""

from collections import namedtuple
import time, math

G = 6.67408e-11
SpaceObject = namedtuple('SpaceObject', 'name mass x y vx vy color')
Force = namedtuple('Force', 'fx fy')

# ========================================

def logging(unit='ms'): # decorator
    def logger(fn):
        def wrapper(*args, **kwargs):
            wrapper.calls += 1
            
            start = time.time() # starts measuring the time
            result = fn(*args, **kwargs)
            end = time.time() # ends measuring the time
            
            exec_time = end - start # calculates the execution time
            
            if (unit == 's'):
                exec_time = exec_time / 1000
            else: # possible to extend for other units
                pass
            
            print(fn.__name__, "-", wrapper.calls, "-", exec_time, unit)
            
            return result
            
        wrapper.calls = 0 # the number of function calls
        
        return wrapper
        
    return logger

# ========================================

@logging(unit='ms')
def calculate_force(specific_object, *objects):
    
    # Final gravitational force and its components
    f_ij = f_x = f_y = 0
    
    # Calculates the sum of gravitational forces and its components
    for object in objects:
    
        # Excludes the specific object
        if (object is specific_object):
            continue
            
        # Calculates the distance between the objects
        distance = math.sqrt(
            (object.x - specific_object.x)**2 + (object.y - specific_object.y)**2
        )
        
        # Calculates the gravitational force
        f_ij += G * specific_object.mass * object.mass / distance**2
        
        # Calculates the components
        f_x += abs(f_ij) * (object.x - specific_object.x) / distance
        f_y += abs(f_ij) * (object.y - specific_object.y) / distance
    
    return Force(f_x, f_y)

# ========================================

@logging(unit='s')
def update_space_object(specific_object, force, timestep):
    
    # Calculates new speed
    final_speed_x = specific_object.vx + force.fx / specific_object.mass * timestep
    final_speed_y = specific_object.vy + force.fy / specific_object.mass * timestep
    
    # Calculates new coordinates
    final_x = specific_object.x + final_speed_x * timestep
    final_y = specific_object.y + final_speed_y * timestep
    
    return SpaceObject(
        specific_object.name,
        specific_object.mass,
        final_x,
        final_y,
        final_speed_x,
        final_speed_y,
        specific_object.color
    )

# ========================================

@logging(unit='ms')
def update_motion(timestep, objects):

    # List of the updated space objects
    updated_objects = list()
    
    # Updates all objects
    for object in objects:
        
        # Calculates the gravitational force and its components
        force = calculate_force(object, *objects)
        
        # Updates the object
        updated_object = update_space_object(object, force, timestep)
        
        # Adds the updated object to the list
        updated_objects.append(updated_object)
    
    return updated_objects
    
# ========================================

@logging()
def simulate_motion(timestep, num_of_timesteps, *objects):

    # Dictionary of the updated space objects
    all_objects_info = dict()
    
    # Copy of the space objects
    all_objects = objects
    
    # Simulates the motion of the space objects
    for _ in range(num_of_timesteps):
    
        # Updates the objects
        all_objects = update_motion(timestep, all_objects)
        
        # Updates the dictionary
        for object in all_objects:
            all_objects_info[object.name] = (object.x, object.y)
            
        yield all_objects_info
