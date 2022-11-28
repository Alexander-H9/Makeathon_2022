const scan_btn = document.querySelector("#scan-btn");
const scan_span = document.querySelector("#scan-span");

scan_btn.addEventListener("click", async () => await scanCoin());

async function scanCoin() {
    scan_span.style.color = "#ffffff"
    scan_span.textContent = "Scanning...";
    let response = await fetch("/scan");
    if (response.status == 200) {
        res = await response.text();
        scan_span.textContent = res;
    } else {
        scan_span.style.color = "#ff0000"
        scan_span.textContent = "Error"
        console.log("failed to load currencies from server");
    }
}