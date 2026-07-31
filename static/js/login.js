const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

function showLoginMessage(message, type) {
    loginMessage.textContent = message;
    loginMessage.className = `message ${type}`;
}

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document
        .getElementById("username")
        .value
        .trim();

    const password = document
        .getElementById("password")
        .value;

    if (username.length < 3) {
        showLoginMessage(
            "Please enter a valid username.",
            "error",
        );
        return;
    }

    if (password.length < 8) {
        showLoginMessage(
            "Password must contain at least 8 characters.",
            "error",
        );
        return;
    }

    try {
        const response = await fetch("/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            showLoginMessage(
                "Invalid username or password.",
                "error",
            );
            return;
        }

        localStorage.setItem(
            "access_token",
            data.access_token,
        );

        localStorage.setItem(
            "token_type",
            data.token_type,
        );

        localStorage.setItem(
            "username",
            data.user.username,
        );

        showLoginMessage(
            "Login successful. JWT token stored.",
            "success",
        );
    } catch (error) {
        console.error("Login error:", error);

        showLoginMessage(
            "Unable to connect to the server.",
            "error",
        );
    }
});