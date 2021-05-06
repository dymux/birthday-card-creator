getTickets("http://localhost:8080/tickets");

var send_ticket_data_button = document.getElementById("send_ticket_data");
send_ticket_data_button.onclick = function() {
  var entrant_name = document.getElementById("entrant_name_input").value;
  var entrant_age = document.getElementById("entrant_age_input").value;
  var guest_name = document.getElementById("guest_name_input").value;

  fetch("http://localhost:8080/tickets", {
    method: "POST",
    credentials: "include",
    body: "entrant_name=" + encodeURIComponent(entrant_name) + "&" +
      "entrant_age=" + encodeURIComponent(entrant_age) + "&" +
      "guest_name=" + encodeURIComponent(guest_name),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  }).then(function(response) {
    if (response.ok) {
      var entrant_name_input = document.querySelector('#entrant_name_input')
      entrant_name_input.value = ""
      var entrant_age_input = document.querySelector('#entrant_age_input')
      entrant_age_input.value = ""
      var guest_name_input = document.querySelector('#guest_name_input')
      guest_name_input.value = ""
    } else {
      response.text().then(function (text) {
  alert(text)
});

    }

  });
  getTickets("http://localhost:8080/tickets");
};

function getTickets(path) {
  var ticket_list = document.getElementById("ticket_list");
  ticket_list.innerHTML = '';
  fetch(path, {
    credentials: "include"
  }).then(function(response) {
    if (response.ok) {
      response.json().then(function(tickets) {
        tickets.forEach(function(ticket) {
          loadTicket(ticket)
        });
        return tickets;
      });
    }
  });
}

function loadTicket(ticket) {
  var entrant_name = ticket.entrant_name;
  var entrant_age = ticket.entrant_age;
  var guest_name = ticket.guest_name;
  var random_token = ticket.random_token;
  var dayOfWeek = new Date().getDay();

  var ticket_box = document.createElement('li');
  if (random_token == dayOfWeek) {
    ticket_box.className = "goldenTicket";
  } else {
    ticket_box.className = "ticket";
  }

  ticket_box.style.margin = '.5em';

  var entrant_name_label = document.createElement('h3');
  entrant_name_label.innerHTML = "Name: " + entrant_name;
  var entrant_age_label = document.createElement('h3');
  entrant_age_label.innerHTML = "Age: " + entrant_age;
  var guest_name_label = document.createElement('h3');
  guest_name_label.innerHTML = "Guest: " + guest_name;

  var ticket_list = document.getElementById("ticket_list");
  ticket_box.appendChild(entrant_name_label);
  ticket_box.appendChild(entrant_age_label);
  ticket_box.appendChild(guest_name_label);
  ticket_list.appendChild(ticket_box);

}
