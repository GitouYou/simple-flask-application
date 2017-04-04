/*jshint esversion: 6 */


class Render{
  constructor(target, currencies){
    this.target = target;
    this.currencies = [];
    var that = this;
    fetch(currencies)
    .then(function(response) {
        return response.json().then(function(json) {
          console.log(json);
          that.currencies = json;
        });
    });
  }

  loadTemplate(templateUrl){
    var that = this;
    fetch(templateUrl)
    .then(function(response) {
      var contentType = response.headers.get("content-type");
        return response.text().then(function(text) {
          console.log(text);
          let output = Mustache.render(text, that.currencies);
          document.querySelector(that.target).innerHTML = output;
        });
    });
  }

  loadChart(chart){
    var that = this;
    if (this.chart == chart) return;
    this.chart = chart;

    var myNode = document.querySelector("#chart");
    while (myNode.firstChild) myNode.removeChild(myNode.firstChild);

    fetch('/chart/' + chart)
    .then(function(response) {
      return response.json().then(function(json) {
        Highcharts.chart('chart', json);
      });
    });
  }
}

window.onload = function (){

  var r = new Render('#target', '/currencies');
  r.loadTemplate('/template/index');
  setTimeout(function (){
    element = document.querySelector('#selector');
    console.log(element);
    r.loadChart(element.options[element.selectedIndex].value);
    document.querySelector('#select-button').addEventListener('click', function(e){
      e = document.querySelector("#selector");
      r.loadChart(e.options[e.selectedIndex].value);
    });}, 1000);
  //r.loadChart();
};
