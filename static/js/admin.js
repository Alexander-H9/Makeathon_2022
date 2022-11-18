const value_inpt = document.querySelector("#value-inpt");
const currency_inpt = document.querySelector("#currency-inpt");
const add_btn = document.querySelector("#add-btn");
const remove_btn = document.querySelector("#remove-btn");

add_btn.addEventListener("click", async () => await sendCoinToServer());

async function sendCoinToServer() {
    var value = value_inpt.value
    var currency = currency_inpt.value
    if (value && currency) {
        let response = await fetch("/coin/add?value="+value+"&currency="+currency, {
            method: "POST",
        });
        if (response.status != 200) {
            console.log("failed to send Coin to Server");
        }
    }
}