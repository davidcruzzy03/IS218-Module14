"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login";
        return;
    }

    const operationNameMap = {
        addition: "Addition",
        subtraction: "Subtraction",
        multiplication: "Multiplication",
        division: "Division",
    };

    let calculationHistory = [];

    function getAuthHeaders() {
        return {
            Authorization: `Bearer ${token}`,
        };
    }

    function handleUnauthorized(response) {
        if (response.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "/login";
            return true;
        }

        return false;
    }

    async function loadSummary() {
        const response = await fetch("/reports/summary", {
            headers: getAuthHeaders(),
        });

        if (handleUnauthorized(response)) {
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to load report summary.");
        }

        const data = await response.json();

        document.querySelector("#total-calculations").textContent =
            data.total_calculations;

        document.querySelector("#average-a").textContent =
            data.average_a ?? "N/A";

        document.querySelector("#average-b").textContent =
            data.average_b ?? "N/A";

        const mostUsedOperation = data.most_used_operation;

        document.querySelector("#most-used-operation").textContent =
            mostUsedOperation
                ? operationNameMap[mostUsedOperation] ?? mostUsedOperation
                : "N/A";

        const countsList = document.querySelector("#operation-counts");
        countsList.innerHTML = "";

        const operationEntries = Object.entries(
            data.operation_counts
        );

        if (operationEntries.length === 0) {
            const item = document.createElement("li");
            item.textContent = "No calculations yet.";
            countsList.appendChild(item);
            return;
        }

        for (const [operation, count] of operationEntries) {
            const item = document.createElement("li");

            const displayName =
                operationNameMap[operation] ?? operation;

            item.textContent = `${displayName}: ${count}`;
            countsList.appendChild(item);
        }
    }

    async function loadHistory() {
        const response = await fetch("/reports/history", {
            headers: getAuthHeaders(),
        });

        if (handleUnauthorized(response)) {
            return;
        }

        if (!response.ok) {
            throw new Error(
                "Unable to load calculation history."
            );
        }

        calculationHistory = await response.json();
        renderHistory(calculationHistory);
    }

    function renderHistory(history) {
        const tableBody = document.querySelector(
            "#history-table-body"
        );

        tableBody.innerHTML = "";

        if (history.length === 0) {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td colspan="4">
                    No calculations found.
                </td>
            `;

            tableBody.appendChild(row);
            return;
        }

        for (const calculation of history) {
            const row = document.createElement("tr");

            const displayOperation =
                operationNameMap[calculation.type]
                ?? calculation.type;

            row.innerHTML = `
                <td>${displayOperation}</td>
                <td>${calculation.a}</td>
                <td>${calculation.b}</td>
                <td>${calculation.result}</td>
            `;

            tableBody.appendChild(row);
        }
    }

    const operationFilter = document.querySelector(
        "#operation-filter"
    );

    operationFilter.addEventListener("change", (event) => {
        const selectedOperation = event.target.value;

        if (selectedOperation === "all") {
            renderHistory(calculationHistory);
            return;
        }

        const filteredHistory = calculationHistory.filter(
            (calculation) =>
                calculation.type === selectedOperation
        );

        renderHistory(filteredHistory);
    });

    const clearHistoryButton = document.querySelector(
        "#clear-history-button"
    );

    clearHistoryButton.addEventListener("click", async () => {
        const confirmed = window.confirm(
            "Are you sure you want to clear your calculation history?"
        );

        if (!confirmed) {
            return;
        }

        const message = document.querySelector(
            "#report-message"
        );

        try {
            const response = await fetch("/reports/history", {
                method: "DELETE",
                headers: getAuthHeaders(),
            });

            if (handleUnauthorized(response)) {
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                message.textContent =
                    data.detail
                    || "Unable to clear calculation history.";
                return;
            }

            message.textContent = data.message;

            await Promise.all([
                loadSummary(),
                loadHistory(),
            ]);
        } catch (error) {
            message.textContent =
                "Unable to clear calculation history.";
        }
    });

    async function initializeReportPage() {
        const message = document.querySelector(
            "#report-message"
        );

        try {
            await Promise.all([
                loadSummary(),
                loadHistory(),
            ]);
        } catch (error) {
            message.textContent = error.message;
        }
    }

    const logoutButton = document.querySelector(
        "#logout-button"
    );

    logoutButton.addEventListener("click", () => {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
    });

    initializeReportPage();
});