window.onload = function ()
{
    // Load the canvas and get a 2d context
    var c = document.getElementById("modules");
    var ctx = c.getContext("2d");

    var modules = ["data/analysisIII.json", "data/algebraII.json", "data/algebraI.json"];

    var module_imgs = loadModules(modules, ctx);

    var index;
    var y = 150;

    for (index = 0 ; index < module_imgs.length ; index++)
    {
        ctx.putImageData(module_imgs[index], 10, y*index);
    }

}

// Function to load the module data base
//      modules: an array containing all the filepaths of the module data
//      context: details of the canvas to draw on
function loadModules(modules, context)
{
    // A varible to keep track of the array index
    var index;
    var moduleArray = [];
    var module;
    var module_data;
    var module_json;
    var url;

    for (index = 0; index < modules.length ; index++)
    {
        // Load the module data
        url = modules[index];
        module_data = importData(url);
        module_json = JSON.parse(module_data);

        // Parse the JSON
        module = new Module(module_json);

        // Get the Module representation
        moduleArray[moduleArray.length] = module.makeModule(context);
    }

    // Return the list of modules
    return moduleArray;
}

// Constructor for a module, takes the following argument
//          moduleData: The parsed JSON file object
function Module(moduleData)
{
    this.name = moduleData.module.name;
    this.year = moduleData.module.year;

    this.makeModule = makeModule;


    // This function draws the module 'box' on screen takes one argument
    //          canvasContext: the context associated with the canvas we
    //                         draw on
    //
    //  It returns the image data representing the module
    function makeModule(canvasContext)
    {
        canvasContext.fillStyle = "#FF0000";
        canvasContext.fillRect(0, 0, 150, 100);
        canvasContext.fillStyle = "#000000";
        canvasContext.fillText("Module Name: ".concat(this.name), 4,10);
        canvasContext.fillText("Year: ".concat(this.year), 4,20);
        var box = canvasContext.getImageData(0,0,150,100);
        canvasContext.clearRect(0,0,150,100);
        return box;
    }
}

// Function to load the JSON file from the database
function importData(url)
{
    var data_file = new XMLHttpRequest();
    data_file.open("GET", url, false);
    data_file.send(null);

    return data_file.responseText;
}

    //ctx.fillStyle = "#FF0000"
    //ctx.fillRect(0,0,150,75);
