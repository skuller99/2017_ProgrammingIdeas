//$( "#details" ).load( link );
        //document.getElementById("details").style.display = 'none';
        //setTimeout(function(){console.log(document.getElementById("details").innerHTML)}, 1000);
        //setTimeout(function(){change(element,document.getElementById("details").innerHTML)}, 1000);
        //document.getElementById("details").style.display = 'block';

function change(element,text){
    var textToDisplay = "";
    textToDisplay += element.innerHTML + "<br>";

    var patt = /neha">(.*)<span class="lesi">/;
    var regex = patt.exec(text);
    textToDisplay += "Pronunciation: " + regex[1] + "<br>";

    var patt = /Unihan definition:<\/b>(.*)<\/p><p><b>Number/;
    var regex = patt.exec(text);
    textToDisplay += "Definition: " + regex[1] + "<br>";

    var patt = /Number of strokes:<\/b>(.*)<br><small>Examples of other characters/;
    var regex = patt.exec(text);
    textToDisplay += "Number of strokes: " + regex[1] + "<br>";

    var patt = /Kangxi radical (.*)">(.*)<\/a>&nbsp/;
    var regex = patt.exec(text);
    textToDisplay += "Radical: " + regex[2] + "<br>";

    var patt = /HSK level:<\/b>(.*)<br><small/;
    var regex = patt.exec(text);
    textToDisplay += "HSK level: " + regex[1] + "<br>";

    var patt = /Frequency rank:<\/b>(.*)<\/p><p><b><a href="\/c/;
    var regex = patt.exec(text);
    textToDisplay += "Frequency rank: " + regex[1] + "<br>";

    var patt = /:<\/div> <div style="float:left;padding-left:15px;">(- (.*)<br>)*<\/div/;
    var regex = patt.exec(text);
    array = regex[1].split("<br>");

    textToDisplay += "Translation: <br>";

    for (i = 0; i<array.length-1; i++){
        textToDisplay += "&emsp;- " + array[i].substring(2) + "<br>";
    }

    document.getElementById("details").innerHTML = textToDisplay;
}