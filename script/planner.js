// {{{ -------------------------------------------------- Events ------------------------

/*
 * This function gets run whenever the page is loaded so for now this is acting as our
 * main control function
 */
window.onload = function ()
{
    // Load the canvas and get a 2d context
    var c = document.getElementById("modules");

    // Resize the canvas to fit/fill screen size
    c.width =  window.innerWidth * 0.9;
    c.height = window.innerHeight * 0.8;

    // Get a drawing context
    var ctx = c.getContext("2d");

    // Load our test course and plot its modules
    var mmath = new Course("data/mmath.json");
    mmath.sortModules();
    mmath.plotModules(ctx);


}

/*
 * This function gets called whenever the window is resized
 */
window.onresize = function ()
{
    var c = document.getElementById("modules");
    c.width =  window.innerWidth * 0.9;
    c.height = window.innerHeight * 0.8;
}

// }}}
