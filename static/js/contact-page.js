document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".zovo-contact-form");

  if (!form) {
    console.error("ZOVO contact form not found.");
    return;
  }

  const submitButton = form.querySelector('button[type="submit"]');

  if (!submitButton) {
    console.error("Contact submit button not found.");
    return;
  }

  const originalButtonHTML = submitButton.innerHTML;

  const statusMessage = document.createElement("div");
  statusMessage.className = "contact-form-status";

  statusMessage.style.marginTop = "16px";
  statusMessage.style.padding = "12px 16px";
  statusMessage.style.borderRadius = "10px";
  statusMessage.style.fontSize = "14px";
  statusMessage.style.fontWeight = "600";
  statusMessage.style.display = "none";

  form.appendChild(statusMessage);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    statusMessage.style.display = "none";
    statusMessage.textContent = "";

    submitButton.disabled = true;

    submitButton.innerHTML = `
      <span>Sending...</span>
    `;

    try {
      const formData = new FormData(form);

      const response = await fetch("/contact", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || "Unable to send your enquiry.");
      }

      statusMessage.textContent =
        result.message || "Your enquiry has been sent successfully.";

      statusMessage.style.display = "block";

      statusMessage.style.color = "#166534";
      statusMessage.style.background = "#f0fdf4";
      statusMessage.style.border = "1px solid #bbf7d0";

      form.reset();
    } catch (error) {
      console.error("Contact form error:", error);

      statusMessage.textContent =
        error.message || "Something went wrong. Please try again.";

      statusMessage.style.display = "block";

      statusMessage.style.color = "#991b1b";
      statusMessage.style.background = "#fef2f2";
      statusMessage.style.border = "1px solid #fecaca";
    } finally {
      submitButton.disabled = false;
      submitButton.innerHTML = originalButtonHTML;

      if (typeof lucide !== "undefined") {
        lucide.createIcons();
      }
    }
  });
});
