const value_inpt = document.querySelector("#value-inpt");
const currency_inpt = document.querySelector("#currency-inpt");
const add_btn = document.querySelector("#add-btn");
const train_btn = document.querySelector("#train-btn");
const select_value = document.querySelector("#select-value");
const select_currency = document.querySelector("#select-currency");
const remove_btn = document.querySelector("#remove-btn");

add_btn.addEventListener("click", async () => await sendCoinToServer());
train_btn.addEventListener("click", async () => await trainAIModel());

async function sendCoinToServer() {
    var value = value_inpt.value
    var currency = currency_inpt.value
    if (value && currency) {
        let response = await fetch("/coin/add?value="+value+"&currency="+currency, {
            method: "POST"
        });
        if (response.status != 200) {
            console.log("failed to send Coin to Server");
        }
    }
}

async function trainAIModel() {
    let response = await fetch("/train", {
        method: "POST"
    });
    if (response.status != 200) {
        console.log("failed to train AI model");
    }
}

async function loadCoinsFromServer() {
    let response = await fetch("/coins/load");
    if (response.status == 200) {
        res = await response.json();
        displayCoinsToDropdowns(res.values, res.currencies)
    } else {
        console.log("failed to load coin informations from server")
    }
}

function displayCoinsToDropdowns(values, currencies) {
    for(var i = 0; i < values.length; i++) {
        var el = document.createElement("option");
        el.textContent = values[i];
        el.value = values[i];
        select_value.appendChild(el);
    }

    for(var i = 0; i < currencies.length; i++) {
        var el = document.createElement("option");
        el.textContent = currencies[i];
        el.value = currencies[i];
        select_currency.appendChild(el);
    }
}

document.addEventListener("DOMContentLoaded", async function() {
    await loadCoinsFromServer();
});