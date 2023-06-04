// Establish a WebSocket connection
var socket = new WebSocket('ws://localhost:8000/ws/messages/');

// Handle WebSocket connection open event
socket.onopen = function(event) {
    console.log('WebSocket connection opened');
};

// Handle WebSocket connection close event
socket.onclose = function(event) {
    console.log('WebSocket connection closed');
};

// Handle WebSocket message event
socket.onmessage = function(event) {
    var data = JSON.parse(event.data);

    // Check the type of the received message
    if (data.type === 'message') {
        // Handle the received message
        var message = data.message;
        displayNotification(message);
    } else if (data.type === 'notification') {
        // Handle the received notification
        var notification = data.notification;
        displayNotification(notification);
    }
};

// Function to display the notification
function displayNotification(notification) {
    // Update the UI to display the notification
    console.log('Notification:', notification);

    // Access the notification-amount badge element
    var badgeElement = document.querySelector('.notification-amount');

    // Update the pending amount number in the badge
    badgeElement.textContent = notification.unread_messages;
}

// Function to send a message (for testing purposes)
function sendMessage() {
    var message = 'Hello, receiver!';
    socket.send(message);
}
