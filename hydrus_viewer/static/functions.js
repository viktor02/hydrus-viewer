function humanFileSize(size) {
    // by Andrew V. from SO
    var i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
    return (size / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
}
function colorTags(querySelector) {
    // get the list of tags
    //const tagList = document.querySelectorAll("ul li a");
    const tagList = document.querySelectorAll(querySelector);
    var tagsArray = [];
    // Create a dictionary for the tag color mapping
    const tagColors = {
        creator: "blue",
        meta: "green",
        character: "purple",
        default: "black"
    }

    // iterate over the tags and check if it has a colon
    tagList.forEach(tag => {
        if (tag.textContent.includes(":")) {
            var leftWord = tag.textContent.split(":")[0];
            // Retrieve color from the dictionary and apply it to the tag
            tag.style.color = tagColors[leftWord] || tagColors.default;

            tagsArray.push(tag);
        }
    });
}

// Debounce function to limit the number of requests made
function debounce(fn, delay) {
    let timeoutId;
    return function () {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, arguments), delay);
    };
}

function searchTips(searchValue) {
    const params = new URLSearchParams({
        q: searchValue
    });
    const endpoint = '/predict_tag';
    fetch(`${endpoint}?${params}`)
        .then(response => response.json())
        .then(data => {
            // Handle JSON data here
            const searchResults = document.getElementById('search-results');
            searchResults.innerHTML = '';
            data.forEach(result => {
                const li = document.createElement('li');
                li.innerText = `${result.value} (${result.count})`;
                li.addEventListener("click", function () {
                    // Get the value of the li element
                    const liValue = result.value;
                    //get the current value of input
                    const inputValue = document.getElementById("search-input").value;
                    //split the inputValue to get the last word
                    const inputWords = inputValue.split(" ");
                    //replace the last word with liValue
                    inputWords[inputWords.length - 1] = liValue;
                    //join the words back to form the final value
                    const finalValue = inputWords.join(" ");
                    // Set the value of the search input to the finalValue
                    document.getElementById("search-input").value = finalValue;
                    searchResults.innerHTML = "";
                });
                searchResults.appendChild(li);
            });
        })
        .catch(error => {
            console.error(error);
        });
}

