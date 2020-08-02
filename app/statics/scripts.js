var canvas, ctx;
const http = new XMLHttpRequest();

window.onload = function () {
    canvas = new fabric.Canvas('sheet');
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 10;
    canvas.freeDrawingBrush.color = "#000000";
    ctx = canvas.getContext("2d");
}

function save() {
    document.getElementById("canvasimg").style.border = "2px solid";
    var dataURL = canvas.toDataURL();

    var url = "/api/v1/stickman";
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json");
    http.onreadystatechange = function () {
        if (http.readyState === 4 && http.status === 200) {
            var json = JSON.parse(http.responseText);
            console.log(json[0]);
            document.getElementById("canvasimg").src = dataURL.slice(0, 22) + json[0];
            document.getElementById("canvasimg").style.display = "inline";
        }
    };
    var data = JSON.stringify({ "data_input": dataURL.slice(22).toString() });
    http.send(data);
}

function erase() {
    ctx.clearRect(0, 0, 400, 400);
    canvas.clear();
    document.getElementById("canvasimg").style.display = "none";
}
