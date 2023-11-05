// Set up cell selector listeners

// Newly entered values go to the container indexed by currentContainer,
// at index currentIndex
var currentContainer = 0;
var currentIndex = 0;

// Set up event listeners for the grid on the left


// Set up listeners for the input board on the right
for (var i = 1; i <= 9; ++i) {
    var buttonName = "input-selector-" + i;

    document.getElementById(buttonName)
    .addEventListener("click", () => { handleInput(i) });
}

function handleInput(val) {
    // select URL
}

// const url = "";

// fetch(url)
// .then(data => renderData(data))
// .catch(err => console.error(err));