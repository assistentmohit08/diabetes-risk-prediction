const form = document.getElementById("risk-form");
const resultBox = document.getElementById("result");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async(event) => {
    event.preventDefault();

    const data = Object.fromEntries(new FormData(form).entries());

    submitBtn.disabled = true;
    submitBtn.textContent = "Predicting...";
    resultBox.className = "result hidden";
    resultBox.replaceChildren();

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const body = await response.json();

        if (!response.ok) {
            showErrors(body.errors || ["Something went wrong"]);
        } else {
            showResult(body);
        }
    } catch (error) {
        showErrors(["Could not reach the server. Is Flask running?"]);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Predict Risk";
    }
});

function showResult(body) {
    const percent = (body.probability * 100).toFixed(1);

    const title = document.createElement("h2");
    title.textContent = body.risk_level + " risk";

    const detail = document.createElement("p");
    detail.textContent = "Estimated probability of diabetes: " + percent + "%";

    resultBox.replaceChildren(title, detail);
    resultBox.className = "result " + body.risk_level.toLowerCase();
}

function showErrors(errors) {
    const title = document.createElement("h2");
    title.textContent = "Please fix the following";

    const list = document.createElement("ul");
    errors.forEach((msg) => {
        const li = document.createElement("li");
        li.textContent = msg;
        list.appendChild(li);
    });

    resultBox.replaceChildren(title, list);
    resultBox.className = "result error";
}