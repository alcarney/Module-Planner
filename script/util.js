
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
