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
// {{{ --------------------------------------------- Course Class ----------------------------------------

/*
 * We are going to wrap everything in a "Course" Class it will handle
 * all the logic on the placement of the modules and handles their inter
 * dependencies
 */

/*
 * The Course Class Constructor function
 *
 * Arguments:
 *              course: The URL of the JSON file describing the contents of the course
 */
function Course(course)
{
    /* We need to import the course from the given URL */
    var course_data = JSON.parse(importData(course));

    // Load the Modules
    this.modules = loadModules(course_data.course.modules);
    this.num_years = course_data.course.num_years;

    // Set the functions
    this.loadModules = loadModules;
    this.sortModules = sortModules;
    this.plotModules = plotModules;

    /*
     * This function organises the modules ready to be 
     * drawn on screen
     *
     * Currently this only works by sorting them by year, we will at some point 
     * have to try and group them by the requirements they possess
     */
    function sortModules()
    {
        // Create an array of arrays - one for each year
        this.module_grid = [];
        var index = 0;

        for (index = 0 ; index < this.num_years; index++)
        {
            this.module_grid[index] = [];
        }
        //console.log(this.module_grid);

        // Now go through the list of modules and sort them according to year
        for(index = 0 ; index < this.modules.length; index++)
        {
            // Get the next module
            var module = this.modules[index];
            this.module_grid[module.year - 1][this.module_grid[module.year - 1].length] = module;
        }
        //console.log(this.module_grid);
    }

    /*
     * Function that places the modules on screen, once this function
     * works, it should not be changed the arrangement of the modules
     * should be governed by sortModules
     *
     * Arguments:
     *              None
     *
     * Returns:
     *              Nothing
     */
    function plotModules(context)
    {
        // Initialise some variables
        var year_index = 0;
        var module_index = 0
        var y = 0;
        var x = 0;

        // Loop through each year
        for(year_index = 0; year_index < this.module_grid.length; year_index++)
        {
            // Loop through each module
            for(module_index = 0 ; module_index < this.module_grid[year_index].length; module_index++)
            {
                // Draw the module
                this.module_grid[year_index][module_index].drawModule(context, x, y);

                // Increase the y offset
                y += 125;
            }

            // Reset the y offset
            y = 0;

            // Increase the x offset
            x += 200;
        }
    }

    /*
     * Function to load the module data base
     *
     * Arguments:
     *      module_list: An array containing all URLs to the modules in the course
     *
     * Returns:
     *      an array containing all modules in the given list
     */
    function loadModules(module_list)
    {

        // A varible to keep track of the array index
        var index;
        var moduleArray = [];
        var module_json;

        for (index = 0; index < module_list.length ; index++)
        {
            // Load the module data
            module_json = JSON.parse(importData(module_list[index].url));

            // Create the module and add it to the array
            moduleArray[moduleArray.length] = new Module(module_json);
        }

        // Return the array of modules
        return moduleArray;
    }
}
// }}}

// {{{ ----------------------------------------------- Module Class ----------------------------------------------

/*
 * The Module Class Contructor function
 *
 * Arguments:
 *           moduleData: parsed JSON object containing course independant 
 *                       module data
 *           isCore:     A boolean value signifying is this is a core module or not
 */
function Module(moduleData, isCore)
{
    this.name = moduleData.module.name;
    this.year = moduleData.module.year;
    this.isCore = isCore;
    this.yearOffset = 200;

    this.drawModule = drawModule;


    /*
     * This function draws the module 'box' on screen 
     *
     * Arguments:
     *
     *          canvasContext: the context associated with the canvas we
     *                         draw on
     *          y:             the y coord of the upper-left corner of the module box
     *          x:             the x coord of the upper left corner of the module box
     *
     * Returns:
     *
     *          Nothing
     */
    function drawModule(canvasContext, x, y)
    {
        canvasContext.fillStyle = "#FF0000";
        canvasContext.fillRect(x, y, 150, 100);
        canvasContext.fillStyle = "#000000";
        canvasContext.fillText("Module Name: ".concat(this.name), (x + 4),(y + 10));
        canvasContext.fillText("Year: ".concat(this.year), (x + 4),(y + 20));
    }
}
// }}}

// {{{  -------------------------------------------- Utility Functions -----------------------------

/*
 * Function that retrieves a text file at the given URL
 *
 * TODO: This function currently doesn't have any form of erorr
 *       handling for example if there is a 404 error etc.
 *
 * Arguments:
 *
 *          url: The URL of the file to retrieve
 *
 * Returns:
 *          The text contained in the file
 */
function importData(url)
{
    var data_file = new XMLHttpRequest();
    data_file.open("GET", url, false);
    data_file.send(null);

    return data_file.responseText;
}
// }}}
