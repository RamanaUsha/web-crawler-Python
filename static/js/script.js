document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('editButton');
    const profileEditSection = document.querySelector('.profile-edit');
    const cancelButton = document.getElementById('cancelButton');

    editButton.addEventListener('click', function() {
        // Toggle the display of the edit section
        if (profileEditSection.style.display === "none" || profileEditSection.style.display === "") {
            profileEditSection.style.display = "block"; // Show the edit section
            editButton.textContent = "Cancel"; // Change button text to Cancel
        } else {
            profileEditSection.style.display = "none"; // Hide the edit section
            editButton.textContent = "Edit"; // Change button text to Edit
        }
    });

    // Add event listener for the cancel button
    cancelButton.addEventListener('click', function() {
        profileEditSection.style.display = "none"; // Hide the edit section
        editButton.textContent = "Edit"; // Reset the edit button text
    });
});
