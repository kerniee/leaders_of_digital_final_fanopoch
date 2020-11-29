var button = $("#smartButton");


button.on("click", async function (e) {
  e.preventDefault();
  // 127.0.0.1     192.168.31.205
  // Срочно до 12:51 починить пресс на участке 234. Поручить это техническое задание мастеру, который сегодня отвечает за этот участок
  var socket = new WebSocket("ws://127.0.0.1:8080");

  socket.onopen = function (e) {
    socket.send($("#smartTaskText").val());
    $("#smartButton").html("Обрабатываю...");
  }

  socket.onmessage = function (event) {
    var data = JSON.parse(event.data);
    var control = $(".form-control");
    if (data[0] === "срочно" || data[0] === "быстро"
      || data[0] === "срочно" || data[0] === "немедленно") {
      control[4].value = 3; // Header
    } else {
      control[4].value = 2;
    }
    control[5].value = data[1];
    control[1].value = data[2] + " " + data[3] + " " + data[4];

    console.log(data);
    console.log(control);
    $("#smartButton").html("Обработать");
    return false;
  };
});