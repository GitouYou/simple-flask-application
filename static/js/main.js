

/**

  A simple hook class to call Mustache and Highcharts

**/

function Content(url) {
  var that = this;
  this.content = false;
  fetch(url)
  .then(function(response) {
      return response.json().then(function(json) {
        that.content = json.currencies;
      });
  });
}

Content.prototype.get = function () {
  if (this.content) return this.content;
};


function render(target, urlTemplate, urlContent){
  var myTemplate, myContent, render;
  fetch(urlTemplate)
  .then(function(response) {
      return response.text().then(function(text) {
        myTemplate = text;
      });
  }).then(function(){
    fetch(urlContent)
    .then(function(response) {
        return response.json().then(function(json) {
          myContent = json;
        });
    })
    .then(function(){
      render = Mustache.render(myTemplate, myContent);
      console.log(render);
      document.querySelector(target).innerHTML  = render;
    });
  });

}


class Render{
  constructor(target, currencies){
    this.target = target;
    this.currencies = [];
    var that = this;
    fetch(currencies)
    .then(function(response) {
        return response.json().then(function(json) {
          that.currencies = json;
        });
    });
  }

  loadTemplate(templateUrl){
    var that = this;
    fetch(templateUrl)
    .then(function(response) {
        return response.text().then(function(text) {
          var output = Mustache.render(text, that.currencies);
          document.querySelector(that.target).innerHTML = output;
        });
    });
  }

  loadChart(chart){
    var that = this;
    if (this.chart == chart) return;
    this.chart = chart;


    /**
      clear all content in a element
    **/
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

function Hook(){
  this.chart = '';
}

Hook.prototype.render = function (target, urlTemplate, urlContent){
  var myTemplate, myContent, render;
  fetch(urlTemplate)
  .then(function(response) {
      return response.text().then(function(text) {
        myTemplate = text;
      });
  }).then(function(){
    fetch(urlContent)
    .then(function(response) {
        return response.json().then(function(json) {
          myContent = json;
        });
    })
    .then(function(){
      render = Mustache.render(myTemplate, myContent);
      document.querySelector(target).innerHTML  = render;
    });
  });
};

Hook.prototype.loadChart = function (chart){
  var that = this;
  if (this.chart == chart) return;
  this.chart = chart;

  /**
    clear all content in a element
  **/
  var myNode = document.querySelector("#chart");
  myNode.innerHTML = '';

  fetch('/chart/' + chart)
  .then(function(response) {
    return response.json().then(function(json) {
      Highcharts.chart('chart', json);
    });
  });
};


docReady(function (){
  var templates = {"index": "/template/index", "banner": "/template/banner"};
  var targets = {"index": "#target", "banner": "#banner"};
  var content = {"index": "/currencies"};
  var hook = new Hook();
  hook.render(targets.index, templates.index, content.index);

  /**
    the snippet code bellow is just to wait until the template are loaded by mustache
  **/
  function load(){




    try{
      var selectorElement = document.querySelector('#selector');
      if (selectorElement){

        var value = selectorElement.options[selectorElement.selectedIndex].value;
        hook.render(targets.banner, templates.banner, '/today/' + value);
        hook.loadChart(value);
        setTimeout(function(){
          document.querySelector("#selector").addEventListener('click', function(e){
            var selectorElement = document.querySelector('#selector');
            var value = selectorElement.options[selectorElement.selectedIndex].value;
            hook.loadChart(value);
            hook.render(targets.banner, templates.banner, '/today/' + value);
        });}, 200);
      }else {
        setTimeout(load, 50);
      }
    }catch(e){
      console.log(e);
    }
  }
  load();
});
