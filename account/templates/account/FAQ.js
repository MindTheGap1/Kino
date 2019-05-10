var buttons = document.getElementsByClassName("FAQ-button");

for (var i = 0; i < buttons.length; i++) {
  buttons[i].onclick = function () {

  	this.classList.toggle('is-open');
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      // accordion is currently open, so close it
      content.style.maxHeight = null;
    } else {
      // accordion is currently closed, so open it
      content.style.maxHeight = content.scrollHeight + "px";
    }
  }
}