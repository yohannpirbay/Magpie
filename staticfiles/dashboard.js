function acceptInvitation(inviteId) {
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');
    
    // Make an AJAX request to accept the invitation
    $.ajax({
        url: `/accept_invite/${inviteId}/`,
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken }, // Include the CSRF token in the request headers
        success: function(data) {
            // On success, remove the corresponding <li> element from the DOM
            const inviteElement = document.getElementById(`invite-${inviteId}`);
            if (inviteElement) {
                inviteElement.remove();
            }
        },
        error: function(error) {
            console.error('Error accepting invitation:', error);
        }
    });
}

function declineInvitation(inviteId) {
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');
    
    // Make an AJAX request to decline the invitation
    $.ajax({
        url: `/decline_invite/${inviteId}/`,
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken }, // Include the CSRF token in the request headers
        success: function(data) {
            // On success, remove the corresponding <li> element from the DOM
            const inviteElement = document.getElementById(`invite-${inviteId}`);
            if (inviteElement) {
                inviteElement.remove();
            }
        },
        error: function(error) {
            console.error('Error declining invitation:', error);
        }
    });
}

// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = $.trim(cookies[i]);
            // Check if the cookie name matches the expected format
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
