

/**

  A simple hook class to call Mustache and Highcharts

**/
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
      var contentType = response.headers.get("content-type");
        return response.text().then(function(text) {
          let output = Mustache.render(text, that.currencies);
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



//Credits :  https://github.com/jfriend00/docReady

(function(funcName, baseObj) {
    "use strict";
    // The public function name defaults to window.docReady
    // but you can modify the last line of this function to pass in a different object or method name
    // if you want to put them in a different namespace and those will be used instead of
    // window.docReady(...)
    funcName = funcName || "docReady";
    baseObj = baseObj || window;
    var readyList = [];
    var readyFired = false;
    var readyEventHandlersInstalled = false;

    // call this when the document is ready
    // this function protects itself against being called more than once
    function ready() {
        if (!readyFired) {
            // this must be set to true before we start calling callbacks
            readyFired = true;
            for (var i = 0; i < readyList.length; i++) {
                // if a callback here happens to add new ready handlers,
                // the docReady() function will see that it already fired
                // and will schedule the callback to run right after
                // this event loop finishes so all handlers will still execute
                // in order and no new ones will be added to the readyList
                // while we are processing the list
                readyList[i].fn.call(window, readyList[i].ctx);
            }
            // allow any closures held by these functions to free
            readyList = [];
        }
    }

    function readyStateChange() {
        if ( document.readyState === "complete" ) {
            ready();
        }
    }

    // This is the one public interface
    // docReady(fn, context);
    // the context argument is optional - if present, it will be passed
    // as an argument to the callback
    baseObj[funcName] = function(callback, context) {
        if (typeof callback !== "function") {
            throw new TypeError("callback for docReady(fn) must be a function");
        }
        // if ready has already fired, then just schedule the callback
        // to fire asynchronously, but right away
        if (readyFired) {
            setTimeout(function() {callback(context);}, 1);
            return;
        } else {
            // add the function and context to the list
            readyList.push({fn: callback, ctx: context});
        }
        // if document already ready to go, schedule the ready function to run
        // IE only safe when readyState is "complete", others safe when readyState is "interactive"
        if (document.readyState === "complete" || (!document.attachEvent && document.readyState === "interactive")) {
            setTimeout(ready, 1);
        } else if (!readyEventHandlersInstalled) {
            // otherwise if we don't have event handlers installed, install them
            if (document.addEventListener) {
                // first choice is DOMContentLoaded event
                document.addEventListener("DOMContentLoaded", ready, false);
                // backup is window load event
                window.addEventListener("load", ready, false);
            } else {
                // must be IE
                document.attachEvent("onreadystatechange", readyStateChange);
                window.attachEvent("onload", ready);
            }
            readyEventHandlersInstalled = true;
        }
    }
})("docReady", window);


function main(){
  element = document.querySelector('#selector');
  count = 1;
  while (!element && count < 5) setTimeout(function(){}, (count++)*10);
  r.loadChart(element.options[element.selectedIndex].value);
  document.querySelector('#select-button').addEventListener('click', function(e){
    e = document.querySelector("#selector");
    r.loadChart(e.options[e.selectedIndex].value);
  });
}

docReady(function main(){

  var render = new Render('#target', '/currencies');
  render.loadTemplate('/template/index');

  /**
    the snippet code bellow is just to wait until the template are loaded by mustache
  **/
  function load(){
    try{
      selectorElement = document.querySelector('#selector');
      buttonElement = document.querySelector('#select-button');
      if (selectorElement && buttonElement){
        render.loadChart(selectorElement.options[selectorElement.selectedIndex].value);
        buttonElement.addEventListener('click', function(e){
          render.loadChart(selectorElement.options[selectorElement.selectedIndex].value);
        });
      }else {
        setTimeout(load, 200);
      }
    }catch(e){
      render.loadTemplate('/template/index');
    }
  }
  load();
});
