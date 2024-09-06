Things I have added in SimepleScene.py (added explanations with comments)

1. declare global variables for PA2
# for PA2
render_pos = np.zeros((4,4)) # position for drawing cow object
draw_point = -1 # for counting 6 points
draw_point_pos = [] # save position values for 6 points (later used for roller coaster)
animStartTime = 0  # set animation Start time (when sixth point has decided)
currentPos = [] # used for implementing vertical dragging

2. Catmull-Rom spline curve function
def Catmull_Rom_spline(t, p0, p1, p2, p3):
    # return position using Catmull-Rom Spline
    term0 = t * ((2 - t) * t - 1) * p0 
    term1 = (t * t * (3 * t - 5) + 2) * p1
    term2 = t * ((4 - 3 * t) * t + 1) * p2
    term3 = (t - 1) * t * t * p3

    return (term0 + term1 + term2 + term3) / 2 

input 4 points and time t (0 <= t <= 1) and calculate the postion using Catmull-Rom Spline

3. code for calculating rotation matrix with respect to x,y,z coord based on input using peak pos and finally update render_pos
def set_pos(pos):
    global render_pos
    # calculate peak for calculating rotation matrix for each axis
    peak = np.arcsin(pos[1])

    if np.arctan2(pos[2], pos[0]) < 0:
        peak = -np.arcsin(pos[1])

    Rx = np.array([[1., 0., 0.],
                  [0., np.cos(peak), -np.sin(peak)],
                  [0., np.sin(peak), np.cos(peak)]])

    Ry = np.array([[np.cos(np.arctan2(pos[2], pos[0])), 0., np.sin(np.arctan2(pos[2], pos[0]))],
                   [0., 1., 0.],
                   [-np.sin(np.arctan2(pos[2], pos[0])), 0., np.cos(np.arctan2(pos[2], pos[0]))]])

    Rz = np.array([[1., 0, 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]])

    render_pos[:3, :3] = (Rz@Ry@Rx).T 

4. in display(), I added code for rendering cow roller coaster
    if -1 < draw_point < 6:   # in this if statement, duplicate cow at clicked location
        for pos in draw_point_pos :
            drawCow(pos, True);

    elif draw_point == 6:     # if 6 points are determined
        cow_pos = np.zeros((4,4))  # made for using the value from Catmull-Rom spline curve function
        animTime = (glfw.get_time() - animStartTime) # animStartTime is determined when 6 points are clicked 

        # repeat 3 times ( 6 animTime == 1 roller coaster cycle)
        if animTime < 18:
            # modulo 6(since there are 6 clicked postions) for processing each steps(move between points)
            step = animTime % 6
            t = float(animTime) - int(animTime) # calculate t value with the value between 0~1

            if 0 <= step and step < 1:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[5], draw_point_pos[0], draw_point_pos[1], draw_point_pos[2])
            elif 1 <= step and step < 2:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[0], draw_point_pos[1], draw_point_pos[2], draw_point_pos[3])
            elif 2 <= step and step < 3:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[1], draw_point_pos[2], draw_point_pos[3], draw_point_pos[4])
            elif 3 <= step and step < 4:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[2], draw_point_pos[3], draw_point_pos[4], draw_point_pos[5])
            elif 4 <= step and step < 5:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[3], draw_point_pos[4], draw_point_pos[5], draw_point_pos[0])
            elif 5 <= step and step < 6:
                cow_pos = Catmull_Rom_spline(t, draw_point_pos[4], draw_point_pos[5], draw_point_pos[0], draw_point_pos[1])

        # if finished for looping 3 times, reset the value (return to original state)
        else:
            cow2wld = render_pos
            draw_point = -1
            draw_point_pos.clear()
            glFlush()
            return

        # draw cow riding roller coaster
        set_pos(normalize(getTranslation(cow_pos) - getTranslation(render_pos)))
        setTranslation(render_pos, getTranslation(cow_pos))
        drawCow(render_pos, False)

    # defalut cow
    if draw_point != 6:
        drawCow(cow2wld, cursorOnCowBoundingBox);														# Draw cow.

    glFlush();

5. in initialize(), I added code for setting initial value to global varaible currentPos
global currentPos
currentPos = getTranslation(cow2wld) # set default location

6. in onMouseButton(), I added code for saving clicked positions and numbers until clicking 6 points
global isDrag, V_DRAG, H_DRAG, cow2wld, render_pos, draw_point, draw_point_pos, animStartTime
    # start vertical dragging
        elif state == GLFW_UP and isDrag!=0:
            isDrag=H_DRAG;
            # add new cow positions
            if cursorOnCowBoundingBox:
                if -1 <= draw_point and draw_point < 6: # increment draw_point until 6 (include -1 for inital box click)
                    draw_point += 1
                    
                # to avoid initial click, start from draw_point 1
                if 0 < draw_point and draw_point < 7:
                    draw_point_pos.append(cow2wld.copy()) # save clicked location
                    
                    if draw_point == 6: # if clicked 6 locations, set animStartTime and set reset render_pos with the first clicked location
                        animStartTime = glfw.get_time()
                        render_pos = draw_point_pos[0].copy()
                        isDrag = 0
                
            print( "Left mouse up\n");

7. in onMouseDrag(), I added code for supporting vertical dragging (most of the codes are similar with horizontal dragging)
    if  isDrag==V_DRAG:
        # vertical dragging
        # TODO:
        # create a dragging plane perpendicular to the ray direction, 
        # and test intersection with the screen ray.
        print('vdrag')

        # calculate dragging plane when dragging
        ray = screenCoordToRay(window, x, y);
        pp = pickInfo;
        p = Plane(ray.direction, currentPos)
        c = ray.intersectsPlane(p);

        # for supporting vertical dragging, making currentPos to have 2 items
        currentPos[1] = ray.getPoint(c[1])[1]

        T = np.eye(4)
        setTranslation(T, currentPos-pp.cowPickPosition)
        cow2wld = T@pp.cowPickConfiguration;

# + in existing code for supporting horizontal dragging, I changed original code (pp.cowPickPosition -> currentPos) 
# since the inital value already determined in initialize()
    p=Plane(np.array((0,1,0)), currentPos);