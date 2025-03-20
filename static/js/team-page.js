// Helper functions for DaisyUI modals
document.addEventListener('DOMContentLoaded', function() {
    // New modal opening event listeners with debug logging
    const addEmailEndingButton = document.getElementById('add-email-ending-btn');
    if (addEmailEndingButton) {
        addEmailEndingButton.addEventListener('click', function() {
            console.log('Add Email Ending button clicked');
            const modal = document.getElementById('addEmailEndingModal');
            console.log('Modal element:', modal);
            modal.showModal();
        });
    } else {
        console.log('Add Email Ending button not found');
    }

    const addCompanyAdminButton = document.getElementById('add-company-admin-btn');
    if (addCompanyAdminButton) {
        addCompanyAdminButton.addEventListener('click', function() {
            console.log('Add Company Admin button clicked');
            const modal = document.getElementById('addCompanyAdminModal');
            console.log('Modal element:', modal);
            modal.showModal();
        });
    } else {
        console.log('Add Company Admin button not found');
    }

    // Add Domain input validation
    document.getElementById('email_ending').addEventListener('input', function(e) {
        const input = e.target;
        const saveButton = document.getElementById('saveEmailEnding');
        const errorDiv = document.getElementById('domain-error');
        
        // Check for @ symbol
        if (input.value.includes('@')) {
            errorDiv.textContent = 'Please enter a domain only (e.g., example.com) without @ symbol';
            errorDiv.classList.remove('hidden');
            saveButton.disabled = true;
            return;
        }
        
        // Basic domain validation
        const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$/;
        if (!domainRegex.test(input.value) && input.value !== '') {
            errorDiv.textContent = 'Please enter a valid domain (e.g., example.com)';
            errorDiv.classList.remove('hidden');
            saveButton.disabled = true;
        } else {
            errorDiv.classList.add('hidden');
            saveButton.disabled = false;
        }
    });
    
    // Add Email Ending handler
    document.getElementById('saveEmailEnding').addEventListener('click', function() {
        const formData = {
            email_ending: document.getElementById('email_ending').value
        };
        
        fetch('/api/allowed_email_endings/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('addEmailEndingModal').close();
                alert('New domain allowed successfully');
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while saving the domain');
        });
    });

    // Add Company Admin handler
    document.getElementById('saveCompanyAdmin').addEventListener('click', function() {
        const formData = {
            email: document.getElementById('email').value
        };
        
        fetch('/api/company_admins/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('addCompanyAdminModal').close();
                alert('Admin added successfully');
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while saving the Company Admin');
        });
    });

    // Close buttons for modals
    const addEmailEndingModalCloseButtons = document.querySelectorAll('#addEmailEndingModal form[method="dialog"] button');
    addEmailEndingModalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('addEmailEndingModal').close();
        });
    });

    const addCompanyAdminModalCloseButtons = document.querySelectorAll('#addCompanyAdminModal form[method="dialog"] button');
    addCompanyAdminModalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('addCompanyAdminModal').close();
        });
    });

    // Delete Admin handlers
    document.querySelectorAll('.delete-admin').forEach(button => {
        button.addEventListener('click', function() {
            const adminId = this.getAttribute('data-admin-id');
            if (confirm('Are you sure you want to delete this admin?')) {
                fetch(`/api/delete_admin/${adminId}`, {
                    method: 'DELETE',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Admin deleted successfully');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the admin');
                });
            }
        });
    });

    // Delete Email Ending handlers
    document.querySelectorAll('.delete-ending').forEach(button => {
        button.addEventListener('click', function() {
            const endingId = this.getAttribute('data-ending-id');
            if (confirm('Are you sure you want to delete this email ending?')) {
                fetch(`/api/delete_email_ending/${endingId}`, {
                    method: 'DELETE',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Email ending deleted successfully');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the email ending');
                });
            }
        });
    });

    // Block admin functionality
    document.querySelectorAll('.block-admin').forEach(button => {
        button.addEventListener('click', function() {
            const adminId = this.getAttribute('data-admin-id');
            if (confirm('Are you sure you want to block this admin?')) {
                fetch(`/api/block_admin/${adminId}`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Admin blocked successfully');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while blocking the admin');
                });
            }
        });
    });

    // Unblock admin functionality
    document.querySelectorAll('.unblock-admin').forEach(button => {
        button.addEventListener('click', function() {
            const adminId = this.getAttribute('data-admin-id');
            if (confirm('Are you sure you want to unblock this admin?')) {
                fetch(`/api/unblock_admin/${adminId}`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Admin unblocked successfully');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while unblocking the admin');
                });
            }
        });
    });
});