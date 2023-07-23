// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"


function getSortedItems(items, sortField, sortDirection) {
    items.sort((a, b) => {
        let comparison = 0;
        if (isNaN(a[sortField]) || isNaN(b[sortField])) {
            comparison = a[sortField].localeCompare(b[sortField]);
        } else {
            comparison = Number(a[sortField]) - Number(b[sortField]);
        }
        return sortDirection === 'asc' ? comparison : -comparison;
    });
    return items;
}


function getFilteredItems(items, filterValue) {
    const exclude = filterValue.startsWith('!');
    if (exclude) {
        filterValue = filterValue.slice(1);
    }
    return items.filter(item => {
        if (exclude) {
            for (let key in item) {
                if (typeof item[key] === 'string' && item[key].includes(filterValue)) {
                    return false;
                }
            }
            return true;
        } else {
            for (let key in item) {
                if (typeof item[key] === 'string' && item[key].includes(filterValue)) {
                    return true;
                }
            }
            return false;
        }
    });
}


function toggleTheme() {
    // Przełączanie między jasnym i ciemnym motywem
    document.body.classList.toggle('dark-theme');
}

document.getElementById('theme-button').addEventListener('click', toggleTheme);


function increaseFont() {
    // Zwiększanie rozmiaru czcionki
    document.body.style.fontSize = (parseFloat(getComputedStyle(document.body).fontSize) + 1) + 'px';
}

function decreaseFont() {
    // Zmniejszanie rozmiaru czcionki
    document.body.style.fontSize = (parseFloat(getComputedStyle(document.body).fontSize) - 1) + 'px';
}

