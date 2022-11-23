const value_inpt = document.querySelector("#value-inpt");
const currency_inpt = document.querySelector("#currency-inpt");
const add_btn = document.querySelector("#add-btn");
const train_btn = document.querySelector("#train-btn");
const select_currency = document.querySelector("#select-currency");
const select_value = document.querySelector("#select-value");
const delete_btn = document.querySelector("#delete-btn");
const plot_img_1 = document.querySelector("#plot-img-1");
const plot_img_2 = document.querySelector("#plot-img-2");

add_btn.addEventListener("click", async () => await sendCoinToServer());
train_btn.addEventListener("click", async () => await trainAIModel());
select_currency.addEventListener("click", currencySelected);
delete_btn.addEventListener("click", async () => await deleteCoinFromServer());

function currencySelected() {
    loadCoinValuesFromServer(select_currency.value)
}

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
    await loadCurrenciesFromServer();
}

async function deleteCoinFromServer() {
    var value = select_value.value;
    var currency = select_currency.value;
    let response = await fetch("/delete?value="+value+"&currency="+currency, {
        method: "DELETE"
    });
    if (response.status != 200) {
        console.log("failed to delete Coin from server");
    }
    await loadCurrenciesFromServer();
}

async function loadCurrenciesFromServer() {
    let response = await fetch("/coins/load/currencies");
    if (response.status == 200) {
        res = await response.json();
        displayCurrenciesToDropdowns(res);
    } else {
        console.log("failed to load currencies from server");
    }
}

async function loadCoinValuesFromServer(currency) {
    let response = await fetch("/coins/load/values?currency="+currency);
    if (response.status == 200) {
        res = await response.json();
        displayCoinValuesToDropdowns(res);
    } else {
        console.log("failed to load coin values from server");
    }
}

function displayCurrenciesToDropdowns(currencies) {
    select_currency.textContent = '';
    for(var i = 0; i < currencies.length; i++) {
        var el = document.createElement("option");
        el.textContent = currencies[i];
        el.value = currencies[i];
        select_currency.appendChild(el);
    }
}

function displayCoinValuesToDropdowns(values) {
    select_value.textContent = '';
    for(var i = 0; i < values.length; i++) {
        var el = document.createElement("option");
        el.textContent = values[i];
        el.value = values[i];
        select_value.appendChild(el);
    }
}

document.addEventListener("DOMContentLoaded", async function() {
    await loadCurrenciesFromServer();
    plot_img_1.src = "./static/images/0,01 Euro.png"
    plot_img_2.src = "./static/images/4D.png"
});