function toggleDarkmode() {
    document.body.classList.toggle("dark");
    if (typeof(Storage) !== "undefined") {
        if (localStorage.darkmode) {
            localStorage.removeItem("darkmode");
        } else {
            localStorage.setItem("darkmode", true);
        }
    }

}

if (typeof(Storage) !== "undefined" && localStorage.darkmode) {
    document.body.classList.add("dark");
}
