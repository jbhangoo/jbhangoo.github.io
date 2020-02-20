var USDA_URL="https://api.ers.usda.gov/data/arms/";
var API_KEY = "USDA-API-KEY";

var AG_STATS_KEY = "AG-KEY"
var AG_STATS_URL="https://quickstats.nass.usda.gov/api/api_GET";


function ersGet(elt) {
  var cmd = document.getElementById("txtResult").value;
  httpGet(USDA_URL+cmd+"?api_key="+API_KEY);
}

function agGet() {

  var crop = document.getElementById("selCrop").value;
  var loctype = "state_alpha"; //document.getElementById("selWhere").value;
  var loc = document.getElementById("txtWhere").value;
  var compare = document.getElementById("selWhen").value;
  var year = document.getElementById("txtWhen").value;
  var url = AG_STATS_URL+"?key="+AG_STATS_KEY+"&"+loctype+"="+loc+"&"+compare+"="+year;
  document.getElementById("txtUrl").innerHTML = url;
  httpGet(url);
}

function httpGet(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("txtResult").innerHTML =url;
        var response = JSON.parse(this.responseText, null, 4);
        var output = ArrayToString(response, 0);
        document.getElementById("txtResult").innerHTML = output;
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function ArrayToString(array, level) {
  var output = "";
  for (var key in array) {
    if ((typeof array[key] == 'string') || (typeof array[key] == 'number')) {
      for (var i=0; i<level; i++)
        output += ' ';
      output += key + ": " + array[key] + "\n";
    } else {
      output += ArrayToString(array[key], level+2);
    }
  }
  return output;
}