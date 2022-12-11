const bankaccount_ul = document.querySelector("#bankaccount-ul");
const scan_btn = document.querySelector("#scan-btn");
const loading_gif = document.querySelector("#loading-gif");
const scan_span = document.querySelector("#scan-span");

scan_btn.addEventListener("click", async () => await scanCoin());

async function scanCoin() {
    scan_span.style.color = "#ffffff"
    scan_span.textContent = "Scanning...";
    loading_gif.src = "./static/images/loading.gif"
    let response = await fetch("/scan");
    if (response.status == 200) {
        res = await response.text();
        scan_span.textContent = res;
        loading_gif.src = "./static/images/spaceholder.png"
        await getBankAccount()
    } else {
        scan_span.style.color = "#ff0000"
        scan_span.textContent = "Error"
        console.log("failed to load currencies from server");
    }
}

async function getBankAccount() {
    let response = await fetch("/load/bankaccount");
    if (response.status == 200) {
        response = await response.json();
        clearBankAccountUL();
        for (let [currency, value] of Object.entries(response)) {
            const span = document.createElement("span");
            const li = document.createElement("li");

            li.classList.add("fs-6");
            li.classList.add("fw-bold");
            span.textContent = value + " " + currency;
            li.appendChild(span);
            bankaccount_ul.appendChild(li);
        }
    } else {
        console.log("failed to load currencies from server");
    }
}

function clearBankAccountUL() {
    while (bankaccount_ul.firstChild) {
        bankaccount_ul.removeChild(bankaccount_ul.lastChild);
    }
}

document.addEventListener("DOMContentLoaded", async function() {
    loading_gif.src = "./static/images/spaceholder.png"
    await getBankAccount()
});