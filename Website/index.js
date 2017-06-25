function mouseOver(element){
    document.getElementById('mouseOver').innerHTML = element.innerHTML;
}

function cleanOver(){
    document.getElementById('mouseOver').innerHTML = "";
}

function startTime() {
    var today = new Date();    

    document.getElementById('time').innerHTML =
        "<b>Date: </b>" + getDate(today) + "<br>" + "<b>Time: </b>"+ getShortTime(today);

    var t = setTimeout(startTime, 1000);
}


function getDate(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    m = checkTime(m);
    d = checkTime(d);
    return y + "-" + m + "-" + d;
}

function getShortTime(date){
    var h = date.getHours();
    var m = date.getMinutes();
    var s = date.getSeconds();
    h = checkTime(h);
    m = checkTime(m);
    s = checkTime(s);
    return h + ":" + m + ":" + s;
}

function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}

//function getRndInteger(min, max) {
//    return Math.floor(Math.random() * (max - min + 1) ) + min;
//}

function getNavigation(){
    var navigationElement = document.getElementById("navigation");

    navigationElement.innerHTML = 
        '<ul>' +
        '<li><a ' + 
        ((navigationElement.innerHTML == "index") ? 'class="active" ' : '') + 'href="/C:/Svarbus%20reikalai/programos/Web/Mano/index.html">Home</a></li>' +
        '<li><a ' +
        ((navigationElement.innerHTML == "chinese") ? 'class="active" ' : '') + 'href="/C:/Svarbus%20reikalai/programos/Web/Mano/chinese/chinese.html">中文汉子</a></li>' +
        '<li><a ' +
        ((navigationElement.innerHTML == "about") ? 'class="active" ' : '') + 'href="/C:/Svarbus%20reikalai/programos/Web/Mano/me.html">Me</a></li>' +
        '<li><div id = "time" class = "time"></div></li>'+
        '</ul>'

    navigationElement.style.display = 'block';
}

window.onload = function () {
    getNavigation();
    startTime();
}


