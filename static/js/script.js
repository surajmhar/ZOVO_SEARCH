console.log("ZOVO SEARCH Loaded Successfully 🚀");
/* ==========================
        FAQ Accordion
========================== */

const faqItems = document.querySelectorAll(".faq-item");

/* ==========================================
        PREMIUM FAQ ACCORDION
========================================== */

const faqCards = document.querySelectorAll(".faq-card");

faqCards.forEach((card) => {
  const button = card.querySelector(".faq-btn");
  const content = card.querySelector(".faq-content");

  // Open the first card by default
  if (card.classList.contains("active")) {
    content.style.maxHeight = content.scrollHeight + "px";
  }

  button.addEventListener("click", () => {
    const isActive = card.classList.contains("active");

    // Close all cards
    faqCards.forEach((item) => {
      item.classList.remove("active");

      item.querySelector(".faq-content").style.maxHeight = null;
    });

    // Open clicked card
    if (!isActive) {
      card.classList.add("active");

      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
});
const menuToggle = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");

// Toggle Menu
menuToggle.addEventListener("click", () => {
  menuToggle.classList.toggle("active");
  navMenu.classList.toggle("active");
  document.body.classList.toggle("menu-open");
});

// Close when clicking menu link
document.querySelectorAll(".nav-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    menuToggle.classList.remove("active");
    navMenu.classList.remove("active");
    document.body.classList.remove("menu-open");
  });
});

// Close when clicking outside
document.addEventListener("click", (e) => {
  if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
    menuToggle.classList.remove("active");
    navMenu.classList.remove("active");
    document.body.classList.remove("menu-open");
  }
});
<script src="{{ url_for('static', filename='js/script.js') }}"></script>

<script src="{{ url_for('static', filename='js/services.js') }}"></script>