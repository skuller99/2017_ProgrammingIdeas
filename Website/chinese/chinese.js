function details(element){
    if (element != null){
        link = "http://hanzidb.org/character/" + element.innerHTML;
        newwindow=window.open(link,'name','height=700,width=700');

        if (window.focus) {
            newwindow.focus()
        };
    } else {
        document.getElementById("details").innerHTML = "";
    }
}

window.onload = function () {
    getNavigation();
    startTime();
    totalElement = document.getElementById("total")
    tableSum = document.querySelectorAll('.character1,.character2,.character3,.character4,.character5');
    totalElement.style.display = 'inline-block';
    totalElement.innerHTML = tableSum.length;
}