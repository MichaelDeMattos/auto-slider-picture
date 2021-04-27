// Navbar Expand
$(document).ready(function() {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {
    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });
});


// Close notification
document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});

// Select file 
const fileInput = document.querySelector('#file-post-form input[type=file]');
  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      const fileName = document.querySelector('#file-post-form .file-name');
      fileName.textContent = fileInput.files[0].name;
    }
}

// Post remove file
function remove_post_file(id){
  var exclude = window.confirm("Confirm exclude file selected ?");
  if (exclude) {
    var file_name = document.getElementById(id).value;
    $.ajax({
          url: '/admin',
          data: {"file_name": file_name},
          type: 'POST',
          success: function(response) {
              alert("File deleted with sucessfully!");
              location.reload();
          },
          error: function(error) {
              alert("Error: " + error);
          }
    }
  );
}

  else {
    console.log("canceled!!") 
  }
}
