$(document).ready(function() {
    // Function to update the background color of the note form based on the selected color
    $('#id_color').change(function() {
        var selectedColor = $(this).val(); // Get the selected color value
        $('form').css('background-color', selectedColor); // Set the background color of the form
    });
});
