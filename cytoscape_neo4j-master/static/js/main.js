//if (window.imageMode) {
//    window.imageMode = true;
//}

var imageMode = false;

$(document).on('click', '.switch-form-submit', function () {
     $("svg").remove();

    if (!imageMode) {
        alert('hello');
        $("#depot_js").attr("src","/static/js/d3.v3.min.js");
        $("#showMode_js").attr("src","/static/js/img_network.js");
    } else {
        alert('hhhhhhhhhh');
        $("#depot_js").attr("src","/static/js/d3.v4.min.js");
        $("#showMode_js").attr("src","/static/js/force_node.js");
    }

    imageMode = !imageMode;



//var jsElem = document.createElement('script');
//jsElem.src='/static/js/d3.v4.min.js';
//document.getElementsByTagName('head')[0].appendChild(jsElem);
//
//var jsElem2 = document.createElement('script');
//jsElem2.src='/static/js/force_node.js';
//document.getElementsByTagName('head')[0].appendChild(jsElem2);

});