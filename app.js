const tabs = [...document.querySelectorAll(".type-tab")];
const fields = [...document.querySelectorAll("[data-field]")];
const form = document.querySelector("#qrForm");
const qrImage = document.querySelector("#qrImage");
const emptyState = document.querySelector("#emptyState");
const payloadPreview = document.querySelector("#payloadPreview");
const statusText = document.querySelector("#statusText");
const downloadBtn = document.querySelector("#downloadBtn");
const copyBtn = document.querySelector("#copyBtn");
const themeToggle = document.querySelector("#themeToggle");

const inputs = {
  text: document.querySelector("#textValue"),
  wifiSsid: document.querySelector("#wifiSsid"),
  wifiPassword: document.querySelector("#wifiPassword"),
  wifiSecurity: document.querySelector("#wifiSecurity"),
  waPhone: document.querySelector("#waPhone"),
  waMessage: document.querySelector("#waMessage"),
  upiId: document.querySelector("#upiId"),
  upiName: document.querySelector("#upiName"),
  upiAmount: document.querySelector("#upiAmount"),
  contactName: document.querySelector("#contactName"),
  contactPhone: document.querySelector("#contactPhone"),
  contactEmail: document.querySelector("#contactEmail"),
  smsPhone: document.querySelector("#smsPhone"),
  smsMessage: document.querySelector("#smsMessage"),
  emailAddress: document.querySelector("#emailAddress"),
  emailSubject: document.querySelector("#emailSubject"),
  emailBody: document.querySelector("#emailBody"),
  phoneNumber: document.querySelector("#phoneNumber"),
  fillColor: document.querySelector("#fillColor"),
  backColor: document.querySelector("#backColor"),
  size: document.querySelector("#sizeValue")
};

const visibleFields = ["text", "wifi", "whatsapp", "upi", "contact", "sms", "email", "phone"];
let activeType = "text";
let latestPayload = "";
let latestImageUrl = "";
let renderTimer = 0;
let requestId = 0;

function getValues() {
  if (activeType === "wifi") {
    return {
      ssid: inputs.wifiSsid.value,
      password: inputs.wifiPassword.value,
      security: inputs.wifiSecurity.value
    };
  }

  if (activeType === "whatsapp") {
    return {
      phone: inputs.waPhone.value,
      message: inputs.waMessage.value
    };
  }

  if (activeType === "upi") {
    return {
      upiId: inputs.upiId.value,
      name: inputs.upiName.value,
      amount: inputs.upiAmount.value
    };
  }

  if (activeType === "contact") {
    return {
      name: inputs.contactName.value,
      phone: inputs.contactPhone.value,
      email: inputs.contactEmail.value
    };
  }

  if (activeType === "sms") {
    return {
      phone: inputs.smsPhone.value,
      message: inputs.smsMessage.value
    };
  }

  if (activeType === "email") {
    return {
      email: inputs.emailAddress.value,
      subject: inputs.emailSubject.value,
      body: inputs.emailBody.value
    };
  }

  if (activeType === "phone") {
    return {
      phone: inputs.phoneNumber.value
    };
  }

  return { text: inputs.text.value };
}

function getFilename() {
  const base = activeType === "text" ? "qrnexa" : `qrnexa-${activeType}`;
  return `${base}-${Date.now()}`;
}

function getBoxSize() {
  const pixelSize = Number(inputs.size.value);
  return Math.round(5 + ((pixelSize - 220) / 300) * 10);
}

function setActiveType(type) {
  activeType = type;
  tabs.forEach(tab => tab.classList.toggle("active", tab.dataset.type === type));
  fields.forEach(field => {
    const matches = field.dataset.field === type || !visibleFields.includes(field.dataset.field);
    field.hidden = !matches;
  });
  scheduleRender();
}

function scheduleRender() {
  clearTimeout(renderTimer);
  renderTimer = setTimeout(generateQr, 220);
}

async function generateQr() {
  const currentRequest = ++requestId;
  statusText.textContent = "Generating...";

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: activeType,
        values: getValues(),
        fill_color: inputs.fillColor.value,
        back_color: inputs.backColor.value,
        size: getBoxSize(),
        filename: getFilename()
      })
    });

    const data = await response.json();
    if (currentRequest !== requestId) return;

    if (!response.ok) {
      throw new Error(data.detail || "Could not generate QR code.");
    }

    latestPayload = data.payload;
    latestImageUrl = `${data.image_url}?v=${Date.now()}`;
    payloadPreview.value = data.payload;
    qrImage.src = latestImageUrl;
    qrImage.hidden = false;
    emptyState.hidden = true;
    statusText.textContent = `Saved as ${data.filename}`;
  } catch (error) {
    if (currentRequest !== requestId) return;
    latestPayload = "";
    latestImageUrl = "";
    payloadPreview.value = "";
    qrImage.removeAttribute("src");
    qrImage.hidden = true;
    emptyState.hidden = false;
    statusText.textContent = error.message;
  }
}

tabs.forEach(tab => tab.addEventListener("click", () => setActiveType(tab.dataset.type)));
form.addEventListener("input", scheduleRender);
form.addEventListener("change", scheduleRender);

downloadBtn.addEventListener("click", () => {
  if (!latestImageUrl) return;
  const link = document.createElement("a");
  link.href = latestImageUrl;
  link.download = `qrnexa-${activeType}.png`;
  link.click();
});

copyBtn.addEventListener("click", async () => {
  if (!latestPayload) return;
  await navigator.clipboard.writeText(latestPayload);
  statusText.textContent = "Payload copied.";
});

themeToggle.addEventListener("click", () => {
  document.documentElement.classList.toggle("dark");
});

inputs.text.value = "https://example.com";
qrImage.hidden = true;
setActiveType("text");
