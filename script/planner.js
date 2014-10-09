window.onload = function ()
{
    // Load the canvas and get a 2d context
    var c = document.getElementById("modules");
    var ctx = c.getContext("2d");

    // Load the data from the database
    var analysis = importData("data/analysisIII.json");
    
    // Try and parse the JSON
    var module = JSON.parse(analysis);

    var current_module = new Module(module);
    var module_img = current_module.makeModule(ctx);
    ctx.putImageData(module_img, 50, 50);


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
