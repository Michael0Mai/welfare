function resizr_pic(){
    if(window.innerWidth < 1100){
        var elements = document.getElementsByClassName("beauty_pic");
        Array.prototype.forEach.call(elements, function (element) {
            element.style.width = "95%";});
    }
    else{
        var elements = document.getElementsByClassName("beauty_pic");
        Array.prototype.forEach.call(elements, function (element) {
            element.style.width = "60%";});
    };
};