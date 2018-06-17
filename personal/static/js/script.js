// DOMSTRINGS 
const DOMstrings = {
    optionalWorkoutSettings: 'optional-dropdown',
    optionalWorkoutSelector: '.optional-selector',
    optionalWorkoutCheckbox: '.optional-checkbox'
};

console.log(document.getElementById(DOMstrings.optionalWorkoutSettings).textContent);

// Workout page script
function workoutUI() {
    const optionalTitle = document.getElementById(DOMstrings.optionalWorkoutSettings);
    const nodesArray = [].slice.call(document.querySelectorAll(DOMstrings.optionalWorkoutSelector));
    const item = document.querySelectorAll(DOMstrings.optionalWorkoutSelector);
    nodesArray.forEach(element => {
        element.style.display = 'none';
    });
    const checkboxes = [].slice.call(document.querySelectorAll(DOMstrings.optionalWorkoutCheckbox));
    checkboxes.forEach(element => {
        element.style.display = 'none';
    });
    optionalTitle.addEventListener('click', function() {
        nodesArray.forEach(element => {
                if (element.style.display === 'block') {
                    document.getElementById('dropdown-icon').classList.add('fa-angle-down');
                    document.getElementById('dropdown-icon').classList.remove('fa-angle-right');
                    element.style.display = 'none';
            } else {
                document.getElementById('dropdown-icon').classList.remove('fa-angle-down');
                document.getElementById('dropdown-icon').classList.add('fa-angle-right');
                element.style.display = 'block';
            }                        
        });
        checkboxes.forEach(element => {
            if (element.style.display === 'block') {
                element.style.display = 'none';
            } else {
                element.style.display = 'block';
            }
        });
    });
    optionalTitle.addEventListener('mouseover', () => {
        optionalTitle.style.cursor = 'pointer';
    });
};

workoutUI();