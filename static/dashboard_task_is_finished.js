function markAsFinished(taskId) {
  // Find the task in the "Tasks" section
  var taskElement = document.getElementById(`task-li-${taskId}`);

  // Check if the task element exists before attempting to clone and remove
  if (taskElement) {
    // Get the CSRF token from the cookie
    var csrftoken = getCookie('csrftoken');

    // Send an Ajax request to update the server with the CSRF token included
    fetch(`/update_task_status/${taskId}/`, {
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, // Include the CSRF token in the headers
      },
      body: JSON.stringify({ is_finished: true }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.success) {
        // If the server successfully updates the task status, perform client-side manipulations
        taskElement.is_finished = true;

        // Clone the task element
        var clonedTaskElement = taskElement.cloneNode(true);

        // Remove the original task from the "Tasks" section
        taskElement.remove();

        // Add the cloned task to the "Finished Tasks" section
        document.getElementById('finished-task-ul').appendChild(clonedTaskElement);
      } else {
        console.error('Error updating task status:', data.error);
      }
    })
    .catch(error => {
      console.error('Error updating task status:', error);
    });
  } else {
    console.error(`Task with ID ${taskId} not found.`);
  }
}

// Helper function to get the CSRF token from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

  