/*
beepmusic.js
  Nick Becker
  17 January, 2016
*/

function initialize() {

};

$("#do4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 261,
    duration: 250
  });
});


$("#re4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 293,
    duration: 250
  });
});

$("#mi4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 329,
    duration: 250
  });
});

$("#fa4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 349,
    duration: 250
  });
});

$("#sol4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 392,
    duration: 250
  });
});

$("#la4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 440,
    duration: 250
  });
});

$("#ti4").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 493,
    duration: 250
  });
});

$("#do5").click(function() {
  $.post("/", {
    action: "beep",
    frequency: 523,
    duration: 250
  });
});

