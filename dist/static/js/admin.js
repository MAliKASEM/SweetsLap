document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const addModal = document.getElementById('add-modal-overlay');
    const editModal = document.getElementById('edit-modal-overlay');
    const btnOpenAdd = document.getElementById('btn-open-add-modal');
    const btnCloseAdd = document.getElementById('btn-close-add-modal');
    const btnCancelAdd = document.getElementById('btn-cancel-add');
    const btnCloseEdit = document.getElementById('btn-close-edit-modal');
    const btnCancelEdit = document.getElementById('btn-cancel-edit');
    
    const addForm = document.getElementById('add-item-form');
    const editForm = document.getElementById('edit-item-form');
    const menuTableBody = document.getElementById('menu-table-body');
    const noItemsRow = document.getElementById('no-items-row');
    
    // File Inputs & Previews
    const addImageInput = document.getElementById('add-image');
    const addPreviewContainer = document.getElementById('add-preview-container');
    const addImagePreview = document.getElementById('add-image-preview');
    
    const editImageInput = document.getElementById('edit-image');
    const editPreviewContainer = document.getElementById('edit-preview-container');
    const editImagePreview = document.getElementById('edit-image-preview');

    // --- Modal Control Functions ---
    const openModal = (modal) => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    };
    
    const closeModal = (modal) => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    btnOpenAdd.addEventListener('click', () => {
        addForm.reset();
        addPreviewContainer.style.display = 'none';
        addImagePreview.src = '';
        openModal(addModal);
    });

    btnCloseAdd.addEventListener('click', () => closeModal(addModal));
    btnCancelAdd.addEventListener('click', () => closeModal(addModal));
    
    btnCloseEdit.addEventListener('click', () => closeModal(editModal));
    btnCancelEdit.addEventListener('click', () => closeModal(editModal));

    // Close on clicking overlay background
    window.addEventListener('click', (e) => {
        if (e.target === addModal) closeModal(addModal);
        if (e.target === editModal) closeModal(editModal);
    });

    // --- File Preview Logic ---
    const setupFilePreview = (input, container, previewImg) => {
        input.addEventListener('change', () => {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImg.src = e.target.result;
                    container.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                previewImg.src = '';
                container.style.display = 'none';
            }
        });
    };

    setupFilePreview(addImageInput, addPreviewContainer, addImagePreview);
    setupFilePreview(editImageInput, editPreviewContainer, editImagePreview);

    // --- CRUD: Helper to Build/Update Table Row ---
    const getRowHTML = (item) => {
        const imageHTML = item.image_path 
            ? `<img src="${item.image_path}" alt="${item.name}" class="admin-thumb">`
            : `<div class="admin-thumb-placeholder">No Pix</div>`;
            
        return `
            <td>${imageHTML}</td>
            <td class="cell-name" style="font-weight: 500;" data-name-ar="${item.name_ar || ''}">${item.name}</td>
            <td class="cell-category">
                <span class="badge badge-${item.category}">${item.category}</span>
            </td>
            <td class="cell-price" style="color: var(--primary); font-weight: 600;">$${parseFloat(item.price).toFixed(2)}</td>
            <td class="cell-ingredients" style="color: var(--text-muted); font-size: 0.9rem;" data-ingredients-ar="${item.ingredients_ar || ''}">${item.ingredients}</td>
            <td>
                <div class="actions-cell">
                    <button class="action-btn btn-edit" data-id="${item.id}">Edit</button>
                    <button class="action-btn action-btn-danger btn-delete" data-id="${item.id}">Delete</button>
                </div>
            </td>
        `;
    };

    // --- CRUD: Create (Add Item) ---
    addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addForm);
        
        try {
            const response = await fetch('/api/menu', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                closeModal(addModal);
                window.showToast(result.message, 'success');
                
                // Add to table
                const newRow = document.createElement('tr');
                newRow.id = `row-${result.item.id}`;
                newRow.dataset.id = result.item.id;
                newRow.innerHTML = getRowHTML(result.item);
                
                if (noItemsRow) {
                    noItemsRow.remove();
                }
                
                menuTableBody.appendChild(newRow);
                attachRowEventListeners(newRow);
            } else {
                window.showToast(result.error || 'Failed to add item', 'error');
            }
        } catch (error) {
            console.error('Error adding item:', error);
            window.showToast('Network error, please try again.', 'error');
        }
    });

    // --- CRUD: Read (Populate Edit Modal) ---
    const handleEditClick = (btn) => {
        const id = btn.dataset.id;
        const row = document.getElementById(`row-${id}`);
        
        if (!row) return;
        
        // Extract content from current row to avoid unnecessary server fetches
        const name = row.querySelector('.cell-name').textContent.trim();
        const nameAr = row.querySelector('.cell-name').dataset.nameAr || '';
        const categoryBadge = row.querySelector('.cell-category span').textContent.trim();
        const priceText = row.querySelector('.cell-price').textContent.trim().replace('$', '');
        const ingredients = row.querySelector('.cell-ingredients').textContent.trim();
        const ingredientsAr = row.querySelector('.cell-ingredients').dataset.ingredientsAr || '';
        const thumbImg = row.querySelector('.admin-thumb');
        
        // Populate form
        document.getElementById('edit-id').value = id;
        document.getElementById('edit-name').value = name;
        document.getElementById('edit-price').value = priceText;
        document.getElementById('edit-category').value = categoryBadge;
        document.getElementById('edit-ingredients').value = ingredients;
        document.getElementById('edit-name-ar').value = nameAr;
        document.getElementById('edit-ingredients-ar').value = ingredientsAr;
        
        if (thumbImg) {
            editImagePreview.src = thumbImg.src;
            editPreviewContainer.style.display = 'block';
        } else {
            editImagePreview.src = '';
            editPreviewContainer.style.display = 'none';
        }
        
        // Clear file input from any previous selections
        editImageInput.value = '';
        
        openModal(editModal);
    };

    // --- CRUD: Update (Save Changes) ---
    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('edit-id').value;
        const formData = new FormData(editForm);
        
        try {
            // Flask accepts POST to dynamic URL for edits when containing files
            const response = await fetch(`/api/menu/${id}`, {
                method: 'POST', 
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                closeModal(editModal);
                window.showToast(result.message, 'success');
                
                // Update table row in-place
                const row = document.getElementById(`row-${id}`);
                if (row) {
                    row.innerHTML = getRowHTML(result.item);
                    attachRowEventListeners(row);
                }
            } else {
                window.showToast(result.error || 'Failed to update item', 'error');
            }
        } catch (error) {
            console.error('Error updating item:', error);
            window.showToast('Network error, please try again.', 'error');
        }
    });

    // --- CRUD: Delete ---
    const handleDeleteClick = async (btn) => {
        const id = btn.dataset.id;
        const row = document.getElementById(`row-${id}`);
        const name = row ? row.querySelector('.cell-name').textContent.trim() : 'this item';
        
        if (confirm(`Are you sure you want to delete "${name}"?`)) {
            try {
                const response = await fetch(`/api/menu/${id}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    window.showToast(result.message, 'success');
                    if (row) {
                        row.remove();
                    }
                    
                    // If no items left, show placeholder row
                    if (menuTableBody.children.length === 0) {
                        const emptyRow = document.createElement('tr');
                        emptyRow.id = 'no-items-row';
                        emptyRow.innerHTML = `
                            <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 3rem 0;">
                                No menu items found. Click "Add New Item" to populate the menu.
                            </td>
                        `;
                        menuTableBody.appendChild(emptyRow);
                    }
                } else {
                    window.showToast(result.error || 'Failed to delete item', 'error');
                }
            } catch (error) {
                console.error('Error deleting item:', error);
                window.showToast('Network error, please try again.', 'error');
            }
        }
    };

    // --- Dynamic Event Delegation Helpers ---
    const attachRowEventListeners = (row) => {
        const editBtn = row.querySelector('.btn-edit');
        const deleteBtn = row.querySelector('.btn-delete');
        
        if (editBtn) {
            editBtn.addEventListener('click', () => handleEditClick(editBtn));
        }
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => handleDeleteClick(deleteBtn));
        }
    };

    // Attach initial event listeners to all rows
    const rows = menuTableBody.querySelectorAll('tr:not(#no-items-row)');
    rows.forEach(attachRowEventListeners);
});
