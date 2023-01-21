

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
                    /* BUG: adding only last word */
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

const debouncedSearchTips = debounce(searchTips, 300);

document.getElementById("search-input").addEventListener("keydown", function (e) {
    if (e.keyCode !== 13) {
        var value = document.getElementById('search-input').value;
        if (value.length < 3) {
            return false; // keep form
        } else {
            debouncedSearchTips(this.value);
        }

    }
});