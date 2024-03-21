document.addEventListener('DOMContentLoaded', function () {
    var mySelect = document.getElementById('pet-type');
    var petBreedSelect = document.getElementById('pet-breed'); // Assuming this is the ID of your breed select

    // Function to hide all elements
    function hideAllElements() {
        var allElements = [document.getElementsByClassName('form-dogs'),
                           document.getElementsByClassName('form-cats'),
                           document.getElementsByClassName('form-fishs'),
                           document.getElementsByClassName('form-birds'),
                           document.getElementsByClassName('form-rodents'),
                           document.getElementsByClassName('form-others')];
        allElements.forEach(function(elements) {
            for (var i = 0; i < elements.length; i++) {
                elements[i].style.display = 'none';
            }
        });
    }

    // Function to show elements of a specific class
    function showElementsByClass(className) {
        var elementsToShow = document.getElementsByClassName(className);
        for (var i = 0; i < elementsToShow.length; i++) {
            elementsToShow[i].style.display = 'inline'; // Or 'block', depending on your layout
        }
    }

    // Listen for changes on the pet type select
    mySelect.addEventListener('change', function() {
        hideAllElements(); // Hide all elements initially
        petBreedSelect.value = ""; // Reset the breed select to its default, unselected state

        // Show the relevant elements based on the selected pet type
        if (this.value === "1") {
            showElementsByClass('form-dogs');
        } else if (this.value === "2") {
            showElementsByClass('form-cats');
        } else if (this.value === "4") {
            showElementsByClass('form-fishs');
        } else if (this.value === "3") {
            showElementsByClass('form-birds');
        } else if (this.value === "5") {
            showElementsByClass('form-rodents');
        } else if (this.value === "6") {
            showElementsByClass('form-others');
        }
    });
});
