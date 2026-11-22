"use strict";

const mobileMenu = document.querySelector(".mobile-menu");
if (mobileMenu) {
  mobileMenu.querySelector("nav").addEventListener("click", (event) => {
    if (event.target.closest("a")) mobileMenu.open = false;
  });
  document.addEventListener("click", (event) => {
    if (mobileMenu.open && !mobileMenu.contains(event.target)) mobileMenu.open = false;
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && mobileMenu.open) {
      mobileMenu.open = false;
      mobileMenu.querySelector("summary").focus();
    }
  });
}

const form = document.querySelector("#request-form");
if (form) {
  const submit = form.querySelector("button[type=submit]");
  const buttonText = submit.querySelector("span");
  const status = document.querySelector(".form-status");
  const smsFallback = document.querySelector(".error-sms");

  const service = new URLSearchParams(window.location.search).get("service");
  const select = form.elements.service;
  if (Array.from(select.options).some((option) => option.value === service)) {
    select.value = service;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submit.disabled || !form.reportValidity()) return;

    submit.disabled = true;
    buttonText.textContent = "Sending…";
    form.setAttribute("aria-busy", "true");
    status.classList.remove("success");
    status.textContent = "";
    smsFallback.hidden = true;

    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: new FormData(form),
        signal: controller.signal
      });
      const result = await response.json();
      if (!response.ok || result.ok === false || result.errors?.length || result.error) throw new Error("Unconfirmed request");

      form.reset();
      form.hidden = true;
      status.classList.add("success");
      status.textContent = "Your search request was sent to Alex. He’ll follow up using the phone number you provided.";
    } catch {
      status.textContent = "Your request hasn’t been confirmed. Your details are still here. You can try again or text Alex directly.";
      smsFallback.hidden = false;
    } finally {
      window.clearTimeout(timeout);
      form.removeAttribute("aria-busy");
      submit.disabled = false;
      buttonText.textContent = "Send request";
      status.focus({ preventScroll: true });
      status.scrollIntoView({ block: "nearest" });
    }
  });
}
