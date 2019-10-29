function toggleDarkMode() {
    document.body.classList.toggle("dark");
    if (typeof(Storage) !== "undefined") {
        if (localStorage.darkMode) {
            localStorage.removeItem("darkMode");
        } else {
            localStorage.setItem("darkMode", true);
        }
    }

}

function toggleGridMode() {
    document.body.classList.toggle("grid");
    if (typeof(Storage) !== "undefined") {
        if (localStorage.gridMode) {
            localStorage.removeItem("gridMode");
        } else {
            localStorage.setItem("gridMode", true);
        }
    }

}

if (typeof(Storage) !== "undefined") {
    if (localStorage.darkMode)
        document.body.classList.add("dark");
    if (localStorage.gridMode)
        document.body.classList.add("grid");
}
