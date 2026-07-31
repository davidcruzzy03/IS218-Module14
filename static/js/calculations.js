const calculationForm = document.getElementById(
    "calculation-form",
);

const numberAInput = document.getElementById("number-a");
const numberBInput = document.getElementById("number-b");

const calculationTypeInput = document.getElementById(
    "calculation-type",
);

const calculationsTableBody = document.getElementById(
    "calculations-table-body",
);

const calculationMessage = document.getElementById(
    "calculation-message",
);

const submitButton = document.getElementById("submit-button");
const cancelEditButton = document.getElementById(
    "cancel-edit-button",
);

const formTitle = document.getElementById("form-title");
const logoutButton = document.getElementById("logout-button");
const currentUserElement = document.getElementById(
    "current-user",
);

let editingCalculationId = null;


function getToken() {
    return localStorage.getItem("access_token");
}


function showMessage(message, type) {
    calculationMessage.textContent = message;
    calculationMessage.className = `message ${type}`;
}


function clearMessage() {
    calculationMessage.textContent = "";
    calculationMessage.className = "message";
}


function redirectToLogin() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
    localStorage.removeItem("username");

    window.location.href = "/login";
}


async function authenticatedFetch(url, options = {}) {
    const token = getToken();

    if (!token) {
        redirectToLogin();
        throw new Error("Authentication required.");
    }

    const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...options.headers,
    };

    const response = await fetch(url, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        redirectToLogin();
        throw new Error("Your session has expired.");
    }

    return response;
}


function resetForm() {
    editingCalculationId = null;

    calculationForm.reset();

    formTitle.textContent = "Add Calculation";
    submitButton.textContent = "Add Calculation";
    cancelEditButton.hidden = true;
}


function displayCalculations(calculations) {
    calculationsTableBody.innerHTML = "";

    if (calculations.length === 0) {
        calculationsTableBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-message">
                    No calculations have been saved.
                </td>
            </tr>
        `;

        return;
    }

    calculations.forEach((calculation) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${calculation.a}</td>
            <td>${calculation.b}</td>
            <td>${calculation.type}</td>
            <td>${calculation.result}</td>
            <td>
                <button
                    class="edit-button"
                    data-action="edit"
                    data-id="${calculation.id}"
                >
                    Edit
                </button>

                <button
                    class="delete-button"
                    data-action="delete"
                    data-id="${calculation.id}"
                >
                    Delete
                </button>
            </td>
        `;

        row.dataset.calculation = JSON.stringify(calculation);

        calculationsTableBody.appendChild(row);
    });
}


async function loadCalculations() {
    try {
        const response = await authenticatedFetch(
            "/calculations",
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error ||
                data.detail ||
                "Unable to load calculations.",
            );
        }

        displayCalculations(data);
    } catch (error) {
        console.error("Load calculations error:", error);

        showMessage(error.message, "error");
    }
}


async function saveCalculation(event) {
    event.preventDefault();
    clearMessage();

    const numberA = Number(numberAInput.value);
    const numberB = Number(numberBInput.value);
    const calculationType = calculationTypeInput.value;

    if (
        !Number.isFinite(numberA) ||
        !Number.isFinite(numberB)
    ) {
        showMessage(
            "Please enter two valid numbers.",
            "error",
        );

        return;
    }

    if (
        calculationType === "Divide" &&
        numberB === 0
    ) {
        showMessage(
            "Cannot divide by zero.",
            "error",
        );

        return;
    }

    const requestBody = {
        a: numberA,
        b: numberB,
        type: calculationType,
    };

    const isEditing = editingCalculationId !== null;

    const url = isEditing
        ? `/calculations/${editingCalculationId}`
        : "/calculations";

    const method = isEditing ? "PUT" : "POST";

    try {
        const response = await authenticatedFetch(url, {
            method,
            body: JSON.stringify(requestBody),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error ||
                data.detail ||
                "Unable to save calculation.",
            );
        }

        showMessage(
            isEditing
                ? "Calculation updated successfully."
                : "Calculation added successfully.",
            "success",
        );

        resetForm();
        await loadCalculations();
    } catch (error) {
        console.error("Save calculation error:", error);

        showMessage(error.message, "error");
    }
}


function beginEdit(calculation) {
    editingCalculationId = calculation.id;

    numberAInput.value = calculation.a;
    numberBInput.value = calculation.b;
    calculationTypeInput.value = calculation.type;

    formTitle.textContent = "Edit Calculation";
    submitButton.textContent = "Save Changes";
    cancelEditButton.hidden = false;

    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
}


async function deleteCalculation(calculationId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this calculation?",
    );

    if (!confirmed) {
        return;
    }

    clearMessage();

    try {
        const response = await authenticatedFetch(
            `/calculations/${calculationId}`,
            {
                method: "DELETE",
            },
        );

        if (!response.ok) {
            const data = await response.json();

            throw new Error(
                data.error ||
                data.detail ||
                "Unable to delete calculation.",
            );
        }

        showMessage(
            "Calculation deleted successfully.",
            "success",
        );

        if (editingCalculationId === calculationId) {
            resetForm();
        }

        await loadCalculations();
    } catch (error) {
        console.error("Delete calculation error:", error);

        showMessage(error.message, "error");
    }
}


calculationsTableBody.addEventListener(
    "click",
    (event) => {
        const button = event.target.closest("button");

        if (!button) {
            return;
        }

        const row = button.closest("tr");

        if (!row || !row.dataset.calculation) {
            return;
        }

        const calculation = JSON.parse(
            row.dataset.calculation,
        );

        const action = button.dataset.action;

        if (action === "edit") {
            beginEdit(calculation);
        }

        if (action === "delete") {
            deleteCalculation(calculation.id);
        }
    },
);


calculationForm.addEventListener(
    "submit",
    saveCalculation,
);


cancelEditButton.addEventListener("click", () => {
    resetForm();
    clearMessage();
});


logoutButton.addEventListener("click", () => {
    redirectToLogin();
});


document.addEventListener("DOMContentLoaded", () => {
    const token = getToken();

    if (!token) {
        redirectToLogin();
        return;
    }

    const username = localStorage.getItem("username");

    if (username) {
        currentUserElement.textContent = `Logged in as ${username}`;
    }

    loadCalculations();
});