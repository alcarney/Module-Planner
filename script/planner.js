/*
 * This function gets run whenever the page is loaded so for now this is acting as our
 * main control function
 */
window.onload = function ()
{
    // Load the canvas and get a 2d context
    var c = document.getElementById("modules");
    var ctx = c.getContext("2d");

}
// {{{ --------------------------------------------- Course Class ----------------------------------------

/*
 * We are going to wrap everything in a "Course" Class it will handle
 * all the logic on the placement of the modules and handles their inter
 * dependencies
 */

/*
 * The Course Class Constructor function
 *
 * Arguements:
 *              course: The URL of the JSON file describing the contents of the course
 */
function Course(course)
{
    /* We need to import the course from the given URL */
    var course_data = JSON.parse(importData(course));

    // Load the Modules
    var modules = loadModules(course_data.course.modules);

    this.loadModules = loadModules;

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

    this.drawModule = drawModule;


    /*
     * This function draws the module 'box' on screen 
     *
     * Arguments:
     *
     *          canvasContext: the context associated with the canvas we
     *                         draw on
     *          x:             the x coord of the upper-left corner of the module box
     *          y:             the y coord of the upper-left corner of the module box
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
