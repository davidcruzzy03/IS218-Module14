const registerForm = document.getElementById("register-form");
const registerMessage = document.getElementById("register-message");

function showRegisterMessage(message, type) {
    registerMessage.textContent = message;
    registerMessage.className = `message ${type}`;
}

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document
        .getElementById("username")
        .value
        .trim();

    const email = document
        .getElementById("email")
        .value
        .trim();

    const password = document
        .getElementById("password")
        .value;

    const confirmPassword = document
        .getElementById("confirm-password")
        .value;

    if (username.length < 3) {
        showRegisterMessage(
            "Username must contain at least 3 characters.",
            "error",
        );
        return;
    }

    if (!email.includes("@")) {
        showRegisterMessage(
            "Please enter a valid email address.",
            "error",
        );
        return;
    }

    if (password.length < 8) {
        showRegisterMessage(
            "Password must contain at least 8 characters.",
            "error",
        );
        return;
    }

    if (password !== confirmPassword) {
        showRegisterMessage(
            "Passwords do not match.",
            "error",
        );
        return;
    }

    try {
        const response = await fetch("/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                email,
                password,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMessage =
                data.error ||
                data.detail ||
                "Registration failed.";

            showRegisterMessage(
                typeof errorMessage === "string"
                    ? errorMessage
                    : "Registration failed.",
                "error",
            );

            return;
        }

        showRegisterMessage(
            "Registration successful. You may now log in.",
            "success",
        );

        registerForm.reset();
    } catch (error) {
        console.error("Registration error:", error);

        showRegisterMessage(
            "Unable to connect to the server.",
            "error",
        );
    }
});