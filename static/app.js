const state = {
    booksEditingId: null,
    issuesEditingId: null,
    returnsEditingId: null,
};

const bookForm = document.getElementById("bookForm");
const issueForm = document.getElementById("issueForm");
const returnForm = document.getElementById("returnForm");
const toast = document.getElementById("toast");

function showToast(message, isError = false) {
    toast.textContent = message;
    toast.className = `toast${isError ? " error" : ""}`;
    window.clearTimeout(showToast.timeoutId);
    showToast.timeoutId = window.setTimeout(() => {
        toast.className = "toast hidden";
    }, 2800);
}

async function request(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
        },
        ...options,
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(payload.error || "Something went wrong.");
    }
    return payload;
}

function formToObject(form) {
    return Object.fromEntries(new FormData(form).entries());
}

function resetBookForm() {
    bookForm.reset();
    bookForm.isbn.disabled = false;
    document.getElementById("bookSubmit").textContent = "Add Book";
    state.booksEditingId = null;
}

function resetIssueForm() {
    issueForm.reset();
    issueForm.isbn.disabled = false;
    document.getElementById("issueSubmit").textContent = "Issue Book";
    state.issuesEditingId = null;
}

function resetReturnForm() {
    returnForm.reset();
    returnForm.isbn.disabled = false;
    document.getElementById("returnSubmit").textContent = "Add Return";
    state.returnsEditingId = null;
}

function populateBookForm(row) {
    if (!row) return;
    state.booksEditingId = row.isbn;
    Object.entries(row).forEach(([key, value]) => {
        if (bookForm.elements[key]) {
            bookForm.elements[key].value = value;
        }
    });
    bookForm.isbn.disabled = true;
    document.getElementById("bookSubmit").textContent = "Update Book";
    bookForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

function populateIssueForm(row) {
    if (!row) return;
    state.issuesEditingId = row.isbn;
    issueForm.isbn.value = row.isbn;
    issueForm.issuer_name.value = row.issuer_name;
    issueForm.date_of_issue.value = row.date_of_issue;
    issueForm.contact_no.value = row.contact_no;
    issueForm.isbn.disabled = true;
    document.getElementById("issueSubmit").textContent = "Update Issue";
    issueForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

function populateReturnForm(row) {
    if (!row) return;
    state.returnsEditingId = row.isbn;
    returnForm.isbn.value = row.isbn;
    returnForm.issuer_name.value = row.issuer_name;
    returnForm.date_of_issue.value = row.date_of_issue;
    returnForm.date_of_return.value = row.date_of_return;
    returnForm.fine.value = row.fine;
    returnForm.contact_no.value = row.contact_no;
    returnForm.isbn.disabled = true;
    document.getElementById("returnSubmit").textContent = "Update Return";
    returnForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

function renderBooks(rows) {
    const tbody = document.getElementById("bookTableBody");
    tbody.innerHTML = rows.length
        ? rows.map((row) => `
            <tr>
                <td>${row.isbn}</td>
                <td>${row.book_title}</td>
                <td>${row.author_name}</td>
                <td>${row.publisher}</td>
                <td>${row.publication_year}</td>
                <td>${row.book_type}</td>
                <td>${row.language}</td>
                <td>
                    <div class="row-actions">
                        <button class="action-edit" data-action="edit-book" data-id="${row.isbn}">Edit</button>
                        <button class="action-delete" data-action="delete-book" data-id="${row.isbn}">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("")
        : `<tr><td colspan="8">No books found.</td></tr>`;

    tbody.querySelectorAll('[data-action="edit-book"]').forEach((button) => {
        button.addEventListener("click", () => populateBookForm(rows.find((row) => row.isbn === button.dataset.id)));
    });

    tbody.querySelectorAll('[data-action="delete-book"]').forEach((button) => {
        button.addEventListener("click", () => handleDelete(`/api/books/${button.dataset.id}`, loadBooks));
    });
}

function renderIssues(rows) {
    const tbody = document.getElementById("issueTableBody");
    tbody.innerHTML = rows.length
        ? rows.map((row) => `
            <tr>
                <td>${row.isbn}</td>
                <td>${row.book_title}</td>
                <td>${row.issuer_name}</td>
                <td>${row.date_of_issue}</td>
                <td>${row.contact_no}</td>
                <td>
                    <div class="row-actions">
                        <button class="action-edit" data-action="edit-issue" data-id="${row.isbn}">Edit</button>
                        <button class="action-delete" data-action="delete-issue" data-id="${row.isbn}">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("")
        : `<tr><td colspan="6">No issue records found.</td></tr>`;

    tbody.querySelectorAll('[data-action="edit-issue"]').forEach((button) => {
        button.addEventListener("click", () => populateIssueForm(rows.find((row) => row.isbn === button.dataset.id)));
    });

    tbody.querySelectorAll('[data-action="delete-issue"]').forEach((button) => {
        button.addEventListener("click", () => handleDelete(`/api/issues/${button.dataset.id}`, loadIssues));
    });
}

function renderReturns(rows) {
    const tbody = document.getElementById("returnTableBody");
    tbody.innerHTML = rows.length
        ? rows.map((row) => `
            <tr>
                <td>${row.isbn}</td>
                <td>${row.book_title}</td>
                <td>${row.issuer_name}</td>
                <td>${row.date_of_issue}</td>
                <td>${row.date_of_return}</td>
                <td>${row.fine}</td>
                <td>${row.contact_no}</td>
                <td>
                    <div class="row-actions">
                        <button class="action-edit" data-action="edit-return" data-id="${row.isbn}">Edit</button>
                        <button class="action-delete" data-action="delete-return" data-id="${row.isbn}">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("")
        : `<tr><td colspan="8">No return records found.</td></tr>`;

    tbody.querySelectorAll('[data-action="edit-return"]').forEach((button) => {
        button.addEventListener("click", () => populateReturnForm(rows.find((row) => row.isbn === button.dataset.id)));
    });

    tbody.querySelectorAll('[data-action="delete-return"]').forEach((button) => {
        button.addEventListener("click", () => handleDelete(`/api/returns/${button.dataset.id}`, loadReturns));
    });
}

async function handleDelete(url, reloadFn) {
    if (!window.confirm("Are you sure you want to delete this record?")) {
        return;
    }

    try {
        const result = await request(url, { method: "DELETE" });
        showToast(result.message);
        await reloadFn();
        await loadDashboard();
    } catch (error) {
        showToast(error.message, true);
    }
}

async function loadBooks() {
    const search = document.getElementById("bookSearch").value.trim();
    const rows = await request(`/api/books?search=${encodeURIComponent(search)}`);
    renderBooks(rows);
}

async function loadIssues() {
    const search = document.getElementById("issueSearch").value.trim();
    const rows = await request(`/api/issues?search=${encodeURIComponent(search)}`);
    renderIssues(rows);
}

async function loadReturns() {
    const search = document.getElementById("returnSearch").value.trim();
    const rows = await request(`/api/returns?search=${encodeURIComponent(search)}`);
    renderReturns(rows);
}

async function loadDashboard() {
    const data = await request("/api/dashboard");
    document.getElementById("totalBooks").textContent = data.total_books;
    document.getElementById("totalIssues").textContent = data.total_issues;
    document.getElementById("totalReturns").textContent = data.total_returns;
}

bookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formToObject(bookForm);
    const editing = state.booksEditingId;
    const url = editing ? `/api/books/${editing}` : "/api/books";
    const method = editing ? "PUT" : "POST";

    try {
        const result = await request(url, {
            method,
            body: JSON.stringify(data),
        });
        showToast(result.message);
        resetBookForm();
        await loadBooks();
        await loadDashboard();
    } catch (error) {
        showToast(error.message, true);
    }
});

issueForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formToObject(issueForm);
    const editing = state.issuesEditingId;
    const url = editing ? `/api/issues/${editing}` : "/api/issues";
    const method = editing ? "PUT" : "POST";

    try {
        const result = await request(url, {
            method,
            body: JSON.stringify(data),
        });
        showToast(result.message);
        resetIssueForm();
        await loadIssues();
        await loadDashboard();
    } catch (error) {
        showToast(error.message, true);
    }
});

returnForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formToObject(returnForm);
    const editing = state.returnsEditingId;
    const url = editing ? `/api/returns/${editing}` : "/api/returns";
    const method = editing ? "PUT" : "POST";

    try {
        const result = await request(url, {
            method,
            body: JSON.stringify(data),
        });
        showToast(result.message);
        resetReturnForm();
        await loadReturns();
        await loadDashboard();
    } catch (error) {
        showToast(error.message, true);
    }
});

document.getElementById("bookReset").addEventListener("click", resetBookForm);
document.getElementById("issueReset").addEventListener("click", resetIssueForm);
document.getElementById("returnReset").addEventListener("click", resetReturnForm);
document.getElementById("bookSearch").addEventListener("input", loadBooks);
document.getElementById("issueSearch").addEventListener("input", loadIssues);
document.getElementById("returnSearch").addEventListener("input", loadReturns);

Promise.all([loadBooks(), loadIssues(), loadReturns(), loadDashboard()]).catch((error) => {
    showToast(error.message, true);
});
